from django.db import models

from ticketvise.models.notification import Notification


class NewTicketNotification(Notification):
    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE, related_name="new_ticket_notifications")

    @property
    def author(self):
        return f"@{self.ticket.author.username}"

    @property
    def content(self):
        return f"A new ticket has been created by {self.ticket.author.get_full_name()}"

    @property
    def inbox(self):
        return self.ticket.inbox

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.receiver == self.ticket.author:
            return

        if self.receiver.notification_comment_mail:
            self.send_mail()

        if self.receiver.notification_comment_app:
            super().save(force_insert, force_update, using, update_fields)