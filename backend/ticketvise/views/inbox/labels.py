from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ticketvise.models.inbox import Inbox
from ticketvise.views.inbox.base import InboxCoordinatorRequiredMixin, LabelCoordinatorRequiredMixin


class InboxLabelsView(InboxCoordinatorRequiredMixin, TemplateView):
    template_name = "inbox/labels.html"

    def get_context_data(self, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs.get("pk"))

        context = super(TemplateView, self).get_context_data(**kwargs)
        context['inbox'] = inbox
        context["coordinator"] = Inbox.get_coordinator(context["inbox"])

        return context


class AddInboxLabelView(InboxLabelsView):
    template_name = "inbox/label.html"


class LabelView(LabelCoordinatorRequiredMixin, TemplateView):
    template_name = "inbox/label.html"

    def get_context_data(self, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs.get("inbox_id"))

        context = super(TemplateView, self).get_context_data(**kwargs)
        context['inbox'] = inbox
        context["coordinator"] = Inbox.get_coordinator(context["inbox"])

        return context
