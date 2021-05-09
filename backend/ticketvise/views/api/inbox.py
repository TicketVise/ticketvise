from django.db.models import Case, BooleanField, When, Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from ticketvise.middleware import CurrentUserMiddleware
from ticketvise.models.inbox import Inbox, SchedulingAlgorithm
from ticketvise.models.label import Label
from ticketvise.models.user import User, Role, UserInbox
from ticketvise.utils import StandardResultsSetPagination
from ticketvise.views.api import DynamicFieldsModelSerializer, LabelSerializer
from ticketvise.views.api.security import UserIsInInboxPermission, UserIsInboxStaffPermission, \
    UserIsSuperUserPermission
from ticketvise.views.api.user import UserSerializer, UserInboxSerializer


class InboxSerializer(DynamicFieldsModelSerializer):
    labels = serializers.SerializerMethodField()
    coordinator = serializers.SerializerMethodField()

    def get_labels(self, obj):
        user = CurrentUserMiddleware.get_current_user()

        labels = obj.labels.filter(is_active=True)

        if user and not user.is_assistant_or_coordinator(obj):
            labels = labels.filter(is_visible_to_guest=True)

        return LabelSerializer(labels, many=True, read_only=False).data

    def get_coordinator(self, obj):
        return UserSerializer(obj.get_coordinator()).data

    class Meta:
        model = Inbox
        fields = [
            "name", "id", "color", "labels", "image", "scheduling_algorithm", "code", "show_assignee_to_guest",
            "fixed_scheduling_assignee", "is_active", "date_created", "close_answered_weeks",
            "alert_coordinator_unanswered_days", "coordinator"
        ]


class InboxStaffApiView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [UserIsInboxStaffPermission]
    staff_roles = [Role.AGENT, Role.MANAGER]

    def get_queryset(self):
        return User.objects.filter(inbox_relationship__role__in=self.staff_roles,
                                   inbox_relationship__inbox_id=self.kwargs["inbox_id"])


class AllInboxLabelsApiView(ListAPIView):
    permission_classes = [UserIsInInboxPermission]
    serializer_class = LabelSerializer

    def get_queryset(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        user = self.request.user

        labels = Label.objects.filter(inbox=inbox, is_active=True)
        if user and not user.is_assistant_or_coordinator(inbox):
            labels = labels.filter(is_visible_to_guest=True)

        return labels.order_by("name")


class InboxLabelsApiView(ListCreateAPIView):
    serializer_class = LabelSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [UserIsInboxStaffPermission]

    def get_queryset(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        search_query = Q()
        for term in self.request.GET.get("q", "").split():
            search_query |= (Q(name__icontains=term) | Q(color__icontains=term))

        return Label.objects.filter(inbox=inbox) \
            .filter(search_query) \
            .order_by("name")

    def perform_create(self, serializer):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        serializer.save(inbox=inbox)


class InboxesApiView(ListAPIView):
    permission_classes = [UserIsSuperUserPermission]

    def get_serializer(self, *args, **kwargs):
        return InboxSerializer(*args, **kwargs, fields=(
            "name", "id", "color", "image", "scheduling_algorithm", "fixed_scheduling_assignee", "date_created"))

    def get_queryset(self):
        return Inbox.objects.all().order_by("-date_created")


class InboxUsersApiView(ListAPIView):
    serializer_class = UserInboxSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [UserIsInboxStaffPermission]

    def get_queryset(self):
        q = self.request.GET.get("q", "")

        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        users = User.objects.filter(inbox_relationship__inbox=inbox).search(q)

        inbox_users = UserInbox.objects.filter(user__in=users, inbox=inbox) \
            .annotate(sort_staff=Case(
            When(role=Role.GUEST, then=True),
            default=False,
            output_field=BooleanField())) \
            .select_related("user") \
            .order_by("sort_staff", "role", "user__first_name")

        return inbox_users


class InboxGuestsAPIView(ListAPIView):
    permission_classes = [UserIsInInboxPermission]

    def get_serializer(self, *args, **kwargs):
        return UserSerializer(*args, **kwargs, fields=(
            "first_name", "last_name", "username", "avatar_url", "id"))

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        size = self.request.GET.get("size", "")
        size = int(size) if size.isdigit() else None

        users = User.objects.filter(inbox_relationship__role=Role.GUEST,
                                    inbox_relationship__inbox_id=self.kwargs["inbox_id"]).search(q)

        return users[:size] if size and size > 0 else users


class UpdateUserInboxSerializer(ModelSerializer):
    class Meta:
        model = UserInbox
        fields = ["is_assignable"]


class UserInboxApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [UserIsInboxStaffPermission]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UpdateUserInboxSerializer

        return UserInboxSerializer

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        return get_object_or_404(UserInbox, inbox=inbox, user__id=self.kwargs["user_id"])


class InboxLabelApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = LabelSerializer
    permission_classes = [UserIsInboxStaffPermission]

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        return get_object_or_404(Label, inbox=inbox, pk=self.kwargs["label_id"])


class InboxSettingsApiView(RetrieveUpdateAPIView):
    queryset = Inbox
    permission_classes = [UserIsInboxStaffPermission]
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

    def update(self, request, *args, **kwargs):
        if "fixed_scheduling_assignee" in request.POST.keys() and not request.POST[
            "fixed_scheduling_assignee"].isdigit():
            request.POST._mutable = True
            request.POST["fixed_scheduling_assignee"] = None
        return super().update(request, *args, **kwargs)


class CurrentUserInboxSerializer(ModelSerializer):
    inbox = InboxSerializer(fields=["name", "id", "color", "labels", "image", "code", "coordinator"])
    role_label = serializers.SerializerMethodField()

    def get_role_label(self, user_inbox):
        return Role[user_inbox.role].label

    class Meta:
        model = UserInbox
        fields = ["id", "role", "role_label", "inbox", "is_bookmarked"]


class CurrentUserInboxesApiView(ListCreateAPIView):
    serializer_class = CurrentUserInboxSerializer

    def get_queryset(self):
        return UserInbox.objects.filter(user=self.request.user).order_by("-date_created")

    def post(self, request, **kwargs):
        inbox_id = request.data.get("inbox_id")
        if inbox_id:
            inbox = Inbox.objects.get(pk=inbox_id)
            if not request.user.has_inbox(inbox):
                raise ValueError(f"User is not assigned to or enrolled in inbox {inbox}")

            relation = request.user.get_entry_by_inbox(inbox)
            relation.is_bookmarked = not relation.is_bookmarked
            relation.save()

        return Response()


class CurrentUserInboxApiView(RetrieveAPIView):
    serializer_class = CurrentUserInboxSerializer
    permission_classes = [UserIsInInboxPermission]

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        if self.request.user.is_superuser:
            return UserInbox(user=self.request.user, inbox=inbox, role=Role.MANAGER)

        return get_object_or_404(UserInbox, inbox=inbox, user=self.request.user)
