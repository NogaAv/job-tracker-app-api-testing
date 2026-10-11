
import requests

from configs.settings import BASE_URL


def test_verify_user_can_login_with_valid_credentials():
    """
    Verify valid credentials return a bearer token and user profile.

    Example response body:
    {
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJzdHVkZW50QGV4YW1wbGUuY29tIiwicm9sZSI6InVzZXIiLCJpYXQiOjE3OTE3MDczMzgsImV4cCI6MTc5MTczNjEzOH0._ZGLMLK2G8yHaBtBQlZpcZh9Kb36VFZ9Qc2vQSpFSNY",
  "token_type": "bearer",
  "expires_in": 28800,
  "user": {
    "id": 1,
    "email": "student@example.com",
    "full_name": "SupersQA Student",
    "role": "user",
    "is_active": true,
    "created_at": "2026-08-06T00:01:52",
    "updated_at": "2026-08-06T00:01:52"
  }
}

    """

    # Make the call
    url = f"{BASE_URL}/api/v1/auth/login"
    payload = {
        "email": "student@example.com",
        "password": "Password123!"
    }

    response = requests.post(url, json=payload)

    # verify status code 200 and return the response body
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # verify the response body
    response_body = response.json()
    assert response_body["access_token"], f"Access token is required, but got {response_body['access_token']}"
    assert response_body["token_type"] == "bearer", "Token type is required"
    assert response_body["expires_in"], f"Expires in is required, but got {response_body['expires_in']}"
    assert response_body["user"], f"User is required, but got {response_body['user']}"
    assert response_body["user"]["id"], f"User id is required, but got {response_body['user']['id']}"
    assert response_body["user"]["email"] == payload["email"], f"User email is required, but got {response_body['user']['email']}"
    assert response_body["user"]["full_name"], f"User full name is required, but got {response_body['user']['full_name']}"
    assert response_body["user"]["role"], f"User role is required, but got {response_body['user']['role']}"
    assert response_body["user"]["is_active"], f"User is active is required, but got {response_body['user']['is_active']}"
    assert response_body["user"]["created_at"], f"User created at is required, but got {response_body['user']['created_at']}"
    assert response_body["user"]["updated_at"], f"User updated at is required, but got {response_body['user']['updated_at']}"


def test_verify_user_cannot_login_with_invalid_credentials():
    """
    Verify invalid credentials return 401 with an INVALID_CREDENTIALS error.

    Example response body:
   {
      "error": {
        "code": "INVALID_CREDENTIALS",
        "message": "Invalid email or password",
        "details": []
      }
    }
    """
    # Make the call
    url = f"{BASE_URL}/api/v1/auth/login"
    payload = {
        "email": "student@example.com",
        "password": "BadPassword123!"
    }

    response = requests.post(url, json=payload)

    # verify status code 401 and return the response body
    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

    # verify the response body
    response_body = response.json()
    assert isinstance(response_body["error"], dict), "Expected response body to have 'error' dictionary."
    assert response_body["error"]["code"] == "INVALID_CREDENTIALS", f"Expected error code INVALID_CREDENTIALS, but got {response_body['error']['code']}"
    assert response_body["error"]["message"] == "Invalid email or password", f"Expected error message 'Invalid email or password', but got {response_body['error']['message']}"
    assert response_body["error"]["details"] == [], f"Expected error details to be an empty list, but got {response_body['error']['details']}"
