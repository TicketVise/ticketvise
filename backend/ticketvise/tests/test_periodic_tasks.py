"""
Test Periodic Tasks
-------------------------------
This file tests the periodic routine tasks that the platform runs.
"""
from django.test import TestCase, Client
from django.utils import timezone

from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User
from ticketvise.tasks import update_tickets, alert_unanswered_tickets


# class PeriodicTasksTestCase(TestCase):
#     def setUp(self):
#         """
#         Setup for each of these tests.
#         We create a course and student and coordinator with which we create tickets to test with.
#
#         :return: None.
#         """
#         self.client = Client()
#
#         self.course = create_course()
#         self.course.close_answered_weeks = 2
#         self.course.alert_coordinator_unanswered_days = 3
#         self.course.save()
#
#         self.student = User.objects.create_user(
#             username="student", email="root@ticketvise.com", password="test12345", is_staff=False,
#         )
#         self.student.set_password("test12345")
#         self.student.save()
#         self.student.add_course(self.course)
#
#         self.coordinator = create_user_with_course(
#             "coordinator",
#             email="root2@ticketvise.com",
#             password="test12345",
#             course=self.course,
#             role=User.Roles.COORDINATOR,
#         )
#
#         self.ticket = create_ticket(self.student, self.student, self.course, "question", content="question")
#
#         self.ticket2 = create_ticket(self.student, self.student, self.course, "question", content="question")
#
#     def test_update_old_answered_tickets_older(self):
#         """
#         Make sure that answered tickets older than the specified time get closed.
#
#         :return: None.
#         """
#         self.ticket.status = Ticket.Status.ANSWERED
#         self.ticket.save()
#
#         Ticket.objects.all().update(date_edited=timezone.now() - timezone.timedelta(days=15))
#
#         update_tickets.apply()
#
#         self.assertEqual(Ticket.Status.CLOSED, Ticket.objects.all()[0].status)
#
#     def test_update_old_answered_tickets_newer(self):
#         """
#         Make sure that answered tickets newer than the specified time remain answered.
#
#         :return: None.
#         """
#         self.ticket.status = Ticket.Status.ANSWERED
#         self.ticket.save()
#
#         Ticket.objects.all().update(date_edited=timezone.now() - timezone.timedelta(days=13))
#
#         update_tickets.apply()
#
#         self.assertEqual(Ticket.Status.ANSWERED, Ticket.objects.all()[0].status)
#
#     def test_update_old_answered_tickets_not_answered(self):
#         """
#         Make sure that tickets that are not answered are not affected by the auto-closing.
#
#         :return: None.
#         """
#         self.ticket.status = Ticket.Status.PENDING
#         self.ticket.save()
#
#         self.ticket2.status = Ticket.Status.ASSIGNED
#         self.ticket2.save()
#
#         Ticket.objects.all().update(date_edited=timezone.now() - timezone.timedelta(days=15))
#
#         update_tickets.apply()
#
#         self.assertFalse(Ticket.objects.filter(status=Ticket.Status.CLOSED).exists())
#
#     def test_unanswered_ticket_alert(self):
#         """
#         Make sure that the email alert task executes successfully.
#
#         :return: None.
#         """
#         self.ticket.status = Ticket.Status.PENDING
#         self.ticket.save()
#
#         self.ticket2.status = Ticket.Status.ASSIGNED
#         self.ticket2.save()
#
#         Ticket.objects.all().update(date_edited=timezone.now() - timezone.timedelta(days=4))
#
#         task = alert_unanswered_tickets.apply()
#         self.assertTrue(task.successful())
