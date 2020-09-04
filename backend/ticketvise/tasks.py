"""
Tasks
-------------------------------
Periodic tsks for changing ticket statuses and sending emails.
"""
from django.db.models import Q
from django.utils import timezone

from .models.inbox import Inbox
from .models.notification.reminder import TicketReminderNotification
from .models.ticket import Ticket, Status
from .models.user import Role


def close_expired_answered_tickets():
    """
    Update the status of all answered tickets older than the amount of days
    specified in inbox.close_answered_weeks to closed.

    :return: None.
    """
    for inbox in Inbox.objects.all():
        if inbox.close_answered_weeks > 0:
            min_age = timezone.now() - timezone.timedelta(weeks=inbox.close_answered_weeks)

            tickets = Ticket.objects.filter(inbox=inbox, status=Status.ANSWERED, date_created__lt=min_age)
            tickets.update(status=Status.CLOSED)


def alert_unanswered_tickets():
    """
    Send an email for tickets that have not been answered for a set amount of
    time. This time is specified in inbox.alert_coordinator_unanswered_days.

    :return: None.
    """
    for inbox in Inbox.objects.all():
        if inbox.alert_coordinator_unanswered_days > 0:
            min_age = timezone.now() - timezone.timedelta(days=inbox.alert_coordinator_unanswered_days)
            tickets = Ticket.objects.filter(Q(status=Status.PENDING) | Q(status=Status.ASSIGNED),
                                            inbox=inbox, date_created__lt=min_age)

            for ticket in tickets:
                if ticket.assignee:
                    TicketReminderNotification.objects.create(receiver=ticket.assignee, ticket=ticket)

                for coordinator in ticket.inbox.get_users_by_role(Role.MANAGER):
                    if coordinator is not ticket.assignee:
                        TicketReminderNotification.objects.create(receiver=coordinator, ticket=ticket)
