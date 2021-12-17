from ticketvise.models.ticket import TicketAttachment
from ticketvise.models.notification.assigned import TicketAssignedNotification
from email.message import EmailMessage
from itertools import product
from django.test import TestCase, override_settings
from ticketvise import settings
from ticketvise.mail.retrieve import submit_email_ticket
from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, Role
import tempfile


class EmailTestCase(TestCase):

    def setUp(self):
        # setup test data
        self.inbox = Inbox.objects.create(code="test", name="test-inbox",
                                          email_enabled=True,
                                          inbound_email_username="ticket@" + settings.DOMAIN,
                                          enable_create_new_ticket_by_email=True,
                                          enable_reply_by_email=True)
        self.student = User.objects.create(
            username="student", email="student@" + settings.DOMAIN)
        self.assistant = User.objects.create(
            username="assistant", email="assistant@" + settings.DOMAIN)
        self.ticket = Ticket.objects.create(inbox=self.inbox, author=self.student, assignee=self.assistant,
                                            title="help", content="pls")
        self.notification = TicketAssignedNotification.objects.get(
            ticket=self.ticket)

        self.student.add_inbox(inbox=self.inbox, role=Role.GUEST)
        self.assistant.add_inbox(inbox=self.inbox, role=Role.AGENT)

    def test_send_new_email_with_email_disabled(self):
        combinations = [(x, y) for x, y in product([True, False], repeat=2)
                        if x != True or y != True]

        for email_enabled, new_ticket_by_email in combinations:
            self.inbox.email_enabled = email_enabled
            self.inbox.enable_create_new_ticket_by_email = new_ticket_by_email
            self.inbox.save()

            msg = EmailMessage()
            content = "This is the content!!??"
            msg.set_content(content)
            msg['Subject'] = "This must be the title2343!!?"
            msg['From'] = self.student.email
            msg['To'] = self.inbox.inbound_email_username
            submit_email_ticket(msg, self.inbox)

            self.assertFalse(Ticket.objects.filter(
                title=msg['Subject'], content=content).exists())

    def test_send_reply_email_with_reply_disabled(self):
        combinations = [(x, y) for x, y in product([True, False], repeat=2)
                        if x != True or y != True]

        for email_enabled, reply_by_email in combinations:
            self.inbox.email_enabled = email_enabled
            self.inbox.enable_reply_by_email = reply_by_email
            self.inbox.save()

            msg = EmailMessage()
            content = "This is the content!!??"
            msg.set_content(content)
            msg['Subject'] = "This must be the title2343!!?"
            msg['From'] = self.student.email
            msg['To'] = self.inbox.inbound_email_username
            msg['References'] = f"<{self.notification.email_message_id}@{settings.DOMAIN}>"

            submit_email_ticket(msg, self.inbox)
            self.assertFalse(Comment.objects.filter(
                ticket=self.ticket, content=content, is_reply=True).exists())

    def test_send_new_email_with_known_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = self.student.email
        msg['To'] = self.inbox.inbound_email_username

        submit_email_ticket(msg, self.inbox)
        self.assertTrue(Ticket.objects.filter(
            title=msg['Subject'], content=content).exists())

    def test_send_new_email_with_unknown_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = "tom.wassing@" + settings.DOMAIN
        msg['To'] = self.inbox.inbound_email_username

        submit_email_ticket(msg, self.inbox)
        self.assertTrue(Ticket.objects.filter(
            title=msg['Subject'], content=content).exists())
        self.assertTrue(User.objects.filter(email=msg['From']).exists())

    @override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
                       MEDIA_ROOT=tempfile.TemporaryDirectory(prefix='ticketvise_test_media_').name)
    def test_send_new_email_with_attachments(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = "tom.wassing@" + settings.DOMAIN
        msg['To'] = self.inbox.inbound_email_username

        msg.add_attachment(b"Hello World!", maintype='text',
                           subtype='plain', filename="hello.txt")
        msg.add_attachment(
            b"import numpy as np\nx = np.array([42, 69])", maintype='text', subtype='plain', filename="test.py")

        submit_email_ticket(msg, self.inbox)
        self.assertTrue(Ticket.objects.filter(
            title=msg['Subject'], content=content).exists())
        self.assertTrue(User.objects.filter(email=msg['From']).exists())

        ticket = Ticket.objects.filter(
            title=msg['Subject'], content=content).first()
        self.assertTrue(TicketAttachment.objects.filter(
            ticket=ticket).count() == 2)

    def test_send_reply_email_with_known_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = self.student.email
        msg['To'] = self.inbox.inbound_email_username
        msg['References'] = f"<{self.notification.email_message_id}@{settings.DOMAIN}>"

        submit_email_ticket(msg, self.ticket.inbox)
        self.assertTrue(Comment.objects.filter(
            ticket=self.ticket, content=content, is_reply=True).exists())

    def test_send_reply_email_with_unknown_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = "tom.wassing@" + settings.DOMAIN
        msg['To'] = self.inbox.inbound_email_username
        msg['References'] = f"<{self.notification.email_message_id}@{settings.DOMAIN}>"

        submit_email_ticket(msg, self.ticket.inbox)
        self.assertTrue(Comment.objects.filter(
            ticket=self.ticket, content=content, is_reply=True).exists())

    def test_send_comment_email_with_known_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = self.student.email
        msg['To'] = self.inbox.inbound_email_username
        msg['References'] = f"<{self.notification.email_message_id}@{settings.DOMAIN}>"

        submit_email_ticket(msg, self.ticket.inbox)
        self.assertTrue(Comment.objects.filter(
            ticket=self.ticket, content=content, is_reply=True).exists())

    def test_send_comment_email_with_unknown_user(self):
        msg = EmailMessage()
        content = "This is the content!!??"
        msg.set_content(content)
        msg['Subject'] = "This must be the title2343!!?"
        msg['From'] = "tom.wassing@" + settings.DOMAIN
        msg['To'] = self.inbox.inbound_email_username
        msg['References'] = f"<{self.notification.email_message_id}@{settings.DOMAIN}>"

        submit_email_ticket(msg, self.ticket.inbox)
        self.assertTrue(Comment.objects.filter(
            ticket=self.ticket, content=content, is_reply=True).exists())
