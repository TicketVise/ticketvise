"""
Test Ticket Form
-------------------------------
This file tests the ticket form page which creates a ticket.
"""
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from ticketvise.tests.test_ticket import TicketTestCase


class TicketFormTestAPI(APITestCase, TicketTestCase):
    def test_create_ticket(self):
        self.client.force_authenticate(self.student)

        url = f"/api/inboxes/{self.inbox.id}/tickets/new"
        data = {
            "title": "TestTicket",
            "content": "TestTicket",
            "labels": [self.label.id],
            "shared_with": []
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        data["ticket_inbox_id"] = response.data["ticket_inbox_id"]
        self.assertDictEqual(response.data, data)

    def test_create_ticket_attachment(self):
        self.client.force_authenticate(self.student)

        url = f"/api/inboxes/{self.inbox.id}/tickets/new"

        file = SimpleUploadedFile('test.txt', b'Testing some text inside of a file')
        data = {
            "title": "TestTicket",
            "content": "TestTicket",
            "inbox": self.inbox.id,
            "attachments": file
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_create_ticket_shared(self):
        self.client.force_authenticate(self.student)

        url = f"/api/inboxes/{self.inbox.id}/tickets/new"
        data = {
            "title": "TestTicket",
            "content": "TestTicket",
            "labels": [self.label.id],
            "shared_with": [self.student2.id]
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        data["ticket_inbox_id"] = response.data["ticket_inbox_id"]
        self.assertDictEqual(response.data, data)

    def test_create_ticket_shared_assistant(self):
        self.client.force_authenticate(self.student)

        url = f"/api/inboxes/{self.inbox.id}/tickets/new"
        data = {
            "title": "TestTicket",
            "content": "TestTicket",
            "inbox": self.inbox.id,
            "labels": [self.label.id],
            "shared_with": [self.assistant.id]
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"shared_with": ["This ticket cannot be shared with one of these users"]})
