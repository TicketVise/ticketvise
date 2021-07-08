import email
import imaplib
import logging
import poplib
import ssl
from uuid import UUID

from django.db import transaction
from django.db.models import Q
from email_reply_parser import EmailReplyParser

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, UserInbox


def retrieve_emails(protocol, host, port, username, password, require_tls, ssl_context=None):
    if not ssl_context:
        ssl_context = ssl.create_default_context()

    if protocol.upper() == "IMAP":
        retrieve_imap_emails(host, port, username, password, require_tls, ssl_context)
    elif protocol.upper == "POP3":
        retrieve_pop3_emails(host, port, username, password, require_tls, ssl_context)
    else:
        raise Exception("Unsupported email protocol, expected IMAP or POP3")


def retrieve_pop3_emails(host, port, username, password, require_tls, ssl_context):
    pop3 = poplib.POP3_SSL(host=host, port=port, context=ssl_context) \
        if require_tls else poplib.POP3(host=host, port=port)

    with pop3 as server:
        if not require_tls:
            try:
                server.stls(context=ssl_context)
            except Exception as err:
                logging.warning(f"Failed to use STLS, error: {err}")

        server.user(username)
        server.pass_(password)

        _, messages = server.list()


def retrieve_imap_emails(host, port, username, password, require_tls, ssl_context):
    imap = imaplib.IMAP4_SSL(host=host, port=port, ssl_context=ssl_context) \
        if require_tls else imaplib.IMAP4(host=host, port=port)

    with imap as server:
        if not require_tls:
            try:
                server.starttls(ssl_context=ssl_context)
            except Exception as err:
                logging.warning(f"Failed to use STARTTLS, error: {err}")

        server.login(username, password)
        server.select()

        status, data = server.search(None, "ALL")
        if status != "OK":
            raise Exception(f"SEARCH returned status code: {status}")

        for msg_uid in data[0].split():
            typ, data = server.fetch(msg_uid, "(RFC822)")
            yield email.message_from_bytes(data[0][1], policy=email.policy.default)


def parse_message_id(raw_message_id):
    parts = raw_message_id.split("@")
    if len(parts) > 1:
        try:
            return UUID(parts[0].replace("<", ""))
        except Exception:
            return None

    return None


def get_ticket_by_email_message_id(message, header="Message-ID"):
    if header not in message:
        return None, None

    message_id = parse_message_id(message[header])
    if not message_id:
        return None, None

    return Ticket.objects.filter(Q(reply_message_id=message_id) | Q(comment_message_id=message_id)).first(), message_id


@transaction.atomic
def submit_email_ticket(message: email.message.EmailMessage):
    email_from = message.get("From")
    subject = message.get("Subject")
    email_tos = message.get_all("To")

    body = message.get_body(preferencelist=('plain',))
    if not body:
        logging.warning(f"Received empty email body from: '{email_from}', with subject: {subject}")
        return

    content = body.get_content()
    reply = EmailReplyParser.parse_reply(content)
    author, _ = User.objects.get_or_create(email=email_from)
    ticket, message_id = get_ticket_by_email_message_id(message)

    # If the ticket already exists, then the email message is a reply/comment to the ticket.
    if ticket:
        if not ticket.inbox.enable_reply_by_email:
            logging.warning(f"Reply by email is disabled for the inbox: {ticket.inbox.name} ({ticket.inbox.id})")
            return

        Comment.objects.create(ticket=ticket, author=author, is_reply=ticket.reply_message_id == message_id,
                               content=reply)
        UserInbox.objects.get_or_create(user=author, inbox=ticket.inbox)

    # Ticket does not exist, threat email as a new ticket.
    else:
        inbox = Inbox.objects.filter(email__in=email_tos).first()
        if not inbox:
            logging.warning(f"Could not find inbox with email(s): {email_tos}")
            return

        if not inbox.enable_create_new_ticket_by_email:
            logging.warning(f"Creation of ticket by email is disabled for the inbox: {inbox.name} ({inbox.id})")
            return

        Ticket.objects.create(author=author, inbox=inbox, title=subject, content=reply)
        UserInbox.objects.get_or_create(user=author, inbox=inbox)
