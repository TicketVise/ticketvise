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
        q = self.request.GET.get("q", "")
        page_number = self.request.GET.get('page', '1')

        if not page_number.isnumeric():
            page_number = 1

        labels = Label.objects.filter(inbox=inbox, name__icontains=q).order_by("name")
        page = Paginator(labels, settings.PAGE_SIZE).get_page(page_number)

        context = super(TemplateView, self).get_context_data(**kwargs)
        context['inbox'] = inbox
        context["index_start"] = (int(page_number) - 1) * settings.PAGE_SIZE + 1
        context["index_end"] = context["index_start"] - 1 + len(page)
        context["total_count"] = labels.count()
        context['labels'] = page

        return context


class EditInboxLabelView(LabelCoordinatorRequiredMixin, UpdateView):
    template_name = "inbox/label.html"
    model = Label
    fields = ["name", "color", "is_visible_to_guest", "is_active"]

    def get_success_url(self):
        return reverse("inbox_labels", args=(self.kwargs["inbox_id"],))


class CreateInboxLabelView(InboxCoordinatorRequiredMixin, CreateView):
    template_name = "inbox/label.html"
    model = Label
    fields = ["name", "color", "is_visible_to_guest", "is_active"]

    def form_valid(self, form):
        form.instance.inbox = get_object_or_404(Inbox, pk=self.kwargs["pk"])

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("inbox_labels", args=(self.kwargs["pk"],))


class DeleteInboxLabelView(LabelCoordinatorRequiredMixin, DeleteView):
    template_name = "inbox/label.html"
    model = Label

    def get_success_url(self):
        return reverse("inbox_labels", args=(self.kwargs["inbox_id"],))
