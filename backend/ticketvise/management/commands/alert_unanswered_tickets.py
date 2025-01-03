from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q

from ticketvise.models.user import Role
from ticketvise.models.notification.reminder import TicketReminderNotification
from ticketvise.models.ticket import Status, Ticket
from ticketvise.models.inbox import Inbox


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Send an email for tickets that have not been answered for a set amount of
        time. This time is specified in inbox.alert_coordinator_unanswered_days.

        :return: None.
        """
        for inbox in Inbox.objects.all():
            if inbox.alert_coordinator_unanswered_days > 0:
                print(inbox)
                min_age = timezone.now() - timezone.timedelta(days=inbox.alert_coordinator_unanswered_days)
                tickets = Ticket.objects.filter(Q(status=Status.PENDING) | Q(status=Status.ASSIGNED),
                                                inbox=inbox, date_created__lt=min_age)
                # Get tickets that has no comments or the last comment is older than the min_age
                tickets_with_comments = tickets.filter((Q(status=Status.PENDING) | Q(status=Status.ASSIGNED)) & (Q(comments__isnull=True) | Q(comments__date_created__lt=min_age)), inbox=inbox)
                num_tickets = tickets.count()
                for ticket in tickets:
                    if ticket.assignee:
                        TicketReminderNotification.objects.create(receiver=ticket.assignee, ticket=ticket)
                    else:
                        for coordinator in ticket.inbox.get_users_by_role(Role.MANAGER):
                            TicketReminderNotification.objects.create(receiver=coordinator, ticket=ticket)

                print(tickets_with_comments)
                print(f"Send notifications about {num_tickets} unanswered tickets in inbox {inbox.name}")
