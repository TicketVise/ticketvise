"""
Notifications
-------------------------------
Contains the view to display the notifications.

**Table of contents**

* :class:`NotificationsView`
* :class:`NotificationStatusForm`
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.forms import forms, IntegerField
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import register
from django.views.generic import TemplateView

from ticketvise.models.notification import Notification, MentionNotification, CommentNotification
from ticketvise.models.ticket import TicketStatusChangedNotification
from ticketvise.models.user import User


@register.simple_tag
def number_of_unread_notifications(user: User):
    """
    Returns the count of all notifications of the receiver with the read
    parameter equal to false. Can be used in templates.

    :param User user: The receiver of the notifications.

    :return: Number of unread notifications.
    :rtype: int
    """
    return Notification.objects.filter(receiver=user, read=False).count()


def get_notifications(user: User, read=""):
    """
    Returns the notifications of the receiver with the possibility to specify if
    the notifications are read or unread.

    :param User user: The receiver of the notifications.
    :param str read: "read" or "unread" specification of read.
    :param int first_item: The first item to show on the page
    :param int last_item: The last item to show on the page

    :return: Notifications according to the given parameter 'read'.
    :rtype: QuerySet<:class:`Notification`
    """

    if read == "read":
        return Notification.objects.filter(receiver=user, read=True).order_by("-date_created").select_subclasses()
    elif read == "unread":
        return Notification.objects.filter(receiver=user, read=False).order_by("-date_created").select_subclasses()

    return Notification.objects.filter(receiver=user).order_by("-date_created").select_subclasses()


class NotificationsView(LoginRequiredMixin, TemplateView):
    """
    View of the notifications page, which requires a logged in user.

    :var str template_name: The template name.
    """

    template_name = "notifications.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """
        Return a dictionary with the parameters of the template.

        :param dict kwargs: Context data to read from.

        :return: Template context.
        :rtype: HttpResponse
        """
        context = super(TemplateView, self).get_context_data(**kwargs)
        read = self.request.GET.get("read", "")

        notification_list = get_notifications(self.request.user, read)
        paginator = Paginator(notification_list, self.paginate_by)
        page_num = self.request.GET.get("page")

        context["read"] = read
        context["notifications"] = paginator.get_page(page_num)

        return context

    def post(self, request, *args, **kwargs):
        """
        Handle post requests by assigning a form, checking if it is valid and
        returning the rendered html.

        :param HttpRequest: Request to the server.
        :param list args: Arguments.
        :param dict kwargs: Keyword arguments from url.

        :return: rendered html.
        :rtype: HttpResponse
        """
        form = NotificationStatusForm(self.request.POST or None, auto_id=False)

        if form.is_valid():
            notification = get_object_or_404(Notification, pk=form.cleaned_data["id"])
            if notification.receiver != request.user:
                self.handle_no_permission()
            notification.is_read = not notification.is_read
            notification.save()
        else:
            Notification.objects.filter(receiver=self.request.user).update(read=True)

        context = self.get_context_data()

        return super(TemplateView, self).render_to_response(context)


class NotificationStatusForm(forms.Form):
    """
    If an id is given to this form, flip the boolean value in the database.

    :var int id: The id.
    """

    id = IntegerField()


def unread_related_ticket_notifications(ticket, user):
    """
    Mark all notifications related to the given ticket as unread.

    :param Ticket ticket: Ticket for which all related notifications are marked
                          unread.
    :param User user: User for which the notifications are marked as unread.

    :return: None.
    """
    MentionNotification.objects.filter(comment__ticket=ticket, receiver=user).update(read=True)
    TicketStatusChangedNotification.objects.filter(ticket=ticket, receiver=user).update(read=True)
    CommentNotification.objects.filter(comment__ticket=ticket, receiver=user).update(read=True)
