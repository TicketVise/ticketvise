"""
Inbox
-------------------------------
Contains all entity sets for the inbox database.

**Table of contents**
* :class:`Inbox`
"""
from django.db import models

from ticketvise.models.user import UserInbox, User
from ticketvise.models.validators import validate_hex_color
from ticketvise.settings import INBOX_IMAGE_DIRECTORY, DEFAULT_INBOX_IMAGE_PATH


class SchedulingAlgorithm(models.TextChoices):
    """
    Choices for the ``scheduling_algorithm`` field of :class:`Label` and
    :class:`Inbox`.
    """

    #: Schedules tickets in a round-robin fashion.
    ROUND_ROBIN = ("round-robin", "Round Robin")
    #: Assigns tickets to the assistant with the least assigned tickets.
    LEAST_ASSIGNED_FIRST = ("least-assigned-first", "Least Assigned First")
    #: Does not use any custom scheduling method.
    MANUAL = ("manual", "Manual")


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

    #: Inbox code, must be unique for every inbox.
    code = models.CharField(max_length=50, unique=True)
    #: Inbox name, maximum length of 100 characters.
    name = models.CharField(max_length=100)
    #: Inbox color, must be a valid hex color.
    color = models.CharField(max_length=7, validators=[validate_hex_color])
    #: Inbox image, shown to users. This image has the inbox color applied to it.
    image = models.ImageField(upload_to=INBOX_IMAGE_DIRECTORY, default=DEFAULT_INBOX_IMAGE_PATH)
    #: Scheduling algorithm for the inbox, used to schedule tickets.
    #: Must be one of the choices in :class:`SchedulingAlgorithms`.
    #: Defaults to :attr:`SchedulingAlgorithms.MANUAL`.
    scheduling_algorithm = models.CharField(choices=SchedulingAlgorithm.choices, max_length=255,
                                            default=SchedulingAlgorithm.LEAST_ASSIGNED_FIRST)
    #: Parameter used for round-robin scheduling. Defaults to ``0``.
    round_robin_parameter = models.PositiveIntegerField(default=0)
    #: Indicates if students can see assignees of tickets. Defaults to ``False``.
    visibility_assignee = models.BooleanField(default=False)
    #: Close all answered tickets after set amount of weeks. Defaults to ``0``.
    close_answered_weeks = models.PositiveIntegerField(default=0)
    #: Alert coordinator of unanswered tickets after set amount of days. Defaults to ``0``.
    alert_coordinator_unanswered_days = models.PositiveIntegerField(default=0)
    #: Indicates if the instance is active or not. Defaults to ``True``.
    is_active = models.BooleanField(default=True)

    def round_robin_parameter_increase(self):
        """
        Increase the round robin parameter and save the inbox.
        """
        self.round_robin_parameter += 1
        self.save()

    def get_users_by_role(self, role):
        """
        Get the users in the inbox that have the role.

        :param str role: The role that the users must have, must be one of the choices in :class:`User.Roles`.

        :return: The users that have the role.
        :rtype: QuerySet<:class:`User`>
        """

        return User.objects.filter(inbox_relationship__inbox=self, inbox_relationship__role=role)

    def get_assistants_and_coordinators(self):
        """
        :return: All assistants and coordinators in the inbox.
        :rtype: QuerySet<:class:`User`>
        """
        roles = [User.Roles.ASSISTANT, User.Roles.COORDINATOR]
        return User.objects.filter(inbox_relationship__inbox=self, inbox_relationship__role__in=roles)

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
