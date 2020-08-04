"""
Error
-------------------------------
Contains the view for a 404 not found page.

**Table of contents**

* :class:`ErrorHandler`
"""
from http.client import responses

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HomeView(LoginRequiredMixin, TemplateView):
    """
    Page to neatly display page not found errors.

    :var int error_code: The error code.
    :var str template_name: Name of the template to render.
    """
    template_name = "inboxs.html"