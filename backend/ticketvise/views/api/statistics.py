from django.db.models import F, Avg, Count
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.views.api.security import UserIsInboxStaffMixin


class InboxTicketsPerDateTypeStatisticsApiView(UserIsInboxStaffMixin, APIView):

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        truncate = TruncDate
        date_type = request.GET["type"]
        if date_type == "month":
            truncate = TruncMonth
        elif date_type == "year":
            truncate = TruncYear

        counts = Ticket.objects.filter(inbox=inbox) \
            .annotate(date=truncate('date_created')) \
            .values('date') \
            .annotate(**{'total': Count('date')}) \
            .order_by('date')

        return JsonResponse(list(counts), safe=False)


class InboxAverageAgentResponseTimeStatisticsApiView(UserIsInboxStaffMixin, APIView):

    def get(self, request, format=None):
        inbox = get_object_or_404(Inbox, pk=self.kwargs.get("inbox_id"))

        avg_response_times = Ticket.objects.filter(inbox=inbox, comments__is_reply=True) \
            .annotate(response_time=F('date_created') - F('comments__date_created')) \
            .aggregate(avg_response_time=Avg('response_time')) \
            .values('assignee') \
            .orderby('response_time')

        return JsonResponse(avg_response_times)
