"""
Test Comment
-------------------------------
This file tests the comments functionality.
"""

from ticketvise.models.comment import Comment, MAX_COMMENT_CHAR_LENGTH
from ticketvise.models.ticket import Ticket, Status
from ticketvise.tests.test_ticket import TicketTestCase


class CommentTestCase(TicketTestCase):

    def test_get_comment_as_student(self):
        """
        Test to verify a student cannot get comments
        """
        self.client.force_authenticate(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                   {"comments": "true"}, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_get_comment_as_shared_with(self):
        """
        Test to verify a student cannot get comments
        """
        self.client.force_authenticate(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}",
                                   {"comments": "true"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"{}")

    def test_get_comment_as_author(self):
        """
        Test to verify an author cannot get comments
        """
        self.client.force_authenticate(self.student)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                   {"comments": "true"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"{}")

    def test_get_comment_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get comments
        """
        self.client.force_authenticate(self.assistant)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                   {"comments": "true"}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_get_comment_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get comments
        """
        self.client.force_authenticate(self.assistant2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                   {"comments": "true"}, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_post_comment_as_student(self):
        """
        Test to verify a student cannot get comments
        """
        self.client.force_authenticate(self.student2)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments/post", )
        self.assertEqual(response.status_code, 403)

    def test_post_comment_as_shared_with(self):
        """
        Test to verify a student cannot get comments
        """
        self.client.force_authenticate(self.student2)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}/comments/post", )
        self.assertEqual(response.status_code, 403)

    def test_post_comment_as_author(self):
        """
        Test to verify an author cannot get comments
        """
        self.client.force_authenticate(self.student)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments/post", data)
        self.assertEqual(response.status_code, 403)

    def test_post_comment_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get comments
        """
        self.client.force_authenticate(self.assistant)
        count = Comment.objects.count()

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments/post", data)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(Comment.objects.count(), count)

    def test_post_comment_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get comments
        """
        self.client.force_authenticate(self.assistant2)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/comments/post", data)
        self.assertEqual(response.status_code, 403)

    def test_get_replies_as_student(self):
        """
        Test to verify a student cannot get replies
        """
        self.client.force_authenticate(self.student3)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                   {"replies": "true"})
        self.assertEqual(response.status_code, 403)

    def test_get_replies_as_shared_with(self):
        """
        Test to verify a shared_with cannot get replies
        """
        self.client.force_authenticate(self.student2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}",
                                   {"replies": "true"})
        self.assertEqual(response.status_code, 200)

    def test_get_replies_as_author(self):
        """
        Test to verify an author cannot get replies
        """
        self.client.force_authenticate(self.student)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                   {"replies": "true"})
        self.assertEqual(response.status_code, 200)

    def test_get_replies_as_ta_in_inbox(self):
        """
        Test to verify an assistant of the inbox can get replies
        """
        self.client.force_authenticate(self.assistant)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                   {"replies": "true"})
        self.assertEqual(response.status_code, 200)

    def test_get_replies_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get replies
        """
        self.client.force_authenticate(self.assistant2)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}",
                                   {"replies": "true"})
        self.assertEqual(response.status_code, 403)

    def test_post_replies_as_student(self):
        """
        Test to verify a student without permissions cannot post replies
        """
        self.client.force_authenticate(self.student2)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies/post", data)
        self.assertEqual(response.status_code, 403)

    def test_post_replies_as_shared_with(self):
        """
        Test to verify a shared_with can get replies
        """
        self.client.force_authenticate(self.student2)
        self.ticket2.status = Status.ANSWERED
        self.ticket2.save()
        count = Comment.objects.count()

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket2.ticket_inbox_id}/replies/post", data)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(Comment.objects.count(), count)

        comment = Comment.objects.get(id=response.data["id"])
        self.assertFalse(comment.is_approved)

        self.assertEqual(Ticket.objects.get(pk=self.ticket2.id).status, Status.ASSIGNED)

    def test_post_replies_as_author(self):
        """
        Test to verify an author can post replies
        """
        self.client.force_authenticate(self.student)
        self.ticket.status = Status.ANSWERED
        self.ticket.save()
        count = Comment.objects.count()

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies/post", data)
        self.assertEqual(response.status_code, 201)

        comment = Comment.objects.get(id=response.data["id"])
        self.assertFalse(comment.is_approved)

        self.assertNotEqual(Comment.objects.count(), count)
        self.assertEqual(Ticket.objects.get(pk=self.ticket.id).status, Status.ASSIGNED)

    def test_post_replies_as_ta_in_inbox_assigned(self):
        """
        Test to verify an assistant of the inbox can get replies
        """
        self.client.force_authenticate(self.assistant)
        self.ticket.status = Status.ASSIGNED
        self.ticket.assignee = self.assistant3
        self.ticket.save()
        count = Comment.objects.count()

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies/post", data)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(Comment.objects.count(), count)

        comment = Comment.objects.get(id=response.data["id"])
        self.assertTrue(comment.is_approved)

        self.assertEqual(Ticket.objects.get(pk=self.ticket.id).status, Status.ANSWERED)
        self.assertEqual(Ticket.objects.get(pk=self.ticket.id).assignee, self.assistant3)

    def test_post_replies_as_ta_in_inbox_unassigned(self):
        """
        Test to verify an assistant of the inbox can get replies
        """
        self.client.force_authenticate(self.assistant)
        self.ticket.status = Status.PENDING
        self.ticket.assignee = None
        self.ticket.save()
        count = Comment.objects.count()

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies/post", data)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(Comment.objects.count(), count)

        comment = Comment.objects.get(id=response.data["id"])
        self.assertTrue(comment.is_approved)

        self.assertTrue(Ticket.objects.get(pk=self.ticket.id).assignee, self.assistant)
        self.assertTrue(Ticket.objects.get(pk=self.ticket.id).status, Status.ANSWERED)

    def test_post_replies_as_ta_not_in_inbox(self):
        """
        Test to verify an assistant not in the inbox cannot get replies
        """
        self.client.force_authenticate(self.assistant2)

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies/post", data)
        self.assertEqual(response.status_code, 403)

    def test_reopen_ticket_pending_student(self):
        """
        Test to verify an closed ticket will be reopened with status pending if no assignee.
        """
        self.client.force_authenticate(self.student)
        self.ticket.status = self.ticket.status.CLOSED
        self.ticket.assignee = None
        self.ticket.save()

        count = Comment.objects.count()

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies/post", data)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(Comment.objects.count(), count)

        ticket = Ticket.objects.get(pk=self.ticket.pk)
        self.assertTrue(ticket.status == self.ticket.status.PENDING)

    def test_reopen_ticket_assigned_student(self):
        """
        Test to verify an closed ticket will be reopened with status assigned if assigned.
        """
        self.client.force_authenticate(self.student)
        self.ticket.status = self.ticket.status.CLOSED
        self.ticket.assignee = self.assistant
        self.ticket.save()

        count = Comment.objects.count()

        data = {
            "content": "Testcontent"
        }

        response = self.client.post(
            f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/replies/post", data)
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(Comment.objects.count(), count)

        ticket = Ticket.objects.get(pk=self.ticket.pk)
        self.assertTrue(ticket.status == self.ticket.status.ASSIGNED)

    def test_replies_content_str(self):
        """
        Test to verify comment.str is formatted correctly.
        """

        comment = Comment.objects.create(content="Testcontent", author=self.student, ticket=self.ticket)
        self.assertEqual("Testcontent", str(comment))

    def test_replies_content_str_trim(self):
        """
        Test to verify comment.str is formatted correctly.
        """
        content = "This test content contains too many characters so it will be cut and the end will be replaced with three dots."

        comment = Comment.objects.create(content=content, author=self.student, ticket=self.ticket)
        self.assertEqual(content[:MAX_COMMENT_CHAR_LENGTH] + "...", str(comment))
