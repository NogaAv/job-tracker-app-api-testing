from xmlrpc.client import DateTime

import requests
from configs.settings import BASE_URL

def test_verify_public_status_endpoint():
    """
    Example response body:
    {
      "app_name": "SuperSQA Job Tracker",
      "api_version": "v1",
      "environment": "local",
      "server_time": "2026-10-11T04:59:59.467739Z"
    }
    """
    # make the call to the public status endpoint
    url = f"{BASE_URL}/api/v1/public/status"
    response = requests.get(url)

    # verify the status code
    status_code = response.status_code
    assert status_code == 200, f"Expected status code 200, but got {status_code}"

    # verify the body of the response
    response_body = response.json()

    assert "app_name" in response_body
    assert response_body["app_name"] == "SuperSQA Job Tracker"
    assert "api_version" in response_body
    assert response_body["api_version"] == "v1"
    assert "environment" in response_body
    assert response_body["environment"] == "local"
    assert "server_time" in response_body, "server_time is missing in the response body"
    assert response_body["server_time"] is not None, "server_time is None"
