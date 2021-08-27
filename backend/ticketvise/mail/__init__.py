import base64

def oauth_2_auth_base64(username, access_token):
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    return base64.b64encode(auth_string.encode("ascii"))
