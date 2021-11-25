import logging
import socket
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ticketvise.views.api.security import UserIsInboxStaffPermission
from ticketvise import settings
from ticketvise.models.inbox import Inbox
import itertools
from msal import ConfidentialClientApplication

def email_username(email):
    return email.split("@")[0]

def email_domain(email):
    return email.split("@")[-1]

class EmailLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class EmailSetupApiView(APIView):
    permission_classes = [UserIsInboxStaffPermission]
    
    def post(self, request, inbox_id):
        serializer = EmailLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        app = ConfidentialClientApplication(settings.MICROSOFT_CLIENT_ID,
                                            settings.MICROSOFT_CLIENT_SECRET)

        scopes = ["https://outlook.office.com/IMAP.AccessAsUser.All",
                 "https://outlook.office.com/POP.AccessAsUser.All", 
                 "https://outlook.office.com/SMTP.Send"]

        redirect_uri = f"https://{request.get_host()}/api/callback"
        auth_code_request = app.initiate_auth_code_flow(scopes, login_hint=email, redirect_uri=redirect_uri)

        inbox.email_login_state = auth_code_request["state"]
        inbox.save()

        return Response(data=auth_code_request, status=status.HTTP_200_OK)


class EmailCallbackApiView(APIView):

    def get(self, request, code):
        state = request.GET.get("state")
        if state == "" or state is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        inbox = get_object_or_404(Inbox, state=state)
        app = ConfidentialClientApplication(settings.MICROSOFT_CLIENT_ID,
                                            settings.MICROSOFT_CLIENT_SECRET)

        auth_code = request.GET.get("code")
        token_response = app.acquire_token_by_auth_code(auth_code, redirect_uri=f"https://{request.get_host()}/api/callback")

        inbox.email_login_state = None
        inbox.email_access_token = token_response["access_token"]
        inbox.email_refresh_token = token_response["refresh_token"]
        inbox.save()

        return Response(status=status.HTTP_200_OK) 

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
        # Testing SMTP configuration possibilties
        for port, subdomain in itertools.product(SMTP_PORTS, SMTP_SUBDOMAINS):
            host = subdomain + domain
            logging.info(f"Testing SMTP connection: f{host}:{port}")
            if s.connect_ex((port, host)):
                smtp_options.append((port, host))

        # Testing IMAP configuration possibilties
        for port, subdomain in itertools.product(IMAP_PORTS, IMAP_SUBDOMAINS):
            host = subdomain + domain
            logging.info(f"Testing IMAP connection: f{host}:{port}")
            if s.connect_ex((port, host)):
                imap_options.append((port, host))

        # Testing POP3 configuration possibilties
        for port, subdomain in itertools.product(POP3_PORTS, POP_SUBDOMAINS):
            host = subdomain + domain
            logging.info(f"Testing POP3 connection: f{host}:{port}")
            if s.connect_ex((port, host)):
                pop3_options.append((port, host))

    return smtp_options, imap_options, pop3_options
