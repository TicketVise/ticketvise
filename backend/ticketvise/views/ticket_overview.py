"""
Ticket Overview
-------------------------------
Contains the view for the ticket overview page.

**Table of contents**

* :class:`TicketOverview`
"""

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ticketvise.models.inbox import Inbox
from ticketvise.views.api.security import UserIsInInboxMixin


class TicketOverview(UserIsInInboxMixin, TemplateView):
    """
    Page to show the overview of the tickets.
    """

    template_name = "ticket_overview/ticket-overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["inbox"] = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        context["coordinator"] = Inbox.get_coordinator(context["inbox"])

        return context
