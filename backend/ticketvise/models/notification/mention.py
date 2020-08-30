from django.db import models

from ticketvise.models.notification import Notification


class MentionNotification(Notification):
    """
    Notification used for when a :class:`User` gets mentioned in a :class:`Comment`.
    """

    #: :class:`Comment` that the notification is associated with.
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="mention_notifications")

    @property
    def ticket(self):
        return self.comment.ticket

    @property
    def author(self):
        return f"@{self.comment.author.username}"

    @property
    def content(self):
        return f"You have been mentioned by {self.comment.author.get_full_name()}"

    @property
    def inbox(self):
        return self.comment.ticket.inbox

    def get_email_comments(self):
        return self.ticket.comments.filter(is_reply=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.receiver == self.comment.author:
            return

        if self.receiver.notification_mention_mail:
            self.send_mail()

        if self.receiver.notification_mention_app:
            super().save(force_insert, force_update, using, update_fields)
