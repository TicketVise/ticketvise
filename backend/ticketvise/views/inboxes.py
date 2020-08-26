"""
Inboxs
-------------------------------
Contains the view for the inboxes overview.

**Table of contents**

* :class:`InboxesView`
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from ticketvise.models.inbox import Inbox
from ticketvise.models.user import UserInbox


class BookmarkInboxForm(ModelForm):
    class Meta:
        """
        Define the model and fields.

        :var UserInbox model: The model.
        :var list fields: Fields defined to the model.
        """

        model = UserInbox
        fields = ["is_bookmarked"]


class InboxesView(LoginRequiredMixin, TemplateView):
    """
    Display all the inboxes for a user.

    :var str template_name: The name of the template to be rendered.
    :var User user: The user visiting the page.
    :var QuerySet<:class: `Inbox`> inboxes: The inboxes to display.
    :var int num_inboxes: The total number of inboxes.
    :var int tiles_per_row: The amount of tiles in a row.
    :var int num_tiles_needed: The amount of empty tiles to get formatting nice.
    """

    template_name = "inboxes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["inboxes"] = Inbox.objects.filter(user_relationship__user=self.request.user).order_by(
            "-user_relationship__is_bookmarked")
        context['tiles_per_row'] = 3
        context['num_tiles_needed'] = context['tiles_per_row'] - context["inboxes"].count() % context['tiles_per_row']
        context['extra_tiles_list'] = list(range(context['num_tiles_needed']))

        return context

    def post(self, request):
        if request.POST["inbox_id"]:
            inbox = Inbox.objects.get(pk=request.POST["inbox_id"])
            if not request.user.has_inbox(inbox):
                raise ValueError(f"User is not assigned to or enrolled in inbox {inbox}")

            relation = request.user.get_entry_by_inbox(inbox)
            relation.is_bookmarked = not relation.is_bookmarked
            relation.save()

        return HttpResponseRedirect(reverse("inboxes"))
