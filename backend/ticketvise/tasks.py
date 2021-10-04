"""
Tasks
-------------------------------
Periodic tsks for changing ticket statuses and sending emails.
"""
from ticketvise.mail.retrieve import retrieve_emails, submit_email_ticket
import datetime
import logging
import sched
from django.db.models import Q
from django.utils import timezone

from .models.inbox import Inbox, MailSecurity
from .models.notification.reminder import TicketReminderNotification
from .models.ticket import Ticket, Status
from .models.user import Role


def start_schedule():
    tasks = [(sync_mail, 60)]
    s = sched.scheduler()

    # setting up repeating tasks
    for task, seconds in tasks:
        def run():
            try:
                task()
                print(f"Task '{task.__name__}' successfully finished!")
            except Exception as e:
                print(f"Task '{task.__name__}' failed with exception: {e}")
            
            # rescheduling task
            s.enter(seconds, 1, run)
            print(f"Task '{task.__name__}' scheduled to repeat in {seconds} seconds.")
        
        # initial task schedule
        s.enter(seconds, 1, run)
    
    s.run()

def sync_mail():
    start_time = datetime.now()
    logging.info(f"Started retrieving email at {start_time}")
    for inbox in Inbox.objects.filter(email_enabled=True):
        logging.info(f"Retrieving email for inbox: {inbox.name} ({inbox.id})")
        for message in retrieve_emails(inbox.inbound_email_protocol,
                                       inbox.inbound_email_server,
                                       inbox.inbound_email_port,
                                       inbox.inbound_email_username,
                                       inbox.inbound_email_password,
                                       inbox.inbound_email_security == MailSecurity.TLS,
                                       inbox.inbound_email_use_oauth2):
            submit_email_ticket(message)
    end_time = datetime.now()
    logging.info(f"Finished retrieving email at {end_time}, took: {end_time - start_time}")


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
