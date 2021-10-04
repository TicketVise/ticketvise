from django.apps import AppConfig


class TicketViseConfig(AppConfig):
    name = "ticketvise"

    def ready(self):
        from ticketvise.tasks import start_schedule
        pass
        # start_schedule()
