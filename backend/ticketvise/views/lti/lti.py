import logging
import os
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token

from pylti1p3.contrib.django import DjangoOIDCLogin, DjangoMessageLaunch, DjangoCacheDataStorage
from pylti1p3.deep_link_resource import DeepLinkResource
from pylti1p3.grade import Grade
from pylti1p3.lineitem import LineItem
from pylti1p3.tool_config import ToolConfJsonFile, ToolConfDict
from pylti1p3.registration import Registration

from ticketvise import settings
from ticketvise.models.inbox import Inbox, InboxSection, InboxUserSection
from ticketvise.models.label import Label
from ticketvise.models.user import User, UserInbox, Role
from ticketvise.security.token import token_expire_handler
from ticketvise.views.lti.validation import LtiLaunchForm


class ExtendedDjangoMessageLaunch(DjangoMessageLaunch):

    def validate_nonce(self):
        """
        Probably it is bug on "https://lti-ri.imsglobal.org":
        site passes invalid "nonce" value during deep links launch.
        Because of this in case of iss == http://imsglobal.org just skip nonce validation.

        """
        iss = self.get_iss()
        deep_link_launch = self.is_deep_link_launch()
        if iss == "http://imsglobal.org" and deep_link_launch:
            return self
        return super().validate_nonce()


def get_tool_conf():
    tool_conf = ToolConfDict({
        "https://lti-ri.imsglobal.org": {
            "default": True,
            "client_id": "123456789",
            "auth_login_url": "https://lti-ri.imsglobal.org/platforms/4645/authorizations/new",
            "auth_token_url": "https://lti-ri.imsglobal.org/platforms/4645/access_tokens",
            "auth_audience": None,
            "key_set_url": "https://lti-ri.imsglobal.org/platforms/4645/platform_keys/4253.json",
            "key_set": None,
            "deployment_ids": ["1"]
        }
    })
    
    return tool_conf


def get_launch_data_storage():
    return DjangoCacheDataStorage()


def get_launch_url(request):
    target_link_uri = request.POST.get('target_link_uri', request.GET.get('target_link_uri'))
    if not target_link_uri:
        raise Exception('Missing "target_link_uri" param')
    return target_link_uri


@method_decorator(csrf_exempt, name="dispatch")
def LTILoginView(request):
    tool_conf = get_tool_conf()
    launch_data_storage = get_launch_data_storage()

    oidc_login = DjangoOIDCLogin(request, tool_conf, launch_data_storage=launch_data_storage)
    target_link_uri = get_launch_url(request)
    return oidc_login \
        .enable_check_cookies() \
        .redirect(target_link_uri)
        
        
@method_decorator(csrf_exempt, name="dispatch")
def LTILaunchView(request):
    tool_conf = get_tool_conf()
    launch_data_storage = get_launch_data_storage()
    message_launch = ExtendedDjangoMessageLaunch(request, tool_conf, launch_data_storage=launch_data_storage)
    message_launch_data = message_launch.get_launch_data()
    print(message_launch_data)
    
    return HttpResponse(message_launch_data.get('https://purl.imsglobal.org/spec/lti/claim/context', 'No name found'))


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
        
        if email == "":
            email = "test_user@ticketvise.com"

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

        if any(s.lower() in ["instructor", "administrator"] for s in user_roles):
            user_role = Role.MANAGER

        if any("teachingassistant" in s.lower() for s in user_roles):
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

        return redirect(f'/inboxes/{inbox.id}/overview?token={token.key}')
