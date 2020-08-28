from datetime import datetime

from django.core.management.base import BaseCommand

from ticketvise.models.notification.assigned import TicketAssignedNotification
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User
from ticketvise.tasks import update_tickets, alert_unanswered_tickets

class Command(BaseCommand):
    """Django command that sends a email to info@ticketvise.com"""
    tasks = [update_tickets, alert_unanswered_tickets]

    def handle(self, *args, **options):
        ticket = Ticket.objects.all().first()

        user = User.objects.get(email="info@ticketvise.com")
        TicketAssignedNotification(ticket=ticket, receiver=user).send_mail()