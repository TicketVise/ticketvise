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

from ticketvise.models.notification.comment import CommentNotification
from ticketvise.models.notification.mention import MentionNotification
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
            MentionNotification.objects.create(receiver=receiver, comment=self)

        if self.is_reply:
            if self.author.is_assistant_or_coordinator(self.ticket.inbox) and self.author != self.ticket.author:
                self.ticket.status = "ANSD"
                if not self.ticket.assignee:
                    self.ticket.assignee = self.author
            elif self.ticket.status == "CLSD":
                if self.ticket.assignee:
                    self.ticket.status = "ASGD"
                else:
                    self.ticket.status = "PNDG"
            elif self.ticket.assignee:
                if self.ticket.assignee:
                    self.ticket.status = "ASGD"
                else:
                    self.ticket.status = "PNDG"

            self.ticket.save()

            CommentNotification.objects.create(receiver=self.ticket.author, comment=self)

        if self.ticket.assignee:
            # Preventing sending a comment and mention notification if assignee is being mentioned.
            if self.ticket.assignee.username not in usernames:
                CommentNotification.objects.create(receiver=self.ticket.assignee, comment=self)
        else:
            for receiver in self.ticket.inbox.get_assistants_and_coordinators():
                CommentNotification.objects.create(receiver=receiver, comment=self)

    def __str__(self):
        content = str(self.content)

        if len(content) < MAX_COMMENT_CHAR_LENGTH:
            return content
        else:
            return content[:MAX_COMMENT_CHAR_LENGTH] + "..."
