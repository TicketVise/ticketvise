"""
Notification
-------------------------------
Contains all entity sets for the Notification database, except TicketStatusChangedNotification due to dependencies.

**Table of contents**
* :class:`Notification`
* :class:`MentionNotification`
* :class:`CommentNotification`
"""
from django.db import models
from model_utils.managers import InheritanceManager

from ticketvise.email import send_mentioned_mail, send_ticket_new_reply_mail, send_ticket_status_changed_mail
from ticketvise.models.ticket import Status


class Notification(models.Model):
    """
    This model is the base for the other notification models.
    """

    objects = InheritanceManager()
    receiver = models.ForeignKey("User", on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def ticket(self):
        raise NotImplementedError

    @property
    def author(self):
        raise NotImplementedError

    @property
    def content(self):
        raise NotImplementedError

    @property
    def inbox(self):
        raise NotImplementedError


class MentionNotification(Notification):
    """
    Notification used for when a :class:`User` gets mentioned in a :class:`Comment`.
    """

    #: :class:`Comment` that the notification is associated with.
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="mention_notifications")

    @property
    def ticket(self):
        """
        :return: The ticket of the notification.
        """
        return self.comment.ticket

    @property
    def author(self):
        """
        :return: The username of the author of the comment, prefixed by ``@``.
        """
        return f"@{self.comment.author.username}"

    @property
    def content(self):
        """
        :return: The content of the notification.
        """
        return f"You have been mentioned by {self.comment.author.get_full_name()}"

    @property
    def inbox(self):
        """
        :return: URL of the inbox connected.
        """
        return self.comment.ticket.inbox

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to only save the notification if the receiver
        has the setting enabled.
        """
        if self.receiver == self.comment.author:
            return

        if self.receiver.notification_mention_mail:
            send_mentioned_mail(self.comment, self.receiver)

        if self.receiver.notification_mention_app:
            super().save(force_insert, force_update, using, update_fields)


class CommentNotification(Notification):
    """
    Notification used for when a :class:`Comment` was posted on a :class:`Ticket`.
    """

    #: :class:`Comment` that was posted.
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE, related_name="comment_notifications")

    @property
    def ticket(self):
        """
        :return: The ticket of the notification.
        """
        return self.comment.ticket

    @property
    def author(self):
        """
        :return: The username of the author of the comment, prefixed by ``@``.
        """
        return f"@{self.comment.author.username}"

    @property
    def content(self):
        """
        :return: The content of the notification.
        """
        if self.comment.is_reply:
            return f"{self.comment.author.get_full_name()} has posted a reply"

        return f"{self.comment.author.get_full_name()} has posted a comment"

    @property
    def inbox(self):
        """
        :return: URL of the inbox connected.
        """
        return self.comment.ticket.inbox

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to only save the notification if the receiver
        has the setting enabled.
        """
        if self.receiver == self.comment.author:
            return

        if self.receiver.notification_comment_mail:
            send_ticket_new_reply_mail(self.ticket, self.comment, self.receiver)

        if self.receiver.notification_comment_app:
            super().save(force_insert, force_update, using, update_fields)


class TicketStatusChangedNotification(Notification):
    """
    Notification used for when the status of a :class:`Ticket` changes.
    """

    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE, related_name="ticket_notifications")
    old_status = models.CharField(max_length=8, choices=Status.choices, null=True)
    new_status = models.CharField(max_length=8, choices=Status.choices)

    @property
    def author(self):
        """
        :return: The author of the ticket, prefixed by ``@``.
        """
        return f"@{self.ticket.author.username}"

    @property
    def content(self):
        """
        :return: The content of the notification.
        """
        if self.old_status:
            return f'Ticket status changed from "{self.old_status}" to "{self.new_status}"'

        return "A new ticket has been opened"

    @property
    def inbox(self):
        """
        :return: URL of the inbox connected.
        """
        return self.ticket.inbox

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to only save the notification if the receiver
        has the setting enabled.
        """
        if self.receiver.notification_ticket_status_change_mail:
            send_ticket_status_changed_mail(self.ticket, self.receiver)

        if self.receiver.notification_ticket_status_change_app:
            super().save(force_insert, force_update, using, update_fields)
