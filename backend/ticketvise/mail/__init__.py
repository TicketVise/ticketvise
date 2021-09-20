import base64

def oauth_2_auth_base64(username, access_token):
    return "user=%s\1auth=Bearer %s\1\1" % (username, access_token)

