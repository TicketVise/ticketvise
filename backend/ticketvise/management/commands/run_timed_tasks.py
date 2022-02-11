from datetime import datetime

from django.core.management.base import BaseCommand

from ticketvise.tasks import start_schedule


class Command(BaseCommand):
    """Django command that runs timed tasks"""

    def handle(self, *args, **options):
        print("Starting tasks at", datetime.now())
        start_schedule()
