import json
import os
from jwcrypto.jwk import JWK
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

from pylti1p3.contrib.django import DjangoOIDCLogin, DjangoMessageLaunch, DjangoCacheDataStorage
from pylti1p3.tool_config import ToolConfDict
from pylti1p3.roles import TeacherRole, TeachingAssistantRole

from ticketvise import settings
from ticketvise.models.inbox import Inbox, InboxSection, InboxUserSection
from ticketvise.models.label import Label
from ticketvise.models.user import User, UserInbox, Role
from ticketvise.models.lti import LTIDeployment, LTIDomain
from ticketvise.views.api.lti import LTIDomainSerializer
from ticketvise.security.token import token_expire_handler


def LTIConfigJSONView(request):
    template_name = "lti-canvas.json"

    json_path = os.path.join(settings.DATA_URL, template_name)
    with open(json_path) as f:
        data = json.load(f)
    
    return JsonResponse(data)


def LTIJWKsView(request):
    data = settings.LTI_PUBLIC_KEY.encode("ascii")
    jwk = JWK()
    jwk.import_from_pem(data)
    data = jwk.export_public(as_dict=True)
    
    return JsonResponse(data, safe=False)

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
    """When called will ask the Names and Roles Provisioning Service for the members of the course and update the users in the inbox.

    Args:
        inbox (Inbox): the context of the course
        message_launch (DjangoMessageLaunch): the launch details
    """
    if not message_launch.has_nrps():
        return

    message_launch_data = message_launch.get_launch_data()

    message_launch._registration.set_tool_public_key(settings.LTI_PUBLIC_KEY)
    message_launch._registration.set_tool_private_key(settings.LTI_PRIVATE_KEY)
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
            
            if member.get("email"):
                new_user.email = member["email"]
            if member.get("picture"):
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
        
@method_decorator(csrf_exempt, name="dispatch")
def LTILaunchView(request):
    tool_conf = get_tool_conf()
    launch_data_storage = get_launch_data_storage()
    message_launch = DjangoMessageLaunch(request, tool_conf, launch_data_storage=launch_data_storage)
    
    # Validate the launch
    if not message_launch.validate():
        return HttpResponse("Invalid launch")
    
    message_launch_data = message_launch.get_launch_data()
    
    # Check if user exists and create if not
    user = handle_lti_user(message_launch)
    
    # Future: Show admin dashboard
    # if message_launch.check_staff_access():
    #     print("Admin login")
    #     return Http404("Admin's dashboard is not implemented yet.")
    
    # Handle inbox and user role
    lti_context_id = message_launch_data["https://purl.imsglobal.org/spec/lti/claim/context"]["id"]
    deployment = LTIDeployment.objects.filter(deployment_id=message_launch_data["https://purl.imsglobal.org/spec/lti/claim/deployment_id"]).first()
    inbox = Inbox.objects.filter(lti_context_id=lti_context_id).first()
    
    if inbox is None and not message_launch.check_teacher_access():
        raise Http404("This course doesn't have an inbox (yet). Please contact your instructor.")
    
    if inbox is None and message_launch.check_teacher_access():
        inbox = Inbox.objects.create(
            lti_context_label=message_launch_data["https://purl.imsglobal.org/spec/lti/claim/context"]["label"], 
            lti_context_id=message_launch_data["https://purl.imsglobal.org/spec/lti/claim/context"]["id"],
            name=message_launch_data["https://purl.imsglobal.org/spec/lti/claim/context"]["title"],
            deployment_id=deployment)

        # Set default labels (TODO: move to setup wizard)
        Label.objects.create(inbox=inbox, color="#d73a4a", name="Assignment")
        Label.objects.create(inbox=inbox, color="#a2eeef", name="Exam")
        Label.objects.create(inbox=inbox, color="#0366d6", name="Lecture")
        Label.objects.create(inbox=inbox, color="#008672", name="Course material")
        
    # Add inboxes without deployment to the deployment (migration lti1.3)
    if inbox.deployment_id is None:
        inbox.deployment_id = deployment
        inbox.save()
    
    # Set user role
    update_user_role(user, inbox, message_launch)

    # Check if sections exist and create if not
    update_inbox_sections(user, inbox, message_launch)
    
    # Request Names and Roles Provisioning Service
    if message_launch.has_nrps() and (message_launch.check_teacher_access() or message_launch.check_teaching_assistant_access()):
        update_inbox_users(inbox, message_launch)

    # Login user
    login(request, user)

    # Retrieving token of user, checking if not expired otherwise a create new one.
    token, _ = Token.objects.get_or_create(user=user)
    _, token = token_expire_handler(token)

    return redirect(f'/inboxes/{inbox.id}/overview?token={token.key}')
