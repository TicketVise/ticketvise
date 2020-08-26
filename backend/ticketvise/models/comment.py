"""
Comment
-------------------------------
Contains all entity sets for the comment database.

**Table of contents**
* :var:`MAX_COMMENT_CHAR_LENGTH`
* :class:`Comment`
"""
import re

from django.db import models

from ticketvise.email import send_mentioned_mail
from ticketvise.models.notification import MentionNotification, CommentNotification
from ticketvise.models.user import User

MAX_COMMENT_CHAR_LENGTH = 50


class Comment(models.Model):
    """
    This model represents a comment. Each comment is associated with a single :class:`Ticket`.

    :reverse relations: * **comment_notifications** -- Set of :class:`CommentNotification` s
                          that are attached to the comment.
                        * **mention_notifications** -- Set of :class:`MentionNotification` s
                          that are attached to the ticket.
    """

    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    is_reply = models.BooleanField(default=False)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    _username_regex = re.compile("(?<=^|(?<=[^a-zA-Z0-9-_\\.]))@([A-Za-z]+[A-Za-z0-9-_]+)")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to send notifications to users when a comment is placed.
        Sends a :class:`MentionNotification` to users who were mentioned in the comment.
        Sends a :class:`CommentNotification` to users when the comment is placed.
        Sends an email to users who were mentioned in the comment.
        """
        super().save(force_insert, force_update, using, update_fields)

        usernames = [match.group(0).replace("@", "") for match in re.finditer(self._username_regex, self.content)]

        for receiver in User.objects.filter(username__in=usernames):
            message = MentionNotification(receiver=receiver, comment=self)
            message.save()

            if self.author.notification_mention_mail:
                send_mentioned_mail(self, receiver)

        if self.is_reply:
            if self.author.is_assistant_or_coordinator(self.ticket.inbox):
                self.ticket.status = "ANSD"
            elif self.ticket.status == "CLSD":
                if self.ticket.assignee:
                    self.ticket.status = "ASGD"
                else:
                    self.ticket.status = "PNDG"

            self.ticket.save()

            message = CommentNotification(receiver=self.ticket.author, comment=self)
            message.save()

        if self.ticket.assignee:
            message = CommentNotification(receiver=self.ticket.assignee, comment=self)
            message.save()
        else:
            for receiver in self.ticket.inbox.get_assistants_and_coordinators():
                message = CommentNotification(receiver=receiver, comment=self)
                message.save()

    def __str__(self):
        content = str(self.content)

        if len(content) < MAX_COMMENT_CHAR_LENGTH:
            return content
        else:
            return content[:MAX_COMMENT_CHAR_LENGTH] + "..."
