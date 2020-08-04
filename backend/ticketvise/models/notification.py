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
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from model_utils.managers import InheritanceManager


class Notification(models.Model):
    """
    This model is the base for the other notification models.
    """

    objects = InheritanceManager()
    #: The :class:`User` that received the notification.
    receiver = models.ForeignKey("User", models.CASCADE, related_name="notifications")
    #: If ``True``, the notification is marked as read. Defaults to ``False``.
    read = models.BooleanField(_("Read"), default=False)
    #: Date that the notification was created. Automatically added on creation.
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)

    def get_ticket_url(self):
        raise NotImplementedError

    def get_title(self):
        raise NotImplementedError

    def get_author(self):
        raise NotImplementedError

    def get_content(self):
        raise NotImplementedError

    def get_course(self):
        raise NotImplementedError


class MentionNotification(Notification):
    """
    Notification used for when a :class:`User` gets mentioned in a :class:`Comment`.
    """

    #: :class:`Comment` that the notification is associated with.
    comment = models.ForeignKey("Comment", models.CASCADE, related_name="mention_notifications")

    def get_ticket_url(self):
        """
        :return: The ticket url of the ticket connected.
        """
        return reverse("ticket", args=(self.comment.ticket.course_id, self.comment.ticket.ticket_course_id))

    def get_title(self):
        """
        :return: The title of the ticket that the comment was posted on.
        """
        return self.comment.ticket.title

    def get_author(self):
        """
        :return: The username of the author of the comment, prefixed by ``@``.
        """
        return f"@{self.comment.author.username}"

    def get_content(self):
        """
        :return: The content of the notification.
        """
        return f"You have been mentioned by {self.comment.author.get_full_name()}"

    def get_course(self):
        """
        :return: URL of the course connected.
        """
        return self.comment.ticket.course

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to only save the notification if the receiver
        has the setting enabled.
        """
        if self.receiver.notification_mention_app and self.receiver != self.comment.author:
            super().save(force_insert, force_update, using, update_fields)


class CommentNotification(Notification):
    """
    Notification used for when a :class:`Comment` was posted on a :class:`Ticket`.
    """

    #: :class:`Comment` that was posted.
    comment = models.ForeignKey("Comment", models.CASCADE, related_name="comment_notifications")

    def get_ticket_url(self):
        """
        :return: The ticket url of the notification.
        """
        return reverse("ticket", args=(self.comment.ticket.course_id, self.comment.ticket.ticket_course_id))

    def get_title(self):
        """
        :return: The title of the ticket that the comment was posted on.
        """
        return self.comment.ticket.title

    def get_author(self):
        """
        :return: The username of the author of the comment, prefixed by ``@``.
        """
        return f"@{self.comment.author.username}"

    def get_content(self):
        """
        :return: The content of the notification.
        """
        if self.comment.is_reply:
            return f"{self.comment.author.get_full_name()} has posted a reply"

        return f"{self.comment.author.get_full_name()} has posted a comment"

    def get_course(self):
        """
        :return: URL of the course connected.
        """
        return self.comment.ticket.course

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to only save the notification if the receiver
        has the setting enabled.
        """
        if self.receiver.notification_comment_app and self.receiver != self.comment.author:
            super().save(force_insert, force_update, using, update_fields)
