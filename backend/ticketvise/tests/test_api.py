"""
Test API
-------------------------------
This file tests the API endpoints of the website.
"""

from django.test import TestCase, Client

from ticketvise.models.user import User
from ticketvise.tests.utils import create_course, create_ticket


class ApiTestCase(TestCase):
    def setUp(self):
        """
        Setup for each of these tests.

        :return: None.
        """
        self.client = Client()
        self.course1 = create_course("coures1", "c1")
        self.course2 = create_course("coures2", "c2")
        self.ta1 = User.objects.create(username="ta1", email="ta1@test.nl", password="ta1")
        self.ta1.add_course(self.course1)
        self.ta1.set_role_for_course(self.course1, User.Roles.ASSISTANT)
        self.ta2 = User.objects.create(username="ta2", email="ta2@test.nl", password="ta2")
        self.ta2.add_course(self.course1)
        self.ta2.set_role_for_course(self.course1, User.Roles.ASSISTANT)
        self.ta3 = User.objects.create(username="ta3", email="ta3@test.nl", password="ta3")
        self.ta3.add_course(self.course1)
        self.ta3.set_role_for_course(self.course1, User.Roles.COORDINATOR)
        self.ta4 = User.objects.create(username="ta4", email="ta4@test.nl", password="ta4")
        self.ta4.add_course(self.course2)
        self.ta4.set_role_for_course(self.course2, User.Roles.COORDINATOR)
        self.ta5 = User.objects.create(username="ta5", email="ta5@test.nl", password="ta5")
        self.ta5.add_course(self.course2)
        self.ta5.set_role_for_course(self.course2, User.Roles.ASSISTANT)
        self.student1 = User.objects.create(username="s1", password="s1")
        self.student1.add_course(self.course1)
        self.student1.set_role_for_course(self.course1, User.Roles.STUDENT)

        self.ticket1 = create_ticket(author=self.student1, assignee=self.ta5, course=self.course2)
        self.ticket2 = create_ticket(author=self.student1, assignee=self.ta4, course=self.course2)
        self.ticket3 = create_ticket(author=self.student1, assignee=self.ta4, course=self.course2)
        self.ticket4 = create_ticket(author=self.student1, assignee=self.ta4, course=self.course1)
        self.ticket5 = create_ticket(author=self.student1, assignee=self.ta4, course=self.course1)

    def test_unknown_course_users(self):
        """
        Testing if a HTTP 404 is returned when a course id does not exist.
        :return: None
        """
        self.client.login(username="ta1", password="ta1")
        response = self.client.get("/api/courses/345345/users", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_unknown_course_tickets(self):
        """
        Testing if a HTTP 404 is returned when a course id does not exist.
        :return: None
        """
        self.client.force_login(self.ta1)
        response = self.client.get("/api/courses/345345/tickets", follow=True)
        self.assertEqual(response.status_code, 404)

    def test_course_tickets(self):
        """
        Testing if the correct tickets which are associated with the course are returned.
        :return: None
        """
        self.client.force_login(self.ta1)
        response = self.client.get(f"/api/courses/{self.course1.id}/tickets", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

        self.assertContains(response, self.ticket4.title)
        self.assertContains(response, self.ticket5.title)
        self.assertNotContains(response, self.ticket1.title)
        self.assertNotContains(response, self.ticket2.title)
        self.assertNotContains(response, self.ticket3.title)
