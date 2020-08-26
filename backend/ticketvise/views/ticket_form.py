"""
Ticket Form View
-------------------------------
The view to create a new ticket as as student.

**Table of contents**

* :class: `TicketFormView`
"""
from django.views.generic import TemplateView

from .api.security import UserIsInInboxMixin


class TicketFormView(UserIsInInboxMixin, TemplateView):
    """
    Form for submitting new tickets.

    :var User user: The user visiting the page.
    :var Inbox inbox: The inbox of the ticket.
    :var int inbox_id: The id of the ticket.
    :var int inbox_id: The id of the ticket.
    :var QuerySet<:class>:`Label`> labels: The labels to display.
    """
    template_name = "ticket_form.html"
