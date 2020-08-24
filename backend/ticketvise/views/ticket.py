"""
Ticket page
-------------------------------
Contains the view to view of the information of a ticket.

**Table of contents**

* :class:`TicketView`
"""
from django.views.generic import TemplateView

from .api.security import UserHasAccessToTicketMixin


class TicketView(UserHasAccessToTicketMixin, TemplateView):
    """
    Page to show information of a ticket.
    """

    template_name = "ticket/ticket.html"
