from ticketvise.models.ticket import TicketLabelEvent, TicketAssigneeEvent, Status, TicketStatusEvent, TicketTitleEvent
from ticketvise.tests.test_ticket import TicketTestCase


class TestTicketEvent(TicketTestCase):

    def test_create_label_ticket_event(self):
        self.client.force_authenticate(self.student)
        TicketLabelEvent.objects.all().delete()
        self.ticket.add_label(self.label)

        self.assertEqual(TicketLabelEvent.objects.filter(label=self.label, is_added=True).count(), 1)

    def test_delete_label_ticket_event(self):
        self.client.force_authenticate(self.student)
        self.ticket.add_label(self.label)

        TicketLabelEvent.objects.all().delete()
        self.ticket.delete_label(self.label)

        self.assertEqual(TicketLabelEvent.objects.filter(ticket=self.ticket, label=self.label,
                                                         is_added=False).count(), 1)

    def test_assignee_ticket_event(self):
        self.client.force_authenticate(self.student)

        TicketAssigneeEvent.objects.all().delete()
        self.ticket.assignee = self.manager
        self.ticket.save()

        self.assertEqual(TicketAssigneeEvent.objects.filter(ticket=self.ticket, assignee=self.manager).count(), 1)

    def test_status_ticket_event(self):
        self.client.force_authenticate(self.student)

        old_status = self.ticket.status

        TicketStatusEvent.objects.all().delete()
        self.ticket.status = Status.CLOSED
        self.ticket.save()

        self.assertEqual(TicketStatusEvent.objects.filter(ticket=self.ticket, old_status=old_status,
                                                          new_status=Status.CLOSED).count(), 1)

    def test_title_ticket_event(self):
        self.client.force_authenticate(self.student)

        old_title = self.ticket.title

        TicketStatusEvent.objects.all().delete()
        self.ticket.title = "something else"
        self.ticket.save()

        self.assertEqual(TicketTitleEvent.objects.filter(ticket=self.ticket, old_title=old_title,
                                                         new_title=self.ticket.title).count(), 1)

    def test_events_api(self):
        self.client.force_authenticate(self.student)
        self.ticket.add_label(self.label)
        self.ticket.delete_label(self.label)
        self.ticket.assignee = self.manager
        self.ticket.status = Status.CLOSED
        self.ticket.title = "something different"
        self.ticket.save()

        params = {
            "events": "true"
        }

        url = "/api/inboxes/{}/tickets/{}".format(self.ticket.inbox.id, self.ticket.ticket_inbox_id)
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "\"new_status\":\"CLSD\"")
        self.assertContains(response, "\"id\":" + str(self.manager.id))
        self.assertContains(response, "\"is_added\":true")
        self.assertContains(response, "\"is_added\":false")
        self.assertContains(response, "\"new_title\":\"something different\"")

    def test_hide_certain_labels_for_student(self):
        self.client.force_authenticate(self.student)

        self.label.is_visible_to_guest = False
        self.label.save()

        self.ticket.add_label(self.label)
        self.ticket.add_label(self.label2)

        params = {
            "events": "true"
        }

        url = "/api/inboxes/{}/tickets/{}".format(self.ticket.inbox.id, self.ticket.ticket_inbox_id)
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.label.name)
        self.assertContains(response, self.label2.name)

    def test_hide_certain_labels_not_for_staff(self):
        self.client.force_authenticate(self.assistant)

        self.label.is_visible_to_guest = False
        self.label.save()

        self.ticket.add_label(self.label)
        self.ticket.add_label(self.label2)

        params = {
            "events": "true"
        }

        url = "/api/inboxes/{}/tickets/{}".format(self.ticket.inbox.id, self.ticket.ticket_inbox_id)
        response = self.client.get(url, params)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)
        self.assertContains(response, self.label2.name)
