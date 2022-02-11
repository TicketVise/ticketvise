import logging
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token

from ticketvise.models.inbox import Inbox, InboxSection, InboxUserSection
from ticketvise.models.label import Label
from ticketvise.models.user import User, UserInbox, Role
from ticketvise.security.token import token_expire_handler
from ticketvise.views.lti.validation import LtiLaunchForm


@method_decorator(csrf_exempt, name="dispatch")
class LtiView(View):
    """
    Implementation of the LTI launch. The form authenticates a user based on its data from the LMS. If the user is
    not present in the database a new one is created and will be associated with the inbox from where the launch was
    initiated from. The implementation also assigns the correct role to the user based on the inbox and LMS role.
    """

    def post(self, request):
        form = LtiLaunchForm(request.POST, request=request)

        if not form.is_valid():
            raise PermissionDenied(form.errors.items())

        user_id = form.cleaned_data["user_id"]
        first_name, last_name = form.cleaned_data["custom_user_full_name"].split(" ", 1)
        username = form.cleaned_data["custom_username"]
        email = form.cleaned_data["custom_email"]
        avatar = form.cleaned_data["custom_image_url"]
        section_ids = form.cleaned_data["custom_section_ids"]

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
        context_label = form.cleaned_data.get("context_label")
        context_id = form.cleaned_data.get("context_id")
        inbox = Inbox.objects.filter(lti_context_label=context_label, lti_context_id=context_id).first()

        if inbox is None:
            # Migrate courses without lti_context_label
            if Inbox.objects.filter(lti_context_label=context_label, lti_context_id=None).exists():
                inboxes = Inbox.objects.filter(lti_context_label=context_label)
                if inboxes.count() > 1:
                    raise Exception("Multiple courses with the same LTI context label found. Please contact your network administrator.")
                inbox = inboxes.first()

                inbox.lti_context_id = context_id
                inbox.save()
                logging.info(f"Migrated course {inbox.name} ({inbox.lti_context_label}) without lti_context_id to {inbox.lti_context_id}")
            elif "instructor" in user_roles:
                inbox_name = form.cleaned_data["custom_course_name"]
                inbox = Inbox.objects.create(lti_context_label=context_label, 
                    lti_context_id=context_id, name=inbox_name)

                # Set default labels
                Label.objects.create(inbox=inbox, color="#d73a4a", name="Assignment")
                Label.objects.create(inbox=inbox, color="#a2eeef", name="Exam")
                Label.objects.create(inbox=inbox, color="#0366d6", name="Lecture")
                Label.objects.create(inbox=inbox, color="#008672", name="Course material")
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

        for section_id in section_ids.split(','):
            section_id = section_id.strip().lower()
            section, _ = InboxSection.objects.get_or_create(code=section_id, inbox=inbox)
            InboxUserSection.objects.get_or_create(user=user, section=section)

        login(request, user)

        # Retrieving token of user, checking if not expired otherwise a create new one.
        token, _ = Token.objects.get_or_create(user=user)
        _, token = token_expire_handler(token)

        return redirect(f'/inboxes/{inbox.id}/tickets?token={token.key}')
