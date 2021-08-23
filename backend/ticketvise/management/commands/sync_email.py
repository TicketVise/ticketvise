from ticketvise.mail.retrieve import retrieve_emails, submit_email_ticket
from ticketvise.models.inbox import Inbox, MailSecurity
from django.core.management.base import BaseCommand
import logging
from datetime import datetime

class Command(BaseCommand):
    """Django command that retrieves all emails and submits them as tickets or comments."""

    def handle(self, *args, **options):
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
