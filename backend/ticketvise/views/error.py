"""
Error
-------------------------------
Contains the view for a 404 not found page.

**Table of contents**

* :class:`ErrorHandler`
"""
from http.client import responses

from django.views.generic import TemplateView


class ErrorHandler(TemplateView):
    """
    Page to neatly display page not found errors.

    :var int error_code: The error code.
    :var str template_name: Name of the template to render.
    """

    error_code = 404
    template_name = "error.html"

    def dispatch(self, request, *args, **kwargs):
        """
        Return get on dispatch.

        :param HttpRequest request: Request to server.
        :param list args: Additional list arguments.
        :param dict kwargs: Additional keyword arguments.

        :return: GET.
        :rtype: Get
        """
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Get context data from request.

        :param dict kwargs: Additional keyword arguments.

        :return: Context.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)

        if "exception" in kwargs:
            context["error_code"] = self.error_code

        context["error_text"] = responses[context["error_code"]]

        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Return render with error code.

        :param context: Request context.
        :param response_kwargs: **kwargs.

        :return: Render.
        :rtype: HttpResponse
        """
        if context["error_code"]:
            self.error_code = context["error_code"]

        response_kwargs = response_kwargs or {}
        response_kwargs.update(status=self.error_code)

        return super().render_to_response(context, **response_kwargs)
