import requests

from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD


def login_user(email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD):
    # get JWT token: login with user and get the token from the response
    # Make the call
    login_url = f"{BASE_URL}/api/v1/auth/login"
    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(login_url, json=payload)

    # verify status code 200
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # verify response body has access token
    response_body = response.json()
    assert response_body["access_token"], f"Access token is required, but got {response_body['access_token']}"

    return response_body["access_token"]