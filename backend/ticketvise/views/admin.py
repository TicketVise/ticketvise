"""
Error
-------------------------------
Contains the view for a 404 not found page.

**Table of contents**

* :class:`ErrorHandler`
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.views.generic import TemplateView

from ticketvise.models.user import User
from ticketvise.models.inbox import Inbox


class SuperUserRequiredMixin(AccessMixin):
    """
    Mixin to verify that the user accessing the view is an admin.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_superuser:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class AdminView(SuperUserRequiredMixin, TemplateView):
    """
    Page to neatly display page not found errors.

    :var str template_name: Name of the template to render.
    """
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["inboxes"] = Inbox.objects.all()
        context["coordinators"] = {}

        for inbox in context["inboxes"]:
            context["coordinators"][inbox] = Inbox.get_coordinator(inbox)

        return context
