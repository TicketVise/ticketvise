from datetime import timedelta, datetime

from django.test import TestCase

from ticketvise.models.inbox import Inbox
from ticketvise.models.notification.reminder import TicketReminderNotification
from ticketvise.models.ticket import Ticket, Status
from ticketvise.models.user import Role, User
from ticketvise.tasks import alert_unanswered_tickets, close_expired_answered_tickets


class TasksTestCase(TestCase):

    def test_close_expired_answered_tickets(self):
        inbox = Inbox.objects.create(code="ABC", name="how to code", close_answered_weeks=1)
        guest = User.objects.create_user(username="guest", email="guest@ticketvise.com")
        guest.add_inbox(inbox)

        ticket = Ticket.objects.create(author=guest, title="How to code?", inbox=inbox, content="pls help?")
        ticket.date_created = datetime.now() - timedelta(days=50)
        ticket.status = Status.ANSWERED
        ticket.save()

        close_expired_answered_tickets()

        updated_ticket = Ticket.objects.get(pk=ticket.id)
        self.assertEqual(updated_ticket.status, Status.CLOSED)

    def test_alert_unanswered_tickets(self):
        inbox = Inbox.objects.create(code="ABC", name="how to code", alert_coordinator_unanswered_days=1)
        guest = User.objects.create_user(username="guest", email="guest@ticketvise.com")
        guest.add_inbox(inbox)

        manager = User.objects.create_user(username="manager", email="manager@ticketvise.com")
        manager.add_inbox(inbox, Role.MANAGER)

        ticket = Ticket.objects.create(author=guest, title="How to code?", inbox=inbox, content="pls help?")
        ticket.date_created = datetime.now() - timedelta(days=2)
        ticket.save()

        alert_unanswered_tickets()

        self.assertTrue(TicketReminderNotification.objects.filter(ticket=ticket, receiver=manager).exists())
