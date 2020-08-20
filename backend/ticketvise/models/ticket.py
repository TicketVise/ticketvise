"""
Ticket
-------------------------------
Contains all entity sets for the ticket database and TicketStatusChangedNotification due to dependencies.

**Table of contents**
* :class:`Ticket`
* :class:`TicketStatuscChangedNotification`
"""
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ticketvise.email import send_email
from ticketvise.models.notification import Notification


class Ticket(models.Model):
    """
    This model represents a ticket. Each ticket is associated with a single :class:`Inbox` and
    can have multiple :class:`Label` s.

    :reverse relations: * **comments** -- Set of :class:`Comment` s that were posted on the ticket.
                        * **ticket_notifications** -- Set of :class:`TicketStatusChangedNotification` s
                          that are attached to the ticket.
    """

    #: The :class:`User` who created the ticket.
    author = models.ForeignKey("User", models.CASCADE, related_name=_("author"))
    #: The :class:`User` who the ticket is shared with.
    shared_with = models.ManyToManyField("User", blank=True, related_name=_("participants"))
    #: The :class:`User` to whom the ticket is assigned. Nullable and optional.
    assignee = models.ForeignKey("User", models.CASCADE, blank=True, null=True, related_name=_("assignee"))
    #: The :class:`Inbox` that the ticket is associated with.
    inbox = models.ForeignKey("ticketvise.Inbox", models.CASCADE, related_name="tickets")
    #: The title of the ticket.
    title = models.CharField(max_length=100)
    #: Ticket ID for the inbox it is part of. Used in URLs and references.
    ticket_inbox_id = models.PositiveIntegerField()

    class Meta:
        unique_together = ("ticket_inbox_id", "inbox")

    class Status(models.TextChoices):
        """
        Choices for the :attr:`Ticket.status` field.
        """

        #: Status when the ticket is first create and not automatically assigned.
        PENDING = "PNDG", _("Pending")
        #: Status when the ticket is assigned to an assistant.
        ASSIGNED = "ASGD", _("Assigned")
        #: Status when an assistant has replied to the ticket.
        ANSWERED = "ANSD", _("Answered")
        #: Status when the ticket has been resolved.
        CLOSED = "CLSD", _("Closed")

    #: Ticket status. Must be one of the choices in :class:`Ticket.Status`.
    #: Defaults to :attr:`Ticket.Status.PENDING`.
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.PENDING)
    #: Date that the ticket was created. Automatically added on creation.
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    #: Date that the ticket was last edited. Automatically changed on attribute change.
    #: Nullable and optional.
    date_edited = models.DateTimeField(_("Date edited"), auto_now=True, blank=True, null=True)
    #: The content inside the ticket.
    content = models.TextField()
    #: The :class:`Label` s associated with the ticket. Optional.
    labels = models.ManyToManyField("Label", blank=True, related_name="tickets")
    #: Indicates if the instance is active or not. Defaults to ``True``.
    is_active = models.BooleanField(_("Is active"), default=True)

    def add_label(self, label):
        """
        Add the label to the :attr:`Ticket.labels` field and update the highest priority label.

        :param Label label: Label to add to the ticket.
        """
        self.labels.add(label)
        self.save()

    def delete_label(self, label):
        """
        Remove the label from the :attr:`Ticket.labels` field and update the highest priority label.

        :param Label label: Label to remove from the ticket.
        """
        self.labels.remove(label)
        self.save()

    def assign_to(self, receiver):
        """
        Assign the ticket to a :class:`User` and update the status to
        :attr:`Ticket.Status.ASSIGNED`.

        :param User user: User to assign the ticket to.
        """
        self.assignee = receiver
        self.status = Ticket.Status.ASSIGNED
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to send a :class:`TicketStatusChangedNotification`
        to the ticket's assignee or to all assistants an coordinators if the ticket has no
        assignee. Also send an email to the student that submitted the ticket if the status has changed to assigned
        or closed. Only send the change to assigned email if show assignee is enabled for the inbox.
        """
        old_status = None

        if self.id:
            old_status = Ticket.objects.get(pk=self.id).get_status()
        else:
            # + 1 so the ticket_inbox_id starts at 1 instead of 0.
            self.ticket_inbox_id = Ticket.objects.filter(inbox=self.inbox).count() + 1

        super().save(force_insert, force_update, using, update_fields)

        if old_status == self.get_status():
            return

        if self.assignee:
            message = TicketStatusChangedNotification(
                receiver=self.assignee, read=False, ticket=self, old_status=old_status, new_status=self.get_status()
            )
            message.save()
        else:
            for receiver in self.inbox.get_assistants_and_coordinators():
                message = TicketStatusChangedNotification(
                    receiver=receiver, read=False, ticket=self, old_status=old_status, new_status=self.get_status()
                )

                message.save()

        if self.author.notification_ticket_status_change_mail:
            if not (self.status == Ticket.Status.ASSIGNED and not self.inbox.visibility_assignee):
                mail_vars = {"ticket": self}

                send_email(
                    "Status change for ticket #%s" % self.ticket_inbox_id,
                    self.author.email,
                    "ticket_status_change",
                    mail_vars,
                )

    def get_status(self):
        """
        :return: Ticket status in human-readable format.
        """
        if self.status == Ticket.Status.PENDING:
            return "Pending"
        elif self.status == Ticket.Status.ASSIGNED:
            return "Assigned"
        elif self.status == Ticket.Status.ANSWERED:
            return "Answered"
        elif self.status == Ticket.Status.CLOSED:
            return "Closed"
        else:
            raise NotImplementedError(f"Status {self.status} not implemented")


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="media/tickets")


class TicketStatusChangedNotification(Notification):
    """
    Notification used for when the status of a :class:`Ticket` changes.
    """

    #: The ticket that had its status changed.
    ticket = models.ForeignKey("Ticket", models.CASCADE, related_name="ticket_notifications")
    #: The ticket's status before it changed. Nullable.
    old_status = models.CharField(max_length=8, choices=Ticket.Status.choices, null=True)
    #: The ticket's status after it changed.
    new_status = models.CharField(max_length=8, choices=Ticket.Status.choices)

    @property
    def get_ticket_url(self):
        """
        :return: The ticket url of the notification.
        """
        return reverse("ticket", args=(self.ticket.inbox_id, self.ticket.ticket_inbox_id))

    @property
    def get_title(self):
        """
        :return: The title of the ticket.
        """
        return self.ticket.title

    @property
    def get_author(self):
        """
        :return: The author of the ticket, prefixed by ``@``.
        """
        return f"@{self.ticket.author.username}"

    @property
    def get_content(self):
        """
        :return: The content of the notification.
        """
        if self.old_status:
            return f'Ticket status changed from "{self.old_status}" to "{self.new_status}"'

        return "A new ticket has been opened"

    @property
    def get_inbox(self):
        """
        :return: URL of the inbox connected.
        """
        return self.ticket.inbox

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to only save the notification if the receiver
        has the setting enabled.
        """
        if self.receiver.notification_ticket_status_change_app or self.receiver.notification_ticket_status_change_mail:
            super().save(force_insert, force_update, using, update_fields)
