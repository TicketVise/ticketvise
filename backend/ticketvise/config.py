from backend.ticketvise.tasks import start_schedule
from django.apps import AppConfig


class TicketViseConfig(AppConfig):
    name = "ticketvise"

    def ready(self):
        start_schedule()
