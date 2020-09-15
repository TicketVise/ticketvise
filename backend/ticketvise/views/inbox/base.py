from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404

from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import UserInbox


class InboxCoordinatorRequiredMixin(AccessMixin):
    """
    Mixin to verify that the user accessing the view is the inbox coordinator.
    """
    inbox_key = "pk"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        inbox_id = kwargs.get(self.inbox_key)
        if not inbox_id:
            return self.handle_no_permission()

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        if not request.user.is_coordinator_for_inbox(inbox):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class InboxStaffRequiredMixin(AccessMixin):
    """
    Mixin to verify that the user accessing the view is staff of the inbox.
    """
    ticket_key = "pk"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        ticket_id = kwargs.get(self.ticket_key)
        if not ticket_id:
            return self.handle_no_permission()
        ticket = get_object_or_404(Ticket, pk=ticket_id)

        inbox = get_object_or_404(Inbox, pk=ticket.inbox.id)
        if not request.user.is_assistant_or_coordinator(inbox):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class LabelCoordinatorRequiredMixin(AccessMixin):
    """
    Mixin to verify that the user accessing the view is the coordinator of the inbox in which the label exists.
    """
    label_key = "pk"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        label_id = kwargs.get(self.label_key)
        if not label_id:
            return self.handle_no_permission()

        label = get_object_or_404(Label, pk=label_id)
        if not request.user.is_coordinator_for_inbox(label.inbox):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class UserCoordinatorRequiredMixin(AccessMixin):
    """
    Mixin to verify that the user accessing the view is the coordinator of the inbox in which the targeted user is
    associated with.
    """
    user_key = "pk"
    inbox_key = "inbox_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        user_id = kwargs.get(self.user_key)
        if not user_id:
            return self.handle_no_permission()

        inbox_id = kwargs.get(self.inbox_key)
        if not inbox_id:
            return self.handle_no_permission()

        user_inbox = get_object_or_404(UserInbox, user__id=user_id, inbox__id=inbox_id)
        if not request.user.is_coordinator_for_inbox(user_inbox.inbox):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
