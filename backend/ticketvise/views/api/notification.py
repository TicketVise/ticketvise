from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ModelSerializer

from ticketvise.models.notification import Notification, CommentNotification, MentionNotification
from ticketvise.models.ticket import TicketStatusChangedNotification, Ticket
from ticketvise.views.api.comment import CommentSerializer
from ticketvise.views.api.inbox import InboxSerializer
from ticketvise.views.api.ticket import TicketSerializer
from ticketvise.views.api.user import UserSerializer


class CommentNotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    get_inbox = InboxSerializer(read_only=True)

    class Meta:
        model = CommentNotification
        fields = ["receiver", "date_created", "read", "comment", "get_title", "get_ticket_url", "get_author",
                  "get_content", "get_inbox"]


class MentionNotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    get_inbox = InboxSerializer(read_only=True)

    class Meta:
        model = MentionNotification
        fields = ["receiver", "date_created", "read", "comment", "get_title", "get_ticket_url", "get_author",
                  "get_content", "get_inbox"]


class TicketStatusChangedNotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)
    old_status = models.CharField(max_length=8, choices=Ticket.Status.choices)
    get_inbox = InboxSerializer(read_only=True)

    class Meta:
        model = TicketStatusChangedNotification
        fields = ["receiver", "date_created", "read", "ticket", "old_status", "get_title", "get_ticket_url",
                  "get_author", "get_content",
                  "get_inbox"]


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
        return Notification.objects.filter(receiver=self.request.user).select_subclasses()
