from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView

from ticketvise import settings


class LtiSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "settings/lti.html"

    def get_context_data(self, **kwargs):
        if not self.request.user.is_superuser:
            raise PermissionDenied

        context = super().get_context_data(**kwargs)

        context["key"] = settings.LTI_KEY
        context["secret"] = settings.LTI_SECRET
        context["url"] = settings.LTI_XML_CONFIG_URL

        return context
