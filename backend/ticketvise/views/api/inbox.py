from django.db.models import Case, BooleanField, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from ticketvise.middleware import CurrentUserMiddleware
from ticketvise.models.inbox import Inbox, SchedulingAlgorithm
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, Role, UserInbox
from ticketvise.utils import StandardResultsSetPagination
from ticketvise.views.api import DynamicFieldsModelSerializer
from ticketvise.views.api.labels import LabelSerializer
from ticketvise.views.api.security import UserIsInboxStaffMixin, UserIsInInboxMixin, UserIsSuperUserMixin, \
    UserIsInboxManagerMixin
from ticketvise.views.api.user import UserSerializer, UserInboxSerializer


class InboxSerializer(DynamicFieldsModelSerializer):
    labels = serializers.SerializerMethodField()

    def get_labels(self, obj):
        user = CurrentUserMiddleware.get_current_user()
        labels = obj.labels.filter(is_active=True)

        if user and not user.is_assistant_or_coordinator(obj):
            labels = labels.filter(is_visible_to_guest=True)

        return LabelSerializer(labels, many=True, read_only=False).data

    class Meta:
        model = Inbox
        fields = [
            "name", "id", "color", "labels", "image", "scheduling_algorithm", "code", "show_assignee_to_guest",
            "fixed_scheduling_assignee", "is_active", "date_created", "close_answered_weeks",
            "alert_coordinator_unanswered_days"
        ]


class InboxLabelsApiView(UserIsInInboxMixin, ListAPIView):
    serializer_class = LabelSerializer

    def get_queryset(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs[self.inbox_key])
        user = CurrentUserMiddleware.get_current_user()

        labels = Label.objects.filter(inbox=inbox, is_active=True).order_by("name")
        if user and not user.is_assistant_or_coordinator(inbox):
            labels = labels.filter(is_visible_to_guest=True)

        return labels


class CoordinatorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class InboxStatsApiView(UserIsSuperUserMixin, APIView):
    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        return JsonResponse({
            'labels': Label.objects.filter(inbox=inbox).count(),
            'tickets': Ticket.objects.filter(inbox=inbox).count(),
            'users': User.objects.filter(inbox_relationship__inbox_id=inbox).count(),
            'coordinator': CoordinatorSerializer(inbox.get_coordinator()).data
        }, safe=False)


class InboxesApiView(ListAPIView):
    def get_serializer(self, *args, **kwargs):
        return InboxSerializer(*args, **kwargs, fields=(
            "name", "id", "color", "image", "scheduling_algorithm", "fixed_scheduling_assignee", "date_created"))

    def get_queryset(self):
        return Inbox.objects.all().order_by("-date_created")


class InboxUsersApiView(UserIsInboxStaffMixin, ListAPIView):
    serializer_class = UserInboxSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        q = self.request.GET.get("q", "")

        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        users = User.objects.filter(inbox_relationship__inbox=inbox).search(q)

        inbox_users = UserInbox.objects.filter(user__in=users) \
            .annotate(sort_staff=Case(
            When(role=Role.GUEST, then=True),
            default=False,
            output_field=BooleanField())) \
            .select_related("user") \
            .order_by("sort_staff", "role", "user__first_name")

        return inbox_users


class InboxGuestsAPIView(UserIsInInboxMixin, ListAPIView):
    def get_serializer(self, *args, **kwargs):
        return UserSerializer(*args, **kwargs, fields=(
            "first_name", "last_name", "email", "username", "avatar_url", "id", "is_active"))

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        size = self.request.GET.get("size", "")
        size = int(size) if size.isdigit() else None

        users = User.objects.filter(inbox_relationship__role=Role.GUEST,
                                    inbox_relationship__inbox_id=self.kwargs[self.inbox_key]).search(q)

        return users[:size] if size and size > 0 else users


class UpdateUserInboxSerializer(ModelSerializer):
    class Meta:
        model = UserInbox
        fields = ["role"]


class UserInboxApiView(UserIsInboxManagerMixin, RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UpdateUserInboxSerializer

        return UserInboxSerializer

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        return get_object_or_404(UserInbox, inbox=inbox, user__id=self.kwargs["user_id"])


class InboxSettingsApiView(UserIsInboxManagerMixin, RetrieveUpdateAPIView):
    queryset = Inbox
    lookup_url_kwarg = "inbox_id"

    def get_serializer(self, *args, **kwargs):
        return InboxSerializer(*args, **kwargs, fields=(
            "name", "id", "color", "image", "scheduling_algorithm", "code", "show_assignee_to_guest",
            "fixed_scheduling_assignee", "close_answered_weeks", "alert_coordinator_unanswered_days"))

    def retrieve(self, request, *args, **kwargs):
        inbox = self.get_object()

        response = {
            "inbox": self.get_serializer(inbox).data,
            "scheduling_options": SchedulingAlgorithm.choices,
            "staff": UserSerializer(inbox.get_assistants_and_coordinators(), many=True).data
        }

        return Response(response)
