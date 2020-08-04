"""
Test Courses
-------------------------------
This file tests the functionality of the courses/home page.
"""
from urllib.parse import urlencode

from django.test import TestCase, Client
from django.urls import reverse

from ticketvise.models.user import User
from ticketvise.tests.utils import create_course


class CourseConfigureTestCase(TestCase):
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

    def test_courses_page_student_200(self):
        """
        Authorized users should see the courses page.
        """
        self.client.force_login(self.student)
        course = create_course("TestCourse", "TestCourse")
        self.student.add_course(course, User.Roles.STUDENT)
        response = self.client.get(reverse("courses"))
        self.assertEqual(response.status_code, 200)

    def test_courses_page_assistant_200(self):
        """
        Authorized users should see the courses page.

        :return: None.
        """
        self.client.force_login(self.assistant)
        course = create_course("TestCourse", "TestCourse")
        self.assistant.add_course(course, User.Roles.ASSISTANT)
        response = self.client.get(reverse("courses"))
        self.assertEqual(response.status_code, 200)

    def test_courses_page_coordinator_200(self):
        """
        Authorized users should see the courses page.

        :return: None.
        """
        self.client.login(username=self.coordinator.username, password="test12345")
        course = create_course("TestCourse", "TestCourse")
        self.coordinator.add_course(course, User.Roles.COORDINATOR)
        response = self.client.get(reverse("courses"))
        self.assertEqual(response.status_code, 200)

    def test_flip_bookmark(self):
        """
        Test if a user can flip the bookmarked status.

        :return: None
        """
        self.client.login(username=self.coordinator.username, password="test12345")
        course = create_course("TestCourse", "TestCourse")
        self.coordinator.add_course(course, User.Roles.COORDINATOR)
        relation = self.coordinator.get_entry_by_course(course)
        self.assertFalse(relation.is_bookmarked)

        data = {
            "course_id": course.id,
        }

        # Check if bookmarked can be flipped to true
        response = self.client.post("/courses", urlencode(data), follow=True,
                                    content_type="application/x-www-form-urlencoded")
        self.assertTrue(response.redirect_chain, "/courses")

        relation = self.coordinator.get_entry_by_course(course)
        self.assertTrue(relation.is_bookmarked)

        # Check if bookrmarked can be flipped to false
        response = self.client.post("/courses", urlencode(data), follow=True,
                                    content_type="application/x-www-form-urlencoded")
        self.assertTrue(response.redirect_chain, "/courses")

        relation = self.coordinator.get_entry_by_course(course)
        self.assertFalse(relation.is_bookmarked)
