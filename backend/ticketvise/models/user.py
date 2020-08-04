"""
User
-------------------------------
Contains all entity sets for the user database.

**Table of contents**
* :class:`User`
* :class:`UserCourseRelationship`
"""
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ticketvise.models.ticket import Ticket
from ticketvise.settings import DEFAULT_AVATAR_PATH


class User(AbstractUser):
    """
    This model represents a user. A user can have different courses and has one
    role associated with each course. The roles can be found in the
    :class:`User.Roles` class. Users also have various notification settings.

    :reverse relations: * **comments** -- Set of :class:`Comment` s written by the user.
                        * **course_relationship** -- Set of :class:`UserCourseRelationship` s belonging to the user.
                        * **notifications** -- Set of :class:`Notification` s belonging to the user.
    """

    #: The user id for authentication using LTI. Maximum length of 150 characters. Nullable.
    lti_id = models.CharField(max_length=150, verbose_name="LTI user ID", null=True)
    #: Username of the user, must be unique. Maximum length of 150 characters.
    username = models.CharField(
        error_messages={"unique": "A user with that username already exists."},
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        verbose_name="username",
    )
    #: First name of the user, maximum length of 30 characters.
    first_name = models.CharField(max_length=30, verbose_name="first name")
    #: Last name of the user, maximum length of 30 characters.
    last_name = models.CharField(max_length=150, verbose_name="last name")
    #: Email address of the user, must be unique.
    email = models.EmailField(unique=True, max_length=254, verbose_name="email address")
    #: The :class:`Course` s that the user is enrolled in or that the user assists.
    courses = models.ManyToManyField("Course", through="ticketvise.UserCourseRelationship", related_name="users")
    #: URL to the avatar picture of the user. Defaults to :const:`ticketvise.settings.DEFAULT_AVATAR_PATH`.
    avatar_url = models.URLField(default=DEFAULT_AVATAR_PATH)
    #: Django groups that the user is part of. Unused.
    groups = models.ManyToManyField(
        blank=True,
        help_text="The groups this user belongs to. A user will get all "
                  + "permissions granted to each of their groups.",
        related_name="user_set",
        related_query_name="user",
        to="auth.Group",
        verbose_name="groups",
    )
    #: Django permissions that the user has. Unused.
    user_permissions = models.ManyToManyField(
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="user_set",
        related_query_name="user",
        to="auth.Permission",
        verbose_name="user permissions",
    )
    #: If the user can access the admin panel. Defaults to ``False``.
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this " + "admin site.",
        verbose_name="staff status",
    )
    #: If the user can access the admin panel. Defaults to ``False``.
    is_superuser = models.BooleanField(
        default=False,
        help_text="Designates that this user has all permissions " + "without explicitly assigning them.",
        verbose_name="superuser status",
    )
    #: Indicates if the instance is active or not. Defaults to ``True``.
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as "
                  + "active. Unselect this instead of deleting accounts.",
        verbose_name="active",
    )
    #: Notification setting. If ``True```, the user receives an email after being mentioned.
    #: Defaults to ``True``.
    notification_mention_mail = models.BooleanField(_("Receive mail mention"), default=True)
    #: Notification setting. If ``True```, the user receives an in-app notification after being mentioned.
    #: Defaults to ``True``.
    notification_mention_app = models.BooleanField(_("Receive in-app mention notification"), default=True)
    #: Notification setting. If ``True```, the user receives an email when a ticket's status has changed.
    #: Defaults to ``True``.
    notification_ticket_status_change_mail = models.BooleanField(
        _("Receive mail after ticket status change"), default=True
    )
    #: Notification setting. If ``True```, the user receives an in-app notification when
    #: a ticket's status has changed. Defaults to ``True``.
    notification_ticket_status_change_app = models.BooleanField(
        _("Receive in-app ticket status change notification"), default=True
    )
    #: Notification setting. If ``True```, the user receives an email when a new ticket is created.
    #: Defaults to ``True``.
    notification_new_ticket_mail = models.BooleanField(_("Receive mail after new_ticket"), default=True)
    #: Notification setting. If ``True```, the user receives an in-app notification when a new ticket is created.
    #: Defaults to ``True``.
    notification_new_ticket_app = models.BooleanField(_("Receive in-app new_ticket notification"), default=True)
    #: Notification setting. If ``True```, the user receives an email when a comment is posted
    #: on a ticket. Defaults to ``True``.
    notification_comment_mail = models.BooleanField(_("Receive mail after comment"), default=True)
    #: Notification setting. If ``True```, the user receives an in-app notification when a comment is posted
    #: on a ticket. Defaults to ``True``.
    notification_comment_app = models.BooleanField(_("Receive in-app comment notification"), default=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        app_label = "ticketvise"

    class Roles(models.TextChoices):
        """
        Choices for the :attr:`User.roles` field.
        """

        #: Students can create new tickets and view only their own tickets.
        STUDENT = "Student", _("Student")
        #: Assistants can comment on, reply to and manage tickets.
        ASSISTANT = "Assistant", _("Assistant")
        #: Coordinators can manage the course and see its statistics.
        COORDINATOR = "Coordinator", _("Coordinator")

    def get_entry_by_course(self, course):
        """
        Get the entry in the :class:`UserCourseRelationship` table for the relationship
        between the user and the provided course.

        :param Course course: Course to filter by.

        :return: Relationship filtered by course.
        :rtype: :class:`UserCourseRelationship`
        """
        return UserCourseRelationship.objects.get(user=self, course=course)

    def is_coordinator_for_course(self, course):
        """
        Check if the user is a coordinator for the provided course.

        :param Course course: Course to check the role for.

        :return: ``True`` if the user has the :attr:`User.Roles.COORDINATOR` role, ``False`` otherwise.
        :rtype: bool
        """
        return self.has_role_in_course(course, User.Roles.COORDINATOR)

    def get_role_by_course(self, course):
        """
        Get the user's role for a course.

        :param Course course: Course to get the role for.

        :return: The role for the user in a specific course.
        :rtype: str
        """
        return self.get_entry_by_course(course).role

    def get_entries_by_role(self, role):
        """
        Filters :class:`UserCourseRelationship` s by role and returns the resulting set.

        :param str role: The role to filter by. Must be one of the choices in :class:`User.Roles`.

        :return: All user-course relationship with the role.
        :rtype: QuerySet<:class:`UserCourserelationship`>
        """
        return UserCourseRelationship.objects.filter(user=self, role=role)

    def get_courses_by_role(self, role):
        """
        Gets a queryset of all courses where the user has the role.

        :param str role: The role to get courses from. Must be one of the choices in :class:`User.Roles`.

        :return: Courses where the user has the role.
        :rtype: QuerySet<:class:`Course`>
        """
        entries = self.get_entries_by_role(role).values("course")
        course_ids = list(map(lambda entry: entry["course"], entries))

        return self.courses.filter(id__in=course_ids)

    def get_tickets_by_course(self, course):
        """
        Gets all tickets of this user of this course
        """
        return Ticket.objects.filter(author=self, course=course).all()

    def has_course(self, course):
        """
        Checks if the user is enrolled in or assigned to the course.

        :param Course course: The course to check. Must be one of the choices in :class:`User.Roles`.

        :return: ``True`` if the user is enrolled in or assigned to the course, ``False`` otherwise.
        :rtype: bool
        """
        return course in self.courses.all()

    def has_role_in_course(self, course, role):
        """
        Checks if the user has the role in the course.

        :param Course course: The course to check.
        :param str role: The role to check. Must be one of the choices in :class:`User.Roles`.

        :return: ``True`` if the user has the role in the course, ``False`` otherwise.
        :rtype: bool
        """
        if not self.has_course(course):
            return False

        return self.get_role_by_course(course) == role

    def is_assistant_or_coordinator(self, course):
        """
        Checks if the user is assistant or coordinator in the course.

        :param Course course: The course to check.

        :return: ``True`` if the user is assistant or coordinator in the course, ``False`` otherwise.
        :rtype: bool
        """
        if not self.has_course(course):
            return

        return self.has_role_in_course(course, User.Roles.ASSISTANT) or self.has_role_in_course(
            course, User.Roles.COORDINATOR
        )

    def is_assistant_or_coordinator_in_a_course(self):
        """
        Checks if the user is assistant or coordinator in any of the associated courses of the user.

        :return: ``True`` if the user is assistant or coordinator in any course, ``False`` otherwise.
        :rtype: bool
        """
        return UserCourseRelationship.objects.filter(
            user=self, role__in=[User.Roles.ASSISTANT, User.Roles.COORDINATOR]
        ).exists()

    def add_course(self, course, role=Roles.STUDENT, bookmarked=False):
        """
        Add a course to the user, with an optional role.

        :param Course course: Course to add
        :param str role: The role to add to the user. Must be one of the choices in :class:`User.Roles`.
                         Defaults to :attr:`User.Roles.STUDENT`.

        :raises ValueError: If the user is already associated with the course.
        """
        if self.has_course(course):
            raise ValueError(f"User already has course {course}")

        relationship = UserCourseRelationship(user=self, course=course, role=role, is_bookmarked=bookmarked)
        relationship.save()

    def set_role_for_course(self, course, role):
        """
        Set the role for the user in a specific course.

        :param Course course: The course to set the role for.
        :param str role: The role to add to the user. Must be one of the choices in :class:`User.Roles`.

        :raises ValueError: If the user isn't associated with the course yet.
        """
        if not self.has_course(course):
            raise ValueError(f"User is not assigned to or enrolled in course {course}")

        relationship = self.get_entry_by_course(course)
        relationship.role = role
        relationship.save()


class UserCourseRelationship(models.Model):
    """
    Through table for :class:`User` to :class:`Course` many-to-many relationship.
    The user and course field values must be unique together.
    """

    user = models.ForeignKey(User, related_name="course_relationship", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", related_name="user_relationship", on_delete=models.CASCADE)
    #: Role that the user has in the course. Maximum length of 40 characters.
    #: Must be one of the choices in the :class:`User.Roles` class. Defaults to :attr:`User.Roles.STUDENT`.
    role = models.CharField(max_length=40, choices=User.Roles.choices, default=User.Roles.STUDENT)
    is_bookmarked = models.BooleanField(default=False,
                                        help_text="Designates if the course is bookmarked by the user",
                                        verbose_name="bookmarked",
                                        )

    class Meta:
        unique_together = ("user", "course")
