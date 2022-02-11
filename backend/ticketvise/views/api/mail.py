import logging
import socket
from django.shortcuts import redirect
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ticketvise.models.utils import InboundMailProtocol, MailSecurity
from ticketvise.views.api.security import UserIsInboxStaffPermission
from ticketvise import settings
from ticketvise.models.inbox import Inbox
import itertools
from django.core.cache import cache

def email_username(email):
    return email.split("@")[0]

def email_domain(email):
    return email.split("@")[-1]

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

class EmailSetupApiView(APIView):
    permission_classes = [UserIsInboxStaffPermission]
    
    def post(self, request, inbox_id):
        serializer = EmailLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        email = serializer.validated_data.get("email")
        app = settings.MICROSOFT_AUTH

        redirect_uri = f"https://{request.get_host()}/api/callback"
        auth_code_request = app.initiate_auth_code_flow(settings.MICROSOFT_EMAIL_SCOPES, login_hint=email, redirect_uri=redirect_uri)
        cache.set(f"auth_code_request_{auth_code_request['state']}", auth_code_request)

        inbox.email_login_state = auth_code_request["state"]
        inbox.smtp_username = email
        inbox.inbound_email_username = email
        inbox.save()

        return Response(data=auth_code_request, status=status.HTTP_200_OK)

    def delete(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        inbox.email_enabled = False
        inbox.email_login_state = None
        inbox.email_access_token = None
        inbox.email_refresh_token = None
        inbox.smtp_server = None
        inbox.smtp_port = 587
        inbox.smtp_security = MailSecurity.TLS
        inbox.smtp_username = None
        inbox.smtp_password = None
        inbox.smtp_use_oauth2 = False
        inbox.inbound_email_protocol = InboundMailProtocol.IMAP
        inbox.inbound_email_server = None
        inbox.inbound_email_port = 993
        inbox.inbound_email_security = MailSecurity.TLS
        inbox.inbound_email_username = None
        inbox.inbound_email_password = None
        inbox.inbound_email_use_oauth2 = False
        inbox.save()

        return Response(status=status.HTTP_200_OK)

class EmailCallbackApiView(APIView):
    authenticaton_classes = []
    permission_classes = []

    def get(self, request):
        state = request.GET.get("state")
        if state == "" or state is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        inbox = get_object_or_404(Inbox, email_login_state=state)
        app = settings.MICROSOFT_AUTH

        auth_code_request = cache.get(f"auth_code_request_{state}")
        if auth_code_request is None:
            logging.error("auth_code_request for {} is None".format(state))
            return Response(status=status.HTTP_400_BAD_REQUEST)

        token_response = app.acquire_token_by_auth_code_flow(auth_code_request, request.GET.dict())
        if "error" in token_response:
            logging.error("Error in token_response: {}".format(token_response))
            return Response(status=status.HTTP_400_BAD_REQUEST)

        inbox.email_enabled = True
        inbox.email_login_state = None
        inbox.inbound_email_server = "outlook.office365.com"
        inbox.inbound_email_use_oauth2 = True
        inbox.smtp_server = "smtp.office365.com"
        inbox.smtp_use_oauth2 = True
        inbox.email_access_token = token_response["access_token"]
        inbox.email_refresh_token = token_response["refresh_token"]
        inbox.save()

        return redirect(f"/inboxes/{inbox.id}/settings")

SMTP_PORTS = [587, 465, 25]
SMTP_SUBDOMAINS = ["", "smtp.", "mail."]
IMAP_PORTS = [993, 143]
IMAP_SUBDOMAINS = ["", "imap.", "mail."]
POP3_PORTS = [995, 110]
POP_SUBDOMAINS = ["", "pop3.", "pop", "mail."]

def guess_basic_auth(email):
    domain = email_domain(email)
    smtp_options = []
    imap_options = []
    pop3_options = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Testing SMTP configuration possibilities
        for port, subdomain in itertools.product(SMTP_PORTS, SMTP_SUBDOMAINS):
            host = subdomain + domain
            logging.info(f"Testing SMTP connection: f{host}:{port}")
            if s.connect_ex((port, host)):
                smtp_options.append((port, host))

        # Testing IMAP configuration possibilities
        for port, subdomain in itertools.product(IMAP_PORTS, IMAP_SUBDOMAINS):
            host = subdomain + domain
            logging.info(f"Testing IMAP connection: f{host}:{port}")
            if s.connect_ex((port, host)):
                imap_options.append((port, host))

        # Testing POP3 configuration possibilities
        for port, subdomain in itertools.product(POP3_PORTS, POP_SUBDOMAINS):
            host = subdomain + domain
            logging.info(f"Testing POP3 connection: f{host}:{port}")
            if s.connect_ex((port, host)):
                pop3_options.append((port, host))

    return smtp_options, imap_options, pop3_options
