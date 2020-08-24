"""
Ticket Overview
-------------------------------
Contains the view for the ticket overview page.

**Table of contents**

* :class:`TicketOverview`
"""
from typing import List

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Value as V
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User
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
