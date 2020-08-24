"""
Test Database
-------------------------------
This file tests the database of the website.
"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from ticketvise.models.ticket import Ticket, Status
from ticketvise.models.user import User, Role
from ticketvise.models.validators import validate_hex_color
from ticketvise.tests.utils import create_user, create_inbox, random_string


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
        self.inbox = create_inbox()
        self.role = Role.AGENT

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
        not_enrolled_inbox = create_inbox()
        student_inbox = create_inbox()

        # Add inboxes
        self.user.add_inbox(self.inbox)
        self.user.add_inbox(student_inbox)
        self.assertRaises(ValueError, self.user.add_inbox, self.inbox)

        # Check inboxes
        self.assertTrue(self.user.has_inbox(self.inbox))
        self.assertTrue(self.user.has_inbox(student_inbox))

        # Check default roles
        self.assertTrue(self.user.has_role_in_inbox(self.inbox, Role.GUEST))
        self.assertTrue(self.user.has_role_in_inbox(student_inbox, Role.GUEST))

        # Check new roles
        self.user.set_role_for_inbox(self.inbox, self.role)
        self.assertTrue(self.user.has_role_in_inbox(self.inbox, self.role))
        self.assertEqual(self.user.get_inboxes_by_role(self.role).first(), self.inbox)
        self.assertRaises(ValueError, self.user.set_role_for_inbox, not_enrolled_inbox, self.role)

        # Check is_assistant_or_coordinator
        self.assertEqual(self.user.is_assistant_or_coordinator(not_enrolled_inbox), None)
        self.assertEqual(self.user.is_assistant_or_coordinator(student_inbox), False)
        self.assertEqual(self.user.is_assistant_or_coordinator(self.inbox), True)

    def test_inbox(self):
        """
        Test the Inbox model functions.

        :return: None.
        """
        # Setup
        student = create_user()
        ticket_assigned = Ticket.objects.create(author=student, assignee=self.user, inbox=self.inbox, status=Status.ASSIGNED)
        ticket_closed = Ticket.objects.create(author=student, assignee=self.user, inbox=self.inbox, status=Status.CLOSED)

        self.user.add_inbox(self.inbox)
        self.user.set_role_for_inbox(self.inbox, self.role)

        # Check functions
        self.assertEqual(self.inbox.get_users_by_role(self.role).first(), self.user)
        self.assertEqual(self.inbox.get_assistants_and_coordinators().first(), self.user)
        self.assertEqual(self.inbox.get_tickets_by_assignee(self.user).first(), ticket_assigned)
        self.assertEqual(self.inbox.get_tickets_by_author(student).first(), ticket_assigned)
        self.assertEqual(self.inbox.get_tickets_by_assignee(self.user, Status.CLOSED).first(), ticket_closed)
        self.assertEqual(self.inbox.get_tickets_by_author(student, Status.CLOSED).first(), ticket_closed)
