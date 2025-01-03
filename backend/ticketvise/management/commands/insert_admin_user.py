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
            self.insert_admin_user()
            print("Successfully inserted admin user")
        except IntegrityError as e:
            print("Database seems already populated with demo data, IntegrityError: ", e)

    @transaction.atomic
    def insert_admin_user(self):
        admin_user = User.objects.create(
            username="admin",
            email="info@ticketvise.com",
            first_name="Admin",
            last_name="User",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        admin_user.set_password("admin")
        admin_user.save()
