from ticketvise.mail.retrieve import retrieve_imap_emails
from ticketvise.mail.retrieve import retrieve_emails, submit_email_ticket
from ticketvise.models.inbox import Inbox, MailSecurity
from django.core.management.base import BaseCommand
import logging
from datetime import datetime
import webbrowser
import http.server
import socketserver
import os 
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session



class Command(BaseCommand):
    """Django command that retrieves all emails and submits them as tickets or comments."""

    AUTHORITY_URL = 'https://login.microsoftonline.com/c28f7262-f172-4000-b13a-c7923c808e64'
    AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
    TOKEN_ENDPOINT = '/oauth2/v2.0/token'

    def handle(self, *args, **options):
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

        client_id = "35bae4d4-fff1-44a3-a1aa-9ed5339f5a3d"
        client_secret = ""
        port = 8080
        redirect_uri = f'http://localhost:{port}/oauth'
        token_url = self.AUTHORITY_URL + self.TOKEN_ENDPOINT
        auth_url = self.AUTHORITY_URL + self.AUTH_ENDPOINT
        scope = ["https://outlook.office.com/IMAP.AccessAsUser.All",
                 "https://outlook.office.com/POP.AccessAsUser.All", 
                 "https://outlook.office.com/SMTP.Send",
                 "offline_access"]

        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,scope=scope)
        authorization_url, state = oauth.authorization_url(auth_url)
        print(authorization_url, state)
        webbrowser.open(authorization_url)

        protocol = "IMAP"
        host = "outlook.office365.com"
        username = "ticket@lydisnl.onmicrosoft.com"
        require_tls = True
        use_oauth2 = True

        class OAuthRedirectHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path.startswith("/oauth"):
                    token = oauth.fetch_token(token_url, client_id=client_id,
                        authorization_response=self.path, client_secret=client_secret)

                    print(token)

                    port = 993
                    password = token["access_token"]
                    emails = list(retrieve_emails(protocol, host, port, username, password, require_tls, use_oauth2))
                    print(emails)

                    self.send_response(200)
                    self.end_headers()
                    self.send_header("Content-type", "text/plain")
                    self.wfile.write("Authenticated".encode("utf-8"))
                else:
                    self.send_response(404)
                    self.end_headers()

        with socketserver.TCPServer(("", port), OAuthRedirectHandler) as httpd:
            print("Server started at localhost:" + str(port))
            httpd.handle_request()



        # password = "eyJ0eXAiOiJKV1QiLCJub25jZSI6Im1mSDNXc3V2R0xuc18tcmZtVS1rZE1DWFBLbXJ3WEl1d3Jrbl8wLTFLV1kiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyIsImtpZCI6Im5PbzNaRHJPRFhFSzFqS1doWHNsSFJfS1hFZyJ9.eyJhdWQiOiJodHRwczovL291dGxvb2sub2ZmaWNlLmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0L2MyOGY3MjYyLWYxNzItNDAwMC1iMTNhLWM3OTIzYzgwOGU2NC8iLCJpYXQiOjE2Mjk5ODcwODEsIm5iZiI6MTYyOTk4NzA4MSwiZXhwIjoxNjI5OTkwOTgxLCJhY2N0IjowLCJhY3IiOiIxIiwiYWlvIjoiQVNRQTIvOFRBQUFBZXlpaXBpZHZySUpLNkFaTzhPSE95YVZ6M3BMU1djSnBQQ2xieXV1OWNXUT0iLCJhbXIiOlsicHdkIiwicnNhIl0sImFwcF9kaXNwbGF5bmFtZSI6IlRpY2tldFZpc2UiLCJhcHBpZCI6IjM1YmFlNGQ0LWZmZjEtNDRhMy1hMWFhLTllZDUzMzlmNWEzZCIsImFwcGlkYWNyIjoiMSIsImRldmljZWlkIjoiMWQ5NGRmNDEtMGNhZC00ODhkLWI3NjctOGMwYzczNjAxMzMyIiwiZW5mcG9saWRzIjpbXSwiaXBhZGRyIjoiOTMuOTUuNS4xOTUiLCJuYW1lIjoiVGlja2V0IHwgTHlkaXMiLCJvaWQiOiIzNmFmYzMyMi1mOTdhLTQxMmMtOTBkNy04ODRjODZlNjY4YzkiLCJwdWlkIjoiMTAwMzIwMDBFMjY3MDAzOCIsInJoIjoiMC5BU0VBWW5LUHduTHhBRUN4T3NlU1BJQ09aTlRrdWpYeF82TkVvYXFlMVRPZldqMGhBSmsuIiwic2NwIjoiSU1BUC5BY2Nlc3NBc1VzZXIuQWxsIFBPUC5BY2Nlc3NBc1VzZXIuQWxsIFNNVFAuU2VuZCIsInNpZCI6ImM3NmM1YTA3LTU4MmItNDNmMy1hZmQ3LTAyNzY1ZTY5YmZkYiIsInNpZ25pbl9zdGF0ZSI6WyJkdmNfbW5nZCIsImR2Y19jbXAiLCJrbXNpIl0sInN1YiI6IjAzM3Y5bnhlaUt2LUF1MEpqUExaQnBiZ0dDYzlDVlZpdVlqdjA1V1ZqZGMiLCJ0aWQiOiJjMjhmNzI2Mi1mMTcyLTQwMDAtYjEzYS1jNzkyM2M4MDhlNjQiLCJ1bmlxdWVfbmFtZSI6InRpY2tldEBseWRpc25sLm9ubWljcm9zb2Z0LmNvbSIsInVwbiI6InRpY2tldEBseWRpc25sLm9ubWljcm9zb2Z0LmNvbSIsInV0aSI6IlZpSEtiVkM3UjBlV2VJQ1FpdXZuQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdfQ.aE86T6r4PqpWphsQUo6KCLbxspgIGaGYmZRs9Jrziebv5-jjC3Obp5ycZGvtEc56LvHAT3uCI9S2S0vgnCBMMQ23s8GbbYNlZz45EPUrV3sshOqrLzB5WpYzGPUhsyoi6mgMUSzBWvFoDT6OnvUSqiXf5cJBiS5NgwNFP5d4Ykpvtc2j0ogvnlVvtF7lqYQHb1yFKVNKWS38F8jaCwFFrgsWGZ72n4C6ZAhquA8R1P6Ym0VLN19Fj6ddmYgsX8oWvpOvvHU5GeK_ZoBlOwxT_VAX_1APuS7vC8_QR5hnqzkq64-n9pwlkAOs7tsJnh1E1MafP7IwSUbsByX2i8p7xQ"
        # emails = list(retrieve_emails(protocol, host, port, username, password, require_tls, use_oauth2))
        # print(emails)
