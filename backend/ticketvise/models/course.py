"""
Course
-------------------------------
Contains all entity sets for the course database.

**Table of contents**
* :class:`Course`
"""
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from ticketvise.models.user import UserCourseRelationship, User
from ticketvise.models.validators import validate_hex_color
from ticketvise.settings import COURSE_IMAGE_DIRECTORY, DEFAULT_COURSE_IMAGE_PATH


class SchedulingAlgorithm(models.TextChoices):
    """
    Choices for the ``scheduling_algorithm`` field of :class:`Label` and
    :class:`Course`.
    """

    #: Schedules tickets in a round-robin fashion.
    ROUND_ROBIN = ("round-robin", "Round Robin")
    #: Assigns tickets to the assistant with the least assigned tickets.
    LEAST_ASSIGNED_FIRST = ("least-assigned-first", "Least Assigned First")
    #: Does not use any custom scheduling method.
    MANUAL = ("manual", "Manual")


class Course(models.Model):
    """
    This model represents a course. Different users can be part of the same course,
    and each user can have multiple courses. Each user-course relationship has
    a role associated with it.

    :reverse relations: * **labels** -- Set of :class:`Label` s belonging to this course.
                        * **tickets** -- Set of :class:`Ticket` s belonging to the course.
                        * **user_relationship** -- Set of :class:`UserCourseRelationship` s belonging to the course.
                        * **users** -- Set of :class:`User` s belonging to the course.
    """

    #: Course code, must be unique for every course.
    code = models.CharField(_("Course Code"), max_length=50, unique=True)
    #: Course name, maximum length of 100 characters.
    name = models.CharField(_("Course Name"), max_length=100)
    #: Course color, must be a valid hex color.
    color = models.CharField(max_length=7, validators=[validate_hex_color])
    #: Course image, shown to users. This image has the course color applied to it.
    image = models.ImageField(upload_to=COURSE_IMAGE_DIRECTORY, default=DEFAULT_COURSE_IMAGE_PATH)
    #: Scheduling algorithm for the course, used to schedule tickets.
    #: Must be one of the choices in :class:`SchedulingAlgorithms`.
    #: Defaults to :attr:`SchedulingAlgorithms.MANUAL`.
    scheduling_algorithm = models.CharField(choices=SchedulingAlgorithm.choices, max_length=255,
                                            default=SchedulingAlgorithm.LEAST_ASSIGNED_FIRST)
    #: Parameter used for round-robin scheduling. Defaults to ``0``.
    round_robin_parameter = models.PositiveIntegerField(default=0)
    #: Indicates if students can see assignees of tickets. Defaults to ``False``.
    visibility_assignee = models.BooleanField(_("Show assignee on student ticket overview"), default=False)
    #: Close all answered tickets after set amount of weeks. Defaults to ``0``.
    close_answered_weeks = models.PositiveIntegerField(default=0)
    #: Alert coordinator of unanswered tickets after set amount of days. Defaults to ``0``.
    alert_coordinator_unanswered_days = models.PositiveIntegerField(default=0)
    #: Indicates if the instance is active or not. Defaults to ``True``.
    is_active = models.BooleanField(_("Is active"), default=True)

    def round_robin_parameter_increase(self):
        """
        Increase the round robin parameter and save the course.
        """
        self.round_robin_parameter += 1
        self.save()

    def get_users_by_role(self, role):
        """
        Get the users in the course that have the role.

        :param str role: The role that the users must have, must be one of the choices in :class:`User.Roles`.

        :return: The users that have the role.
        :rtype: QuerySet<:class:`User`>
        """

        return User.objects.filter(course_relationship__course=self, course_relationship__role=role)

    def get_assistants_and_coordinators(self):
        """
        :return: All assistants and coordinators in the course.
        :rtype: QuerySet<:class:`User`>
        """
        roles = [User.Roles.ASSISTANT, User.Roles.COORDINATOR]
        return User.objects.filter(course_relationship__course=self, course_relationship__role__in=roles)

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
