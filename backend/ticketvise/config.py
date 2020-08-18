from django.apps import AppConfig

from ticketvise.email import SmtpServer


class TicketViseConfig(AppConfig):
    name = "ticketvise"
    smtp_server = SmtpServer()

    def ready(self):
        self.smtp_server.start()


