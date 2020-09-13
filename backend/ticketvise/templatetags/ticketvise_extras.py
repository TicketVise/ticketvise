"""
TicketVise Extras
-------------------------------
Contains various templatetags that can be used in the html templates.
"""
from django import template

from ..models.notification import Notification
from ..models.user import User, Role

register = template.Library()


@register.simple_tag
def user_is_coordinator(user, inbox):
    """
    Check if a user is a coordinator.
    :param User user: The user.
    :param Inbox inbox: The inbox.
    :return: If the user is assistant or coordinator in the inbox.
    :rtype: bool
    """
    return user.is_coordinator_for_inbox(inbox) or user.is_superuser


@register.simple_tag
def abs_value(value):
    return abs(value)


@register.simple_tag
def get_user_role(user, inbox):
    """
    Get the role of a user.

    :param User user: The user.
    :param Inbox inbox: The inbox.

    :return: The role of the user in the inbox.
    :rtype: Role
    """
    return user.get_role_label_by_inbox(inbox)


@register.simple_tag
def get_simple_role_name(role):
    return Role[role].label


@register.simple_tag
def get_staff(inbox):
    """
    Get all staff members of inbox.

    :param Inbox inbox: The inbox.

    :return: all staff members of inbox.
    :rtype: list
    """
    staff_roles = [Role.AGENT, Role.MANAGER]

    return User.objects.filter(inbox_relationship__role__in=staff_roles, inbox_relationship__inbox=inbox)


@register.simple_tag
def user_has_bookmarked(user, inbox):
    """
    Check if the inbox is bookmarked by the user.

    :param User user: The user
    :param Inbox inbox: The inbox.
    :return: is_bookmarked
    :rtype: bool
    """
    return user.get_entry_by_inbox(inbox).is_bookmarked


@register.filter(name="times")
def times(x):
    """
    Allow for a loop to be used in a template.

    :param int x: The amount of times to loop.

    :return: Range up to x.
    :rtype: Range object
    """
    return range(x)
