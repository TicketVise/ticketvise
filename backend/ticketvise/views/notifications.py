"""
Notifications
-------------------------------
Contains the view to display the notifications.

**Table of contents**

* :class:`NotificationsView`
* :class:`NotificationStatusForm`
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import register
from django.views.generic import TemplateView

from ticketvise.models.notification import Notification
from ticketvise.models.notification.assigned import TicketAssignedNotification
from ticketvise.models.notification.comment import CommentNotification
from ticketvise.models.notification.mention import MentionNotification
from ticketvise.models.notification.new import NewTicketNotification
from ticketvise.models.notification.reminder import TicketReminderNotification
from ticketvise.models.user import User


class NotificationsView(LoginRequiredMixin, TemplateView):
    """
    View of the notifications page, which requires a logged in user.

    :var str template_name: The template name.
    """

    template_name = "notifications.html"


@register.simple_tag
def number_of_unread_notifications(user: User):
    """
    Returns the count of all notifications of the receiver with the read
    parameter equal to false. Can be used in templates.

    :param User user: The receiver of the notifications.

    :return: Number of unread notifications.
    :rtype: int
    """
    return Notification.objects.filter(receiver=user, is_read=False).count()


def unread_related_ticket_notifications(ticket, user):
    """
    Mark all notifications related to the given ticket as unread.

    :param Ticket ticket: Ticket for which all related notifications are marked
                          unread.
    :param User user: User for which the notifications are marked as unread.

    :return: None.
    """
    TicketAssignedNotification.objects.filter(ticket=ticket, receiver=user).update(is_read=True)
    CommentNotification.objects.filter(comment__ticket=ticket, receiver=user).update(is_read=True)
    MentionNotification.objects.filter(comment__ticket=ticket, receiver=user).update(is_read=True)
    NewTicketNotification.objects.filter(ticket=ticket, receiver=user).update(is_read=True)
    TicketReminderNotification.objects.filter(ticket=ticket, receiver=user).update(is_read=True)
