
import base64

def oauth_2_auth_base64(username, access_token):
    auth_string = f"user={username}\1auth=Bearer {access_token}\1\1"
    return base64.b64encode(auth_string)