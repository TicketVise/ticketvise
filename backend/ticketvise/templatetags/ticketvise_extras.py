"""
TicketVise Extras
-------------------------------
Contains various templatetags that can be used in the html templates.
"""
import markdown as md
from django import template
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import stringfilter
from django.utils.http import urlsafe_base64_encode

from ..utils import get_text_color

register = template.Library()


@register.simple_tag
def abs_value(value):
    return abs(value)


@register.simple_tag
def get_label_text_color(label):
    """
    Get the color of a label.

    :param Label label: The label.

    :return: The text color for the label.
    :rtype: str
    """
    return get_text_color(label.color)


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
def user_is_assistant_or_coordinator(user, inbox):
    """
    Check if a user is an assistant or coordinator for a inbox.

    :param User user: The user.
    :param Inbox inbox: The inbox.

    :return: If the user is assistant or coordinator in the inbox.
    :rtype: bool
    """
    return user.is_assistant_or_coordinator(inbox)


@register.simple_tag
def user_is_coordinator(user, inbox):
    """
    Check if a user is a coordinator.

    :param User user: The user.
    :param Inbox inbox: The inbox.

    :return: If the user is assistant or coordinator in the inbox.
    :rtype: bool
    """
    return user.is_coordinator_for_inbox(inbox)


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


@register.filter()
@stringfilter
def markdown(value):
    """
    Interpret the markdown syntax and convert it to html elements to display
    on the page.

    :param str value: The markdown.

    :return: The stylized html.
    :rtype: str
    """
    return md.markdown(value, extensions=["markdown.extensions.fenced_code"])


@register.filter(name="times")
def times(x):
    """
    Allow for a loop to be used in a template.

    :param int x: The amount of times to loop.

    :return: Range up to x.
    :rtype: Range object
    """
    return range(x)


@register.simple_tag
def get_reset_password_url(user):
    """
    Returns a url to where the user can change his password without requireing the old password.

    :param User user: The user for which the url must be generated.

    :return: The password reset url.
    """
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(str(user.id).encode("utf-8"))

    return f"/reset/{uidb64}/{token}/"
