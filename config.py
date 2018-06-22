client_id = '88e81a62-91c4-4a4a-bce2-76b99d3578ef'
client_secret = '05fae519-d30f-4d0f-a51e-22c06485c7ab'
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
