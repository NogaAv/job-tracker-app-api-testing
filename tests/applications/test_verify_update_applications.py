import pytest
from clients.api_client import APIClient


@pytest.mark.tcid("TC-008")
def test_verify_user_can_update_application_status():
    """Verify that a user can update the status of an existing application."""
    # setup
    # create a new application
    create_application_endpoint = f"/api/v1/applications"
    payload = {
      "company_name": "SuperSQA",
      "job_url": "https://supersqa.com/jobs/us-test-engineer",
      "location": "Remote",
      "next_action": "Follow up with manager",
      "notes": "Submitted through api testing.",
      "remote_type": "remote",
      "role_title": "API Test Engineer",
      "salary_range": "$170k - $230k",
      "status": "applied"
    }

    # make the api call
    api_client = APIClient()
    post_response_body = api_client.post_json(create_application_endpoint, data=payload)
    application_id = post_response_body["id"]


    # Test
    # update the status of the application
    update_application_endpoint = f"/api/v1/applications/{application_id}"
    update_payload = {
        "status": "in_progress"
    }
    patch_json_response = api_client.patch_json(update_application_endpoint, data=update_payload)
    assert patch_json_response["status"] == update_payload["status"]

    get_endpoint = f"/api/v1/applications/{application_id}"
    get_application_response = api_client.get_json(get_endpoint)
    assert get_application_response["status"] == update_payload["status"]

    # Teardown / Cleanup
    # delete the application created for the test
    delete_endpoint = f"/api/v1/applications/{application_id}"
    # we just make the call, the client verifies 204 response and that is good enough
    api_client.delete(delete_endpoint)

