import requests

from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD


# APIClient class for making API requests
class APIClient:
    def __init__(self, authenticated=True, email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD):
        self.authenticated = authenticated
        self.email = email
        self.password = password
        self.headers = {}
        if authenticated:
            access_token = self.login(email, password)
            self.headers["Authorization"] = f"Bearer {access_token}"


    def login(self, email, password):
        login_url = f"/api/v1/auth/login"
        payload = {
            "email": email,
            "password": password
        }

        response_body = self.post_json(login_url, data=payload)
        # verify response body has access token
        assert response_body["access_token"], f"Access token is required, but got {response_body['access_token']}"
        return response_body["access_token"]

    def get(self, endpoint, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)
        response = requests.get(url, headers=headers)
        self.verify_status_code(response, expected_status_code, url)
        return response

    def get_json(self, endpoint, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        response = self.get(endpoint, headers, expected_status_code)
        return response.json()

    def post(self, endpoint, data, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)
        response = requests.post(url, headers=headers, json=data)
        self.verify_status_code(response, expected_status_code, url)
        return response

    def post_json(self, endpoint, data, headers=None, expected_status_code=200):
        headers = self.build_headers(headers)
        response = self.post(endpoint, data, headers=headers, expected_status_code=expected_status_code)
        return response.json()

    def put(self, endpoint, data):
        # Implement PUT request logic here
        pass

    def delete(self, endpoint):
        # Implement DELETE request logic here
        pass

    def build_headers(self, headers=None):
        """
        Build headers for the request, including authentication if enabled.

        Args:
            headers: Optional additional headers to include.

        Returns:
            A dictionary of headers.
        """
        final_headers = self.headers.copy()
        if headers:
            final_headers.update(headers)
        return final_headers


    def verify_status_code(self, response, expected_status_code, endpoint):
        """
        Assert that the response status matches the expected value.

        Args:
            response: HTTP response to validate.
            expected_status_code: Status code the response must match.
            endpoint: Request endpoint included in the assertion message on failure.
        """
        assert response.status_code == expected_status_code, \
            f"Status code. Expected: {expected_status_code}, \
            Actual: {response.status_code}, URL: {endpoint}, Response: {response.content}"

    def build_url(self, endpoint):
        """
        Build the full URL for the request.

        Args:
            endpoint: API path appended to the base URL.
        """
        return f"{BASE_URL}{endpoint}"