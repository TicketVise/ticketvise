from django.urls import reverse
from django.views.generic import UpdateView

from ticketvise.models.inbox import Inbox
from ticketvise.views.inbox.base import InboxCoordinatorRequiredMixin


class InboxSettingsView(InboxCoordinatorRequiredMixin, UpdateView):
    template_name = "inbox/settings.html"
    model = Inbox
    inbox_key = "pk"
    fields = ["name", "code", "color", "close_answered_weeks", "show_assignee_to_guest",
              "alert_coordinator_unanswered_days", "scheduling_algorithm", "image"]

    def get_success_url(self):
        return reverse("inbox_settings", args=(self.kwargs["pk"],))
