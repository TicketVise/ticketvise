"""
Account
-------------------------------
Contains the view to view the account of a user.

**Table of contents**

* :class:`AccountAvatarForm`
* :class:`AccountNotificationsForm`
* :class:`AccountView`
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AccountView(LoginRequiredMixin, TemplateView):
    """
    View of the account page, which requires a logged in user.

    :var str template_name: The template name.
    """

    template_name = "account.html"
