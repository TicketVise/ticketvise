from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket, Status, TicketStatusEvent
from ticketvise.models.user import UserInbox, Role
from ticketvise.statistics import get_average_response_time
from ticketvise.views.inbox.base import InboxCoordinatorRequiredMixin


class InboxStatisticsView(InboxCoordinatorRequiredMixin, TemplateView):
    template_name = "inbox/statistics.html"

    def get_context_data(self, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs.get("pk"))

        context = super().get_context_data(**kwargs)
        context['inbox'] = inbox

        return context
