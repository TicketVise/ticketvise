from ticketvise.mail.retrieve import retrieve_emails, submit_email_ticket
from ticketvise.models.inbox import Inbox, MailSecurity
from django.core.management.base import BaseCommand
import logging
from datetime import datetime

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

class Command(BaseCommand):
    """Django command that retrieves all emails and submits them as tickets or comments."""

    AUTHORITY_URL = 'https://login.microsoftonline.com/common'
    AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
    TOKEN_ENDPOINT = '/oauth2/v2.0/token'

    def handle(self, *args, **options):
        client_id = "35bae4d4-fff1-44a3-a1aa-9ed5339f5a3d"
        client_secret = "IlFoa-oUxZ.c0_vz~dZS3._3K88.DBsO90"
        url = self.AUTHORITY_URL + self.TOKEN_ENDPOINT
        client = BackendApplicationClient(client_id=client_id)

        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=url, client_id=client_id, client_secret=client_secret)
        print(token)

