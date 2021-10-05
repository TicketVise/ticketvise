import csv
import sys
import re

from django.core.management import BaseCommand
from django.db import IntegrityError, transaction
from django.utils import timezone

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, Status
from ticketvise.models.user import User, UserInbox, Role


class Command(BaseCommand):
    """Django command that insert demo data into the database."""

    def handle(self, *args, **options):
        """Handle the command"""
        try:
            self.import_csv_data()
            print("Successfully imported csv data!")
        except IntegrityError as e:
            print("Something went wrong importing data, IntegrityError: ", e)

    @transaction.atomic
    def import_csv_data(self):
        from langdetect import detect

        csv.field_size_limit(sys.maxsize)

        with open('tickets.backup') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(row)
                    line_count += 1
                    continue

            inbox_id = 1
            if row[9] == inbox_id:
