from django.db import models

from ticketvise.models.notification import Notification


class TicketReminderNotification(Notification):
    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE, related_name="ticket_reminder_notifications")

    @property
    def author(self):
        return f"@{self.ticket.author.username}"

    @property
    def content(self):
        alert_days = self.ticket.inbox.alert_coordinator_unanswered_days
        return f"Ticket ${self.ticket.ticket_inbox_id} has been unanswered for {alert_days} days"

    @property
    def inbox(self):
        return self.ticket.inbox

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.receiver == self.ticket.author:
            return

        if self.pk is None and self.receiver.notification_ticket_reminder_mail:
            self.send_mail()

        if self.receiver.notification_ticket_reminder_app:
            super().save(force_insert, force_update, using, update_fields)