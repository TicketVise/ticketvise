from django.core.management.base import BaseCommand

from ticketvise import settings
from ticketvise.mail import submit_email_ticket
from ticketvise.mail import retrieve_emails


class Command(BaseCommand):
    """Django command that retrieves all emails and submits them as tickets or comments."""

    def handle(self, *args, **options):
        protocol = settings.INBOUND_EMAIL_PROTOCOL
        host = settings.INBOUND_EMAIL_SERVER
        port = settings.INBOUND_EMAIL_PORT
        username = settings.INBOUND_EMAIL_USERNAME
        password = settings.INBOUND_EMAIL_PASSWORD
        require_tls = settings.INBOUND_EMAIL_REQUIRE_TLS

        for message in retrieve_emails(protocol, host, port, username, password, require_tls):
            submit_email_ticket(message)
