from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404

from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket


class UserIsInInboxMixin(AccessMixin):
    inbox_key = "inbox_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        inbox_id = kwargs.get(self.inbox_key)
        if not inbox_id:
            return self.handle_no_permission()

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        if not request.user.has_inbox(inbox) and not request.user.is_assistant_or_coordinator(inbox):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class UserIsInboxStaffMixin(AccessMixin):
    inbox_key = "inbox_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        inbox_id = kwargs.get(self.inbox_key)
        if not inbox_id:
            return self.handle_no_permission()

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        if not request.user.is_assistant_or_coordinator(inbox):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class UserIsInboxManagerMixin(AccessMixin):
    inbox_key = "inbox_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        inbox_id = kwargs.get(self.inbox_key)
        if not inbox_id:
            return self.handle_no_permission()

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        if not request.user.is_coordinator_for_inbox(inbox):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class UserIsTicketAuthorOrInboxStaffMixin(AccessMixin):
    inbox_key = "inbox_id"
    ticket_key = "ticket_inbox_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        inbox_id = kwargs.get(self.inbox_key)
        if not inbox_id:
            return self.handle_no_permission()

        ticket_inbox_id = kwargs.get(self.ticket_key)
        if not ticket_inbox_id:
            return self.handle_no_permission()

        ticket = get_object_or_404(Ticket, inbox_id=inbox_id, ticket_inbox_id=ticket_inbox_id)
        if not (request.user.id == ticket.author.id or request.user.is_assistant_or_coordinator(ticket.inbox)):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class UserHasAccessToTicketMixin(AccessMixin):
    inbox_key = "inbox_id"
    ticket_key = "ticket_inbox_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        inbox_id = kwargs.get(self.inbox_key)
        if not inbox_id:
            return self.handle_no_permission()

        ticket_inbox_id = kwargs.get(self.ticket_key)
        if not ticket_inbox_id:
            return self.handle_no_permission()

        ticket = get_object_or_404(Ticket, inbox_id=inbox_id, ticket_inbox_id=ticket_inbox_id)
        if not (request.user.id == ticket.author.id or request.user.is_assistant_or_coordinator(
                ticket.inbox) or ticket.shared_with.filter(pk=request.user.id).exists()):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
