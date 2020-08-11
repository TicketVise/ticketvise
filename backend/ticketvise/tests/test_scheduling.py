"""
Test Scheduling
-------------------------------
This file tests the scheduling algorithms to divide the workload amond TAs.
"""
from django.test import TestCase, Client

from ticketvise.models.inbox import SchedulingAlgorithm
from ticketvise.models.ticket import Ticket, TicketLabel
from ticketvise.models.user import User, UserInbox, Role
from ticketvise.scheduling import schedule_ticket
from ticketvise.tests.utils import create_inbox


class TicketTestCase(TestCase):
    def setUp(self):
        """
        Set up the database for the tests.

        :return: None.
        """
        self.client = Client()

        self.inbox = create_inbox("inbox1", "code1", "#000000")
        self.inbox.save()

        self.student = User.objects.create(username="student", email="student@test.com")
        UserInbox.objects.create(user=self.student, inbox=self.inbox, role=Role.GUEST)

        self.assistant1 = User.objects.create(username="assistant1", email="assistant1@test.com")
        UserInbox.objects.create(user=self.assistant1, inbox=self.inbox, role=Role.AGENT)

        self.assistant2 = User.objects.create(username="assistant2", email="assistant2@test.com")
        UserInbox.objects.create(user=self.assistant2, inbox=self.inbox, role=Role.AGENT)

        self.assistant3 = User.objects.create(username="assistant3", email="assistant3@test.com")
        UserInbox.objects.create(user=self.assistant3, inbox=self.inbox, role=Role.AGENT)

        self.assistants = [self.assistant1, self.assistant2, self.assistant3]

        self.ticket1 = Ticket.objects.create(author=self.student, assignee=self.assistant1, title="Ticket1", content="",
                                             inbox=self.inbox)
        self.ticket2 = Ticket.objects.create(author=self.student, assignee=self.assistant2, title="Ticket2", content="",
                                             inbox=self.inbox)
        Ticket.objects.create(author=self.student, assignee=self.assistant2, title="Ticket2", content="",
                              inbox=self.inbox)
        self.ticket3 = Ticket.objects.create(author=self.student, assignee=self.assistant3, title="Ticket3", content="",
                                             inbox=self.inbox)
        Ticket.objects.create(author=self.student, assignee=self.assistant3, title="Ticket3", content="",
                                             inbox=self.inbox)
        self.ticket4 = Ticket.objects.create(author=self.student, title="Ticket4", content="", inbox=self.inbox)

    def test_inbox_manual_scheduling(self):
        """
        Test if scheduling is using the inbox when no labels are assigned to the ticket.

        :return: None.
        """
        self.client.force_login(self.assistant3)
        self.inbox.scheduling_algorithm = SchedulingAlgorithm.MANUAL
        self.inbox.save()

        schedule_ticket(self.ticket4)
        self.assertEqual(self.ticket4.assignee, None)

    def test_inbox_least_assigned_first_scheduling(self):
        """
        Assign to least assigned assistant using inbox.

        :return: None.
        """
        self.inbox.scheduling_algorithm = SchedulingAlgorithm.LEAST_ASSIGNED_FIRST
        self.inbox.save()

        schedule_ticket(self.ticket4)
        self.assertEqual(self.ticket4.assignee, self.assistant1)

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
                TicketLabel.objects.filter(ticket=self.ticket4).delete()
                self.ticket4.save()

                schedule_ticket(self.ticket4)
                self.assertEqual(self.ticket4.assignee, assistant)

        self.assertEqual(self.inbox.round_robin_parameter,
                         schedule_amount * len(self.assistants))
