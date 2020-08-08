from django.db.models import F, Count, Window, OuterRef, Subquery, Avg
from django.db.models.functions import TruncDate, TruncMonth, TruncYear, RowNumber
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.views.api.security import UserIsInboxStaffMixin


class InboxTicketsPerDateTypeStatisticsApiView(UserIsInboxStaffMixin, APIView):

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        truncate = TruncDate
        date_type = request.GET.get("type")
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

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        first_comment = Comment.objects.filter(ticket=OuterRef('pk')).order_by("-date_created")

        tickets = Ticket.objects.filter(inbox=inbox)\
            .annotate(first_comment_created=Subquery(first_comment.values("date_created")[:1]))\
            .annotate(first_comment_author=Subquery(first_comment.values("author")[:1]))\
            .filter(first_comment_author__isnull=False)\
            .annotate(response_time=F('date_created') - F('first_comment_created'))\
            .values("first_comment_author")\
            .annotate(avg_response_time=Avg("response_time"))

        return JsonResponse(list(tickets), safe=False)


class InboxAverageTimeToCloseStatisticsApiView(UserIsInboxStaffMixin, APIView):

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        first_comment = Comment.objects.filter(ticket=OuterRef('pk')).order_by("-date_created")


        return JsonResponse(list([]), safe=False)
