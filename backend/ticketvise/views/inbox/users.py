from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Case, BooleanField, When
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView, DeleteView

from ticketvise import settings
from ticketvise.models.inbox import Inbox
from ticketvise.models.user import User, UserInbox, Role
from ticketvise.views.inbox.base import InboxCoordinatorRequiredMixin, UserCoordinatorRequiredMixin


class InboxUsersView(InboxCoordinatorRequiredMixin, TemplateView):
    template_name = "inbox/users.html"

    def get_context_data(self, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs.get("pk"))
        context = super(TemplateView, self).get_context_data(**kwargs)

        context['inbox'] = inbox

        return context


class InboxUserView(UserCoordinatorRequiredMixin, TemplateView):
    template_name = "inbox/user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inbox"] = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return context


class InboxUserDeleteView(UserCoordinatorRequiredMixin, DeleteView):
    template_name = "inbox/user.html"
    model = UserInbox

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(User, pk=self.kwargs["pk"])
        context["inbox"] = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        context["coordinator"] = Inbox.get_coordinator(context["inbox"])

        return context

    def get_object(self, queryset=None):
        return UserInbox.objects.get(user__id=self.kwargs["pk"],
                                     inbox__id=self.kwargs["inbox_id"])

    def get_success_url(self):
        return reverse("inbox_users", args=(self.kwargs["inbox_id"],))
