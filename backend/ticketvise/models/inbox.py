"""
Inbox
-------------------------------
Contains all entity sets for the inbox database.

**Table of contents**
* :class:`Inbox`
"""
import logging
from secrets import token_urlsafe
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from ticketvise import settings
from ticketvise.middleware import CurrentUserMiddleware
from ticketvise.models.utils import InboundMailProtocol, MailSecurity
from ticketvise.mail.retrieve import retrieve_emails, submit_email_ticket
from ticketvise.models.user import User, Role
from ticketvise.models.validators import validate_hex_color
from ticketvise.utils import random_preselected_color


class SchedulingAlgorithm(models.TextChoices):
    """
    Choices for the ``scheduling_algorithm`` field of :class:`Label` and
    :class:`Inbox`.
    """

    #: Schedules tickets in a round-robin fashion.
    ROUND_ROBIN = ("round-robin", "Round Robin")
    #: Assigns tickets to the assistant with the least assigned tickets.
    LEAST_ASSIGNED_FIRST = ("least-assigned-first", "Least Assigned First")
    # Schedule tickets based on sections
    SECTIONS = ("sections", "Workgroup")
    # Schedule all to one assistant
    FIXED = ("fixed", "Fixed")



def inbox_directory_path(instance, filename):
    return f"inboxes/{instance.id}/images/{token_urlsafe(64)}/{filename}"

class Inbox(models.Model):
    """
    This model represents a ticket inbox. Different users can be part of the same inbox,
    and each user can have multiple inboxes. Each user-inbox relationship has
    a role associated with it.

    :reverse relations: * **labels** -- Set of :class:`Label` s belonging to this inbox.
                        * **tickets** -- Set of :class:`Ticket` s belonging to the inbox.
                        * **user_relationship** -- Set of :class:`UserInbox` s belonging to the inbox.
                        * **users** -- Set of :class:`User` s belonging to the inbox.
    """

    lti_context_label = models.CharField(max_length=255, null=True, blank=True)
    lti_context_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, validators=[validate_hex_color], default=random_preselected_color)
    image = models.ImageField(upload_to=inbox_directory_path, max_length=1000, null=True, blank=True)
    scheduling_algorithm = models.CharField(choices=SchedulingAlgorithm.choices, max_length=255,
                                            default=SchedulingAlgorithm.LEAST_ASSIGNED_FIRST)
    round_robin_parameter = models.PositiveIntegerField(default=0)
    fixed_scheduling_assignee = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True)
    show_assignee_to_guest = models.BooleanField(default=False)
    visible_coordinator = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True, related_name="visible_coordinator")
    close_answered_weeks = models.PositiveIntegerField(default=0)
    alert_coordinator_unanswered_days = models.PositiveIntegerField(default=0)
    enable_create_new_ticket_by_email = models.BooleanField(default=False)
    enable_reply_by_email = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    email_enabled = models.BooleanField(default=False)
    email_login_state = models.CharField(max_length=255, null=True, blank=True)
    email_access_token = models.TextField(null=True, blank=True)
    email_refresh_token = models.TextField(null=True, blank=True)

    smtp_server = models.CharField(max_length=255, null=True, blank=True)
    smtp_port = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(65535)], default=587)
    smtp_security = models.CharField(choices=MailSecurity.choices, default=MailSecurity.TLS, max_length=8)
    smtp_username = models.EmailField(null=True, blank=True)
    smtp_sender = models.EmailField(null=True, blank=True)
    smtp_password = models.CharField(max_length=255, null=True, blank=True)
    smtp_use_oauth2 = models.BooleanField(default=False)

    inbound_email_protocol = models.CharField(choices=InboundMailProtocol.choices, default=InboundMailProtocol.IMAP,
                                              max_length=4)
    inbound_email_server = models.CharField(max_length=255, null=True, blank=True)
    inbound_email_port = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(65535)], default=993)
    inbound_email_security = models.CharField(choices=MailSecurity.choices, default=MailSecurity.TLS, max_length=8)
    inbound_email_username = models.EmailField(null=True, blank=True)
    inbound_email_password = models.CharField(max_length=255, null=True, blank=True)
    inbound_email_use_oauth2 = models.BooleanField(default=False)

    class Meta:
        unique_together = ("lti_context_label", "lti_context_id")

    def round_robin_parameter_increase(self):
        """
        Increase the round robin parameter and save the inbox.
        """
        self.round_robin_parameter += 1
        self.save()

    def get_users_by_role(self, role):
        """
        Get the users in the inbox that have the role.

        :param str role: The role that the users must have, must be one of the choices in :class:`Role`.

        :return: The users that have the role.
        :rtype: QuerySet<:class:`User`>
        """

        return User.objects.filter(inbox_relationship__inbox=self, inbox_relationship__role=role)

    def get_assistants_and_coordinators(self):
        """
        :return: All assistants and coordinators in the inbox.
        :rtype: QuerySet<:class:`User`>
        """
        roles = [Role.AGENT, Role.MANAGER]
        return User.objects.filter(inbox_relationship__inbox=self, inbox_relationship__role__in=roles)

    def get_assignable_assistants_and_coordinators(self):
        """
        :return: All assistants and coordinators in the inbox.
        :rtype: QuerySet<:class:`User`>
        """
        roles = [Role.AGENT, Role.MANAGER]
        return User.objects.filter(inbox_relationship__inbox=self, inbox_relationship__role__in=roles,
                                   inbox_relationship__is_assignable=True)

    def get_coordinator(self):
        """
        :return: Get the first coordinator of the course
        :rtype: QuerySet<:class:`User`>
        """
        return User.objects.filter(inbox_relationship__inbox=self, pk=self.visible_coordinator_id).first() if self.visible_coordinator_id else User.objects.filter(inbox_relationship__inbox=self, inbox_relationship__role=Role.MANAGER).order_by("date_created").first()

    def get_tickets_by_assignee(self, assignee, status=None):
        """
        Get all tickets for an assignee with an optional status parameter.

        :param User assignee: User that is the assignee of the tickets.
        :param str status: Status of the tickets, defaults to ``None``.
                           Must be one of the choices in :class:`Ticket.Status`.

        :return: All tickets with the assignee assigned to them.
        :rtype: QuerySet<:class:`Ticket`>
        """
        if status is None:
            return self.tickets.filter(assignee=assignee)

        return self.tickets.filter(assignee=assignee, status=status)

    def get_tickets_by_author(self, author, status=None):
        """
        Get all tickets for an author with an optional status parameter.

        :param User author: User that is the author of the tickets.
        :param str status: Status of the tickets, defaults to ``None``.
                           Must be one of the choices in :class:`Ticket.Status`.

        :return: All tickets created by the author.
        :rtype: QuerySet<:class:`Ticket`>
        """
        if status is None:
            return self.tickets.filter(author=author)

        return self.tickets.filter(author=author, status=status)

    def is_classic_email_setup(self):
        return self.inbound_email_server is not None and \
            self.inbound_email_username is not None and \
            self.inbound_email_password is not None and \
            self.smtp_server is not None and \
            self.smtp_username is not None and \
            self.smtp_password is not None

    def is_email_setup(self):
        # if SMTP and IMAP are enabled, we consider the inbox setup
        return self.email_enabled and ((self.is_classic_email_setup()) \
                or (self.email_access_token is not None and self.email_refresh_token is not None))

    def get_email_access_token(self):
        if not self.email_enabled or not (self.smtp_use_oauth2 and self.inbound_email_use_oauth2):
            return None

        accounts = [a for a in settings.MICROSOFT_AUTH.get_accounts() if a["username"] in [self.inbound_email_username, self.smtp_username]]
        if accounts:
            result = settings.MICROSOFT_AUTH.acquire_token_silent_with_error(scopes=settings.MICROSOFT_EMAIL_SCOPES, account=accounts[0])
        else:
            result = settings.MICROSOFT_AUTH.acquire_token_by_refresh_token(self.email_refresh_token, settings.MICROSOFT_EMAIL_SCOPES)
        
        return result.get('access_token')

    def sync_email(self):
        if not self.email_enabled:
            logging.info(f"Skipping retrieving email for inbox: {self.name} ({self.id})")
            return

        logging.info(f"Retrieving email for inbox: {self.name} ({self.id})")
        email_password = self.inbound_email_password
        if self.inbound_email_use_oauth2:
            email_password = self.get_email_access_token()

        emails = retrieve_emails(self.inbound_email_protocol,
                           self.inbound_email_server,
                           self.inbound_email_port,
                           self.inbound_email_username,
                           email_password,
                           self.inbound_email_security == MailSecurity.TLS,
                           self.inbound_email_use_oauth2)
        for message, raw_message in emails:
            submit_email_ticket(message, self, raw_message=raw_message)

    def __str__(self):
        return self.name


class InboxSection(models.Model):
    code = models.CharField(max_length=100)
    inbox = models.ForeignKey(Inbox, related_name="sections", on_delete=models.CASCADE)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("code", "inbox")


class InboxUserSection(models.Model):
    user = models.ForeignKey("User", related_name="inbox_sections", on_delete=models.CASCADE)
    section = models.ForeignKey(InboxSection, related_name="inbox_users", on_delete=models.CASCADE)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "section")


def inbox_directory_path(instance, filename):
    return f"inboxes/{instance.inbox.id}/material/{token_urlsafe(64)}/{filename}"


class InboxMaterial(models.Model):
    inbox = models.ForeignKey(Inbox, related_name="inbox_material", on_delete=models.CASCADE)
    file = models.FileField(upload_to=inbox_directory_path, max_length=1000)
    uploader = models.ForeignKey("User", on_delete=models.CASCADE, null=True)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.uploader = CurrentUserMiddleware.get_current_user()

        super().save(force_insert, force_update, using, update_fields)

    def delete(self, *args, **kwargs):
        # Set save to false to remove file from s3 storage
        self.file.delete(save=False)
        super().delete()
