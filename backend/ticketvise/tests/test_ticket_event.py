from django.test import TestCase

from ticketvise.models.ticket import TicketLabelEvent, TicketAssigneeEvent, Status, TicketStatusEvent
from ticketvise.tests.test_ticket import TicketTestCase


class TestTicketEvent(TicketTestCase):

    def test_create_label_ticket_event(self):
        self.client.force_login(self.student)
        TicketLabelEvent.objects.all().delete()
        self.ticket.add_label(self.label)

        self.assertEqual(TicketLabelEvent.objects.filter(label=self.label, is_added=True).count(), 1)

    def test_delete_label_ticket_event(self):
        self.client.force_login(self.student)
        self.ticket.add_label(self.label)

        TicketLabelEvent.objects.all().delete()
        self.ticket.delete_label(self.label)

        self.assertEqual(TicketLabelEvent.objects.filter(ticket=self.ticket, label=self.label,
                                                         is_added=False).count(), 1)

    def test_assignee_ticket_event(self):
        self.client.force_login(self.student)

        TicketAssigneeEvent.objects.all().delete()
        self.ticket.assignee = self.manager
        self.ticket.save()

        self.assertEqual(TicketAssigneeEvent.objects.filter(ticket=self.ticket, assignee=self.manager).count(), 1)

    def test_status_ticket_event(self):
        self.client.force_login(self.student)

        old_status = self.ticket.status

        TicketStatusEvent.objects.all().delete()
        self.ticket.status = Status.CLOSED
        self.ticket.save()

        self.assertEqual(TicketStatusEvent.objects.filter(ticket=self.ticket, old_status=old_status,
                                                          new_status=Status.CLOSED).count(), 1)

    def test_events_api(self):
        self.client.force_login(self.student)
        self.ticket.add_label(self.label)
        self.ticket.delete_label(self.label)
        self.ticket.assignee = self.manager
        self.ticket.status = Status.CLOSED
        self.ticket.save()

        url = "/api/inboxes/{}/tickets/{}/events".format(self.ticket.inbox.id, self.ticket.ticket_inbox_id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "\"new_status\":\"CLSD\"")
        self.assertContains(response, "\"id\":" + str(self.manager.id))
        self.assertContains(response, "\"is_added\":true")
        self.assertContains(response, "\"is_added\":false")
