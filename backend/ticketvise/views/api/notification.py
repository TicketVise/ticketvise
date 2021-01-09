from django.db.models import Q
from django.http import JsonResponse
from rest_framework.generics import ListAPIView, UpdateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from ticketvise.models.notification import Notification
from ticketvise.views.api.inbox import InboxSerializer
from ticketvise.views.api.ticket import TicketSerializer
from ticketvise.views.api.user import UserSerializer


class NotificationSerializer(ModelSerializer):
    receiver = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    ticket = TicketSerializer(read_only=True, fields=("id", "title", "name", "ticket_inbox_id", "date_created"))
    inbox = InboxSerializer(read_only=True, fields=("id", "name", "color"))

    class Meta:
        model = Notification
        fields = ["id", "receiver", "date_created", "is_read", "ticket", "author", "content", "inbox"]


class NotificationPagination(PageNumberPagination):
    page_size = 20


class NotificationsAPIView(ListAPIView):
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


class NotificationFlipRead(UpdateAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification

    def put(self, request, *args, **kwargs):
        notification = get_object_or_404(Notification, pk=self.kwargs["pk"], receiver=request.user)
        notification.is_read = not notification.is_read
        notification.save()

        return Response()


class NotificationsReadAll(UpdateAPIView):
    serializer_class = NotificationSerializer

    def put(self, request, *args, **kwargs):
        Notification.objects.filter(receiver=request.user).update(is_read=True)
        return Response()


class NotificationUnreadCountAPI(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(Notification.objects.filter(receiver=request.user, is_read=False).count(), safe=False)
