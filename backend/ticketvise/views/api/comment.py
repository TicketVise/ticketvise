from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.generics import CreateAPIView
from rest_framework.serializers import ModelSerializer

from ticketvise.models.comment import Comment
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import UserInbox
from ticketvise.views.api.security import UserIsInboxStaffPermission, UserHasAccessToTicketPermission
from ticketvise.views.api.user import UserSerializer, RoleSerializer


class CommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        role = UserInbox.objects.get(user=obj.author, inbox=obj.ticket.inbox).role
        return RoleSerializer(role).data

    class Meta:
        model = Comment
        fields = ["author", "content", "id", "date_created", "role"]


class CreateCommentApiView(CreateAPIView):
    permission_classes = [UserIsInboxStaffPermission]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        inbox_id = self.kwargs["inbox_id"]
        ticket_inbox_id = self.kwargs["ticket_inbox_id"]
        ticket = get_object_or_404(Ticket, inbox_id=inbox_id, ticket_inbox_id=ticket_inbox_id)

        serializer.save(ticket=ticket, author=self.request.user, is_reply=False)


class CreateReplyApiView(CreateAPIView):
    permission_classes = [UserHasAccessToTicketPermission]
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        inbox_id = self.kwargs["inbox_id"]
        ticket_inbox_id = self.kwargs["ticket_inbox_id"]
        ticket = get_object_or_404(Ticket, inbox_id=inbox_id, ticket_inbox_id=ticket_inbox_id)

        serializer.save(ticket=ticket, author=self.request.user, is_reply=True)
