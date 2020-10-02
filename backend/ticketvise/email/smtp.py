from email import policy
from email.parser import BytesParser

from aiosmtpd.controller import Controller
from asgiref.sync import sync_to_async
from django.db.models import Q
from email_reply_parser import EmailReplyParser

from ticketvise import settings
from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User


class SmtpServer:

    def __init__(self) -> None:
        self.controller = Controller(self, hostname="127.0.0.1", port=settings.SMTP_INBOUND_PORT)
        super().__init__()

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

            if "Message-ID" in message:
                self.handle_reply(mail_from, message["Message-ID"], reply)
            else:
                self.handle_new_ticket(mail_from, envelope.rcpt_tos, message["Subject"], reply)

        return '250 OK'

    def handle_new_ticket(self, mail_from, rcpt_tos, subject, content):
        user = User.objects.get_or_create(email=mail_from)

        inbox = Inbox.objects.get(email__in=rcpt_tos)
        Ticket.objects.create(author=user, inbox=inbox, title=subject, content=content)

    def handle_reply(self, mail_from, message_id, content):
        user = User.objects.get_or_create(email=mail_from)

        ticket = Ticket.objects.get(Q(reply_message_id=message_id) | Q(comment_message_id=message_id))
        Comment.objects.create(ticket=ticket, author=user, is_reply=ticket.reply_message_id == message_id,
                               content=content)

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
