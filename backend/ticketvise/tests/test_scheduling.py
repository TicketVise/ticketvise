"""
Test Scheduling
-------------------------------
This file tests the scheduling algorithms to divide the workload amond TAs.
"""
from django.test import TestCase, Client

from ticketvise.models.inbox import SchedulingAlgorithm, Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, UserInbox, Role


class TicketTestCase(TestCase):
    def setUp(self):
        """
        Set up the database for the tests.

        :return: None.
        """
        self.client = Client()

        self.inbox = Inbox.objects.create(name="TestInbox", code="TestCode", color="#FF6600")

        self.student = User.objects.create(username="student", email="student@test.com")
        UserInbox.objects.create(user=self.student, inbox=self.inbox, role=Role.GUEST)

        self.assistant1 = User.objects.create(username="assistant1", email="assistant1@test.com")
        UserInbox.objects.create(user=self.assistant1, inbox=self.inbox, role=Role.AGENT)

        self.assistant2 = User.objects.create(username="assistant2", email="assistant2@test.com")
        UserInbox.objects.create(user=self.assistant2, inbox=self.inbox, role=Role.AGENT)

        self.assistant3 = User.objects.create(username="assistant3", email="assistant3@test.com")
        UserInbox.objects.create(user=self.assistant3, inbox=self.inbox, role=Role.AGENT)

        self.assistants = [self.assistant1, self.assistant2, self.assistant3]

    def test_inbox_fixed_none_scheduling(self):
        """
        Test if scheduling is using the inbox when no labels are assigned to the ticket.

        :return: None.
        """
        self.inbox.scheduling_algorithm = SchedulingAlgorithm.FIXED
        self.inbox.fixed_scheduling_assignee = None
        self.inbox.save()

        ticket = Ticket.objects.create(author=self.student, title="Ticket4", content="", inbox=self.inbox)

        self.assertEqual(ticket.assignee, None)

    def test_inbox_least_assigned_first_scheduling(self):
        """
        Assign to least assigned assistant using inbox.

        :return: None.
        """
        self.inbox.scheduling_algorithm = SchedulingAlgorithm.LEAST_ASSIGNED_FIRST
        self.inbox.save()

        ticket = Ticket.objects.create(author=self.student, title="Ticket4", content="", inbox=self.inbox)

        self.assertEqual(ticket.assignee, self.assistant1)

    def test_inbox_fixed_scheduling(self):
        """
        Assign to fixed assistant using inbox.

        :return: None.
        """
        self.inbox.scheduling_algorithm = SchedulingAlgorithm.FIXED
        self.inbox.fixed_scheduling_assignee = self.assistant1
        self.inbox.save()

        ticket1 = Ticket.objects.create(author=self.student, title="Ticket4", content="", inbox=self.inbox)
        ticket2 = Ticket.objects.create(author=self.student, title="Foo", content="", inbox=self.inbox)

        self.assertEqual(ticket1.assignee, self.assistant1)
        self.assertEqual(ticket2.assignee, self.assistant1)

    def test_round_robin_scheduling(self):
        """
        Test round robin scheduling algorithm for the inbox.

        :return: None.
        """
        self.inbox.scheduling_algorithm = SchedulingAlgorithm.ROUND_ROBIN
        self.inbox.save()
        schedule_amount = 3

        for i in range(schedule_amount):
            for assistant in self.assistants:
                ticket = Ticket.objects.create(author=self.student, title="Ticket4", content="", inbox=self.inbox)

                self.assertEqual(ticket.assignee, assistant)
                Ticket.objects.get(pk=ticket.id).delete()

        self.assertEqual(self.inbox.round_robin_parameter,
                         schedule_amount * len(self.assistants))

    def test_not_implemented_algorithm(self):
        self.inbox.scheduling_algorithm = "Test"
        with self.assertRaises(NotImplementedError):
            Ticket.objects.create(author=self.student, title="Ticket4", content="", inbox=self.inbox)
