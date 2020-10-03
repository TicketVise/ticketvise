"""
Ticket Form View
-------------------------------
The view to create a new ticket as as student.

**Table of contents**

* :class: `TicketFormView`
"""
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from .api.security import UserIsInInboxMixin

from ticketvise.models.inbox import Inbox


class NewTicketView(UserIsInInboxMixin, TemplateView):
    """
    Form for submitting new tickets.

    :var User user: The user visiting the page.
    :var Inbox inbox: The inbox of the ticket.
    :var int inbox_id: The id of the ticket.
    :var int inbox_id: The id of the ticket.
    :var QuerySet<:class>:`Label`> labels: The labels to display.
    """
    template_name = "new_ticket.html"

    def get_context_data(self, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs.get("inbox_id"))

        context = super(TemplateView, self).get_context_data(**kwargs)
        context['inbox'] = inbox
        context["coordinator"] = Inbox.get_coordinator(context["inbox"])

        return context