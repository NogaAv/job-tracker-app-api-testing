from xmlrpc.client import DateTime

import requests

from clients.api_client import APIClient
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
    endpoint = f"/api/v1/public/status"
    api_client = APIClient(authenticated=False)

    response_body = api_client.get_json(endpoint)

    assert "app_name" in response_body
    assert response_body["app_name"] == "SuperSQA Job Tracker"
    assert "api_version" in response_body
    assert response_body["api_version"] == "v1"
    assert "environment" in response_body
    assert response_body["environment"] == "local"
    assert "server_time" in response_body, "server_time is missing in the response body"
    assert response_body["server_time"] is not None, "server_time is None"
