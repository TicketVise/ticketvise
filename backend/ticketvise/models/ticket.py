"""
Ticket
-------------------------------
Contains all entity sets for the ticket database and TicketStatusChangedNotification due to dependencies.

**Table of contents**
* :class:`Ticket`
* :class:`TicketStatuscChangedNotification`
"""
import os
import uuid

from django.db import models, transaction
from django.db.models import Max
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from model_utils.managers import InheritanceManager

from ticketvise import settings
from ticketvise.middleware import CurrentUserMiddleware
from ticketvise.models.label import Label
from ticketvise.models.notification.assigned import TicketAssignedNotification
from ticketvise.models.notification.new import NewTicketNotification
from ticketvise.scheduling import schedule_ticket


class Status(models.TextChoices):
    """
    Choices for the :attr:`Ticket.status` field.
    """

    PENDING = "PNDG", _("Pending")
    ASSIGNED = "ASGD", _("Assigned")
    ANSWERED = "ANSD", _("Awaiting response")
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
    shared_with = models.ManyToManyField("User", blank=True, through="TicketSharedUser", through_fields=("ticket", "user"))
    assignee = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="assigned_tickets")
    inbox = models.ForeignKey("Inbox", on_delete=models.CASCADE, related_name="tickets")
    title = models.CharField(max_length=100)
    ticket_inbox_id = models.PositiveIntegerField()
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.PENDING)
    content = models.TextField()
    labels = models.ManyToManyField("Label", blank=True, related_name="tickets", through="TicketLabel")
    is_public = models.BooleanField(default=False)
    publish_requested = models.BooleanField(default=False)
    reply_message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
    comment_message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False)
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
        self.status = Status.ASSIGNED if receiver else Status.PENDING

    def reopen(self):
        last_comment = self.comments.filter(is_reply=True).order_by("-date_created").first()

        if last_comment and last_comment.author.is_assistant_or_coordinator(self.inbox):
            self.status = Status.ANSWERED
        elif self.assignee is None:
            self.status = Status.PENDING
        else:
            self.status = Status.ASSIGNED

    @transaction.atomic
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Override the Django ``save`` method to send a :class:`TicketStatusChangedNotification`
        to the ticket's assignee or to all assistants an coordinators if the ticket has no
        assignee. Also send an email to the student that submitted the ticket if the status has changed to assigned
        or closed. Only send the change to assigned email if show assignee is enabled for the inbox.
        """
        old_ticket = Ticket.objects.filter(pk=self.id).first() if self.id else None

        if old_ticket:
            if old_ticket.status == Status.PENDING and old_ticket.assignee is None and self.assignee:
                self.status = Status.ASSIGNED
            if old_ticket.status == Status.ASSIGNED and old_ticket.assignee and not self.assignee:
                self.status = Status.PENDING
        else:
            # + 1 so the ticket_inbox_id starts at 1 instead of 0.
            self.ticket_inbox_id = (Ticket.objects.filter(inbox=self.inbox)
                                    .aggregate(Max('ticket_inbox_id'))["ticket_inbox_id__max"] or 0) + 1
            if not self.assignee:
                schedule_ticket(self)

        super().save(force_insert, force_update, using, update_fields)


        if old_ticket and old_ticket.status != self.status:
            TicketStatusEvent.objects.create(ticket=self, initiator=CurrentUserMiddleware.get_current_user(),
                                             old_status=old_ticket.status, new_status=self.status)

        if self.assignee and (not old_ticket or old_ticket.assignee != self.assignee):
            current_user = CurrentUserMiddleware.get_current_user()
            TicketAssigneeEvent.objects.create(ticket=self, assignee=self.assignee,
                                               initiator=current_user)
            if current_user != self.assignee:
                TicketAssignedNotification.objects.create(ticket=self, receiver=self.assignee)
        elif not self.assignee:
            for user in self.inbox.get_assistants_and_coordinators():
                NewTicketNotification.objects.create(ticket=self, receiver=user)

        if old_ticket and old_ticket.title != self.title:
            TicketTitleEvent.objects.create(ticket=self, initiator=CurrentUserMiddleware.get_current_user(),
                                            old_title=old_ticket.title, new_title=self.title)


class TicketSharedUser(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="shared_with_by")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="shared_with_me")
    sharer = models.ForeignKey("User", null=True, on_delete=models.SET_NULL, related_name="shared_to",
                               default=CurrentUserMiddleware.get_current_user)
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
    uploader = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.uploader = CurrentUserMiddleware.get_current_user()

        super().save(force_insert, force_update, using, update_fields)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(TicketAttachment, self).delete()


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


class TicketTitleEvent(TicketEvent):
    old_title = models.CharField(max_length=100)
    new_title = models.CharField(max_length=100)