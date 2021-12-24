import time
from ticketvise.tasks import sync_mail
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command that retrieves all emails and submits them as tickets or comments."""

    def handle(self, *args, **options):
        while True:
            sync_mail()
            time.sleep(60)
