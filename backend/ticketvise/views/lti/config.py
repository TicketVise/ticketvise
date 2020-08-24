from django.views.generic import TemplateView

from ticketvise import settings


class LtiConfigView(TemplateView):
    content_type = "text/xml"
    template_name = "lti-config.xml"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host"] = settings.LTI_HOST

        return context
