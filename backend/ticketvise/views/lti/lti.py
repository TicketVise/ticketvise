from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, TemplateView, FormView

from ticketvise import settings
from ticketvise.models.inbox import Inbox
from ticketvise.models.user import User, UserInbox, Role
from ticketvise.views.lti.validation import LtiLaunchForm


@method_decorator(csrf_exempt, name="dispatch")
class LtiView(FormView):
    """
    Implementation of the LTI launch. The form authenticates a user based on its data from the LMS. If the user is
    not present in the database a new one is created and will be associated with the inbox from where the launch was
    initiated from. The implementation also assigns the correct role to the user based on the inbox and LMS role.
    """
    form_class = LtiLaunchForm
    template_name = "lti.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["full_window_launch_url"] = settings.LTI_HOST + "/lti"

        return context

    def post(self, request, *args, **kwargs):
        platform_redirect_url = request.GET.get("platform_redirect_url")
        if platform_redirect_url:
            return redirect(platform_redirect_url)

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Handles the LTI launch request.

        :param list args: Additional list arguments.
        :param dict kwargs: Additional keyword arguments.

        :return: The url to redirect the user.
        :rtype: str or None
        """
        user_id = form.cleaned_data["user_id"]
        first_name, last_name = form.cleaned_data["custom_user_full_name"].split(" ", 1)
        username = form.cleaned_data["custom_username"]
        email = form.cleaned_data["custom_email"]
        avatar = form.cleaned_data["custom_image_url"]

        user = User.objects.filter(lti_id=user_id).first()

        if user is None:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                lti_id=user_id,
                avatar_url=avatar,
                password=make_password(None),
            )
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.avatar_url = avatar
            user.save()

        user_roles = [role.split("/")[-1].lower() for role in form.cleaned_data["roles"].split(",")]
        inbox_code = form.cleaned_data["context_label"]
        inbox = Inbox.objects.filter(code=inbox_code).first()

        if inbox is None:
            if "instructor" in user_roles:
                inbox_name = form.cleaned_data["custom_course_name"]
                inbox = Inbox.objects.create(code=inbox_code, name=inbox_name)
            else:
                raise Http404("Course does not have a ticket system (yet). Please contact your instructor.")

        user_role = Role.GUEST

        if any("instructor" in s for s in user_roles):
            user_role = Role.MANAGER

        if any("teachingassistant" in s for s in user_roles):
            user_role = Role.AGENT

        relation = UserInbox.objects.filter(user=user, inbox=inbox).first()

        if relation is None:
            UserInbox.objects.create(user=user, inbox=inbox, role=user_role)
        elif relation.role != user_role:
            relation.role = user_role
            relation.save()

        login(self.request, user)

        next_url = reverse("ticket_overview", args=[inbox.id])
        if user.has_role_in_inbox(inbox, Role.GUEST):
            next_url = reverse("new_ticket", args=[inbox.id])

        context = self.get_context_data()
        context["next_url"] = next_url

        return render(self.request, self.template_name, context)


