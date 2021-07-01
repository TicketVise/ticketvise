from django.apps import AppConfig


class TicketViseConfig(AppConfig):
    name = "ticketvise"
    smtp_server = None

    def ready(self):
        from ticketvise.email.smtp import SmtpServer

        if not self.smtp_server:
            self.smtp_server = SmtpServer()
        self.smtp_server.start()
