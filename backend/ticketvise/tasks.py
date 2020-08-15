"""
Tasks
-------------------------------
Periodic tsks for changing ticket statuses and sending emails.
"""
from django.db.models import Q
from django.utils import timezone

from .email import send_email
from .models.inbox import Inbox
from .models.ticket import Ticket
from .models.user import Role


def update_tickets():
    """
    Update the status of all answered tickets older than the amount of days
    specified in inbox.close_answered_weeks to closed.

    :return: None.
    """
    for inbox in Inbox.objects.all():
        if inbox.close_answered_weeks > 0:
            min_age = timezone.now() - timezone.timedelta(weeks=inbox.close_answered_weeks)

            tickets = Ticket.objects.filter(inbox=inbox, status=Ticket.Status.ANSWERED, date_edited__lt=min_age)
            tickets.update(status=Ticket.Status.CLOSED)


def alert_unanswered_tickets():
    """
    Send an email for tickets that have not been answered for a set amount of
    time. This time is specified in inbox.alert_coordinator_unanswered_days.

    :return: None.
    """
    for inbox in Inbox.objects.all():
        if inbox.close_answered_weeks > 0:
            min_age = timezone.now() - timezone.timedelta(days=inbox.alert_coordinator_unanswered_days)

            tickets = Ticket.objects.filter(
                Q(status=Ticket.Status.PENDING) | Q(status=Ticket.Status.ASSIGNED), date_edited__lt=min_age
            )

            for ticket in tickets:
                for coordinator in ticket.inbox.get_users_by_role(Role.MANAGER):
                    mail_vars = {"ticket": ticket}

                    send_email(
                        "Unanswered ticket: #%s" % ticket.ticket_inbox_id,
                        coordinator.email,
                        "ticket_unanswered_alert",
                        mail_vars,
                    )
