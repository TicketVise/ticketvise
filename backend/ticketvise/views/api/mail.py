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
from msal import PublicClientApplication

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
        app = PublicClientApplication(settings.MICROSOFT_CLIENT_ID)

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

