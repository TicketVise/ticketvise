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

        if not self.request.user.is_coordinator_for_inbox(inbox) and not self.request.user.is_superuser:
            raise PermissionDenied()

        q = self.request.GET.get("q", "")
        page_number = self.request.GET.get('page', '1')

        if not page_number.isnumeric():
            page_number = 1

        inbox_users = UserInbox.objects

        for term in q.split():
            inbox_users = (UserInbox.objects.filter(inbox=inbox, user__username__icontains=term)
                           | UserInbox.objects.filter(inbox=inbox, user__first_name__icontains=term)
                           | UserInbox.objects.filter(inbox=inbox, user__last_name__icontains=term)
                           | UserInbox.objects.filter(inbox=inbox, user__email__contains=term))

        inbox_users = inbox_users.annotate(sort_staff=Case(
            When(role=Role.GUEST, then=True),
            default=False,
            output_field=BooleanField()
        )) \
            .select_related("user") \
            .order_by("sort_staff", "role", "user__first_name")

        context = super(TemplateView, self).get_context_data(**kwargs)

        page = Paginator(inbox_users, settings.PAGE_SIZE).get_page(page_number)

        context['inbox'] = inbox
        context["index_start"] = (int(page_number) - 1) * settings.PAGE_SIZE + 1
        context["index_end"] = context["index_start"] - 1 + len(page)
        context["total_count"] = inbox_users.count()
        context['inbox_users'] = page

        return context


class InboxUserView(UserCoordinatorRequiredMixin, UpdateView):
    template_name = "inbox/user.html"
    model = UserInbox
    fields = ["role"]

    def get_object(self, queryset=None):
        return UserInbox.objects.get(user__id=self.kwargs.get("pk"),
                                     inbox_id=self.kwargs.get("inbox_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(User, pk=self.kwargs["pk"])
        context["inbox"] = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return context

    def get_success_url(self):
        return reverse("inbox_users", args=(self.kwargs["inbox_id"],))


class InboxUserDeleteView(UserCoordinatorRequiredMixin, DeleteView):
    template_name = "inbox/user.html"
    model = UserInbox

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(User, pk=self.kwargs["pk"])
        context["inbox"] = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return context

    def get_object(self, queryset=None):
        return UserInbox.objects.get(user__id=self.kwargs["pk"],
                                     inbox__id=self.kwargs["inbox_id"])

    def get_success_url(self):
        return reverse("inbox_users", args=(self.kwargs["inbox_id"],))
