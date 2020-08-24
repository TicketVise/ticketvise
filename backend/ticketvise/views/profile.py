"""
Profile
-------------------------------
Contains the view to view the profile of a user.

**Table of contents**

* :class:`ProfileAvatarForm`
* :class:`ProfileNotificationsForm`
* :class:`ProfileView`
"""
from pathlib import Path
from typing import Union

import django.forms as forms
from PIL import Image
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import FormView

from ticketvise import settings
from ticketvise.models.user import User


class ProfileAvatarForm(forms.ModelForm):
    """
    Form used for the avatar upload.

    :var str avatar: The path to the image
    """

    avatar = forms.ImageField()

    class Meta:
        """
        Define the model and fields.

        :var User model: The model.
        :var list fields: Field defined to the model.
        """

        model = User
        fields = []

    def save(self, commit=True):
        """
        Edit the uploaded image and save it.

        :param bool commit: Used to save the changes if save is called.

        :return: None.
        """
        im = Image.open(self.cleaned_data["avatar"])
        width, height = im.size
        largest_square = min(width, height)

        left = (width - largest_square) / 2
        top = (height - largest_square) / 2
        right = (width + largest_square) / 2
        bottom = (height + largest_square) / 2

        im = im.crop((left, top, right, bottom))
        im = im.resize((128, 128))
        im = im.convert("RGB")

        Path(settings.MEDIA_ROOT + settings.AVATAR_DIRECTORY).mkdir(parents=True, exist_ok=True)
        filename = str(self.instance.id) + ".jpeg"
        relative_path = "/" + settings.AVATAR_DIRECTORY + "/" + filename
        absolute_path = settings.MEDIA_ROOT + settings.AVATAR_DIRECTORY + "/" + filename

        im.save(absolute_path)

        self.instance.avatar_url = relative_path
        self.instance.save()

        return super().save(commit)


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
            "notification_ticket_status_change_mail",
            "notification_ticket_status_change_app",
            "notification_new_ticket_mail",
            "notification_new_ticket_app",
            "notification_comment_mail",
            "notification_comment_app",
        ]


def password_change(
        request,
        template_name="registration/password_change.html",
        post_change_redirect=None,
        password_change_form=PasswordChangeForm,
        current_app="ticketvise",
        extra_context=None,
):
    """
    Change the password of a user.

    :param HttpRequest request: The request.
    :param str template_name: The name of the file.
    :param str post_change_redirect: The redirect URL after the password change is done.
    :param Form password_change_form: The form to change the password.
    :param str current_app: The current app.
    :param Dict extra_context: Extra context.

    :return: Template response.
    :rtype: HttpResponse
    """
    if post_change_redirect is None:
        post_change_redirect = reverse("django.contrib.auth.views.password_change_done")

    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)

    context = {
        "form": form,
    }

    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context, current_app=current_app)


class ProfileView(LoginRequiredMixin, FormView):
    """
    View of the profile page, which requires a logged in user.

    :var str template_name: The template name.
    :var str success_url: The success url.
    """

    template_name = "profile/profile.html"
    success_url = "/profile"

    def dispatch(self, request, *args, **kwargs):
        if self.request.POST and self.request.POST["action"] == "delete_account":
            self.request.user.delete()
            logout(self.request)
            return HttpResponseRedirect("/")

        return super().dispatch(request, *args, **kwargs)

    def get_form(self, **kwargs) -> Union[ProfileAvatarForm, ProfileNotificationsForm, PasswordChangeForm]:
        """
        Retrieve the form and check if the form post is meant for the avatar upload,
        or the notification settings change.

        :param dict kwargs: Additional dictionary arguments.

        :return: The form to get.
        :rtype: HttpResponse
        """
        if not self.request.user.is_anonymous and self.request.method == "POST":
            action = self.request.POST["action"]

            if action == "avatar":
                return ProfileAvatarForm(**self.get_form_kwargs(), instance=self.request.user)
            elif action == "notifications":
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
