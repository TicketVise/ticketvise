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

        return context


class EditInboxLabelView(LabelCoordinatorRequiredMixin, UpdateView):
    template_name = "inbox/label.html"
    model = Label
    fields = ["name", "color", "is_visible_to_guest", "is_active"]

    def get_success_url(self):
        return reverse("inbox_labels", args=(self.kwargs["inbox_id"],))

    def get_context_data(self, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs.get("inbox_id"))

        context = super(UpdateView, self).get_context_data(**kwargs)
        context['inbox'] = inbox
        context["coordinator"] = Inbox.get_coordinator(context["inbox"])

        return context


class CreateInboxLabelView(InboxCoordinatorRequiredMixin, CreateView):
    template_name = "inbox/label.html"
    model = Label
    fields = ["name", "color", "is_visible_to_guest", "is_active"]

    def form_valid(self, form):
        form.instance.inbox = get_object_or_404(Inbox, pk=self.kwargs["pk"])

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("inbox_labels", args=(self.kwargs["pk"],))

    def get_context_data(self, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs.get("pk"))

        context = super(CreateView, self).get_context_data(**kwargs)
        context['inbox'] = inbox
        context["coordinator"] = Inbox.get_coordinator(context["inbox"])

        return context
