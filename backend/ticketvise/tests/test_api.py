"""
Test API
-------------------------------
This file tests the API endpoints of the website.
"""
import json

from django.test import TestCase
from rest_framework.test import APIClient

from ticketvise.models.user import User, Role
from ticketvise.tests.utils import create_inbox, create_ticket


class ApiTestCase(TestCase):
    def setUp(self):
        """
        Setup for each of these tests.

        :return: None.
        """
        self.client = APIClient()
        self.inbox1 = create_inbox("coures1", "c1")
        self.inbox2 = create_inbox("coures2", "c2")
        self.inbox3 = create_inbox("coures3", "c3")
        self.manager1 = User.objects.create(username="m1", email="m1@test.nl", password="m1")
        self.manager1.add_inbox(self.inbox1)
        self.manager1.set_role_for_inbox(self.inbox1, Role.MANAGER)
        self.ta1 = User.objects.create(username="ta1", password="ta1")
        self.ta1.add_inbox(self.inbox1)
        self.ta1.add_inbox(self.inbox3)
        self.ta1.set_role_for_inbox(self.inbox1, Role.AGENT)
        self.ta2 = User.objects.create(username="ta2", password="ta2")
        self.ta2.add_inbox(self.inbox1)
        self.ta2.set_role_for_inbox(self.inbox1, Role.AGENT)
        self.ta3 = User.objects.create(username="ta3", password="ta3")
        self.ta3.add_inbox(self.inbox1)
        self.ta3.set_role_for_inbox(self.inbox1, Role.MANAGER)
        self.ta4 = User.objects.create(username="ta4", password="ta4")
        self.ta4.add_inbox(self.inbox2)
        self.ta4.set_role_for_inbox(self.inbox2, Role.MANAGER)
        self.ta5 = User.objects.create(username="ta5", password="ta5")
        self.ta5.add_inbox(self.inbox2)
        self.ta5.set_role_for_inbox(self.inbox2, Role.AGENT)
        self.student1 = User.objects.create(username="s1", password="s1")
        self.student1.add_inbox(self.inbox1)
        self.student1.set_role_for_inbox(self.inbox1, Role.GUEST)
        self.student2 = User.objects.create(username="s2", password="s2")
        self.student2.add_inbox(self.inbox1)
        self.student2.set_role_for_inbox(self.inbox1, Role.GUEST)
        self.student3 = User.objects.create(username="s3", password="s3")

        self.ticket1 = create_ticket(author=self.student1, assignee=self.ta5, inbox=self.inbox2)
        self.ticket2 = create_ticket(author=self.student1, assignee=self.ta4, inbox=self.inbox2)
        self.ticket3 = create_ticket(author=self.student1, assignee=self.ta4, inbox=self.inbox2)
        self.ticket4 = create_ticket(author=self.student1, assignee=self.ta4, inbox=self.inbox1)
        self.ticket5 = create_ticket(author=self.student1, assignee=self.ta4, inbox=self.inbox1)

    def test_unknown_inbox_users(self):
        """
        Testing if a HTTP 404 is returned when a inbox id does not exist.
        :return: None
        """
        self.client.force_authenticate(self.ta1)
        response = self.client.get("/api/inboxes/345345/users", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_unknown_inbox_tickets(self):
        """
        Testing if a HTTP 404 is returned when a inbox id does not exist.
        :return: None
        """
        self.client.force_authenticate(self.ta1)
        response = self.client.get("/api/inboxes/345345/tickets", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_inbox_tickets(self):
        """
        Testing if the correct tickets which are associated with the inbox are returned.
        :return: None
        """
        self.client.force_authenticate(self.ta1)
        response = self.client.get(f"/api/inboxes/{self.inbox1.id}/tickets", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

        self.assertContains(response, self.ticket4.title)
        self.assertContains(response, self.ticket5.title)
        self.assertNotContains(response, self.ticket1.title)
        self.assertNotContains(response, self.ticket2.title)
        self.assertNotContains(response, self.ticket3.title)

    def test_get_user_unknown_username(self):
        """
        Test get unknown username by valid user
        :return: None
        """
        self.client.force_authenticate(self.ta1)
        response = self.client.get(f"/api/inboxes/{self.inbox1.id}/users/unknown", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_get_user_username_not_in_inbox(self):
        """
        Test get username not in inbox by valid user
        :return: None
        """
        self.client.force_authenticate(self.ta4)
        response = self.client.get(f"/api/inboxes/{self.inbox2.id}/users/{self.student1}", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_get_self_role(self):
        self.client.force_authenticate(self.student1)
        response = self.client.get(f"/api/inboxes/{self.inbox1.id}/role")
        self.assertContains(response, "GUEST")

        self.client.force_authenticate(self.ta1)
        response = self.client.get(f"/api/inboxes/{self.inbox1.id}/role")
        self.assertContains(response, "AGENT")

        self.client.force_authenticate(self.manager1)
        response = self.client.get(f"/api/inboxes/{self.inbox1.id}/role")
        self.assertContains(response, "MANAGER")

    def test_get_current_user(self):
        self.client.force_authenticate(self.student1)
        response = self.client.get("/api/me")
        self.assertContains(response, self.student1.username)

        self.client.force_authenticate(self.ta1)
        response = self.client.get("/api/me")
        self.assertContains(response, self.ta1.username)

        self.client.force_authenticate(self.manager1)
        response = self.client.get("/api/me")
        self.assertContains(response, self.manager1.username)

    def test_get_user_settings(self):
        self.client.force_authenticate(self.student1)
        response = self.client.get("/api/me/settings")

        notifications = [
            "notification_mention_mail",
            "notification_mention_app",
            "notification_new_ticket_mail",
            "notification_new_ticket_app",
            "notification_comment_mail",
            "notification_comment_app",
            "notification_assigned_mail",
            "notification_assigned_app",
            "notification_ticket_reminder_mail",
            "notification_ticket_reminder_app"
        ]

        for notification in notifications:
            self.assertContains(response, notification)

    def test_get_users_filter(self):
        self.client.force_authenticate(self.student1)
        response = self.client.get(f"/api/inboxes/{self.inbox1.id}/guests")
        self.assertContains(response, "s1")
        self.assertEqual(str(response.content).count("s1"), 1)
        self.assertContains(response, "s2")

        response = self.client.get(f"/api/inboxes/{self.inbox1.id}/guests", {"q": "1"})
        self.assertContains(response, "s1")
        self.assertEqual(str(response.content).count("s1"), 1)
        self.assertNotContains(response, "s2")

    def test_get_users(self):
        self.client.force_authenticate(self.manager1)

        response = self.client.get(f"/api/inboxes/{self.inbox1.id}/users")

        self.assertContains(response, self.ta1.username)
        self.assertContains(response, self.ta2.username)
        self.assertContains(response, self.ta3.username)
        self.assertNotContains(response, self.ta4.username)

        self.assertEqual(str(response.content).count(self.ta1.username), 1)
        self.assertEqual(str(response.content).count(self.ta2.username), 1)
        self.assertEqual(str(response.content).count(self.ta3.username), 1)

    def test_introduction(self):
        self.client.force_authenticate(self.ta1)

        response = self.client.get(f"/api/me")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertTrue(data["give_introduction"])

        self.client.put(f"/api/me/introduction")

        response = self.client.get(f"/api/me")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertFalse(data["give_introduction"])

