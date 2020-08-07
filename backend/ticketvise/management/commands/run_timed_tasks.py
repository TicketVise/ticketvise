from django.core.management.base import BaseCommand

from ticketvise.tasks import update_tickets, alert_unanswered_tickets


class Command(BaseCommand):
    """Django command that runs timed tasks"""
    tasks = [update_tickets, alert_unanswered_tickets]

    def handle(self, *args, **options):
        for task in self.tasks:

            try:
                task()
                print("Task '{}' successfully finished!".format(task.__name__))
            except Exception as e:
                print("Task '{}' failed with exception: {}".format(task.__name__, e))
