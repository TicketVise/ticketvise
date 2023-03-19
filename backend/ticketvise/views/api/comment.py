from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from ticketvise.models.user import User
from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.views.api import CommentSerializer
from ticketvise.views.api.security import UserIsInboxStaffPermission, UserHasAccessToTicketPermission


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


class SplitCommentApiView(DestroyAPIView):
    permission_classes = [UserIsInboxStaffPermission]

    def get_object(self):
        comment_id = self.kwargs["comment_id"]
        return get_object_or_404(Comment, id=comment_id)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        # delete existing comment and create a new ticket with the same content
        inbox_id = self.kwargs["inbox_id"]
        author_id = self.request.data['author']['id']
        author = get_object_or_404(User, id=author_id)
        assignee_id = self.request.data['assignee']['id'] if self.request.data['assignee'] else None
        assignee = None
        if assignee_id:
            assignee = get_object_or_404(User, id=assignee_id)
        
        # Create new ticket with the same content
        new_ticket = Ticket.objects.create(
            title=self.request.data['title'],
            content=self.request.data['content'],
            author=author,
            inbox_id=inbox_id,
            assignee=assignee
        )
        
        # Get the id's from the labels and set them to the new ticket
        new_ticket.labels.set(list(map(lambda x: x['id'], list(self.request.data['labels']))))
        new_ticket.save()

        # Delete comment because we don't need that anymore
        super().perform_destroy(self.get_object())
        
        # Return the new ticket id with status 201
        return Response(status=status.HTTP_201_CREATED, data={"ticket_id": new_ticket.ticket_inbox_id})
