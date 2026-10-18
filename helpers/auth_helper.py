"""Helpers for authenticating users against the API under test.

This module exposes a small convenience helper for retrieving a valid JWT
access token so tests can authenticate requests without duplicating login
logic.
"""

from clients.api_client import APIClient

from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD


def login_user(email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD):
    """Log in with the provided credentials and return the access token.

    Args:
        email: Email address for the login request.
        password: Password for the login request.

    Returns:
        The JWT access token returned by the API.
    """
    login_endpoint = "/api/v1/auth/login"
    payload = {
        "email": email,
        "password": password,
    }

    api_client = APIClient()
    response_body = api_client.post_json(login_endpoint, data=payload, expected_status_code=200)

    assert response_body["access_token"], f"Access token is required, but got {response_body['access_token']}"

    return response_body["access_token"]
