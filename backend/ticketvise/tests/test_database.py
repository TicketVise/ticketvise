"""
Test Database
-------------------------------
This file tests the database of the website.
"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User
from ticketvise.models.validators import validate_hex_color
from ticketvise.tests.utils import create_user, create_course, random_string


class DatabaseTestCase(TestCase):
    """
    Tests for the database.
    """

    def setUp(self):
        """
        Set up the database.

        :return: None.
        """
        self.user = create_user()
        self.course = create_course()
        self.role = User.Roles.ASSISTANT

    def test_validate_hex_color(self):
        """
        Test the validate_hex_color validator.

        :return: None.

        :raises AssertionError: When validate_hex_color raises an error for valid color.
        """
        try:
            validate_hex_color("#ffffff")
        except ValidationError:
            raise AssertionError("Method raised an exception where it shouldn't have.")

        self.assertRaises(ValidationError, validate_hex_color, random_string())

    def test_user(self):
        """
        Test the User model functions.

        :return: None.
        """
        not_enrolled_course = create_course()
        student_course = create_course()

        # Add courses
        self.user.add_course(self.course)
        self.user.add_course(student_course)
        self.assertRaises(ValueError, self.user.add_course, self.course)

        # Check courses
        self.assertTrue(self.user.has_course(self.course))
        self.assertTrue(self.user.has_course(student_course))

        # Check default roles
        self.assertTrue(self.user.has_role_in_course(self.course, User.Roles.STUDENT))
        self.assertTrue(self.user.has_role_in_course(student_course, User.Roles.STUDENT))

        # Check new roles
        self.user.set_role_for_course(self.course, self.role)
        self.assertTrue(self.user.has_role_in_course(self.course, self.role))
        self.assertEqual(self.user.get_courses_by_role(self.role).first(), self.course)
        self.assertRaises(ValueError, self.user.set_role_for_course, not_enrolled_course, self.role)

        # Check is_assistant_or_coordinator
        self.assertEqual(self.user.is_assistant_or_coordinator(not_enrolled_course), None)
        self.assertEqual(self.user.is_assistant_or_coordinator(student_course), False)
        self.assertEqual(self.user.is_assistant_or_coordinator(self.course), True)

    def test_course(self):
        """
        Test the Course model functions.

        :return: None.
        """
        # Setup
        student = create_user()
        ticket_assigned = Ticket.objects.create(author=student, assignee=self.user, course=self.course, status=Ticket.Status.ASSIGNED)
        ticket_closed = Ticket.objects.create(author=student, assignee=self.user, course=self.course, status=Ticket.Status.CLOSED)

        self.user.add_course(self.course)
        self.user.set_role_for_course(self.course, self.role)

        # Check functions
        self.assertEqual(self.course.get_users_by_role(self.role).first(), self.user)
        self.assertEqual(self.course.get_assistants_and_coordinators().first(), self.user)
        self.assertEqual(self.course.get_tickets_by_assignee(self.user).first(), ticket_assigned)
        self.assertEqual(self.course.get_tickets_by_author(student).first(), ticket_assigned)
        self.assertEqual(self.course.get_tickets_by_assignee(self.user, Ticket.Status.CLOSED).first(), ticket_closed)
        self.assertEqual(self.course.get_tickets_by_author(student, Ticket.Status.CLOSED).first(), ticket_closed)
