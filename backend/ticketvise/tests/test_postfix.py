import smtplib
from email.message import EmailMessage

from django.test import TestCase

from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket


class PostfixTestCase(TestCase):

    SMTP_HOSTNAME = "mail"

    def test_receive_mail_as_ticket(self):
        inbox = Inbox.objects.create(code="ABC", name="TestVak", enable_create_new_ticket_by_email=True,
                                     email="abc@local.ticketvise.com")

        msg = EmailMessage()
        msg.set_content("Email contents")
        msg["Subject"] = "Email subject"
        msg["From"] = "tom@example.com"
        msg["To"] = inbox.email

        with smtplib.SMTP(self.SMTP_HOSTNAME) as s:
            s.send_message(msg)

        self.assertEqual(Ticket.objects.count(), 1)

        ticket = Ticket.objects.first()
        self.assertEqual(ticket.title, "Email subject")
        self.assertEqual(ticket.content, "Email contents")
        self.assertEqual(ticket.inbox, inbox)
