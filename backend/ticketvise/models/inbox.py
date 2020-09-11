"""
Inbox
-------------------------------
Contains all entity sets for the inbox database.

**Table of contents**
* :class:`Inbox`
"""
from django.db import models

from ticketvise.models.user import User, Role
from ticketvise.models.validators import validate_hex_color
from ticketvise.settings import INBOX_IMAGE_DIRECTORY, DEFAULT_INBOX_IMAGE_PATH
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
    # Schedule all to one assistant
    FIXED = ("fixed", "Fixed")


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

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, validators=[validate_hex_color], default=random_preselected_color)
    image = models.ImageField(upload_to=INBOX_IMAGE_DIRECTORY, default=DEFAULT_INBOX_IMAGE_PATH)
    scheduling_algorithm = models.CharField(choices=SchedulingAlgorithm.choices, max_length=255,
                                            default=SchedulingAlgorithm.LEAST_ASSIGNED_FIRST)
    round_robin_parameter = models.PositiveIntegerField(default=0)
    fixed_scheduling_assignee = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True)
    show_assignee_to_guest = models.BooleanField(default=False)
    close_answered_weeks = models.PositiveIntegerField(default=0)
    alert_coordinator_unanswered_days = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

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

    def get_coordinator(self):
        """
        :return: Get the first coordinator of the course
        :rtype: QuerySet<:class:`User`>
        """
        return User.objects.filter(inbox_relationship__inbox=self, inbox_relationship__role=Role.MANAGER) \
            .order_by("date_created").first()

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

    def __str__(self):
        return self.name

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     p = ''
    #     if not path.exists(f"ticketvise/{self.image}") or self.image == DEFAULT_INBOX_IMAGE_PATH:
    #         p = self.image
    #         self.image = Image.open(f"ticketvise{DEFAULT_INBOX_IMAGE_PATH}")
    #     else:
    #         p = self.image
    #         self.image = Image.open(f"ticketvise/{self.image}")
    #
    #     self.image = crop_image(self.image)
    #     self.image.save(f"ticketvise/{p}", quality=60)
    #
    #     super().save(force_insert, force_update, using, update_fields)
