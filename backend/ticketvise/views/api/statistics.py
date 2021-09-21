from datetime import datetime, timedelta

from django.db.models import F, Count, OuterRef, Subquery, Avg
from django.db.models.functions import TruncDate, TruncMonth, TruncYear, TruncWeek, \
    ExtractHour
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, TicketStatusEvent, Status
from ticketvise.models.user import User, Role, UserInbox
from ticketvise.statistics import get_average_response_time
from ticketvise.views.api.security import UserIsInboxStaffPermission
from ticketvise.views.api.ticket import LabelSerializer
from ticketvise.views.api.user import UserSerializer


class InboxTicketsPerDateTypeStatisticsApiView(APIView):
    permission_classes = [UserIsInboxStaffPermission]
    truncaters = [TruncYear, TruncMonth, TruncWeek, TruncDate]
    extracters = [ExtractHour]

    def get_date_modifier(self, request):
        date_type = request.GET.get("date_type")

        for truncate in self.truncaters:
            if truncate.kind == date_type:
                return truncate

        for extract in self.extracters:
            if extract.lookup_name == date_type:
                return extract

        return TruncDate

    def fill_gaps(self, request, results):
        date_type = request.GET.get("date_type")

        if date_type == "hour":
            return [
                {
                    "date": hour,
                    "total": next((result["total"] for result in results if result["date"] == hour), 0)
                } for hour in range(24)
            ]
        elif date_type == "date":
            base = results[0]["date"]
            end = list(results)[-1]["date"]
            date_list = [base + timedelta(days=i) for i in range((end - base).days + 1)]
            return [
                {
                    "date": date,
                    "total": next((result["total"] for result in results if result["date"] == date), 0)
                } for date in date_list
            ]
        elif date_type == "labels":
            base = None
            end = None
            for label in results:
                for result in results[label]:
                    if base == None or (result["date"] - base).days < 0:
                        base = result["date"]
                    if end == None or (result["date"] - end).days > 0:
                        end = result["date"]
            date_list = [base + timedelta(days=i) for i in range((end - base).days + 1)]
            return dict({
                "labels": date_list,
                "datasets": [
                    {
                        "label": LabelSerializer(label).data,
                        "data": list(results[label])
                    } for label in results
                ]
            })

        return list(results)

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        date_modifier = self.get_date_modifier(request)

        if request.GET.get("date_type") == "labels":
            labels = Label.objects.filter(inbox=inbox)
            counts = dict()
            for label in labels:
                label_counts = Ticket.objects.filter(inbox=inbox, labels=label) \
                    .annotate(date=date_modifier('date_created')) \
                    .values('date') \
                    .annotate(**{'total': Count('date')}) \
                    .order_by("date")
                counts[label] = label_counts
        else:
            counts = Ticket.objects.filter(inbox=inbox) \
                .annotate(date=date_modifier('date_created')) \
                .values('date') \
                .annotate(**{'total': Count('date')}) \
                .order_by("date")

        results = self.fill_gaps(request, counts)

        return JsonResponse(results, safe=False)


class InboxAverageAgentResponseTimeSerializer(ModelSerializer):
    avg_response_time = serializers.DurationField(read_only=True)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ["avg_response_time"]


class InboxAverageAgentResponseTimeStatisticsApiView(APIView):
    permission_classes = [UserIsInboxStaffPermission]

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        recent_comment_ids = Comment.objects.filter(ticket__inbox=inbox, is_reply=True,
                                                    author=OuterRef(OuterRef("pk"))) \
            .order_by("ticket", "-date_created") \
            .distinct("ticket") \
            .values("id")

        avg_response_time = Comment.objects.filter(id__in=Subquery(recent_comment_ids)) \
            .annotate(response_time=F('date_created') - F('ticket__date_created')) \
            .values("author") \
            .annotate(avg_response_time=Avg("response_time"))

        roles = [Role.AGENT, Role.MANAGER]
        users = User.objects.filter(inbox_relationship__inbox=inbox, inbox_relationship__role__in=roles) \
            .annotate(avg_response_time=Subquery(avg_response_time.values("avg_response_time")))

        return JsonResponse(InboxAverageAgentResponseTimeSerializer(users, many=True).data, safe=False)


class InboxStatisticsApiView(APIView):
    permission_classes = [UserIsInboxStaffPermission]

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        now = datetime.now()
        last_7_days = now - timedelta(days=7)
        last_14_days = now - timedelta(days=14)

        return JsonResponse({
            "current_week_pending": TicketStatusEvent.objects.filter(ticket__inbox=inbox,
                                                                     date_created__gte=last_7_days,
                                                                     old_status=Status.PENDING).count(),
            "current_week_assigned": TicketStatusEvent.objects.filter(ticket__inbox=inbox,
                                                                      date_created__gte=last_7_days,
                                                                      new_status=Status.ASSIGNED).count(),
            "current_week_answered": TicketStatusEvent.objects.filter(ticket__inbox=inbox,
                                                                      date_created__gte=last_7_days,
                                                                      new_status=Status.ANSWERED).count(),
            "current_week_closed": TicketStatusEvent.objects.filter(ticket__inbox=inbox,
                                                                    date_created__gte=last_7_days,
                                                                    new_status=Status.CLOSED).count(),
            "last_week_pending": TicketStatusEvent.objects.filter(ticket__inbox=inbox,
                                                                  date_created__lte=last_7_days,
                                                                  date_created__gte=last_14_days,
                                                                  old_status=Status.PENDING).count(),
            "last_week_assigned": TicketStatusEvent.objects.filter(ticket__inbox=inbox,
                                                                   date_created__lte=last_7_days,
                                                                   date_created__gte=last_14_days,
                                                                   new_status=Status.ASSIGNED).count(),
            "last_week_answered": TicketStatusEvent.objects.filter(ticket__inbox=inbox,
                                                                   date_created__lte=last_7_days,
                                                                   date_created__gte=last_14_days,
                                                                   new_status=Status.ANSWERED).count(),
            "last_week_closed": TicketStatusEvent.objects.filter(ticket__inbox=inbox,
                                                                 date_created__lte=last_7_days,
                                                                 date_created__gte=last_14_days,
                                                                 new_status=Status.ANSWERED).count(),
            "avg_response_time": get_average_response_time(inbox),
            "total_guests": UserInbox.objects.filter(inbox=inbox, role=Role.GUEST).count(),
            "last_week_total_tickets": Ticket.objects.filter(inbox=inbox, date_created__lte=last_7_days).count(),
            'total_tickets': Ticket.objects.filter(inbox=inbox).count(),
            'labels': Label.objects.filter(inbox=inbox).count(),
            'users': User.objects.filter(inbox_relationship__inbox_id=inbox).count(),
            'coordinator': UserSerializer(inbox.get_coordinator()).data
        }, safe=False)


class InboxAverageTimeToCloseStatisticsApiView(APIView):
    permission_classes = [UserIsInboxStaffPermission]

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        first_close_event = TicketStatusEvent.objects.filter(ticket=OuterRef('pk'),
                                                             status=Status.CLOSED).order_by("-date_created")

        data = Ticket.objects.filter(inbox=inbox) \
            .annotate(first_close_event_created=Subquery(first_close_event.values("date_created")[:1])) \
            .filter(first_close_event_created__isnull=False) \
            .annotate(time_to_close=F('date_created') - F('first_close_event_created')) \
            .aggregate(avg_time_to_close=Avg("time_to_close"))

        return JsonResponse(data, safe=False)


class LabelWithCountSerializer(ModelSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Label
        fields = LabelSerializer.Meta.fields + ["count"]


class LabelsCountStatisticsApiView(APIView):
    permission_classes = [UserIsInboxStaffPermission]

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)
        labels = Label.objects.filter(inbox=inbox).annotate(count=Count("tickets")).order_by("-count")

        return JsonResponse(LabelWithCountSerializer(labels, many=True).data, safe=False)

class UserStatisticsApiView(APIView):
    def get(self, request):

        return JsonResponse({
            "inboxes": UserInbox.objects.filter(user=request.user).count(),
            "tickets": Ticket.objects.filter(author=request.user).count(),
            "public_tickets": Ticket.objects.filter(author=request.user, is_public__isnull=False).count()
        })
