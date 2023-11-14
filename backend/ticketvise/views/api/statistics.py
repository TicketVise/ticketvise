from datetime import datetime, timedelta

from django.db.models import F, Count, OuterRef, Subquery, Avg
from django.db.models.functions import TruncDate, TruncMonth, TruncYear, TruncWeek, \
    ExtractHour, ExtractWeekDay
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
from ticketvise.statistics import get_average_response_time, get_average_response_time_ta, calculate_timedelta_hours, get_most_answered_label_ta, get_amount_of_helpful_reacted_comments, get_helpfulness
from ticketvise.views.api import DynamicFieldsModelSerializer
from ticketvise.views.api.security import UserIsInboxStaffPermission
from ticketvise.views.api.ticket import LabelSerializer
from ticketvise.views.api.user import UserSerializer


class InboxTicketsPerDateTypeStatisticsApiView(APIView):
    permission_classes = [UserIsInboxStaffPermission]
    truncaters = [TruncYear, TruncMonth, TruncWeek, TruncDate]
    extracters = [ExtractHour, ExtractWeekDay]

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
        elif date_type == "week_day":
            return [
                {
                    "date": weekday,
                    "total": next((result["total"] for result in results if result["date"] == weekday), 0)
                } for weekday in range(1, 8)
            ]
        elif date_type == "date":
            if results.count() == 0:
                return []
            base = results[0]["date"]
            end = list(results)[-1]["date"]
            date_list = [base + timedelta(days=i) for i in range((end - base).days + 1)]
            return [
                {
                    "date": datetime.strftime(date, "%d-%m-%Y"),
                    "total": next((result["total"] for result in results if result["date"] == date), 0),
                    "public": next((result["public"] for result in results if result["date"] == date), 0)
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

            if base == None or end == None:
                return dict({
                    "labels": [],
                    "datasets": []
                })
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
                .annotate(**{'total': Count('date'), 'public': Count('is_public')}) \
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
            "avg_response_time": get_average_response_time(inbox),
            "avg_ticket_per_student": 0 if UserInbox.objects.filter(inbox=inbox, role=Role.GUEST).count() == 0 else Ticket.objects.filter(inbox=inbox).count() / UserInbox.objects.filter(inbox=inbox, role=Role.GUEST).count(),
            "total_guests": UserInbox.objects.filter(inbox=inbox, role=Role.GUEST).count(),
            "last_week_total_tickets": Ticket.objects.filter(inbox=inbox, date_created__lte=last_7_days).count(),
            "total_tickets": Ticket.objects.filter(inbox=inbox).count(),
            "total_open_tickets": Ticket.objects.filter(inbox=inbox, status=Status.PENDING).count(),
            "total_public_tickets": Ticket.objects.filter(inbox=inbox, is_public__isnull=False).count(),
            "labels": Label.objects.filter(inbox=inbox).count(),
            "users": User.objects.filter(inbox_relationship__inbox_id=inbox).count(),
            "coordinator": UserSerializer(inbox.get_coordinator()).data
        }, safe=False)
        
        
class StaffInboxStatisticsSerializer(DynamicFieldsModelSerializer):
    tickets_count = serializers.SerializerMethodField()
    avg_response_time = serializers.SerializerMethodField()
    most_answered_label = serializers.SerializerMethodField()
    amount_of_helpful_comments = serializers.SerializerMethodField()
    helpfulness = serializers.SerializerMethodField()
    
    def get_tickets_count(self, obj):
        return obj.tickets_count

    def get_avg_response_time(self, obj):
        return obj.avg_response_time

    def get_most_answered_label(self, obj):
        return LabelSerializer(obj.most_answered_label).data

    def get_amount_of_helpful_comments(self, obj):
        return obj.amount_of_helpful_comments

    def get_helpfulness(self, obj):
        return obj.helpfulness

    class Meta:
        model = User
        fields = ["first_name", "last_name", "avatar_url", "id", "is_active", "tickets_count", "avg_response_time", "most_answered_label", "amount_of_helpful_comments", "helpfulness"]
    
        
class StaffInboxStatisticsAPIView(APIView):
    permission_classes = [UserIsInboxStaffPermission]
    
    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)
        
        staff = inbox.get_assistants_and_coordinators()
        for user in staff:
            user.tickets_count = Ticket.objects.filter(inbox=inbox, assignee=user, comments__author=user, comments__is_reply=True).distinct().count()
            user.avg_response_time = calculate_timedelta_hours(get_average_response_time_ta(inbox, user))
            user.most_answered_label = get_most_answered_label_ta(inbox, user)
            user.amount_of_helpful_comments = get_amount_of_helpful_reacted_comments(inbox, user)
            user.helpfulness = get_helpfulness(inbox, user)
        
        return JsonResponse({
            "total_tickets": Ticket.objects.filter(inbox=inbox).count(),
            "avg_response_time": get_average_response_time(inbox),
            "avg_tickets_per_staff": 0 if UserInbox.objects.filter(inbox=inbox, role=Role.AGENT).count() == 0 else Ticket.objects.filter(inbox=inbox).count() / UserInbox.objects.filter(inbox=inbox, role=Role.AGENT).count(),
            "staff": StaffInboxStatisticsSerializer(staff, many=True).data
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
