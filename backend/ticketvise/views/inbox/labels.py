from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView

from ticketvise import settings
from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.views.inbox.base import LabelCoordinatorRequiredMixin, InboxCoordinatorRequiredMixin


class InboxLabelsView(InboxCoordinatorRequiredMixin, TemplateView):
    template_name = "inbox/labels.html"

    def get_context_data(self, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs.get("pk"))

        context = super(TemplateView, self).get_context_data(**kwargs)
        context['inbox'] = inbox
        context["coordinator"] = Inbox.get_coordinator(context["inbox"])

        return context


class LabelView(LabelCoordinatorRequiredMixin, TemplateView):
    template_name = "inbox/label.html"

    def get_context_data(self, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs.get("inbox_id"))

        context = super(TemplateView, self).get_context_data(**kwargs)
        context['inbox'] = inbox
        context["coordinator"] = Inbox.get_coordinator(context["inbox"])

        return context