import email
import imaplib
import logging
import poplib
import re
import ssl
from uuid import UUID
from django.core.files.base import ContentFile

from django.db import transaction
from email_reply_parser import EmailReplyParser
from bs4 import BeautifulSoup
import html2text

from ticketvise.mail import oauth_2_auth_base64
from ticketvise.models.notification import Notification
from ticketvise.models.comment import Comment
from ticketvise.models.ticket import Ticket
from ticketvise.models.ticket import TicketAttachment
from ticketvise.models.user import User, UserInbox

def is_autogenerated(message):
    # https://www.arp242.net/autoreply.html
    return any([
        message.get(
            "Auto-Submitted") and message.get("Auto-Submitted").strip().lower() != "no",
        message.get("X-Auto-Response-Suppress") and message.get(
            "X-Auto-Response-Suppress").strip().lower() in ("dr", "autoreply", "all"),
        message.get("Precedence") and message.get(
            "Precedence").strip().lower() in ("bulk", "auto_reply", "list"),
        message.get(
            "X-Autoreply") and message.get("X-Autoreply").strip().lower() == "yes",
        message.get("List-Id"),
        message.get("List-Unsubscribe"),
        message.get("Feedback-ID"),
        re.match(message.get("From").lower(), "^no.?reply@"),
        "mailer-daemon" in message.get("From").lower(),
        "Mail Delivery Subsystem" in message.get("From").lower(),
        message.get("X-Mailer") and message.get("X-Mailer").strip(
        ).lower() == "Microsoft CDO for Windows 2000".lower()
    ])


def extract_message_id(raw_message_id):
    """Extracts the generated UUID Message-ID from a RFC822 compliant Message-Id header value."""
    parts = raw_message_id.split("@")
    if len(parts) > 1:
        try:
            return UUID(parts[0].replace("<", "").strip().lower())
        except Exception:
            return None

    return None


def get_ticket_by_email_message_id(message):
    references = message.get("References")
    if not references:
        return None

    message_id = extract_message_id(references.split()[0])
    if not message_id:
        return None

    notification = Notification.objects.filter(email_message_id=message_id).select_subclasses().first()
    if not notification:
        return None

    return notification.ticket


@transaction.atomic
def submit_email_ticket(message: email.message.EmailMessage, inbox):
    # Check if email is autogenerated, e.g., autorepy, newsletter
    if is_autogenerated(message):
        logging.warning(f"Ignored autogenerated message")
        return

    # Get basic email data
    email_from = message.get("From")
    subject = message.get("Subject", "No subject")
    recipients = message.get_all("To")

    # Parse email body
    logging.info(f"Processing email '{subject}' from '{email_from}' send to '{recipients}'")
    body = message.get_body(preferencelist=('plain', 'html'))
    if not body:
        logging.warning(
            f"Received empty email body from: '{email_from}', with subject: {subject}")
        return

    content = body.get_content()
    if body.get_content_type() == "text/html":
        content = html2text.html2text(content)
    reply = EmailReplyParser.parse_reply(content)

    # Extract name and email adress from 'From' header
    realname, address = email.utils.parseaddr(email_from)
    if not address:
        logging.warning(f"Unable to parse RFC288 FROM header in email")
        return

    # If the email address have not been seen before, create new user.
    author = User.objects.filter(email=address).first()
    if not author:
        # Split name from email into first and last name, if possible.
        realname_split = realname.split(" ", 1)
        first_name, last_name = "", ""
        if len(realname_split) > 1:
            first_name, last_name = realname_split

        # Form username as the front part of email, if it does already exist
        # use the email address.
        username = address.split("@", 1)[0]
        if User.objects.filter(username=username).exists():
            username = address

        author = User.objects.create(
            username=username, email=address, first_name=first_name, last_name=last_name)

    ticket = get_ticket_by_email_message_id(message)

    # If the ticket already exists, then the email message is a reply/comment to the ticket.
    if ticket:
        if not ticket.inbox.email_enabled:
            logging.warning(
                f"Email is disabled for the inbox: {ticket.inbox.name} ({ticket.inbox.id})")
            return

        if not ticket.inbox.enable_reply_by_email:
            logging.warning(
                f"Reply by email is disabled for the inbox: {ticket.inbox.name} ({ticket.inbox.id})")
            return

        Comment.objects.create(ticket=ticket, author=author, is_reply=True, content=reply)
        UserInbox.objects.get_or_create(user=author, inbox=ticket.inbox)

    # Ticket does not exist, threat email as a new ticket.
    else:
        # TODO: check if recipient is in email config?
        # inbox = Inbox.objects.filter(
        #     inbound_email_username__in=recipients).first()
        # if not inbox:
        #     logging.warning(f"Could not find inbox with email(s): {recipients}")
        #     return

        if not inbox.email_enabled:
            logging.warning(
                f"Email is disabled for the inbox: {inbox.name} ({inbox.id})")
            return

        if not inbox.enable_create_new_ticket_by_email:
            logging.warning(
                f"Creation of ticket by email is disabled for the inbox: {inbox.name} ({inbox.id})")
            return

        ticket = Ticket.objects.create(author=author, inbox=inbox,
                                       title=subject, content=reply)
        UserInbox.objects.get_or_create(user=author, inbox=inbox)

    for attachment in message.iter_attachments():
        file = ContentFile(attachment.get_payload(decode=True), 
                           name=attachment.get_filename())
        TicketAttachment.objects.create(ticket=ticket, file=file,
                                        uploader=author)


def retrieve_emails(protocol, host, port, username, password, require_tls, use_oauth2, ssl_context=None):
    if not ssl_context:
        ssl_context = ssl.create_default_context()

    if protocol.upper() == "IMAP":
        return retrieve_imap_emails(host, port, username, password, require_tls, use_oauth2, ssl_context)
    elif protocol.upper == "POP3":
        return retrieve_pop3_emails(host, port, username, password, require_tls, use_oauth2, ssl_context)
    else:
        raise Exception("Unsupported email protocol, expected IMAP or POP3")

def retrieve_pop3_emails(host, port, username, password, require_tls, use_oauth2, ssl_context):
    pop3 = poplib.POP3_SSL(host=host, port=port, context=ssl_context) \
        if require_tls else poplib.POP3(host=host, port=port)

    with pop3 as server:
        if not require_tls:
            try:
                server.stls(context=ssl_context)
            except Exception as err:
                logging.warning(f"Failed to use STLS, error: {err}")


        if use_oauth2:
            auth_string = oauth_2_auth_base64(username, password)

            # Try single line: https://developers.google.com/gmail/imap/xoauth2-protocol#pop_protocol_exchange
            try:
                server._shortcmd(f"AUTH XOAUTH2 {auth_string}")
            except poplib.error_proto as e:
                logging.warning(f"Single line 'AUTH XOAUTH2' failed with: {e}")
                # Try two line: https://docs.microsoft.com/en-us/exchange/client-developer/legacy-protocols/how-to-authenticate-an-imap-pop-smtp-application-by-using-oauth
                server._shortcmd(f"AUTH XOAUTH2")
                server._shortcmd(auth_string)
        else:
            server.user(username)
            server.pass_(password)

        _, messages = server.list()
        for i in range(len(messages)):
            for data in server.retr(i + 1)[1]:
                yield email.message_from_bytes(data[0][1], policy=email.policy.default)


def retrieve_imap_emails(host, port, username, password, require_tls, use_oauth2, ssl_context):
    imap = imaplib.IMAP4_SSL(host=host, port=port, ssl_context=ssl_context) \
        if require_tls else imaplib.IMAP4(host=host, port=port)

    with imap as server:
        if not require_tls:
            try:
                server.starttls(ssl_context=ssl_context)
            except Exception as err:
                logging.warning(f"Failed to use STARTTLS, error: {err}")

        if use_oauth2:
            auth_string = oauth_2_auth_base64(username, password)
            server.authenticate("XOAUTH2", lambda x: auth_string)
        else:
            server.login(username, password)
        
        server.select()
        status, data = server.search(None, "ALL")
        if status != "OK":
            raise Exception(f"SEARCH returned status code: {status}")

        for msg_uid in data[0].split():
            _, data = server.fetch(msg_uid, "(RFC822)")
            yield email.message_from_bytes(data[0][1], policy=email.policy.default)
            # imap.store(msg_uid, '+FLAGS', '\\Deleted')
        imap.expunge()
