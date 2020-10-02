from smtplib import SMTP
from django.test import TestCase

from ticketvise.email.smtp import SmtpServer
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, Role


class SmtpServerTestCase(TestCase):

    def setUp(self):
        # setup of test SMTP server
        self.smtp_server = SmtpServer()
        self.smtp_server.start()

        self.controller = self.smtp_server.controller
        self.addCleanup(self.smtp_server.stop)
        self.address = (self.smtp_server.controller.hostname, self.smtp_server.controller.port)

        # setup test data
        self.inbox = Inbox.objects.create(code="test", name="test-inbox", email="ticket@ticketvise.com")
        self.student = User.objects.create(username="student", email="student@ticketvise.com")
        self.assistant = User.objects.create(username="assistant", email="assistant@ticketvise.com")
        self.ticket = Ticket.objects.create(inbox=self.inbox, author=self.student, assignee=self.assistant, title="help",
                                            content="pls")

        self.student.add_inbox(inbox=self.inbox, role=Role.GUEST)
        self.assistant.add_inbox(inbox=self.inbox, role=Role.AGENT)

    def test_send_new_email_with_known_user(self):
        with SMTP(*self.address) as client:
            client.sendmail('anne@example.com', ['bart@example.com'], """\
        From: Anne Person <anne@example.com>
        To: Bart Person <bart@example.com>
        Subject: A test
        Testing
        """)

    def test_send_new_email_with_unknown_user(self):
        raise NotImplemented

    def test_send_reply_email_with_known_user(self):
        raise NotImplemented

    def test_send_reply_email_with_unknown_user(self):
        raise NotImplemented
