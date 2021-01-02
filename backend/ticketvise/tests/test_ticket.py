"""
Test Ticket
-------------------------------
This file tests the ticket page that show the information of a ticket.
"""
import json

from django.db import transaction
from django.http import JsonResponse
from django.test import Client, TransactionTestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox, SchedulingAlgorithm
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, Status
from ticketvise.models.user import User, Role
from ticketvise.views.api.ticket import TicketSerializer
from ticketvise.views.api.user import UserSerializer


class TicketTestCase(TransactionTestCase):

    @transaction.atomic
    def setUp(self):
        """
        Set up the database for the tests.

        :return: None.
        """
        self.client = APIClient()
        self.inbox = Inbox.objects.create(name="TestInbox", code="TestCode", color="#FF6600")
        self.student = User.objects.create(username="student", password="test12345", email="student@ticketvise.com")
        self.student.add_inbox(self.inbox)
        self.student.set_role_for_inbox(self.inbox, Role.GUEST)
        self.student2 = User.objects.create(username="student2", password="test12345", email="student2@ticketvise.com")
        self.student2.add_inbox(self.inbox)
        self.student2.set_role_for_inbox(self.inbox, Role.GUEST)
        self.student3 = User.objects.create(username="student3", password="test12345", email="student2@ticketvise.com")
        self.student3.add_inbox(self.inbox)
        self.student3.set_role_for_inbox(self.inbox, Role.GUEST)
        self.assistant = User.objects.create(username="assistant", password="test67891",
                                             email="assistant@ticketvise.com")
        self.assistant.add_inbox(self.inbox)
        self.assistant.set_role_for_inbox(self.inbox, Role.AGENT)
        self.assistant2 = User.objects.create(username="assistant2", password="test67891",
                                              email="assistant2@ticketvise.com")
        self.assistant3 = User.objects.create(username="assistant3", password="test67891",
                                              email="assistant3@ticketvise.com")
        self.assistant3.add_inbox(self.inbox)
        self.assistant3.set_role_for_inbox(self.inbox, Role.AGENT)

        self.manager = User.objects.create(username="manager", password="test67891",
                                           email="manager@ticketvise.com")
        self.manager.add_inbox(self.inbox)
        self.manager.set_role_for_inbox(self.inbox, Role.MANAGER)

        self.label = Label.objects.create(name="Test-Label", inbox=self.inbox, is_visible_to_guest=True)
        self.label2 = Label.objects.create(name="TestLabel2", inbox=self.inbox, is_visible_to_guest=True)

        self.ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title="Ticket1",
                                            content="TestContent", inbox=self.inbox)
        self.ticket2 = Ticket.objects.create(author=self.student, assignee=self.assistant, title="Ticket2",
                                             content="TestContent", inbox=self.inbox)
        self.ticket2.shared_with.set([self.student2, self.student3])
        self.ticket3 = Ticket.objects.create(author=self.student2, assignee=self.assistant2, title="Ticket3",
                                             content="TestContent", inbox=self.inbox)
        self.ticket3.add_label(self.label)
        self.ticket2.add_label(self.label2)


class TicketTestBackendCase(TicketTestCase):
    def test_ticket_page_200(self):
        """
        Authorized users should see their own ticket.

        :return: None.
        """
        self.client.force_authenticate(self.student)
        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]))
        self.assertEqual(response.status_code, 200)

    def test_ticket_page_401(self):
        """
        Unauthorized users should be redirected to the login page. When logged in
        it should redirect to the ticket.

        :return: None.
        """
        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]))
        self.assertEqual(response.status_code, 401)

    def test_error_dispatch(self):
        """
        If the user is not the author of the ticket and the user is not
        a coordinator or a TA, it should give a 401 error.

        :return: None.
        """
        self.client.force_authenticate(self.student2)
        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]))
        self.assertEqual(response.status_code, 403)

    def test_get_ticket_as_unauthorized_student(self):
        """
        Test to verify a student cannot get the ticket
        """
        self.client.force_authenticate(self.student2)

        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]))
        self.assertEqual(response.status_code, 403)

    def test_get_ticket_as_author(self):
        """
        Test to verify an author can get the ticket
        """
        self.client.force_authenticate(self.student)

        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]))
        self.assertEqual(response.status_code, 200)

    def test_get_ticket_as_shared_with(self):
        """
        Test to verify an author can get the ticket
        """
        self.client.force_authenticate(self.student2)

        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket2.ticket_inbox_id]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_ticket_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get the ticket
        """
        self.client.force_authenticate(self.assistant)

        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]))
        self.assertEqual(response.status_code, 200)

    def test_get_ticket_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get the ticket
        """
        self.client.force_authenticate(self.assistant2)

        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]))
        self.assertEqual(response.status_code, 403)

    def test_get_staff_as_student(self):
        """
        Test to verify a student cannot get staff
        """
        self.client.force_authenticate(self.student2)

        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]),
                                   {"staff": "true"},
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_staff_as_author(self):
        """
        Test to verify an author cannot get staff
        """
        self.client.force_authenticate(self.student)

        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]),
                                   {"staff": "true"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"{}")

    def test_get_staff_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get staff
        """
        self.client.force_authenticate(self.assistant)

        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]),
                                   {"staff": "true"}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_staff_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get staff
        """
        self.client.force_authenticate(self.assistant2)

        response = self.client.get(reverse("api_inbox_ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]),
                                   {"staff": "true"}, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_labels_as_student(self):
        """
        Test to verify a student cannot get labels
        """
        self.client.force_authenticate(self.student2)

        response = self.client.get(reverse("api_all_inbox_labels", args=(self.inbox.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)

    def test_get_labels_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get labels
        """
        self.client.force_authenticate(self.assistant)

        response = self.client.get(reverse("api_all_inbox_labels", args=(self.inbox.id,)))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.label.name)

    def test_get_labels_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get labels
        """
        self.client.force_authenticate(self.assistant2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/labels",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_recent_as_student(self):
        """
        Test to verify a student cannot get recent tickets
        """
        self.client.force_authenticate(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/users/{self.ticket.author.id}/tickets/recent",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_recent_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get recent tickets
        """
        self.client.force_authenticate(self.assistant)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/users/{self.ticket.author.id}/tickets/recent",
                                   follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_recent_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get recent tickets
        """
        self.client.force_authenticate(self.assistant2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/users/{self.ticket.author.id}/tickets/recent",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_put_assignee_as_student(self):
        """
        Test to verify a student cannot change assignees
        """
        self.client.force_authenticate(self.student2)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/assignee",
                                   data={"assignee": self.assistant.id}, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertNotEqual(ticket.assignee, self.assistant3)

    def test_put_assignee_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can change assignees
        """
        self.client.force_authenticate(self.assistant)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/assignee",
                                   data={"assignee": self.assistant3.id})
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertEqual(ticket.assignee, self.assistant3)

    def test_put_assignee_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot change assignees
        """
        self.client.force_authenticate(self.assistant2)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/assignee",
                                   data={"assignee": self.assistant.id})
        self.assertEqual(response.status_code, 403)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertNotEqual(ticket.assignee, self.assistant3)

    def test_put_assignee_change_status(self):
        """
        Test to verify an assistant of the inbox can change assignees
        """
        self.client.force_authenticate(self.assistant)
        self.ticket.status = Status.PENDING
        self.ticket.assignee = None
        self.ticket.save()

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/assignee",
                                   data={"assignee": self.assistant3.id})
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertEqual(ticket.assignee, self.assistant3)
        self.assertEqual(ticket.status, "ASGD")

    def test_put_assignee_unassign(self):
        """
        Test to verify an assistant of the inbox can change assignees
        """
        self.client.force_authenticate(self.assistant)
        self.ticket.status = Status.ASSIGNED
        self.ticket.save()

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/assignee",
                                   {"assignee": ""})
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertEqual(ticket.assignee, None)
        self.assertEqual(ticket.status, "PNDG")

    def test_put_assignee_not_valid(self):
        """
        Test to verify an assistant of the inbox can change assignees
        """
        self.client.force_authenticate(self.assistant)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/assignee",
                                   data={"assignee": self.student.id})
        self.assertEqual(response.status_code, 400)

    def test_put_shared_with_as_author(self):
        """
        Test to verify a author cannot change shared_with
        """
        self.client.force_authenticate(self.student)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/shared",
                                   data={"shared_with": [self.student3.id]})
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertEqual(ticket.shared_with.all()[0], self.student3)

    def test_put_shared_with_as_shared_with(self):
        """
        Test to verify a shared_with cannot change shared_with
        """
        self.client.force_authenticate(self.student2)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}/shared",
                                   data={"shared_with": [self.student3.id]})
        self.assertEqual(response.status_code, 403)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertFalse(ticket.shared_with.all())

    def test_put_shared_with_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can change shared_with
        """
        self.client.force_authenticate(self.assistant)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/shared",
                                   data={"shared_with": [self.student3.id]})
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertEqual(ticket.shared_with.all()[0], self.student3)

    def test_put_shared_with_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot change shared_with
        """
        self.client.force_authenticate(self.assistant2)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/shared",
                                   data={"shared_with": [self.student3.id]})
        self.assertEqual(response.status_code, 403)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertFalse(ticket.shared_with.all())

    def test_get_shared_with_as_author(self):
        """
        Test to verify an author can retrieve shared with users.
        """
        self.client.force_authenticate(self.student)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}",
                                   {"ticket": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "student2")
        self.assertContains(response, "student3")

    def test_get_shared_with_as_shared_with(self):
        """
        Test to verify a shared_with cannot change shared_with
        """
        self.client.force_authenticate(self.student2)
        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}",
                                   {"ticket": "true"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.student2.username)

    def test_get_shared_with_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can change shared_with
        """
        self.client.force_authenticate(self.assistant)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}",
                                   {"ticket": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserSerializer(self.student2, fields=(
            ["first_name", "last_name", "username", "avatar_url", "id"])).data in response.data["ticket"]["shared_with"])

    def test_get_shared_with_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot change shared_with
        """
        self.client.force_authenticate(self.assistant2)
        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}",
                                   {"ticket": "true"})

        self.assertEqual(response.status_code, 403)

    def test_add_label(self):
        old_labels_count = self.ticket.labels.count()
        self.ticket.add_label(self.label)
        self.assertNotEqual(old_labels_count, Ticket.objects.get(pk=self.ticket.pk).labels.count())

    def test_delete_label(self):
        old_labels_count = self.ticket.labels.count()
        self.ticket.add_label(self.label)
        self.assertNotEqual(old_labels_count, Ticket.objects.get(pk=self.ticket.pk).labels.count())

        old_labels_count = self.ticket.labels.count()
        self.ticket.delete_label(self.label)
        self.assertNotEqual(old_labels_count, Ticket.objects.get(pk=self.ticket.pk).labels.count())

    def test_add_duplicate_label(self):
        old_labels_count = self.ticket.labels.count()
        self.ticket.add_label(self.label)
        self.assertNotEqual(old_labels_count, Ticket.objects.get(pk=self.ticket.pk).labels.count())

        old_labels_count = self.ticket.labels.count()
        self.ticket.add_label(self.label)
        self.assertEqual(old_labels_count, Ticket.objects.get(pk=self.ticket.pk).labels.count())

    def test_remove_no_label(self):
        old_labels_count = self.ticket.labels.count()
        self.ticket.delete_label(self.label)
        self.assertEqual(old_labels_count, Ticket.objects.get(pk=self.ticket.pk).labels.count())

    def test_inbox_show_assignee_to_guest_as_guest(self):
        """
        Test to verify that the assignee is hidden to a guest when the manager has disabled it in the inbox settings.
        """
        self.client.force_authenticate(self.student)

        self.inbox.show_assignee_to_guest = False
        self.inbox.save()

        self.ticket.assignee = self.assistant
        self.ticket.save()

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                   {"ticket": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "username: " + self.ticket.assignee.username)

        self.inbox.show_assignee_to_guest = True
        self.inbox.save()

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                   {"ticket": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ticket.assignee.username)

    def test_inbox_show_assignee_to_guest_as_staff(self):
        """
        Test to verify that the assignee is always visible to a staff member.
        """
        for user in [self.assistant3, self.manager]:
            self.client.force_authenticate(user)

            self.inbox.show_assignee_to_guest = False
            self.inbox.save()

            self.ticket.assignee = self.assistant
            self.ticket.save()

            response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                       {"ticket": "true"})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.ticket.assignee.username)

            self.inbox.show_assignee_to_guest = True
            self.inbox.save()

            response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                       {"ticket": "true"})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.ticket.assignee.username)

    def test_ticket_inbox_id_unique_removal_bug(self):
        """Tests for issue #157."""
        Ticket.objects.create(author=self.student, assignee=self.assistant, title="TestTicket",
                              content="TestContent", inbox=self.inbox)
        ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title="TestTicket",
                                       content="TestContent", inbox=self.inbox)
        Ticket.objects.create(author=self.student, assignee=self.assistant, title="TestTicket",
                              content="TestContent", inbox=self.inbox)
        ticket.delete()
        Ticket.objects.create(author=self.student, assignee=self.assistant, title="TestTicket",
                              content="TestContent", inbox=self.inbox)

    def test_get_tickets_id_contains_id(self):
        """
        Test for issue #315.
        """
        test_student = User()
        test_student.id = 91
        test_student.username = "student91"
        test_student.password = "test12345"
        test_student.email = "student91@ticketvise.com"
        test_student.save()
        test_student.add_inbox(self.inbox)
        test_student.set_role_for_inbox(self.inbox, Role.GUEST)
        test_ticket = Ticket.objects.create(author=self.student2, assignee=self.assistant, title="TestTicket315",
                                            content="TestTicket315", inbox=self.inbox)
        test_ticket.shared_with.set([test_student])
        test_ticket.shared_with.set([self.student3])
        test_ticket.save()

        self.client.force_authenticate(self.student)

        data = {
            "columns": False
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "TestTicket315")

    def test_get_tickets_guest(self):
        """
        Test InboxTicketsApiView for guest
        """
        self.client.force_authenticate(self.student)

        data = {
            "columns": False
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.content)[0], dict)
        self.assertContains(response, "Ticket1")
        self.assertNotContains(response, "Ticket3")

    def test_get_tickets_agent(self):
        """
        Test InboxTicketsApiView for agent
        """
        self.client.force_authenticate(self.assistant)

        data = {
            "columns": False
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.content)[0], dict)
        self.assertContains(response, "Ticket1")
        self.assertContains(response, "Ticket3")

    def test_get_tickets_manager(self):
        """
        Test InboxTicketsApiView for manager
        """
        self.client.force_authenticate(self.assistant)

        data = {
            "columns": False
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.content)[0], dict)
        self.assertContains(response, "Ticket1")
        self.assertContains(response, "Ticket3")

    def test_get_personal_tickets_agent(self):
        """
        Test InboxTicketsApiView for agent
        """
        self.client.force_authenticate(self.assistant)

        data = {
            "show_personal": "true"
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ticket1")
        self.assertNotContains(response, "Ticket3")

    def test_get_non_personal_tickets_agent(self):
        """
        Test InboxTicketsApiView for agent
        """
        self.client.force_authenticate(self.assistant)

        data = {
            "show_personal": "false"
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ticket1")
        self.assertContains(response, "Ticket3")

    def test_get_column_four_tickets_guest(self):
        """
        Test InboxTicketsApiView for guest
        """
        self.client.force_authenticate(self.student)
        self.inbox.show_assignee_to_guest = True
        self.inbox.save()
        Ticket.objects.create(inbox=self.inbox, status=Status.CLOSED, content="CLOSED", title="CLOSED",
                              author=self.student)
        Ticket.objects.create(inbox=self.inbox, status=Status.ASSIGNED, content="ASSIGNED", title="ASSIGNED",
                              author=self.student)

        data = {
            "columns": "true"
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 4)
        self.assertContains(response, "label")
        self.assertContains(response, "Ticket1")
        self.assertNotContains(response, "Ticket3")

    def test_get_column_tickets_agent(self):
        """
        Test InboxTicketsApiView for agent
        """
        self.client.force_authenticate(self.assistant)
        Ticket.objects.create(inbox=self.inbox, status=Status.CLOSED, content="CLOSED", title="CLOSED",
                              author=self.student)

        data = {
            "columns": "true"
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 4)
        self.assertContains(response, "label")
        self.assertContains(response, "Ticket1")
        self.assertContains(response, "Ticket3")

    def test_get_column_tickets_manager(self):
        """
        Test InboxTicketsApiView for manager
        """
        self.client.force_authenticate(self.assistant)
        Ticket.objects.create(inbox=self.inbox, status=Status.CLOSED, content="CLOSED", title="CLOSED",
                              author=self.student)

        data = {
            "columns": "true"
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 4)
        self.assertContains(response, "label")
        self.assertContains(response, "Ticket1")
        self.assertContains(response, "Ticket3")

    def test_filter_labels(self):
        """
        Test InboxTicketsApiView for manager
        """
        self.client.force_authenticate(self.assistant)
        Ticket.objects.create(inbox=self.inbox, status=Status.CLOSED, content="CLOSED", title="CLOSED",
                              author=self.student)

        data = {
            "labels[]": self.label.id
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Ticket1")
        self.assertContains(response, "Ticket3")

    def test_filter_unlabelled_labels(self):
        """
        Test InboxTicketsApiView for manager
        """
        self.client.force_authenticate(self.assistant)
        Ticket.objects.create(inbox=self.inbox, status=Status.CLOSED, content="CLOSED", title="CLOSED",
                              author=self.student)

        data = {
            "labels[]": [0, self.label2.id]
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ticket1")
        self.assertContains(response, "Ticket2")
        self.assertNotContains(response, "Ticket3")

    def test_hide_pending(self):
        """
        Test InboxTicketsApiView for manager
        """
        self.client.force_authenticate(self.assistant)

        data = {"columns": "true"}
        self.inbox.tickets.all().delete()

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        # Scheduling algorithm does not support pending status, so should be hidden.
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, Status.PENDING.label)

        self.inbox.scheduling_algorithm = SchedulingAlgorithm.FIXED
        self.inbox.fixed_scheduling_assignee = None
        self.inbox.save()

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        # Scheduling algorithm does support pending status, so should be visible.
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, Status.PENDING.label)

        self.inbox.scheduling_algorithm = SchedulingAlgorithm.FIXED
        self.inbox.fixed_scheduling_assignee = None
        self.inbox.save()

        # Scheduling algorithm does not support pending status, but contains a ticket with the status, so the column
        # should be visible.
        Ticket.objects.create(inbox=self.inbox, content="content", title="test", author=self.student)
        self.inbox.scheduling_algorithm = SchedulingAlgorithm.ROUND_ROBIN
        self.inbox.save()

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, Status.PENDING.label)

    def test_close_ticket_api(self):
        self.client.force_authenticate(self.assistant)

        self.assertNotEqual(self.ticket.status, Status.CLOSED)

        response = self.client.patch(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/status/close")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ticket.objects.get(pk=self.ticket.id).status, Status.CLOSED)

    def test_open_ticket_api(self):
        self.client.force_authenticate(self.assistant)

        # Testing reopen Closed to Assigned
        self.ticket.status = Status.CLOSED
        self.ticket.save()

        response = self.client.patch(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/status/open")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ticket.objects.get(pk=self.ticket.id).status, Status.ASSIGNED)

        # Testing reopen Closed to Pending
        self.ticket.status = Status.CLOSED
        self.ticket.assignee = None
        self.ticket.save()

        response = self.client.patch(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/status/open")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ticket.objects.get(pk=self.ticket.id).status, Status.PENDING)

        # Testing reopen Closed to Answered
        self.ticket.status = Status.CLOSED
        self.ticket.save()

        Comment.objects.create(ticket=self.ticket, author=self.assistant, content="test", is_reply=True)

        response = self.client.patch(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/status/open")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ticket.objects.get(pk=self.ticket.id).status, Status.ANSWERED)

    def test_get_ticket_search(self):
        self.client.force_authenticate(self.student)
        self.ticket.shared_with.set([self.student])
        self.ticket2.shared_with.set([self.student])
        self.ticket3.shared_with.set([self.student])

        data = {
            "q": "",
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        response_data = json.loads(response.content)

        self.assertEqual(len(response_data[0]["tickets"]), 3)

        data = {
            "q": "student2",
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data)
        response_data = json.loads(response.content)

        self.assertEqual(len(response_data[0]["tickets"]), 1)
        self.assertContains(response, "Ticket3")
        self.assertNotContains(response, "Ticket2")

        data = {
            "q": "Ticket3",
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data)
        response_data = json.loads(response.content)

        self.assertEqual(len(response_data[0]["tickets"]), 1)
        self.assertContains(response, "Ticket3")
        self.assertNotContains(response, "Ticket2")

    def test_get_ticket_search_reply(self):
        self.client.force_authenticate(self.student)
        Comment.objects.create(ticket=self.ticket, author=self.assistant, content="Elephant", is_reply=True)

        data = {
            "q": "elephant",
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data)
        response_data = json.loads(response.content)

        self.assertEqual(len(response_data[1]["tickets"]), 1)
        self.assertContains(response, "Ticket1")

    def test_get_ticket_search_comment_student(self):
        self.client.force_authenticate(self.student)
        Comment.objects.create(ticket=self.ticket, author=self.assistant, content="Fairy tale", is_reply=False)

        data = {
            "q": "fairy tale",
        }

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets", data=data)
        json_data = JsonResponse(TicketSerializer(self.ticket, fields=(
            "id", "title", "name", "assignee", "ticket_inbox_id", "date_created", "labels")).data, safe=False)
        self.assertNotEqual(response.content, b"[" + json_data.content + b"]")
