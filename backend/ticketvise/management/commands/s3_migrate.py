import datetime

from django.core.management import BaseCommand
from django.db import IntegrityError, transaction

from ticketvise.models.ticket import TicketAttachment


class Command(BaseCommand):
    """Django command that insert demo data into the database."""

    def handle(self, *args, **options):
        """Handle the command"""
        try:
            self.transfer_objects()
            print("Successfully tranfered s3 objects!")
        except IntegrityError as e:
            print("Database seems already populated with demo data, IntegrityError: ", e)

    @transaction.atomic
    def transfer_objects(self):
        attachments = TicketAttachment.objects.all()
        
        # for each attachment get the s3 from the old minio s3 bucket and save it to digitalocean spaces s3 bucket but leave the url the same
        for attachment in attachments:
            file = attachment.file
