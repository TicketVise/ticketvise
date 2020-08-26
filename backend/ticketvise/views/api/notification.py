from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, UpdateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from ticketvise.models.inbox import Inbox
from ticketvise.models.notification import Notification, CommentNotification, MentionNotification
from ticketvise.models.ticket import TicketStatusChangedNotification, Ticket, Status
from ticketvise.views.api.comment import CommentSerializer
from ticketvise.views.api.inbox import InboxSerializer
from ticketvise.views.api.security import UserHasAccessToTicketMixin
from ticketvise.views.api.ticket import TicketSerializer
from ticketvise.views.api.user import UserSerializer


class CommentNotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)
    inbox = InboxSerializer(read_only=True)

    class Meta:
        model = CommentNotification
        fields = ["id", "receiver", "date_created", "is_read", "comment", "ticket", "author", "content",
                  "inbox"]


class MentionNotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)
    inbox = InboxSerializer(read_only=True)

    class Meta:
        model = MentionNotification
        fields = ["id", "receiver", "date_created", "is_read", "comment", "ticket", "author", "content",
                  "inbox"]


class TicketStatusChangedNotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True)
    ticket = TicketSerializer(read_only=True)
    old_status = models.CharField(max_length=8, choices=Status.choices)
    inbox = InboxSerializer(read_only=True)

    class Meta:
        model = TicketStatusChangedNotification
        fields = ["id", "receiver", "date_created", "is_read", "old_status", "ticket", "author",
                  "content", "inbox"]


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
        read = self.request.GET.get("is_read", "")

        notifications = Notification.objects.filter(receiver=self.request.user).select_subclasses().order_by(
            "-date_created")

        if read == "True":
            notifications = notifications.filter(is_read=True)
        if read == "False":
            notifications = notifications.filter(is_read=False)

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

    def put(self, request, *args, **kwargs):
        Notification.objects.filter(receiver=self.request.user).update(is_read=True)
        return Response()


class VisitTicketNotificationApi(UserHasAccessToTicketMixin, UpdateAPIView):
    serializer_class = NotificationSerializer

    def put(self, request, *args, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        ticket = Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

        MentionNotification.objects.filter(comment__ticket=ticket, receiver=self.request.user).update(is_read=True)
        TicketStatusChangedNotification.objects.filter(ticket=ticket, receiver=self.request.user).update(is_read=True)
        CommentNotification.objects.filter(comment__ticket=ticket, receiver=self.request.user).update(is_read=True)
        return Response()


class NotificationUnreadCountAPI(LoginRequiredMixin, RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(Notification.objects.filter(receiver=request.user, is_read=False).count(), safe=False)
