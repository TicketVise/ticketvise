"""
Ticket
-------------------------------
Contains all entity sets for the ticket database and TicketStatusChangedNotification due to dependencies.

**Table of contents**
* :class:`Ticket`
* :class:`TicketStatuscChangedNotification`
"""
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from model_utils.managers import InheritanceManager

from ticketvise.email import send_email
from ticketvise.middleware import CurrentUserMiddleware
from ticketvise.models.label import Label
from ticketvise.models.notification import Notification
from ticketvise.scheduling import schedule_ticket


class Status(models.TextChoices):
    """
    Choices for the :attr:`Ticket.status` field.
    """

    PENDING = "PNDG", _("Pending")
    ASSIGNED = "ASGD", _("Assigned")
    ANSWERED = "ANSD", _("Answered")
    CLOSED = "CLSD", _("Closed")


class Ticket(models.Model):
    """
    This model represents a ticket. Each ticket is associated with a single :class:`Inbox` and
    can have multiple :class:`Label` s.

    :reverse relations: * **comments** -- Set of :class:`Comment` s that were posted on the ticket.
                        * **ticket_notifications** -- Set of :class:`TicketStatusChangedNotification` s
                          that are attached to the ticket.
    """

    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="tickets")
    shared_with = models.ManyToManyField("User", blank=True, through="TicketSharedUser")
    assignee = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="assigned_tickets")
    inbox = models.ForeignKey("Inbox", on_delete=models.CASCADE, related_name="tickets")
    title = models.CharField(max_length=100)
    ticket_inbox_id = models.PositiveIntegerField()
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.PENDING)
    content = models.TextField()
    labels = models.ManyToManyField("Label", blank=True, related_name="tickets", through="TicketLabel")
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("ticket_inbox_id", "inbox")

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
        self.status = Status.ASSIGNED
        self.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to send a :class:`TicketStatusChangedNotification`
        to the ticket's assignee or to all assistants an coordinators if the ticket has no
        assignee. Also send an email to the student that submitted the ticket if the status has changed to assigned
        or closed. Only send the change to assigned email if show assignee is enabled for the inbox.
        """
        old_ticket = None
        old_status = None

        if self.id:
            old_ticket = Ticket.objects.get(pk=self.id)
            old_status = old_ticket.get_status()

            if old_ticket.status == Status.PENDING and old_ticket.assignee is None and self.assignee:
                self.status = Status.ASSIGNED
            if old_ticket.status == Status.ASSIGNED and old_ticket.assignee and not self.assignee:
                self.status = Status.PENDING
        else:
            # + 1 so the ticket_inbox_id starts at 1 instead of 0.
            self.ticket_inbox_id = Ticket.objects.filter(inbox=self.inbox).count() + 1

        super().save(force_insert, force_update, using, update_fields)

        if old_ticket:
            if old_ticket.status != self.status:
                TicketStatusEvent.objects.create(ticket=self, initiator=CurrentUserMiddleware.get_current_user(),
                                                 old_status=old_status, new_status=self.status)

            if self.assignee and old_ticket.assignee != self.assignee:
                TicketAssigneeEvent.objects.create(ticket=self, assignee=self.assignee,
                                                   initiator=CurrentUserMiddleware.get_current_user())

        else:
            schedule_ticket(self)

        if old_status == self.get_status():
            return

        if self.assignee:
            message = TicketStatusChangedNotification(
                receiver=self.assignee, is_read=False, ticket=self, old_status=old_status,
                new_status=self.get_status()
            )
            message.save()
        else:
            for receiver in self.inbox.get_assistants_and_coordinators():
                message = TicketStatusChangedNotification(
                    receiver=receiver, is_read=False, ticket=self, old_status=old_status,
                    new_status=self.get_status()
                )

                message.save()

        if self.author.notification_ticket_status_change_mail:
            if not (self.status == Status.ASSIGNED and not self.inbox.show_assignee_to_guest):
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
        if self.status == Status.PENDING:
            return "Pending"
        elif self.status == Status.ASSIGNED:
            return "Assigned"
        elif self.status == Status.ANSWERED:
            return "Answered"
        elif self.status == Status.CLOSED:
            return "Closed"
        else:
            raise NotImplementedError(f"Status {self.status} not implemented")


class TicketSharedUser(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)


class TicketLabel(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

        if not self.id:
            TicketLabelEvent.objects.create(ticket=self.ticket, label=self.label, is_added=True,
                                            initiator=CurrentUserMiddleware.get_current_user())

    def delete(self, using=None, keep_parents=False):
        TicketLabelEvent.objects.create(ticket=self.ticket, label=self.label, is_added=False,
                                        initiator=CurrentUserMiddleware.get_current_user())

        return super().delete(using, keep_parents)


@receiver(m2m_changed, sender=Ticket.labels.through)
def labels_changed_handler(sender, action, instance, model, **kwargs):
    ticket = instance
    labels = Label.objects.filter(id__in=kwargs["pk_set"])

    if action == "post_add":
        for label in labels:
            TicketLabelEvent.objects.create(ticket=ticket, label=label, is_added=True,
                                            initiator=CurrentUserMiddleware.get_current_user())
    elif action == "post_remove":
        for label in labels:
            TicketLabelEvent.objects.create(ticket=ticket, label=label, is_added=False,
                                            initiator=CurrentUserMiddleware.get_current_user())


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="media/tickets")
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)


class TicketStatusChangedNotification(Notification):
    """
    Notification used for when the status of a :class:`Ticket` changes.
    """

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="ticket_notifications")
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
        if self.receiver.notification_ticket_status_change_app or self.receiver.notification_ticket_status_change_mail:
            super().save(force_insert, force_update, using, update_fields)


class TicketEvent(models.Model):
    objects = InheritanceManager()
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    initiator = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)


class TicketStatusEvent(TicketEvent):
    old_status = models.CharField(max_length=8, choices=Status.choices, null=True)
    new_status = models.CharField(max_length=8, choices=Status.choices, null=False)


class TicketAssigneeEvent(TicketEvent):
    assignee = models.ForeignKey("User", on_delete=models.CASCADE)


class TicketLabelEvent(TicketEvent):
    label = models.ForeignKey("Label", on_delete=models.CASCADE)
    is_added = models.BooleanField()
