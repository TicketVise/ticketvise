from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket, TicketAttachment


class UserIsInInboxPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        inbox_id = view.kwargs.get("inbox_id")
        if not inbox_id:
            return False

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        return request.user.has_inbox(inbox)


class UserIsInboxStaffPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        inbox_id = view.kwargs.get("inbox_id")
        if not inbox_id:
            return False

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        return request.user.is_assistant_or_coordinator(inbox)


class UserIsInboxManagerPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        inbox_id = view.kwargs.get("inbox_id")
        if not inbox_id:
            return False

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        return request.user.is_coordinator_for_inbox(inbox)


class UserIsTicketAuthorOrInboxStaffPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        inbox_id = view.kwargs.get("inbox_id")
        if not inbox_id:
            return False

        ticket_inbox_id = view.kwargs.get("ticket_inbox_id")
        if not ticket_inbox_id:
            return False

        ticket = get_object_or_404(Ticket, inbox_id=inbox_id, ticket_inbox_id=ticket_inbox_id)
        return request.user.id == ticket.author.id or request.user.is_assistant_or_coordinator(ticket.inbox)


class UserHasAccessToTicketPermission(IsAuthenticated):
    inbox_key = "inbox_id"
    ticket_key = "ticket_inbox_id"

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        inbox_id = view.kwargs.get(self.inbox_key)
        if not inbox_id:
            return False

        ticket_inbox_id = view.kwargs.get(self.ticket_key)
        if not ticket_inbox_id:
            return False

        ticket = get_object_or_404(Ticket, inbox_id=inbox_id, ticket_inbox_id=ticket_inbox_id)
        return request.user.id == ticket.author.id \
               or request.user.is_assistant_or_coordinator(ticket.inbox) \
               or ticket.shared_with.filter(pk=request.user.id).exists()


class UserIsSuperUserPermission(IsAuthenticated):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser


class UserIsAttachmentUploaderOrInboxStaffPermission(UserHasAccessToTicketPermission):
    inbox_key = "inbox_id"
    ticket_key = "ticket_inbox_id"
    attachment_key = "pk"

    def has_permission(self, request, view):
        attachment_id = view.kwargs.get(self.attachment_key)
        attachment = get_object_or_404(TicketAttachment, pk=attachment_id)

        inbox_id = view.kwargs.get(self.inbox_key)
        if not inbox_id:
            return False

        ticket_inbox_id = view.kwargs.get(self.ticket_key)
        if not ticket_inbox_id:
            return False

        ticket = get_object_or_404(Ticket, inbox_id=inbox_id, ticket_inbox_id=ticket_inbox_id)
        return super(UserHasAccessToTicketPermission, self).has_permission(request, view) \
               and (request.user.id == attachment.uploader.id or request.user.is_assistant_or_coordinator(ticket.inbox))
