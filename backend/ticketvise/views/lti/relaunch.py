from django.views.generic import TemplateView


class LtiRelaunchView(TemplateView):
    template_name = "lti-relaunch.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url"] = self.request.GET.get("platform_redirect_url")

        return context


