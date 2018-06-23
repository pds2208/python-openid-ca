client_id = '77d9c32d-3a02-4cb4-8c69-33946505d553'
client_secret = 'f9feada3-973f-43c1-9737-70636d576130'
discovery_endpoint = 'https://localhost:8443/.well-known/openid-configuration'

# set the environment CURL_CA_BUNDLE=
# to ignore certificate errors

OAUTH_CREDENTIALS = {
    'CA': {
        'id': client_id,
        'secret': client_secret,
        'discovery_endpoint': discovery_endpoint
    }
}
