import datetime

from django.core.management import BaseCommand
from django.db import IntegrityError, transaction
from django.utils import timezone
from ticketvise.models.automation import Automation, AutomationCondition
from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, Status
from ticketvise.models.user import User, UserInbox, Role


class Command(BaseCommand):
    """Django command that removes demo data from the database."""

    def handle(self, *args, **options):
        """Handle the command"""
        try:
            self.remove_data()
            print("Successfully removed data from database!")
        except IntegrityError as e:
            print("Database seems already populated with demo data, IntegrityError: ", e)

    @transaction.atomic
    def remove_data(self):
        """Remove demo data from the database."""
        # Delete all data
        Automation.objects.all().delete()
        AutomationCondition.objects.all().delete()
        Comment.objects.all().delete()
        Inbox.objects.all().delete()
        Label.objects.all().delete()
        Ticket.objects.all().delete()
        UserInbox.objects.all().delete()
        User.objects.all().delete()
