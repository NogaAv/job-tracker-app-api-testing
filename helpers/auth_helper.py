from clients.api_client import APIClient

from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD


def login_user(email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD):
    # get JWT token: login with user and get the token from the response
    # Make the call
    login_endpoint = f"/api/v1/auth/login"
    payload = {
        "email": email,
        "password": password
    }

    api_client = APIClient()
    response_body = api_client.post_json(login_endpoint, data=payload)

    # verify response body has access token
    assert response_body["access_token"], f"Access token is required, but got {response_body['access_token']}"

    return response_body["access_token"]