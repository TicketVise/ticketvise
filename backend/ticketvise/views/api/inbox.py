from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.serializers import ModelSerializer

from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.user import User, Role
from ticketvise.views.api.security import UserIsInboxStaffMixin, UserIsInInboxMixin
from ticketvise.views.api.ticket import LabelSerializer
from ticketvise.views.api.user import UserSerializer


class InboxSerializer(ModelSerializer):
    class Meta:
        model = Inbox
        fields = ["name", "id"]


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
        return Label.objects.filter(inbox=inbox).order_by("name")
