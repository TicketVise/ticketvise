from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.serializers import ModelSerializer

from ticketvise.middleware import CurrentUserMiddleware
from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.user import User, Role
from ticketvise.views.api.security import UserIsInboxStaffMixin, UserIsInInboxMixin
from ticketvise.views.api.ticket import LabelSerializer
from ticketvise.views.api.user import UserSerializer


class InboxSerializer(ModelSerializer):
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
            "name", "id", "color", "labels", "image", "scheduling_algorithm", 
            "is_active", "date_created"
        ]


class InboxStaffApiView(UserIsInboxStaffMixin, ListAPIView):
    serializer_class = UserSerializer
    staff_roles = [Role.AGENT, Role.MANAGER]

    def get_queryset(self):
        return User.objects.filter(inbox_relationship__role__in=self.staff_roles,
                                   inbox_relationship__inbox_id=self.kwargs[self.inbox_key])


class InboxLabelsApiView(UserIsInInboxMixin, ListAPIView):
    serializer_class = LabelSerializer

    def get_queryset(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs[self.inbox_key])
        user = CurrentUserMiddleware.get_current_user()

        labels = Label.objects.filter(inbox=inbox, is_active=True).order_by("name")
        if user and not user.is_assistant_or_coordinator(inbox):
            labels = labels.filter(is_visible_to_guest=True)

        return labels


class InboxApiView(UserIsInInboxMixin, RetrieveAPIView):
    serializer_class = InboxSerializer
    queryset = Inbox
    lookup_url_kwarg = "inbox_id"


class InboxesApiView(ListAPIView):
    serializer_class = InboxSerializer
    
    def get_queryset(self):
        return Inbox.objects.all()
