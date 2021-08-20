from django.utils import timezone

from ticketvise.models.ticket import Ticket
from ticketvise.tests.test_ticket import TicketTestCase


class PublicTicketTestBackendCase(TicketTestCase):
    def test_get_public_tickets_as_student(self):
        self.client.force_authenticate(self.student)

        response = self.client.get(f"/api/inboxes/{self.ticket.inbox.id}/tickets?public=true")
        self.assertEqual(response.status_code, 200)

    # def test_get_non_public_ticket_as_author(self):
    #     self.client.force_authenticate(self.student)

    #     response = self.client.get(f"/api/inboxes/{self.ticket.inbox.id}/public/{self.ticket.ticket_inbox_id}")

    #     self.assertEqual(response.status_code, 404)

    # def test_get_non_public_ticket_as_student(self):
    #     self.client.force_authenticate(self.student2)

    #     response = self.client.get(f"/api/inboxes/{self.ticket.inbox.id}/public/{self.ticket.ticket_inbox_id}")

    #     self.assertEqual(response.status_code, 404)

    # def test_get_non_public_ticket_as_staff(self):
    #     self.client.force_authenticate(self.assistant)

    #     response = self.client.get(f"/api/inboxes/{self.ticket.inbox.id}/public/{self.ticket.ticket_inbox_id}")

    #     self.assertEqual(response.status_code, 404)

    # def test_get_public_ticket_as_author(self):
    #     self.client.force_authenticate(self.student)

    #     response = self.client.get(f"/api/inboxes/{self.ticket.inbox.id}/public/{self.ticket3.ticket_inbox_id}")

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "author")

    # def test_get_public_ticket_as_staff(self):
    #     self.client.force_authenticate(self.assistant)

    #     response = self.client.get(f"/api/inboxes/{self.ticket.inbox.id}/public/{self.ticket3.ticket_inbox_id}")

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "author")

    # def test_get_public_ticket_as_student(self):
    #     self.client.force_authenticate(self.student2)

    #     response = self.client.get(f"/api/inboxes/{self.ticket.inbox.id}/public/{self.ticket3.ticket_inbox_id}")

    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "author")

    # def test_get_public_anonymous_ticket_as_author(self):
    #     self.client.force_authenticate(self.student)

    #     response = self.client.get(f"/api/inboxes/{self.ticket.inbox.id}/public/{self.ticket4.ticket_inbox_id}")

    #     self.assertEqual(response.status_code, 200)
    #     self.assertNotContains(response, "author")

    # def test_get_public_anonymous_ticket_as_staff(self):
    #     self.client.force_authenticate(self.assistant)

    #     response = self.client.get(f"/api/inboxes/{self.ticket.inbox.id}/public/{self.ticket4.ticket_inbox_id}")

    #     self.assertEqual(response.status_code, 200)
    #     self.assertNotContains(response, "author")

    # def test_get_public_anonymous_ticket_as_student(self):
    #     self.client.force_authenticate(self.student2)

    #     response = self.client.get(f"/api/inboxes/{self.ticket.inbox.id}/public/{self.ticket4.ticket_inbox_id}")

    #     self.assertEqual(response.status_code, 200)
    #     self.assertNotContains(response, "author")

    def test_request_publish_ticket(self):
        self.client.force_authenticate(self.assistant)

        ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title="temp ticket",
                                       content="TestContent", inbox=self.inbox)

        response = self.client.get(f"/api/inboxes/{ticket.inbox.id}/public/{ticket.ticket_inbox_id}")
        self.assertEqual(response.status_code, 404)
        self.assertFalse(ticket.publish_request_created)

        response = self.client.put(f"/api/inboxes/{ticket.inbox.id}/tickets/{ticket.ticket_inbox_id}/request-publish")
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(id=ticket.id)
        self.assertTrue(ticket.publish_request_created)
        self.assertEqual(ticket.publish_request_initiator.id, self.assistant.id)

    def test_accept_request_publish_ticket(self):
        self.client.force_authenticate(self.student)

        ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title="temp ticket",
                                       content="TestContent", inbox=self.inbox, publish_request_created=timezone.now(),
                                       publish_request_initiator=self.assistant)

        response = self.client.put(f"/api/inboxes/{ticket.inbox.id}/tickets/{ticket.ticket_inbox_id}/publish")
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(id=ticket.id)
        self.assertTrue(ticket.is_public)

    def test_publish_ticket_not_requested_ticket(self):
        self.client.force_authenticate(self.student)

        ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title="temp ticket",
                                       content="TestContent", inbox=self.inbox)

        response = self.client.put(f"/api/inboxes/{ticket.inbox.id}/tickets/{ticket.ticket_inbox_id}/publish")
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(id=ticket.id)
        self.assertTrue(ticket.is_public)

    def test_pin_ticket_as_staff(self):
        self.client.force_authenticate(self.assistant)

        ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title="temp ticket",
                                       content="TestContent", inbox=self.inbox)

        self.assertFalse(ticket.is_pinned)
        self.assertFalse(ticket.pin_initiator)

        response = self.client.put(f"/api/inboxes/{ticket.inbox.id}/tickets/{ticket.ticket_inbox_id}/pin")
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(id=ticket.id)

        self.assertTrue(ticket.is_pinned)
        self.assertEqual(ticket.pin_initiator.id, self.assistant.id)

    def test_pin_ticket_as_author(self):
        self.client.force_authenticate(self.student)

        ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title="temp ticket",
                                       content="TestContent", inbox=self.inbox)

        self.assertFalse(ticket.is_pinned)
        self.assertFalse(ticket.pin_initiator)

        response = self.client.put(f"/api/inboxes/{ticket.inbox.id}/tickets/{ticket.ticket_inbox_id}/pin")
        self.assertEqual(response.status_code, 403)

        ticket = Ticket.objects.get(id=ticket.id)

        self.assertFalse(ticket.is_pinned)
        self.assertFalse(ticket.pin_initiator)

    def test_unpin_ticket_as_staff(self):
        self.client.force_authenticate(self.assistant)

        ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title="temp ticket",
                                       content="TestContent", inbox=self.inbox, is_pinned=timezone.now(),
                                       pin_initiator=self.assistant)

        self.assertTrue(ticket.is_pinned)
        self.assertEqual(ticket.pin_initiator.id, self.assistant.id)

        response = self.client.put(f"/api/inboxes/{ticket.inbox.id}/tickets/{ticket.ticket_inbox_id}/pin")
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(id=ticket.id)

        self.assertFalse(ticket.is_pinned)
        self.assertFalse(ticket.pin_initiator)

    def test_unpin_ticket_as_author(self):
        self.client.force_authenticate(self.student)

        ticket = Ticket.objects.create(author=self.student, assignee=self.assistant, title="temp ticket",
                                       content="TestContent", inbox=self.inbox, is_pinned=timezone.now(),
                                       pin_initiator=self.assistant)

        self.assertTrue(ticket.is_pinned)
        self.assertEqual(ticket.pin_initiator.id, self.assistant.id)

        response = self.client.put(f"/api/inboxes/{ticket.inbox.id}/tickets/{ticket.ticket_inbox_id}/pin")
        self.assertEqual(response.status_code, 403)

        ticket = Ticket.objects.get(id=ticket.id)

        self.assertTrue(ticket.is_pinned)
        self.assertEqual(ticket.pin_initiator.id, self.assistant.id)
