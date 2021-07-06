import smtplib
import socket
from email.message import EmailMessage
from django.test import LiveServerTestCase


from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket


class PostfixTestCase(LiveServerTestCase):

    SMTP_HOSTNAME = "mail"
    port = 6000

    def test_receive_mail_as_ticket(self):
        inbox = Inbox.objects.create(code="ABC", name="TestVak", enable_create_new_ticket_by_email=True,
                                     email="abc@local.ticketvise.com")

        msg = EmailMessage()
        msg.set_content("Email contents")
        msg["Subject"] = "Email subject"
        msg["From"] = "tom@ticketvise.com"
        msg["To"] = inbox.email

        with smtplib.SMTP(self.SMTP_HOSTNAME) as s:
            s.send_message(msg)

        self.assertEqual(Ticket.objects.count(), 1)

        print(socket.gethostname())

        ticket = Ticket.objects.first()
        self.assertEqual(ticket.title, "Email subject")
        self.assertEqual(ticket.content, "Email contents")
        self.assertEqual(ticket.inbox, inbox)

    def test_should_not_relay_public(self):
        msg = EmailMessage()
        msg.set_content("Email contents")
        msg["Subject"] = "Email subject"
        msg["From"] = "abc@local.ticketvise.com"
        msg["To"] = "tjwassing@gmail.com"

        with smtplib.SMTP(self.SMTP_HOSTNAME) as s:
            s.send_message(msg)
