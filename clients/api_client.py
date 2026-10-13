"""Helpers for sending authenticated and unauthenticated API requests.

This module centralizes the login flow and common HTTP calls used by the
project tests. It keeps URL construction, authentication headers, and status
verification in one place so callers can focus on their business logic.
"""

import logging

import requests

from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD

logger = logging.getLogger(__name__)


class APIClient:
    """Small HTTP client for the project API.

    The client can run in authenticated or unauthenticated mode. When
    authentication is enabled, it logs in with the configured credentials and
    stores the access token in the request headers for subsequent calls.
    """

    def __init__(self, authenticated=True, email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD):
        """Initialize the API client.

        Args:
            authenticated: Whether to authenticate the client immediately using
                the provided email and password.
            email: Email address used for authentication.
            password: Password used for authentication.
        """
        self.authenticated = authenticated
        self.email = email
        self.password = password
        self.headers = {}

        logger.debug("Initializing APIClient for email=%s authenticated=%s", email, authenticated)

        if authenticated:
            logger.info("Authenticating API client for %s", email)
            access_token = self.login(email, password)
            self.headers["Authorization"] = f"Bearer {access_token}"

    def login(self, email, password):
        """Authenticate the provided user and return the access token.

        Args:
            email: Email address for the login request.
            password: Password for the login request.

        Returns:
            The access token returned by the API.

        Raises:
            AssertionError: If the server response does not include an access
                token.
        """
        login_url = "/api/v1/auth/login"
        payload = {
            "email": email,
            "password": password,
        }

        logger.info("Logging in user %s", email)
        logger.debug("POST %s for email=%s", login_url, email)
        response_body = self.post_json(login_url, data=payload)
        assert response_body["access_token"], (
            f"Access token is required, but got {response_body['access_token']}"
        )
        logger.info("Login successful for %s", email)
        return response_body["access_token"]

    def get(self, endpoint, headers=None, expected_status_code=200):
        """Send an HTTP GET request to the given API endpoint.

        Args:
            endpoint: API path, such as "/api/v1/jobs".
            headers: Additional headers to merge into the request.
            expected_status_code: Expected HTTP status code for the response.

        Returns:
            The response object returned by ``requests.get``.
        """
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)
        logger.debug("GET %s", url)
        response = requests.get(url, headers=headers)
        self.verify_status_code(response, expected_status_code, url)
        return response

    def get_json(self, endpoint, headers=None, expected_status_code=200):
        """Send a GET request and parse the JSON response body.

        Args:
            endpoint: API path to request.
            headers: Additional headers to include in the request.
            expected_status_code: Expected HTTP status code for the response.

        Returns:
            The parsed JSON payload from the API response.
        """
        headers = self.build_headers(headers)
        response = self.get(endpoint, headers, expected_status_code)
        return response.json()

    def post(self, endpoint, data, headers=None, expected_status_code=200):
        """Send an HTTP POST request with a JSON body.

        Args:
            endpoint: API path to request.
            data: JSON payload to include in the request body.
            headers: Additional headers to merge into the request.
            expected_status_code: Expected HTTP status code for the response.

        Returns:
            The response object returned by ``requests.post``.
        """
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)
        logger.debug("POST %s", url)
        response = requests.post(url, headers=headers, json=data)
        self.verify_status_code(response, expected_status_code, url)
        return response

    def post_json(self, endpoint, data, headers=None, expected_status_code=200):
        """Send a POST request and parse the JSON response body.

        Args:
            endpoint: API path to request.
            data: JSON payload to include in the request body.
            headers: Additional headers to merge into the request.
            expected_status_code: Expected HTTP status code for the response.

        Returns:
            The parsed JSON payload from the API response.
        """
        headers = self.build_headers(headers)
        response = self.post(endpoint, data, headers=headers, expected_status_code=expected_status_code)
        return response.json()

    def put(self, endpoint, data):
        """Send a PUT request.

        Args:
            endpoint: API path to update.
            data: JSON payload to send with the request.

        Note:
            This method is still a stub and requires implementation.
        """
        # Implement PUT request logic here
        pass

    def delete(self, endpoint):
        """Send a DELETE request.

        Args:
            endpoint: API path to delete.

        Note:
            This method is still a stub and requires implementation.
        """
        # Implement DELETE request logic here
        pass

    def build_headers(self, headers=None):
        """Build request headers including the auth token when present.

        Args:
            headers: Optional extra headers to merge into the default client
                headers.

        Returns:
            A dictionary of headers ready to send with a request.
        """
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)
        return final_headers

    def verify_status_code(self, response, expected_status_code, endpoint):
        """Assert the HTTP status matches the expected status code.

        Args:
            response: HTTP response object returned by ``requests``.
            expected_status_code: Status code that should be returned.
            endpoint: Requested endpoint used in failure messages.

        Raises:
            AssertionError: If the actual status code differs from the expected
                value.
        """
        logger.debug(
            "Verifying status for %s: expected %s, actual %s",
            endpoint,
            expected_status_code,
            response.status_code,
        )
        assert response.status_code == expected_status_code, (
            f"Status code. Expected: {expected_status_code}, "
            f"Actual: {response.status_code}, URL: {endpoint}, "
            f"Response: {response.content}"
        )

    def build_url(self, endpoint):
        """Build the full URL for the provided API endpoint.

        Args:
            endpoint: API path appended to the base URL.

        Returns:
            The full URL for the request.
        """
        url = f"{BASE_URL}{endpoint}"
        logger.debug("Built URL: %s", url)
        return url
