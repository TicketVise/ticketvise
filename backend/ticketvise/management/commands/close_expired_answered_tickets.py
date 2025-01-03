from django.core.management.base import BaseCommand
from django.utils import timezone

from ticketvise.models.ticket import Status, Ticket
from ticketvise.models.inbox import Inbox


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Update the status of all answered tickets older than the amount of days
        specified in inbox.close_answered_weeks to closed.

        :return: None.
        """
        for inbox in Inbox.objects.all():
            # print(inbox)
            if inbox.close_answered_weeks > 0:
                min_age = timezone.now() - timezone.timedelta(weeks=inbox.close_answered_weeks)

                tickets = Ticket.objects.filter(inbox=inbox, status=Status.ANSWERED, date_created__lt=min_age)
                num_tickets = tickets.count()
                tickets.update(status=Status.CLOSED)
                print(f"Closed {num_tickets} tickets in inbox {inbox.name}")
