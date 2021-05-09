from django.test import TestCase
from rest_framework.test import APIClient

from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, Role


class UserTestCase(TestCase):
    def setup(self):
        self.client = APIClient()
        self.inbox = Inbox.objects.create(name="TestInbox", code="TestCode", color="#FF6600")
        self.inbox2 = Inbox.objects.create(name="TestInbox2", code="TestCode", color="#FF6600")
        self.student = User.objects.create(username="student", password="test12345", email="student@ticketvise.com")
        self.student.add_inbox(self.inbox)
        self.student.set_role_for_inbox(self.inbox, Role.GUEST)
        self.student2 = User.objects.create(username="student2", password="test12345", email="student2@ticketvise.com")
        self.student2.add_inbox(self.inbox)
        self.student2.set_role_for_inbox(self.inbox, Role.GUEST)
        self.student3 = User.objects.create(username="student3", password="test12345", email="student2@ticketvise.com")
        self.student3.add_inbox(self.inbox)
        self.student3.set_role_for_inbox(self.inbox, Role.GUEST)
        self.assistant = User.objects.create(username="assistant", password="test67891",
                                             email="assistant@ticketvise.com")
        self.assistant.add_inbox(self.inbox)
        self.assistant.set_role_for_inbox(self.inbox, Role.AGENT)

        self.manager = User.objects.create(username="manager", password="test67891",
                                           email="manager@ticketvise.com")
        self.manager.add_inbox(self.inbox)
        self.manager.set_role_for_inbox(self.inbox, Role.MANAGER)

        self.ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title="Ticket1",
                                            content="TestContent", inbox=self.inbox)
        self.ticket2 = Ticket.objects.create(author=self.student2, assignee=self.assistant, title="Ticket2",
                                             content="TestContent", inbox=self.inbox)
        self.ticket3 = Ticket.objects.create(author=self.student, assignee=self.assistant, title="Ticket3",
                                             content="TestContent", inbox=self.inbox2)

    def test_add_subscription_student(self):
        self.client.force_login(self.student)

        response = self.client.post(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.id}/subscribe")
        self.assertEqual(response.status_code, 200)