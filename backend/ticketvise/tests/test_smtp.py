from smtplib import SMTP, SMTPDataError

from ticketvise import settings
from ticketvise.email.smtp import SmtpServer
from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, Role
from ticketvise.tests.utils import LiveServerSingleThreadedTestCase


class SmtpServerTestCase(LiveServerSingleThreadedTestCase):
    """A single threaded test case is needed since SQLite does not support concurrency. The SMTP server is async which
    uses multiple threads. When this case test is ran with multiple threads SQLite will lock tables and the tests will
    fail the single threaded test case bypasses this. This is not a issue with the database used in production, since it
    supports concurrency."""

    def setUp(self):

        # setup of test SMTP server
        self.smtp_server = SmtpServer(port=2524)
        self.smtp_server.start()

        self.controller = self.smtp_server.controller
        self.addCleanup(self.smtp_server.stop)
        self.address = (self.smtp_server.controller.hostname, self.smtp_server.controller.port)

        # setup test data
        self.inbox = Inbox.objects.create(code="test", name="test-inbox", email="ticket@" + settings.DOMAIN, enable_create_new_ticket_by_email=True)
        self.student = User.objects.create(username="student", email="student@" + settings.DOMAIN)
        self.assistant = User.objects.create(username="assistant", email="assistant@" + settings.DOMAIN)
        self.ticket = Ticket.objects.create(inbox=self.inbox, author=self.student, assignee=self.assistant,
                                            title="help", content="pls")

        self.student.add_inbox(inbox=self.inbox, role=Role.GUEST)
        self.assistant.add_inbox(inbox=self.inbox, role=Role.AGENT)


    def test_send_new_email_with_known_user(self):
        from_email = self.student.email
        to_email = self.inbox.email
        title = "This must be the title2343!!?"
        content = "This is the content!!??"
        email_message = "\n".join([
            f"From: {from_email}",
            f"To: {to_email}",
            f"Subject: {title}",
            "",
            content
        ])

        with SMTP(*self.address) as client:
            client.sendmail(from_email, [to_email], email_message)

        self.assertTrue(Ticket.objects.filter(title=title, content=content).exists())

    def test_send_new_email_with_unknown_user(self):
        from_email = "tom.wassing@" + settings.DOMAIN
        to_email = self.inbox.email
        title = "This must be the title2343!!?"
        content = "This is the content!!??"
        email_message = "\n".join([
            f"From: {from_email}",
            f"To: {to_email}",
            f"Subject: {title}",
            "",
            content
        ])

        with SMTP(*self.address) as client:
            client.sendmail(from_email, [to_email], email_message)

        self.assertTrue(Ticket.objects.filter(title=title, content=content).exists())
        self.assertTrue(User.objects.filter(email=from_email).exists())

    def test_send_reply_email_with_known_user(self):
        from_email = self.student.email
        to_email = self.inbox.email
        content = "This is the content!!??"
        email_message = "\n".join([
            f"From: {from_email}",
            f"To: {to_email}",
            f"Subject: This must be the title2343!!?",
            f"Message-ID: <{self.ticket.reply_message_id}@{settings.DOMAIN}>",
            "",
            content
        ])

        with SMTP(*self.address) as client:
            client.sendmail(from_email, [to_email], email_message)

        self.assertTrue(Comment.objects.filter(ticket=self.ticket, content=content, is_reply=True).exists())

    def test_send_reply_email_with_unknown_user(self):
        from_email = "tom.wassing@" + settings.DOMAIN
        to_email = self.inbox.email
        content = "This is the content!!??"
        email_message = "\n".join([
            f"From: {from_email}",
            f"To: {to_email}",
            f"Subject: This must be the title2343!!?",
            f"Message-ID: <{self.ticket.reply_message_id}@{settings.DOMAIN}>",
            "",
            content
        ])

        with SMTP(*self.address) as client:
            client.sendmail(from_email, [to_email], email_message)

        self.assertTrue(Comment.objects.filter(ticket=self.ticket, content=content, is_reply=True).exists())

    def test_send_comment_email_with_known_user(self):
        from_email = self.student.email
        to_email = self.inbox.email
        content = "This is the content!!??"
        email_message = "\n".join([
            f"From: {from_email}",
            f"To: {to_email}",
            f"Subject: This must be the title2343!!?",
            f"Message-ID: <{self.ticket.comment_message_id}@{settings.DOMAIN}>",
            "",
            content
        ])

        with SMTP(*self.address) as client:
            client.sendmail(from_email, [to_email], email_message)

        self.assertTrue(Comment.objects.filter(ticket=self.ticket, content=content, is_reply=False).exists())

    def test_send_comment_email_with_unknown_user(self):
        from_email = "tom.wassing@" + settings.DOMAIN
        to_email = self.inbox.email
        content = "This is the content!!??"
        email_message = "\n".join([
            f"From: {from_email}",
            f"To: {to_email}",
            f"Subject: This must be the title2343!!?",
            f"Message-ID: <{self.ticket.comment_message_id}@{settings.DOMAIN}",
            "",
            content
        ])

        with SMTP(*self.address) as client:
            client.sendmail(from_email, [to_email], email_message)

        self.assertTrue(Comment.objects.filter(ticket=self.ticket, content=content, is_reply=False).exists())

    def test_reply_by_email_disabled(self):
        self.inbox.enable_reply_by_email = False
        self.inbox.save()

        from_email = self.student.email
        to_email = self.inbox.email
        content = "This is the content!!??"
        email_message = "\n".join([
            f"From: {from_email}",
            f"To: {to_email}",
            f"Subject: This must be the title2343!!?",
            f"Message-ID: <{self.ticket.comment_message_id}@{settings.DOMAIN}>",
            "",
            content
        ])

        with self.assertRaises(SMTPDataError):
            with SMTP(*self.address) as client:
                client.sendmail(from_email, [to_email], email_message)

        self.assertFalse(Comment.objects.filter(ticket=self.ticket, content=content, is_reply=False).exists())

    def test_create_ticket_by_email_disabled(self):
        self.inbox.enable_create_new_ticket_by_email = False
        self.inbox.save()

        from_email = self.student.email
        to_email = self.inbox.email
        title = "This must be the title2343!!?"
        content = "This is the content!!??"
        email_message = "\n".join([
            f"From: {from_email}",
            f"To: {to_email}",
            f"Subject: {title}",
            "",
            content
        ])

        with self.assertRaises(SMTPDataError):
            with SMTP(*self.address) as client:
                client.sendmail(from_email, [to_email], email_message)

        self.assertFalse(Ticket.objects.filter(title=title, content=content).exists())