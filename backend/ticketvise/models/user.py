"""
User
-------------------------------
Contains all entity sets for the user database.

**Table of contents**
* :class:`User`
* :class:`UserInbox`
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from ticketvise import settings
from ticketvise.settings import DEFAULT_AVATAR_PATH


class Role(models.TextChoices):
    """
    Choices for the :attr:`Role` field.
    """

    GUEST = "GUEST", _(settings.ROLE_GUEST_DISPLAY_NAME)
    AGENT = "AGENT", _(settings.ROLE_AGENT_DISPLAY_NAME)
    MANAGER = "MANAGER", _(settings.ROLE_MANAGER_DISPLAY_NAME)


class User(AbstractUser):
    """
    This model represents a user. A user can have different inboxes and has one
    role associated with each inbox. The roles can be found in the
    :class:`Role` class. Users also have various notification settings.

    :reverse relations: * **comments** -- Set of :class:`Comment` s written by the user.
                        * **inbox_relationship** -- Set of :class:`UserInbox` s belonging to the user.
                        * **notifications** -- Set of :class:`Notification` s belonging to the user.
    """

    lti_id = models.CharField(max_length=150, null=True)
    inboxes = models.ManyToManyField("Inbox", through="UserInbox", related_name="users")
    avatar_url = models.URLField(default=DEFAULT_AVATAR_PATH)
    notification_mention_mail = models.BooleanField(default=False)
    notification_mention_app = models.BooleanField(default=True)
    notification_new_ticket_mail = models.BooleanField(default=False)
    notification_new_ticket_app = models.BooleanField(default=True)
    notification_comment_mail = models.BooleanField(default=False)
    notification_comment_app = models.BooleanField(default=True)
    notification_assigned_mail = models.BooleanField(default=False)
    notification_assigned_app = models.BooleanField(default=True)
    notification_ticket_reminder_mail = models.BooleanField(default=False)
    notification_ticket_reminder_app = models.BooleanField(default=True)

    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def get_entry_by_inbox(self, inbox):
        """
        Get the entry in the :class:`UserInboxRelationship` table for the relationship
        between the user and the provided inbox.

        :param Inbox inbox: Inbox to filter by.

        :return: Relationship filtered by inbox.
        :rtype: :class:`UserInbox`
        """
        return UserInbox.objects.get(user=self, inbox=inbox)

    def is_coordinator_for_inbox(self, inbox):
        """
        Check if the user is a coordinator for the provided inbox.

        :param Inbox inbox: Inbox to check the role for.

        :return: ``True`` if the user has the :attr:`Role.MANAGER` role, ``False`` otherwise.
        :rtype: bool
        """
        return self.has_role_in_inbox(inbox, Role.MANAGER) or self.is_superuser

    def get_role_by_inbox(self, inbox):
        """
        Get the user's role for a inbox.

        :param Inbox inbox: Inbox to get the role for.

        :return: The role for the user in a specific inbox.
        :rtype: str
        """
        return self.get_entry_by_inbox(inbox).role

    def get_role_label_by_inbox(self, inbox):
        """
        Get the user's role for a inbox.

        :param Inbox inbox: Inbox to get the role for.

        :return: The role for the user in a specific inbox.
        :rtype: str
        """
        return Role[self.get_role_by_inbox(inbox)].label

    def get_entries_by_role(self, role):
        """
        Filters :class:`UserInbox` s by role and returns the resulting set.

        :param str role: The role to filter by. Must be one of the choices in :class:`Role`.

        :return: All user-inbox relationship with the role.
        :rtype: QuerySet<:class:`UserInboxrelationship`>
        """
        return UserInbox.objects.filter(user=self, role=role)

    def get_inboxes_by_role(self, role):
        """
        Gets a queryset of all inboxes where the user has the role.

        :param str role: The role to get inboxes from. Must be one of the choices in :class:`Role`.

        :return: Inboxs where the user has the role.
        :rtype: QuerySet<:class:`Inbox`>
        """
        entries = self.get_entries_by_role(role).values("inbox")
        inbox_ids = list(map(lambda entry: entry["inbox"], entries))

        return self.inboxes.filter(id__in=inbox_ids)

    def has_inbox(self, inbox):
        """
        Checks if the user is enrolled in or assigned to the inbox.

        :param Inbox inbox: The inbox to check. Must be one of the choices in :class:`Role`.

        :return: ``True`` if the user is enrolled in or assigned to the inbox, ``False`` otherwise.
        :rtype: bool
        """
        return inbox in self.inboxes.all()

    def has_role_in_inbox(self, inbox, role):
        """
        Checks if the user has the role in the inbox.

        :param Inbox inbox: The inbox to check.
        :param str role: The role to check. Must be one of the choices in :class:`Role`.

        :return: ``True`` if the user has the role in the inbox, ``False`` otherwise.
        :rtype: bool
        """
        if not self.has_inbox(inbox):
            return False

        return self.get_role_by_inbox(inbox) == role

    def is_assistant_or_coordinator(self, inbox):
        """
        Checks if the user is assistant or coordinator in the inbox.

        :param Inbox inbox: The inbox to check.

        :return: ``True`` if the user is assistant or coordinator in the inbox, ``False`` otherwise.
        :rtype: bool
        """
        if self.is_superuser:
            return True

        if not self.has_inbox(inbox):
            return

        return self.has_role_in_inbox(inbox, Role.AGENT) or self.has_role_in_inbox(
            inbox, Role.MANAGER
        )

    def add_inbox(self, inbox, role=Role.GUEST, bookmarked=False):
        """
        Add a inbox to the user, with an optional role.

        :param Inbox inbox: Inbox to add
        :param str role: The role to add to the user. Must be one of the choices in :class:`Role`.
                         Defaults to :attr:`Role.GUEST`.

        :raises ValueError: If the user is already associated with the inbox.
        """
        if self.has_inbox(inbox):
            raise ValueError(f"User already has inbox {inbox}")

        relationship = UserInbox(user=self, inbox=inbox, role=role, is_bookmarked=bookmarked)
        relationship.save()

    def set_role_for_inbox(self, inbox, role):
        """
        Set the role for the user in a specific inbox.

        :param Inbox inbox: The inbox to set the role for.
        :param str role: The role to add to the user. Must be one of the choices in :class:`Role`.

        :raises ValueError: If the user isn't associated with the inbox yet.
        """
        if not self.has_inbox(inbox):
            raise ValueError(f"User is not assigned to or enrolled in inbox {inbox}")

        relationship = self.get_entry_by_inbox(inbox)
        relationship.role = role
        relationship.save()


class UserInbox(models.Model):
    """
    Through table for :class:`User` to :class:`Inbox` many-to-many relationship.
    The user and inbox field values must be unique together.
    """

    user = models.ForeignKey(User, related_name="inbox_relationship", on_delete=models.CASCADE)
    inbox = models.ForeignKey("Inbox", related_name="user_relationship", on_delete=models.CASCADE)
    role = models.CharField(max_length=40, choices=Role.choices, default=Role.GUEST)
    is_bookmarked = models.BooleanField(default=False)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "inbox")
