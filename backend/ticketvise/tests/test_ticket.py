"""
Test Ticket
-------------------------------
This file tests the ticket page that show the information of a ticket.
"""
import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, Role


class TicketTestCase(TestCase):
    def setUp(self):
        """
        Set up the database for the tests.

        :return: None.
        """
        self.client = Client()
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
        self.label = Label.objects.create(name="TestLabel", inbox=self.inbox)

        self.ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title="TestTicket",
                                            content="TestContent", inbox=self.inbox)
        self.ticket2 = Ticket.objects.create(author=self.student, assignee=self.assistant, title="TestTicket",
                                             content="TestContent", inbox=self.inbox)
        self.ticket2.shared_with.set([self.student2])

    def test_ticket_page_200(self):
        """
        Authorized users should see their own ticket.

        :return: None.
        """
        self.client.force_login(self.student)
        response = self.client.get(reverse("ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]))
        self.assertEqual(response.status_code, 200)

    def test_ticket_page_401(self):
        """
        Unauthorized users should be redirected to the login page. When logged in
        it should redirect to the ticket.

        :return: None.
        """
        response = self.client.get(reverse("ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]))
        self.assertRedirects(response, '/login/?next=' + reverse("ticket", args=(
            self.ticket.inbox.id, self.ticket.ticket_inbox_id,)))

    def test_correct_template_used(self):
        """
        The ticket page should use the ticket.html template.

        :return: None.
        """
        self.client.force_login(self.student)
        response = self.client.get(reverse("ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]))
        self.assertTemplateUsed(response, 'ticket/ticket.html')

    def test_error_dispatch(self):
        """
        If the user is not the author of the ticket and the user is not
        a coordinator or a TA, it should give a 401 error.

        :return: None.
        """
        self.client.force_login(self.student2)
        response = self.client.get(reverse("ticket", args=[self.ticket.inbox.id, self.ticket.ticket_inbox_id]))
        self.assertEqual(response.status_code, 403)


class TicketTestApi(APITestCase, TicketTestCase):
    def test_get_ticket_as_unauthorized_student(self):
        """
        Test to verify a student cannot get the ticket
        """
        self.client.force_login(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}", follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_ticket_as_author(self):
        """
        Test to verify an author can get the ticket
        """
        self.client.force_login(self.student)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_ticket_as_shared_with(self):
        """
        Test to verify an author can get the ticket
        """
        self.client.force_login(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_ticket_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get the ticket
        """
        self.client.force_login(self.assistant)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}", follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_ticket_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get the ticket
        """
        self.client.force_login(self.assistant2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}", follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_comment_as_student(self):
        """
        Test to verify a student cannot get comments
        """
        self.client.force_login(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_comment_as_shared_with(self):
        """
        Test to verify a student cannot get comments
        """
        self.client.force_login(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}/comments",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_comment_as_author(self):
        """
        Test to verify an author cannot get comments
        """
        self.client.force_login(self.student)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_comment_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get comments
        """
        self.client.force_login(self.assistant)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments",
                                   follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_comment_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get comments
        """
        self.client.force_login(self.assistant2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_post_comment_as_student(self):
        """
        Test to verify a student cannot get comments
        """
        self.client.force_login(self.student2)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments/post", data,
            follow=True)
        self.assertEqual(response.status_code, 403)

    def test_post_comment_as_shared_with(self):
        """
        Test to verify a student cannot get comments
        """
        self.client.force_login(self.student2)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}/comments/post", data,
            follow=True)
        self.assertEqual(response.status_code, 403)

    def test_post_comment_as_author(self):
        """
        Test to verify an author cannot get comments
        """
        self.client.force_login(self.student)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments/post", data, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_post_comment_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get comments
        """
        self.client.force_login(self.assistant)
        count = Comment.objects.count()

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments/post", data, follow=True)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(Comment.objects.count(), count)

    def test_post_comment_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get comments
        """
        self.client.force_login(self.assistant2)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments/post", data, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_replies_as_student(self):
        """
        Test to verify a student cannot get replies
        """
        self.client.force_login(self.student3)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_replies_as_shared_with(self):
        """
        Test to verify a shared_with cannot get replies
        """
        self.client.force_login(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}/replies",
                                   follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_replies_as_author(self):
        """
        Test to verify an author cannot get replies
        """
        self.client.force_login(self.student)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies",
                                   follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_replies_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get replies
        """
        self.client.force_login(self.assistant)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies",
                                   follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_replies_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get replies
        """
        self.client.force_login(self.assistant2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_post_replies_as_student(self):
        """
        Test to verify a student cannot get replies
        """
        self.client.force_login(self.student2)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies/post", data,
            follow=True)
        self.assertEqual(response.status_code, 403)

    def test_post_replies_as_shared_with(self):
        """
        Test to verify a shared_with can get replies
        """
        self.client.force_login(self.student2)
        count = Comment.objects.count()

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}/replies/post", data,
            follow=True)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(Comment.objects.count(), count)

    def test_post_replies_as_author(self):
        """
        Test to verify an author cannot get replies
        """
        self.client.force_login(self.student)
        count = Comment.objects.count()

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies/post", data, follow=True)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(Comment.objects.count(), count)

    def test_post_replies_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get replies
        """
        self.client.force_login(self.assistant)
        count = Comment.objects.count()

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies/post", data, follow=True)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(Comment.objects.count(), count)

    def test_post_replies_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get replies
        """
        self.client.force_login(self.assistant2)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies/post", data, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_staff_as_student(self):
        """
        Test to verify a student cannot get staff
        """
        self.client.force_login(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/staff",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_staff_as_author(self):
        """
        Test to verify an author cannot get staff
        """
        self.client.force_login(self.student)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/staff",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_staff_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get staff
        """
        self.client.force_login(self.assistant)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/staff",
                                   follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_staff_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get staff
        """
        self.client.force_login(self.assistant2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/staff",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_labels_as_student(self):
        """
        Test to verify a student cannot get labels
        """
        self.client.force_login(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/labels",
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content),
                         [{"name": self.label.name, "color": self.label.color, "id": self.label.id}])

    def test_get_labels_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get labels
        """
        self.client.force_login(self.assistant)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/labels",
                                   follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(json.loads(response.content),
                         [{"name": self.label.name, "color": self.label.color, "id": self.label.id}])

    def test_get_labels_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get labels
        """
        self.client.force_login(self.assistant2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/labels",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_recent_as_student(self):
        """
        Test to verify a student cannot get recent tickets
        """
        self.client.force_login(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/users/{self.ticket.author.id}/tickets/recent",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_recent_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get recent tickets
        """
        self.client.force_login(self.assistant)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/users/{self.ticket.author.id}/tickets/recent",
                                   follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_recent_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get recent tickets
        """
        self.client.force_login(self.assistant2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/users/{self.ticket.author.id}/tickets/recent",
                                   follow=True)
        self.assertEqual(response.status_code, 403)

    def test_put_assignee_as_student(self):
        """
        Test to verify a student cannot change assignees
        """
        self.client.force_login(self.student2)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/assignee",
                                   data={"assignee": self.assistant.id}, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertNotEqual(ticket.assignee, self.assistant3)

    def test_put_assignee_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can change assignees
        """
        self.client.force_login(self.assistant)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/assignee",
                                   data={"assignee": self.assistant3.id}, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertEqual(ticket.assignee, self.assistant3)

    def test_put_assignee_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot change assignees
        """
        self.client.force_login(self.assistant2)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/assignee",
                                   data={"assignee": self.assistant.id}, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertNotEqual(ticket.assignee, self.assistant3)

    def test_put_shared_with_as_author(self):
        """
        Test to verify a author cannot change shared_with
        """
        self.client.force_login(self.student)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/shared",
                                   data={"shared_with": [self.student3.id]}, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertEqual(ticket.shared_with.all()[0], self.student3)

    def test_put_shared_with_as_shared_with(self):
        """
        Test to verify a shared_with cannot change shared_with
        """
        self.client.force_login(self.student2)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}/shared",
                                   data={"shared_with": [self.student3.id]}, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertFalse(ticket.shared_with.all())

    def test_put_shared_with_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can change shared_with
        """
        self.client.force_login(self.assistant)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/shared",
                                   data={"shared_with": [self.student3.id]}, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertEqual(ticket.shared_with.all()[0], self.student3)

    def test_put_shared_with_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot change shared_with
        """
        self.client.force_login(self.assistant2)

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/shared",
                                   data={"shared_with": [self.student3.id]}, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertFalse(ticket.shared_with.all())
