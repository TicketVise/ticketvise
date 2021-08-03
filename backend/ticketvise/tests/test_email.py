from email.message import EmailMessage

from django.test import TestCase
from ticketvise import settings
from ticketvise.mail.retrieve import submit_email_ticket
from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, Role


class EmailTestCase(TestCase):

    def setUp(self):
        # setup test data
        self.inbox = Inbox.objects.create(code="test", name="test-inbox",
                                          email_enabled=True,
                                          inbound_email_username="ticket@" + settings.DOMAIN,
                                          enable_create_new_ticket_by_email=True)
        self.student = User.objects.create(username="student", email="student@" + settings.DOMAIN)
        self.assistant = User.objects.create(username="assistant", email="assistant@" + settings.DOMAIN)
        self.ticket = Ticket.objects.create(inbox=self.inbox, author=self.student, assignee=self.assistant,
                                            title="help", content="pls")

        self.student.add_inbox(inbox=self.inbox, role=Role.GUEST)
        self.assistant.add_inbox(inbox=self.inbox, role=Role.AGENT)

    def test_send_new_email_with_known_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = self.student.email
        msg['To'] = self.inbox.inbound_email_username

        submit_email_ticket(msg)
        self.assertTrue(Ticket.objects.filter(title=msg['Subject'], content=content).exists())

    def test_send_new_email_with_unknown_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = "tom.wassing@" + settings.DOMAIN
        msg['To'] = self.inbox.inbound_email_username

        submit_email_ticket(msg)
        self.assertTrue(Ticket.objects.filter(title=msg['Subject'], content=content).exists())
        self.assertTrue(User.objects.filter(email=msg['From']).exists())

    def test_send_reply_email_with_known_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = self.student.email
        msg['To'] = self.inbox.inbound_email_username
        msg['Message-ID'] = f"<{self.ticket.reply_message_id}@{settings.DOMAIN}>"

        submit_email_ticket(msg)
        self.assertTrue(Comment.objects.filter(ticket=self.ticket, content=content, is_reply=True).exists())

    def test_send_reply_email_with_unknown_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = "tom.wassing@" + settings.DOMAIN
        msg['To'] = self.inbox.inbound_email_username
        msg['Message-ID'] = f"<{self.ticket.reply_message_id}@{settings.DOMAIN}>"

        submit_email_ticket(msg)
        self.assertTrue(Comment.objects.filter(ticket=self.ticket, content=content, is_reply=True).exists())

    def test_send_comment_email_with_known_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = self.student.email
        msg['To'] = self.inbox.inbound_email_username
        msg['Message-ID'] = f"<{self.ticket.reply_message_id}@{settings.DOMAIN}>"

        submit_email_ticket(msg)
        self.assertTrue(Comment.objects.filter(ticket=self.ticket, content=content, is_reply=True).exists())

    def test_send_comment_email_with_unknown_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = "tom.wassing@" + settings.DOMAIN
        msg['To'] = self.inbox.inbound_email_username
        msg['Message-ID'] = f"<{self.ticket.reply_message_id}@{settings.DOMAIN}>"

        submit_email_ticket(msg)
        self.assertTrue(Comment.objects.filter(ticket=self.ticket, content=content, is_reply=True).exists())
