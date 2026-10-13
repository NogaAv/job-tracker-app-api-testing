import requests

from clients.api_client import APIClient
from configs.settings import BASE_URL
from tests.auth.test_verify_login import api_client


def test_verify_public_demo_stats_endpoint():
    """Verify the public demo stats endpoint returns seeded totals and status counts."""
    # make the call to the public demo stats endpoint
    endpoint = f"/api/v1/public/demo-stats"
    api_client = APIClient(authenticated=False)

    response_body = api_client.get_json(endpoint)

    # verify the number of keys in the response body
    assert len(response_body.keys()) == 2, f"Expected 2 keys in the response body, but got {len(response_body.keys())}"
    # verify the values are of the correct type
    assert "total_seeded_applications" in response_body
    assert isinstance(response_body["total_seeded_applications"], int), f"Expected total_seeded_applications to be an integer, but got {type(response_body['total_seeded_applications'])}"
    assert "status_counts" in response_body
    status_count = response_body["status_counts"]
    assert isinstance(status_count, dict), f"Expected status_counts to be a dictionary, but got {type(response_body['status_counts'])}"

    # verify the status_counts keys are correct and their values are integers
    for k, v in status_count.items():
        assert isinstance(v, int), f"Expected value for {k} to be an integer, but got {type(v)}"
