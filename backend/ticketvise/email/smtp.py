from email import policy
from email.parser import BytesParser
from uuid import UUID

from aiosmtpd.controller import Controller
from asgiref.sync import sync_to_async
from django.db.models import Q
from email_reply_parser import EmailReplyParser

from ticketvise import settings
from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, UserInbox


class SmtpServer:

    def __init__(self, port=settings.SMTP_INBOUND_PORT) -> None:
        self.controller = Controller(self, hostname="0.0.0.0", port=port)
        super().__init__()

    def parse_message_id(self, raw_message_id):
        parts = raw_message_id.split("@")
        if len(parts) > 1:
            try:
                return UUID(parts[0].replace("<", ""))
            except:
                return None

        return None

    def get_ticket(self, message):
        if "Message-ID" not in message:
            return None, None

        message_id = self.parse_message_id(message["Message-ID"])
        if not message_id:
            return None, None

        return Ticket.objects.filter(
            Q(reply_message_id=message_id) | Q(comment_message_id=message_id)).first(), message_id

    @sync_to_async
    def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not Inbox.objects.filter(email=address).exists():
            return '550 not relaying to that domain'

        envelope.rcpt_tos.append(address)

        return '250 OK'

    @sync_to_async
    def handle_DATA(self, server, session, envelope):
        mail_from = envelope.mail_from

        message = BytesParser(policy=policy.default).parsebytes(envelope.content)
        body = message.get_body(preferencelist=('plain',))
        if body:
            content = body.get_content()
            reply = EmailReplyParser.parse_reply(content)
            author, _ = User.objects.get_or_create(email=mail_from)
            ticket, message_id = self.get_ticket(message)

            if ticket:
                if not ticket.inbox.enable_reply_by_email:
                    return '450 Reply by email is disabled for the inbox'

                Comment.objects.create(ticket=ticket, author=author, is_reply=ticket.reply_message_id == message_id,
                                       content=reply)
                UserInbox.objects.get_or_create(user=author, inbox=ticket.inbox)

            else:
                inbox = Inbox.objects.get(email__in=envelope.rcpt_tos, )
                if not inbox.enable_create_new_ticket_by_email:
                    return '450 Creation of ticket by email is disabled for the inbox'

                Ticket.objects.create(author=author, inbox=inbox, title=message["Subject"], content=reply)
                UserInbox.objects.get_or_create(user=author, inbox=inbox)

        return '250 OK'

    def start(self):
        try:
            self.controller.stop()
        except:
            pass

        try:
            self.controller.start()
            print("SMTP server started on port {}".format(settings.SMTP_INBOUND_PORT))
        except:
            pass

    def stop(self):
        self.controller.stop()
