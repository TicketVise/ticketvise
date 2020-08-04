"""
Tasks
-------------------------------
Periodic tsks for changing ticket statuses and sending emails.
"""
from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import Q
from django.utils import timezone

from .email import send_email
from .models.inbox import Course
from .models.ticket import Ticket
from .models.user import User


@periodic_task(run_every=crontab(minute=0, hour=0))
def update_tickets():
    """
    Update the status of all answered tickets older than the amount of days
    specified in course.close_answered_weeks to closed.

    :return: None.
    """
    for course in Course.objects.all():
        if course.close_answered_weeks > 0:
            min_age = timezone.now() - timezone.timedelta(weeks=course.close_answered_weeks)

            tickets = Ticket.objects.filter(course=course, status=Ticket.Status.ANSWERED, date_edited__lt=min_age)
            tickets.update(status=Ticket.Status.CLOSED)


@periodic_task(run_every=crontab(minute=0, hour=0))
def alert_unanswered_tickets():
    """
    Send an email for tickets that have not been answered for a set amount of
    time. This time is specified in course.alert_coordinator_unanswered_days.

    :return: None.
    """
    for course in Course.objects.all():
        if course.close_answered_weeks > 0:
            min_age = timezone.now() - timezone.timedelta(days=course.alert_coordinator_unanswered_days)

            tickets = Ticket.objects.filter(
                Q(status=Ticket.Status.PENDING) | Q(status=Ticket.Status.ASSIGNED), date_edited__lt=min_age
            )

            for ticket in tickets:
                for coordinator in ticket.course.get_users_by_role(User.Roles.COORDINATOR):
                    mail_vars = {"ticket": ticket}

                    send_email(
                        "Unanswered ticket: #%s" % ticket.ticket_course_id,
                        coordinator.email,
                        "ticket_unanswered_alert",
                        mail_vars,
                    )
