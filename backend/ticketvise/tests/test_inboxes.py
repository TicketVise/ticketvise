"""
Test Inboxs
-------------------------------
This file tests the functionality of the inboxes/home page.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ticketvise.models.user import User, Role
from ticketvise.tests.utils import create_inbox


class InboxConfigureTestCase(TestCase):
    def setUp(self):
        """
        Set up the database for the tests.

        :return: None.
        """
        self.client = APIClient()
        self.student = User.objects.create_user(username="student", email="root@ticketvise.com", password="test12345",
                                                is_staff=False)
        self.assistant = User.objects.create_user(username="assistant", email="assitant@ticketvise.com",
                                                  password="test12345", is_staff=False)
        self.coordinator = User.objects.create_user(username="coordinator", email="coordinator@ticketvise.com",
                                                    password="test12345", is_staff=False)

    def test_inboxes_page_student_200(self):
        """
        Authorized users should see the inboxes page.
        """
        self.client.force_authenticate(self.student)
        inbox = create_inbox("TestInbox", "TestInbox")
        self.student.add_inbox(inbox, Role.GUEST)
        response = self.client.get(reverse("api_me_inboxes"))
        self.assertEqual(response.status_code, 200)

    def test_inboxes_page_assistant_200(self):
        """
        Authorized users should see the inboxes page.

        :return: None.
        """
        self.client.force_authenticate(self.assistant)
        inbox = create_inbox("TestInbox", "TestInbox")
        self.assistant.add_inbox(inbox, Role.AGENT)
        response = self.client.get(reverse("api_me_inboxes"))
        self.assertEqual(response.status_code, 200)

    def test_inboxes_page_coordinator_200(self):
        """
        Authorized users should see the inboxes page.

        :return: None.
        """
        self.client.force_authenticate(self.coordinator)
        inbox = create_inbox("TestInbox", "TestInbox")
        self.coordinator.add_inbox(inbox, Role.MANAGER)
        response = self.client.get(reverse("api_me_inboxes"))
        self.assertEqual(response.status_code, 200)

    def test_flip_bookmark(self):
        """
        Test if a user can flip the bookmarked status.

        :return: None
        """
        self.client.force_authenticate(self.coordinator)
        inbox = create_inbox("TestInbox", "TestInbox")
        self.coordinator.add_inbox(inbox, Role.MANAGER)
        relation = self.coordinator.get_entry_by_inbox(inbox)
        self.assertFalse(relation.is_bookmarked)

        data = {
            "inbox_id": inbox.id,
        }

        # Check if bookmarked can be flipped to true
        response = self.client.post(reverse("api_me_inboxes"), data)
        self.assertTrue(response.status_code, 200)

        relation = self.coordinator.get_entry_by_inbox(inbox)
        self.assertTrue(relation.is_bookmarked)

        # Check if bookrmarked can be flipped to false
        response = self.client.post(reverse("api_me_inboxes"), data)
        self.assertTrue(response.status_code, 200)

        relation = self.coordinator.get_entry_by_inbox(inbox)
        self.assertFalse(relation.is_bookmarked)

    def test_bookmark_unrelated(self):
        """
        Test if unrelated user can bookmark inbox
        """
        student2 = User.objects.create_user(username="student2", email="student2@ticketvise.com", password="test12345",
                                           is_staff=False)
        self.client.force_authenticate(student2)
        inbox = create_inbox("TestInbox", "TestInbox")
        data = {
            "inbox_id": inbox.id,
        }

        with self.assertRaises(ValueError):
            self.client.post("/api/me/inboxes", data)

    def test_inbox_sorting(self):
        """
        Test if Inboxes are sorted by user joined date
        """
        self.client.force_authenticate(self.student)

        inbox1 = create_inbox("TestInbox1", "TestInbox1")
        inbox2 = create_inbox("TestInbox2", "TestInbox2")
        inbox3 = create_inbox("TestInbox3", "TestInbox3")
        self.student.add_inbox(inbox1, Role.GUEST)
        self.student.add_inbox(inbox3, Role.GUEST)
        self.student.add_inbox(inbox2, Role.GUEST)

        response = self.client.get(reverse("api_me_inboxes"))
        self.assertTrue(response.status_code, 200)

        self.assertEqual(response.data[0]["inbox"]["name"], "TestInbox2")
        self.assertEqual(response.data[1]["inbox"]["name"], "TestInbox3")