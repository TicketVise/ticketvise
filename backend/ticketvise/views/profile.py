"""
Profile
-------------------------------
Contains the view to view the profile of a user.

**Table of contents**

* :class:`ProfileAvatarForm`
* :class:`ProfileNotificationsForm`
* :class:`ProfileView`
"""
from typing import Union

import django.forms as forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from ticketvise.models.user import User


class ProfileNotificationsForm(forms.ModelForm):
    """
    Form used to change the notification settings.
    """

    class Meta:
        """
        Define the model and fields.

        :var User model: The model.
        :var list fields: Fields defined to the model.
        """

        model = User
        fields = [
            "notification_mention_mail",
            "notification_mention_app",
            "notification_new_ticket_mail",
            "notification_new_ticket_app",
            "notification_comment_mail",
            "notification_comment_app",
            "notification_assigned_mail",
            "notification_assigned_app",
            "notification_ticket_reminder_mail",
            "notification_ticket_reminder_app"

        ]


class ProfileView(LoginRequiredMixin, FormView):
    """
    View of the profile page, which requires a logged in user.

    :var str template_name: The template name.
    :var str success_url: The success url.
    """

    template_name = "profile.html"
    success_url = "/profile"

    def get_form(self, **kwargs) -> Union[ProfileNotificationsForm, PasswordChangeForm]:
        """
        Retrieve the form and check if the form post is meant for the avatar upload,
        or the notification settings change.

        :param dict kwargs: Additional dictionary arguments.

        :return: The form to get.
        :rtype: HttpResponse
        """
        if not self.request.user.is_anonymous and self.request.method == "POST":
            return ProfileNotificationsForm(**self.get_form_kwargs(), instance=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Return a dictionary with the parameters of the template.

        :param dict kwargs: Additional dictionary arguments.

        :return: Context.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        context.update(forms.model_to_dict(self.request.user))

        return context

    def form_valid(self, form):
        """
        It validates the form.

        :param Form form: form to validate.

        :return: None.
        """
        if self.request.POST["action"] == "avatar" and not self.request.FILES:
            return HttpResponseRedirect("profile")

        form.save()

        return super(ProfileView, self).form_valid(form)
