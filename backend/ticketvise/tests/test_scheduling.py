"""
Test Scheduling
-------------------------------
This file tests the scheduling algorithms to divide the workload amond TAs.
"""
from django.test import TestCase, Client

from ticketvise.models.inbox import SchedulingAlgorithm
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, UserCourseRelationship
from ticketvise.scheduling import schedule_ticket
from ticketvise.tests.utils import create_course


class TicketTestCase(TestCase):
    def setUp(self):
        """
        Set up the database for the tests.

        :return: None.
        """
        self.client = Client()

        self.course = create_course("course1", "code1", "#000000")
        self.course.save()

        self.student = User.objects.create(username="student", email="student@test.com")
        UserCourseRelationship.objects.create(user=self.student, course=self.course, role=User.Roles.STUDENT)

        self.assistant1 = User.objects.create(username="assistant1", email="assistant1@test.com")
        UserCourseRelationship.objects.create(user=self.assistant1, course=self.course, role=User.Roles.ASSISTANT)

        self.assistant2 = User.objects.create(username="assistant2", email="assistant2@test.com")
        UserCourseRelationship.objects.create(user=self.assistant2, course=self.course, role=User.Roles.ASSISTANT)

        self.assistant3 = User.objects.create(username="assistant3", email="assistant3@test.com")
        UserCourseRelationship.objects.create(user=self.assistant3, course=self.course, role=User.Roles.ASSISTANT)

        self.assistants = [self.assistant1, self.assistant2, self.assistant3]

        self.ticket1 = Ticket.objects.create(author=self.student, assignee=self.assistant1, title="Ticket1", content="",
                                             course=self.course)
        self.ticket2 = Ticket.objects.create(author=self.student, assignee=self.assistant2, title="Ticket2", content="",
                                             course=self.course)
        Ticket.objects.create(author=self.student, assignee=self.assistant2, title="Ticket2", content="",
                              course=self.course)
        self.ticket3 = Ticket.objects.create(author=self.student, assignee=self.assistant3, title="Ticket3", content="",
                                             course=self.course)
        Ticket.objects.create(author=self.student, assignee=self.assistant3, title="Ticket3", content="",
                                             course=self.course)
        self.ticket4 = Ticket.objects.create(author=self.student, title="Ticket4", content="", course=self.course)

    def test_course_manual_scheduling(self):
        """
        Test if scheduling is using the course when no labels are assigned to the ticket.

        :return: None.
        """
        self.course.scheduling_algorithm = SchedulingAlgorithm.MANUAL
        self.course.save()

        schedule_ticket(self.ticket4)
        self.assertEqual(self.ticket4.assignee, None)

    def test_course_least_assigned_first_scheduling(self):
        """
        Assign to least assigned assistant using course.

        :return: None.
        """
        self.course.scheduling_algorithm = SchedulingAlgorithm.LEAST_ASSIGNED_FIRST
        self.course.save()

        schedule_ticket(self.ticket4)
        self.assertEqual(self.ticket4.assignee, self.assistant1)

    def test_round_robin_scheduling(self):
        """
        Test round robin scheduling algorithm for the course.

        :return: None.
        """
        self.course.scheduling_algorithm = SchedulingAlgorithm.ROUND_ROBIN
        self.course.save()
        schedule_amount = 3

        for i in range(schedule_amount):
            for assistant in self.assistants:
                self.ticket4.labels.clear()
                self.ticket4.save()

                schedule_ticket(self.ticket4)
                self.assertEqual(self.ticket4.assignee, assistant)

        self.assertEqual(self.course.round_robin_parameter,
                         schedule_amount * len(self.assistants))
