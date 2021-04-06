from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.serializers import ModelSerializer

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import UserInbox
from ticketvise.views.api import DynamicFieldsModelSerializer
from ticketvise.views.api.security import UserIsInboxStaffPermission, UserHasAccessToTicketPermission
from ticketvise.views.api.user import UserSerializer, RoleSerializer


class CommentSerializer(DynamicFieldsModelSerializer):
    author = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        role = UserInbox.objects.get(user=obj.author, inbox=obj.ticket.inbox).role
        return RoleSerializer(role).data

    class Meta:
        model = Comment
        fields = ["author", "content", "id", "date_created", "role", "is_approved"]


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
        inbox = get_object_or_404(Inbox, id=inbox_id)
        is_approved = None

        # Replies from staff are always approved
        if self.request.user.is_assistant_or_coordinator(inbox):
            is_approved = timezone.now()

        serializer.save(ticket=ticket, author=self.request.user, is_reply=True, is_approved=is_approved)


class ApproveCommentAPIView(UpdateAPIView):
    permission_classes = [UserIsInboxStaffPermission]

    def get_object(self):
        comment_id = self.kwargs["comment_id"]
        return get_object_or_404(Comment, id=comment_id)

    def get_serializer(self, *args, **kwargs):
        return CommentSerializer(fields=(["is_approved"]), *args, **kwargs)

    def update(self, request, *args, **kwargs):
        update_request = request
        update_request.data["is_approved"] = timezone.now()
        return super().update(update_request, *args, **kwargs)
