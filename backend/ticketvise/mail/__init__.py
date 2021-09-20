
def oauth_2_auth_base64(username, access_token):
    return f'user={username}\1auth=Bearer {access_token}\1\1'

def create_microsoft_config(tenant, version=2):
    base_url = f'https://login.microsoftonline.com/{tenant}'
    if version == 1:
        metadata_url = base_url + '/.well-known/openid-configuration'
    elif version == 2:
        metadata_url = base_url + '/v2.0/.well-known/openid-configuration'
    else:
        raise ValueError('Invalid version value')

    return {
        'api_base_url': 'https://graph.microsoft.com/',
        'server_metadata_url': metadata_url,
        'client_kwargs': {'scope': 'openid email profile'},
    }
