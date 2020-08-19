from datetime import datetime

from django.core.management.base import BaseCommand

from ticketvise.email import send_ticket_shared_mail
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User
from ticketvise.tasks import update_tickets, alert_unanswered_tickets


class Command(BaseCommand):
    """Django command that runs timed tasks"""
    tasks = [update_tickets, alert_unanswered_tickets]

    def handle(self, *args, **options):
        ticket = Ticket.objects.all().first()

        user = User()
        user.email = "info@ticketvise.com"

        send_ticket_shared_mail(ticket, user)
