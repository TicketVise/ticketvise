import json

from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket, Status
from ticketvise.models.user import User, Role


class InboxTestCase(TransactionTestCase):
    def setUp(self):
        self.client = APIClient()
        self.inbox = Inbox.objects.create(name="TestInbox", code="TestCode", color="#FF6600")

        self.student = User.objects.create(username="student", password="test12345", email="student@ticketvise.com")
        self.student.add_inbox(self.inbox)
        self.student.set_role_for_inbox(self.inbox, Role.GUEST)

        self.student2 = User.objects.create(username="student2", password="test12345", email="student@ticketvise.com")

        self.assistant = User.objects.create(username="assistant", password="test67891",
                                             email="assistant@ticketvise.com")
        self.assistant.add_inbox(self.inbox)
        self.assistant.set_role_for_inbox(self.inbox, Role.AGENT)

        for i in range(26):
            self.ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title=i, content=i,
                                                inbox=self.inbox, status=Status.ASSIGNED)

    def test_inbox_page_200(self):
        self.client.force_authenticate(self.student)
        response = self.client.get(reverse("api_inbox_tickets", args=[self.inbox.id]))
        self.assertEqual(response.status_code, 200)

    def test_ticket_page_401(self):
        response = self.client.get(reverse("api_inbox_tickets", args=[self.inbox.id]))
        self.assertEqual(response.status_code, 401)

    def test_error_dispatch(self):
        self.client.force_authenticate(self.student2)
        response = self.client.get(reverse("api_inbox_tickets", args=[self.inbox.id]))
        self.assertEqual(response.status_code, 403)

    def test_load_partial(self):
        self.client.force_authenticate(self.assistant)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets?show_personal=false")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(len(data), 3)
        self.assertEqual(len(data[0]["tickets"]), 25)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets?show_personal=false&status=Assigned&page=2")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertFalse(data["has_next"])
        self.assertEqual(len(data["results"]), 1)

    def test_introduction(self):
        self.client.force_authenticate(self.assistant)

        response = self.client.get(f"/api/me/inboxes/{self.inbox.id}")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertTrue(data["give_introduction"])

        self.client.put(f"/api/me/inboxes/{self.inbox.id}/introduction")

        response = self.client.get(f"/api/me/inboxes/{self.inbox.id}")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertFalse(data["give_introduction"])
