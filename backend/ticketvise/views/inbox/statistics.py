from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket, Status
from ticketvise.models.user import UserInbox, User, Role
from ticketvise.statistics import get_average_response_time
from ticketvise.views.inbox.base import InboxCoordinatorRequiredMixin


class InboxStatisticsView(InboxCoordinatorRequiredMixin, TemplateView):
    template_name = "inbox/statistics.html"

    def get_context_data(self, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs.get("pk"))

        context = super().get_context_data(**kwargs)

        context['inbox'] = inbox
        context['total_tickets'] = Ticket.objects.filter(inbox=inbox).count()
        context['total_students'] = UserInbox.objects.filter(inbox=inbox,
                                                             role=Role.GUEST).count()
        context['avg_response_time'] = get_average_response_time(inbox)

        now = datetime.now()
        last_7_days = now - timedelta(days=7)
        context['current_week_pending'] = Ticket.objects.filter(inbox=inbox, date_created__gte=last_7_days,
                                                                status=Status.PENDING).count()
        context['current_week_assigned'] = Ticket.objects.filter(inbox=inbox, date_created__gte=last_7_days,
                                                                 status=Status.ASSIGNED).count()
        context['current_week_answered'] = Ticket.objects.filter(inbox=inbox, date_created__gte=last_7_days,
                                                                 status=Status.ANSWERED).count()
        context['current_week_closed'] = Ticket.objects.filter(inbox=inbox, date_created__gte=last_7_days,
                                                               status=Status.CLOSED).count()

        last_14_days = now - timedelta(days=14)
        context['last_week_pending'] = Ticket.objects.filter(inbox=inbox, date_created__lte=last_7_days,
                                                             date_created__gte=last_14_days,
                                                             status=Status.PENDING).count()
        context['last_week_assigned'] = Ticket.objects.filter(inbox=inbox, date_created__lte=last_7_days,
                                                              date_created__gte=last_14_days,
                                                              status=Status.ASSIGNED).count()
        context['last_week_answered'] = Ticket.objects.filter(inbox=inbox, date_created__lte=last_7_days,
                                                              date_created__gte=last_14_days,
                                                              status=Status.ANSWERED).count()
        context['last_week_closed'] = Ticket.objects.filter(inbox=inbox, date_created__lte=last_7_days,
                                                            date_created__gte=last_14_days,
                                                            status=Status.CLOSED).count()

        context['pending_pct'] = calculate_increase(context['current_week_pending'], context['last_week_pending'])
        context['assigned_pct'] = calculate_increase(context['current_week_assigned'], context['last_week_assigned'])
        context['answered_pct'] = calculate_increase(context['current_week_answered'], context['last_week_answered'])
        context['closed_pct'] = calculate_increase(context['current_week_closed'], context['last_week_closed'])

        return context


def calculate_increase(current_week, last_week):
    return round(current_week / last_week, 2) * 100 if last_week else 0

# def get_average_response_time_all_ta(inbox):
#     return Ticket.objects.filter(inbox=inbox, comments__is_reply=True) \
#         .annotate(response_time=F('date_created') - F('comments__date_created')) \
#         .aggregate(avg_response_time=Avg('response_time')) \
#         .values('assignee') \
#         .orderby('response_time')
