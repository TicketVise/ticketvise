"""
Test Ticket Form
-------------------------------
This file tests the ticket form page which creates a ticket.
"""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase

from ticketvise.tests.test_ticket import TicketTestCase


class TicketFormTestCase(TicketTestCase):
    def test_new_ticket_page_200(self):
        """
        Authorized users should see their own ticket.

        :return: None.
        """
        self.client.force_login(self.student)
        response = self.client.get(reverse("new_ticket", args=[self.inbox.id]))
        self.assertEqual(response.status_code, 200)

    def test_ticket_page_401(self):
        """
        Unauthorized users should be redirected to the login page. When logged in
        it should redirect to the ticket.

        :return: None.
        """
        response = self.client.get(reverse("new_ticket", args=[self.inbox.id]))
        self.assertRedirects(response, '/login/?next=' + reverse("new_ticket", args=[self.inbox.id]))

    def test_correct_template_used(self):
        """
        The ticket form page should use the ticket_form.html template.

        :return: None.
        """
        self.client.force_login(self.student)
        response = self.client.get(reverse("new_ticket", args=(self.inbox.id,)))
        self.assertTemplateUsed(response, "ticket_form.html")


class TicketFormTestAPI(APITestCase, TicketTestCase):
    def test_create_ticket(self):
        self.client.force_login(self.student)

        url = f"/api/inboxes/{self.inbox.id}/tickets/new"
        data = {
            "title": "TestTicket",
            "content": "TestTicket",
            "inbox": self.inbox.id,
            "labels": [self.label.id]
        }

        response = self.client.post(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, data)

    def test_create_ticket_attachment(self):
        self.client.force_login(self.student)

        url = f"/api/inboxes/{self.inbox.id}/tickets/new"

        file = SimpleUploadedFile('test.txt', b'Testing some text inside of a file')
        data = {
            "title": "TestTicket",
            "content": "TestTicket",
            "inbox": self.inbox.id,
            "attachments": file
        }

        response = self.client.post(url, data, format='json', follow=True)
        self.assertEqual(response.status_code, 201)
