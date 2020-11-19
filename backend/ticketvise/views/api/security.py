from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket


class UserIsInInboxPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        inbox_id = view.kwargs.get("inbox_id")
        if not inbox_id:
            return False

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        if not request.user.has_inbox(inbox) and not request.user.is_assistant_or_coordinator(inbox):
            return False

        return True


class UserIsInboxStaffPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        inbox_id = view.kwargs.get("inbox_id")
        if not inbox_id:
            return False

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        if not request.user.is_assistant_or_coordinator(inbox):
            return False

        return True


class UserIsInboxManagerPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        inbox_id = view.kwargs.get("inbox_id")
        if not inbox_id:
            return False

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        if not request.user.is_coordinator_for_inbox(inbox):
            return False

        return True


class UserIsTicketAuthorOrInboxStaffPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        inbox_id = view.kwargs.get("inbox_id")
        if not inbox_id:
            return False

        ticket_inbox_id = view.kwargs.get("ticket_inbox_id")
        if not ticket_inbox_id:
            return False

        ticket = get_object_or_404(Ticket, inbox_id=inbox_id, ticket_inbox_id=ticket_inbox_id)
        if not (request.user.id == ticket.author.id or request.user.is_assistant_or_coordinator(ticket.inbox)):
            return False

        return True


class UserHasAccessToTicketMixin(IsAuthenticated):
    inbox_key = "inbox_id"
    ticket_key = "ticket_inbox_id"

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        inbox_id = view.kwargs.get(self.inbox_key)
        if not inbox_id:
            return False

        ticket_inbox_id = view.kwargs.get(self.ticket_key)
        if not ticket_inbox_id:
            return False

        ticket = get_object_or_404(Ticket, inbox_id=inbox_id, ticket_inbox_id=ticket_inbox_id)
        if not (request.user.id == ticket.author.id or request.user.is_assistant_or_coordinator(
                ticket.inbox) or ticket.shared_with.filter(pk=request.user.id).exists()):
            return False

        return True


class UserIsSuperUserPermission(IsAuthenticated):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not request.user.is_superuser:
            return False

        return True
