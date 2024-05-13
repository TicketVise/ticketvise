import json
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
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.core.serializers.json import DjangoJSONEncoder

from pylti1p3.contrib.django import DjangoOIDCLogin, DjangoMessageLaunch, DjangoCacheDataStorage
from pylti1p3.lineitem import LineItem
from pylti1p3.tool_config import ToolConfDict
from pylti1p3.roles import TeacherRole, TeachingAssistantRole

from ticketvise import settings
from ticketvise.models.inbox import Inbox, InboxSection, InboxUserSection
from ticketvise.models.label import Label
from ticketvise.models.user import User, UserInbox, Role
from ticketvise.models.lti import LTIDomain
from ticketvise.views.api.lti import LTIDomainSerializer
from ticketvise.security.token import token_expire_handler
from ticketvise.views.lti.validation import LtiLaunchForm


def LTIConfigJSONView(request):
    template_name = "lti-canvas.json"

    json_path = os.path.join(settings.DATA_URL, template_name)
    with open(json_path) as f:
        data = json.load(f)
    
    return JsonResponse(data)


def LTIJWKsView(request):
    template_name = "jwks.json"

    json_path = os.path.join(settings.DATA_URL, template_name)
    with open(json_path) as f:
        data = json.load(f)
    
    return JsonResponse(data)

def get_tool_conf():
    tool_conf_json = {}
    for domain in LTIDomain.objects.all():
        tool_conf_json[domain.domain] = LTIDomainSerializer(domain).data['clients']
    
    return ToolConfDict(tool_conf_json)


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
        
def handle_lti_user(message_launch: DjangoMessageLaunch) -> User:
    message_launch_data = message_launch.get_launch_data()
    user = None
    user_id = message_launch_data["sub"]

    # Check for the deprecated lti1.1 user_id to migrate to lti1.3
    lti1p1_user_id = message_launch_data["https://purl.imsglobal.org/spec/lti/claim/lti1p1"]["user_id"]
    if User.objects.filter(lti_id=lti1p1_user_id).exists():
        # convert old lti1.1 user_id to new lti1.3 user_id
        user = User.objects.filter(lti_id=lti1p1_user_id).first()
        user.lti_id = user_id
        user.save()

    if not User.objects.filter(lti_id=user_id).exists():
        # Create new user
        user = User.objects.create(
            first_name=message_launch_data["given_name"],
            last_name=message_launch_data["family_name"],
            username=message_launch_data["name"],
            email=message_launch_data["email"],
            lti_id=user_id, # use new lti1.3 user_id
            password=make_password(None),
            avatar_url=message_launch_data["picture"],
        )
    else:
        # Update user data
        user = User.objects.filter(lti_id=user_id).first()
        user.first_name = message_launch_data["given_name"]
        user.last_name = message_launch_data["family_name"]
        user.email = message_launch_data["email"]
        user.avatar_url = message_launch_data["picture"]
        user.save()
        
    return user

def update_user_role(user: User, inbox: Inbox, message_launch: DjangoMessageLaunch):
    user_role = Role.GUEST
    
    if message_launch.check_teacher_access():
        user_role = Role.MANAGER
    elif message_launch.check_teaching_assistant_access():
        user_role = Role.AGENT

    relation = UserInbox.objects.filter(user=user, inbox=inbox).first()

    if relation is None:
        UserInbox.objects.create(user=user, inbox=inbox, role=user_role)
    elif relation.role != user_role:
        relation.role = user_role
        relation.save()
        
def update_inbox_sections(user: User, inbox: Inbox, message_launch: DjangoMessageLaunch):
    message_launch_data = message_launch.get_launch_data()
    section_ids = message_launch_data["https://purl.imsglobal.org/spec/lti/claim/custom"]["section_ids"]
    
    for section_id in section_ids.split(','):
        section_id = section_id.strip().lower()
        section, _ = InboxSection.objects.get_or_create(code=section_id, inbox=inbox)
        InboxUserSection.objects.get_or_create(user=user, section=section)
        
def update_inbox_users(inbox: Inbox, message_launch: DjangoMessageLaunch):
    if not message_launch.has_nrps():
        return

    message_launch_data = message_launch.get_launch_data()

    message_launch._registration.set_tool_public_key(public_key)
    message_launch._registration.set_tool_private_key(private_key)
    nrps = message_launch.get_nrps()
    members = nrps.get_members()
    
    for member in members:
        new_user = None
        user_id = message_launch_data["sub"]

        # Check for the deprecated lti1.1 user_id to migrate to lti1.3
        lti1p1_user_id = member["lti11_legacy_user_id"]
        if User.objects.filter(lti_id=lti1p1_user_id).exists():
            # convert old lti1.1 user_id to new lti1.3 user_id
            lti1p1_member = User.objects.filter(lti_id=lti1p1_user_id).first()
            lti1p1_member.lti_id = user_id
            lti1p1_member.save()

        if not User.objects.filter(lti_id=user_id).exists():
            # Create new user
            new_user = User.objects.create(
                first_name=member["given_name"],
                last_name=member["family_name"],
                username=member["name"],
                email=member["email"],
                lti_id=user_id, # use new lti1.3 user_id
                password=make_password(None),
                avatar_url=member["picture"],
            )
        else:
            # Update user data
            new_user = User.objects.filter(lti_id=user_id).first()
            new_user.first_name = member["given_name"]
            new_user.last_name = member["family_name"]
            new_user.email = member["email"]
            new_user.avatar_url = member["picture"]
            new_user.save()
            
        jwt_body = {}
        jwt_body["https://purl.imsglobal.org/spec/lti/claim/roles"] = member["roles"]

        user_role = Role.GUEST
        if TeacherRole(jwt_body).check():
            user_role = Role.MANAGER
        elif TeachingAssistantRole(jwt_body).check():
            user_role = Role.AGENT

        relation = UserInbox.objects.filter(user=new_user, inbox=inbox).first()

        if relation is None:
            UserInbox.objects.create(user=new_user, inbox=inbox, role=user_role)
        elif relation.role != user_role:
            relation.role = user_role
            relation.save()
        
public_key = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAwfiSy8Rx3Pw2y+7l1y5F
InGh5RUoELueVfCgmGo36DmqGspjWKsyaEu7GOki1Z6g8oaGtjRCHIacx8NqM4l4
LYRUuOA4NnTD2gAJDQBR0wG36/T8yD8bQy3Qkck4+h031nElicDfnHfWXV0Pp916
Ms0zyO3u7I/vwpJheR5wiwsthqMisEOSetqyOx4Y6lVg5KLc8zc5Gp/Wv/hIwwOj
CCPyTjZnwLjEkS7SMJhllYPJ7Kd9x48dhAic/cCwK49IUAKdVlGhyi3twn/xdYGB
Vfh8YTAbu2LFu3EBjJ3seco4Cv4oD1FX2FlxF9/mqiDgrllHFO30KiYoXnloi7St
h/zT9b2sbB3XRQ5UcZ982bvYffS22UjWJ/gnw40m1J5bVJrhBN+eUG64WSbw8mq5
EvgEOsb2Kgu50eZWzjEhQUD4b1NMYxMKXd6aRgjs7mS7x1q11M87T1FfAAyn07MR
Axbs4tfwAwb9xd0uCLfnFWlX9RiMygZMNRQttj8GZM6zkwKz4mdVgmWUS16snvog
qxWje0i2PWRvAwEZ7tFkbXngS04/Je9mW0iRT2Vbtzgcpb56luvWlCqd/GKDds4B
rGnRWAMWc8yulrbMEXYAbixlnqgYs/y+bbpKMz8K20Rl6GFba23IpkjMNUdGlOKL
APEBSOvPmjGsHoJChZ2gLOsCAwEAAQ==
-----END PUBLIC KEY-----"""
private_key = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""
        
@method_decorator(csrf_exempt, name="dispatch")
def LTILaunchView(request):
    tool_conf = get_tool_conf()
    launch_data_storage = get_launch_data_storage()
    message_launch = DjangoMessageLaunch(request, tool_conf, launch_data_storage=launch_data_storage)
    message_launch_data = message_launch.get_launch_data()
    
    # Validate the launch
    if not message_launch.validate():
        return HttpResponse("Invalid launch")
    
    # Check if user exists and create if not
    user = handle_lti_user(message_launch)
    
    # Future: Show admin dashboard
    # if message_launch.check_staff_access():
    #     print("Admin login")
    #     return Http404("Admin's dashboard is not implemented yet.")
    
    # Handle inbox and user role
    lti_context_id = message_launch_data["https://purl.imsglobal.org/spec/lti/claim/context"]["id"]
    inbox = Inbox.objects.filter(lti_context_id=lti_context_id).first()
    
    if inbox is None and not message_launch.check_teacher_access():
        raise Http404("This course doesn't have an inbox (yet). Please contact your instructor.")
    
    if inbox is None and message_launch.check_teacher_access():
        print("Creating new inbox")
        inbox = Inbox.objects.create(
            lti_context_label=message_launch_data["https://purl.imsglobal.org/spec/lti/claim/context"]["label"], 
            lti_context_id=message_launch_data["https://purl.imsglobal.org/spec/lti/claim/context"]["id"],
            name=message_launch_data["https://purl.imsglobal.org/spec/lti/claim/context"]["title"])

        # Set default labels (TODO: move to setup wizard)
        Label.objects.create(inbox=inbox, color="#d73a4a", name="Assignment")
        Label.objects.create(inbox=inbox, color="#a2eeef", name="Exam")
        Label.objects.create(inbox=inbox, color="#0366d6", name="Lecture")
        Label.objects.create(inbox=inbox, color="#008672", name="Course material")
    
    # Set user role
    update_user_role(user, inbox, message_launch)

    # Check if sections exist and create if not
    update_inbox_sections(user, inbox, message_launch)
    
    # Request Names and Roles Provisioning Service
    update_inbox_users(inbox, message_launch)

    # Login user
    login(request, user)

    # Retrieving token of user, checking if not expired otherwise a create new one.
    token, _ = Token.objects.get_or_create(user=user)
    _, token = token_expire_handler(token)

    return redirect(f'/inboxes/{inbox.id}/overview?token={token.key}')
