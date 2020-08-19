"""
Test Inboxs
-------------------------------
This file tests the functionality of the inboxes/home page.
"""
from urllib.parse import urlencode

from django.test import TestCase, Client
from django.urls import reverse

from ticketvise.models.user import User, Role
from ticketvise.tests.utils import create_inbox
from ticketvise.utils import get_text_color


class InboxConfigureTestCase(TestCase):
    def setUp(self):
        """
        Set up the database for the tests.

        :return: None.
        """
        self.client = Client()
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
        self.client.force_login(self.student)
        inbox = create_inbox("TestInbox", "TestInbox")
        self.student.add_inbox(inbox, Role.GUEST)
        response = self.client.get(reverse("inboxes"))
        self.assertEqual(response.status_code, 200)

    def test_inboxes_page_assistant_200(self):
        """
        Authorized users should see the inboxes page.

        :return: None.
        """
        self.client.force_login(self.assistant)
        inbox = create_inbox("TestInbox", "TestInbox")
        self.assistant.add_inbox(inbox, Role.AGENT)
        response = self.client.get(reverse("inboxes"))
        self.assertEqual(response.status_code, 200)

    def test_inboxes_page_coordinator_200(self):
        """
        Authorized users should see the inboxes page.

        :return: None.
        """
        self.client.login(username=self.coordinator.username, password="test12345")
        inbox = create_inbox("TestInbox", "TestInbox")
        self.coordinator.add_inbox(inbox, Role.MANAGER)
        response = self.client.get(reverse("inboxes"))
        self.assertEqual(response.status_code, 200)

    def test_flip_bookmark(self):
        """
        Test if a user can flip the bookmarked status.

        :return: None
        """
        self.client.login(username=self.coordinator.username, password="test12345")
        inbox = create_inbox("TestInbox", "TestInbox")
        self.coordinator.add_inbox(inbox, Role.MANAGER)
        relation = self.coordinator.get_entry_by_inbox(inbox)
        self.assertFalse(relation.is_bookmarked)

        data = {
            "inbox_id": inbox.id,
        }

        # Check if bookmarked can be flipped to true
        response = self.client.post("/inboxes", urlencode(data), follow=True,
                                    content_type="application/x-www-form-urlencoded")
        self.assertTrue(response.redirect_chain, "/inboxes")

        relation = self.coordinator.get_entry_by_inbox(inbox)
        self.assertTrue(relation.is_bookmarked)

        # Check if bookrmarked can be flipped to false
        response = self.client.post("/inboxes", urlencode(data), follow=True,
                                    content_type="application/x-www-form-urlencoded")
        self.assertTrue(response.redirect_chain, "/inboxes")

        relation = self.coordinator.get_entry_by_inbox(inbox)
        self.assertFalse(relation.is_bookmarked)

