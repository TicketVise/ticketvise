from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView

from ticketvise.models.inbox import Inbox
from ticketvise.views.inbox.base import InboxCoordinatorRequiredMixin


class InboxAutomationView(InboxCoordinatorRequiredMixin, UpdateView):
    template_name = "inbox/automation.html"
    model = Inbox
    inbox_key = "pk"
    fields = ["name", "code", "color", "close_answered_weeks", "show_assignee_to_guest",
              "alert_coordinator_unanswered_days", "scheduling_algorithm", "fixed_scheduling_assignee", "image"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["inbox"] = get_object_or_404(Inbox, pk=self.kwargs["pk"])
        context["coordinator"] = Inbox.get_coordinator(context["inbox"])

        return context

    def get_success_url(self):
        return reverse("inbox_automation", args=(self.kwargs["pk"],))
