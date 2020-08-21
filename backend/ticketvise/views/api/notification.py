from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import JsonResponse
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from ticketvise.models.notification import Notification, CommentNotification, MentionNotification
from ticketvise.models.ticket import TicketStatusChangedNotification, Ticket
from ticketvise.views.api.comment import CommentSerializer
from ticketvise.views.api.inbox import InboxSerializer
from ticketvise.views.api.security import UserHasAccessToTicketMixin
from ticketvise.views.api.ticket import TicketSerializer
from ticketvise.views.api.user import UserSerializer


class CommentNotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    get_ticket = TicketSerializer(read_only=True)
    get_inbox = InboxSerializer(read_only=True)

    class Meta:
        model = CommentNotification
        fields = ["id", "receiver", "date_created", "read", "comment", "get_ticket", "get_author", "get_content",
                  "get_inbox"]


class MentionNotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    get_ticket = TicketSerializer(read_only=True)
    get_inbox = InboxSerializer(read_only=True)

    class Meta:
        model = MentionNotification
        fields = ["id", "receiver", "date_created", "read", "comment", "get_ticket", "get_author", "get_content",
                  "get_inbox"]


class TicketStatusChangedNotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True)
    get_ticket = TicketSerializer(read_only=True)
    old_status = models.CharField(max_length=8, choices=Ticket.Status.choices)
    get_inbox = InboxSerializer(read_only=True)

    class Meta:
        model = TicketStatusChangedNotification
        fields = ["id", "receiver", "date_created", "read", "old_status", "get_ticket", "get_author",
                  "get_content", "get_inbox"]


class NotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True)

    def to_representation(self, instance):
        if isinstance(instance, CommentNotification):
            return CommentNotificationSerializer(instance=instance).data
        elif isinstance(instance, MentionNotification):
            return MentionNotificationSerializer(instance=instance).data
        elif isinstance(instance, TicketStatusChangedNotification):
            return TicketStatusChangedNotificationSerializer(instance=instance).data

        return super().to_representation(instance)

    class Meta:
        model = Notification
        fields = "__all__"


class NotificationPagination(PageNumberPagination):
    page_size = 20


class NotificationsAPIView(LoginRequiredMixin, ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination

    def get_queryset(self):
        read = self.request.GET.get("read", "")

        notifications = Notification.objects.filter(receiver=self.request.user).select_subclasses()

        if read == "True":
            notifications = notifications.filter(read=True)
        if read == "False":
            notifications = notifications.filter(read=False)

        return notifications

    def validate_read(self, read):
        if read == "True":
            return True
        elif read == "False":
            return False
        return None


class NotificationFlipRead(LoginRequiredMixin, UpdateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification


class NotificationsReadAll(LoginRequiredMixin, UpdateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification

    def put(self, request, *args, **kwargs):
        Notification.objects.filter(receiver=self.request.user).update(read=True)
        return Response()


class VisitTicketNotificationApi(UserHasAccessToTicketMixin, UpdateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification

    def put(self, request, *args, **kwargs):
        Notification.objects.filter(receiver=self.request.user).update(read=True)
        return Response()
