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

    def get_email_comments(self):
        if not self.comment.is_reply:
            return self.ticket.comments.filter(is_reply=False)

        return super().get_email_comments()

    def get_message_id(self):
        return self.ticket.comment_message_id

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to only save the notification if the receiver
        has the setting enabled.
        """
        if self.receiver == self.comment.author:
            return

        if self.pk is None and self.receiver.notification_comment_mail:
            self.send_mail()

        if self.receiver.notification_comment_app:
            super().save(force_insert, force_update, using, update_fields)