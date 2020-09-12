"""
Profile
-------------------------------
Contains the view to view the profile of a user.

**Table of contents**

* :class:`ProfileAvatarForm`
* :class:`ProfileNotificationsForm`
* :class:`ProfileView`
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView


class ProfileView(LoginRequiredMixin, FormView):
    """
    View of the profile page, which requires a logged in user.

    :var str template_name: The template name.
    """

    template_name = "profile.html"
