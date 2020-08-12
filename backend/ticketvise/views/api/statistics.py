from django.db.models import F, Count, Window, OuterRef, Subquery, Avg
from django.db.models.functions import TruncDate, TruncMonth, TruncYear, RowNumber, TruncHour
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, TicketStatusEvent, Status
from ticketvise.views.api.security import UserIsInboxStaffMixin
from ticketvise.views.api.ticket import LabelSerializer


class InboxTicketsPerDateTypeStatisticsApiView(UserIsInboxStaffMixin, APIView):

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        truncate = TruncDate
        date_type = request.GET.get("date_type")
        if date_type == "month":
            truncate = TruncMonth
        elif date_type == "year":
            truncate = TruncYear
        elif date_type == "hour":
            truncate = TruncHour

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

        return JsonResponse(tickets, safe=False)


class InboxAverageTimeToCloseStatisticsApiView(UserIsInboxStaffMixin, APIView):

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        first_close_event = TicketStatusEvent.objects.filter(ticket=OuterRef('pk'),
                                                             status=Status.CLOSED).order_by("-date_created")

        data = Ticket.objects.filter(inbox=inbox)\
            .annotate(first_close_event_created=Subquery(first_close_event.values("date_created")[:1]))\
            .filter(first_close_event_created__isnull=False)\
            .annotate(time_to_close=F('date_created') - F('first_close_event_created'))\
            .aggregate(avg_time_to_close=Avg("time_to_close"))

        return JsonResponse(data, safe=False)


class LabelWithCountSerializer(ModelSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Label
        fields = LabelSerializer.Meta.fields + ["count"]


class LabelsCountStatisticsApiView(UserIsInboxStaffMixin, APIView):

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)
        labels = Label.objects.filter(inbox=inbox).annotate(count=Count("tickets")).order_by("-count")

        return JsonResponse(LabelWithCountSerializer(labels, many=True).data, safe=False)