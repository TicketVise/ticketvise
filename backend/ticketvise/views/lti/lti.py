from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView

from ticketvise.models.inbox import Inbox
from ticketvise.models.user import User, UserInbox
from ticketvise.views.lti.validation import LtiLaunchForm


@method_decorator(csrf_exempt, name="dispatch")
class LtiView(RedirectView):
    """
    Implementation of the LTI launch. The form authenticates a user based on its data from the LMS. If the user is
    not present in the database a new one is created and will be associated with the course from where the launch was
    initiated from. The implementation also assigns the correct role to the user based on the course and LMS role.
    """

    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        """
        Handles the LTI launch request.

        :param list args: Additional list arguments.
        :param dict kwargs: Additional keyword arguments.

        :return: The url to redirect the user.
        :rtype: str or None
        """
        form = LtiLaunchForm(self.request.POST, request=self.request)

        if not form.is_valid():
            raise PermissionDenied(form.errors.items())

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
        course_code = form.cleaned_data["context_label"]
        course = Inbox.objects.filter(code=course_code).first()

        if course is None:
            if "instructor" in user_roles:
                course_name = form.cleaned_data["custom_course_name"]
                course = Inbox.objects.create(code=course_code, name=course_name)
            else:
                raise Http404("Course does not have a ticket system (yet). Please contact your instructor.")

        user_role = User.Roles.STUDENT

        if any("instructor" in s for s in user_roles):
            user_role = User.Roles.COORDINATOR

        if any("teachingassistant" in s for s in user_roles):
            user_role = User.Roles.ASSISTANT

        relation = UserInbox.objects.filter(user=user, course=course).first()

        if relation is None:
            UserInbox.objects.create(user=user, course=course, role=user_role)
        elif relation.role != user_role:
            relation.role = user_role
            relation.save()

        login(self.request, user)

        if user.has_role_in_course(course, User.Roles.STUDENT):
            return reverse("new_ticket", args=[course.id])

        return reverse("ticket_overview", args=[course.id])
