from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, UpdateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from ticketvise.models.inbox import Inbox
from ticketvise.models.notification import Notification
from ticketvise.models.ticket import Ticket
from ticketvise.views.api.inbox import InboxSerializer
from ticketvise.views.api.security import UserHasAccessToTicketMixin
from ticketvise.views.api.ticket import TicketSerializer
from ticketvise.views.api.user import UserSerializer
from ticketvise.views.notifications import unread_related_ticket_notifications


class NotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    ticket = TicketSerializer(read_only=True)
    inbox = InboxSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "receiver", "date_created", "is_read", "ticket", "author", "content", "inbox"]


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


class NotificationFlipRead(LoginRequiredMixin, UpdateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification

    def put(self, request, *args, **kwargs):
        Notification.objects.filter(pk=self.kwargs["pk"]).update(is_read=Q(is_read=False))
        return Response()


class NotificationsReadAll(LoginRequiredMixin, UpdateAPIView):
    serializer_class = NotificationSerializer

    def put(self, request, *args, **kwargs):
        Notification.objects.filter(receiver=request.user).update(is_read=True)
        return Response()


class VisitTicketNotificationApi(UserHasAccessToTicketMixin, UpdateAPIView):
    serializer_class = NotificationSerializer

    def put(self, request, *args, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

        unread_related_ticket_notifications(ticket, request.user)

        return Response()


class NotificationUnreadCountAPI(LoginRequiredMixin, RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(Notification.objects.filter(receiver=request.user, is_read=False).count(), safe=False)
