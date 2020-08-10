from django.apps import AppConfig

from ticketvise.email import SmtpServer


class TicketViseConfig(AppConfig):
    name = "ticketvise"

    def ready(self):
        SmtpServer().start()
