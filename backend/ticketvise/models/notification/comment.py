from django.db import models

from ticketvise.models.notification import Notification


class CommentNotification(Notification):
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="comment_notifications")

    @property
    def ticket(self):
        return self.comment.ticket

    @property
    def author(self):
        return f"@{self.comment.author.username}"

    @property
    def content(self):
        if self.comment.is_reply:
            return f"{self.comment.author.get_full_name()} has posted a reply"

        return f"{self.comment.author.get_full_name()} has posted a comment"

    @property
    def inbox(self):
        return self.comment.ticket.inbox

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to only save the notification if the receiver
        has the setting enabled.
        """
        if self.receiver == self.comment.author:
            return

        if self.receiver.notification_comment_mail:
            self.send_mail()

        if self.receiver.notification_comment_app:
            super().save(force_insert, force_update, using, update_fields)