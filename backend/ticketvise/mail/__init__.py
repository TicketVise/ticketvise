
def oauth_2_auth_base64(username, access_token):
    return f'user={username}\1auth=Bearer {access_token}\1\1'
