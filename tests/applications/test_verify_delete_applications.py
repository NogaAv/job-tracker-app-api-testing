import pytest
from clients.api_client import APIClient


@pytest.mark.tcid("TC-012")
def test_verify_user_can_delete_application():
    # Setup - Create an application (payload)
    payload = {
            "company_name": "SuperSQA",
            "job_url": "https://supersqa.com/jobs/us-test-engineer",
            "location": "Remote",
            "next_action": "Follow up with manager",
            "notes": "Submitted through api testing.",
            "remote_type": "remote",
            "role_title": "API Test Engineer",
            "salary_range": "$170k - $200k",
            "status": "applied"
            }

    # make the api call to create an application
    endpoint = "/api/v1/applications"
    api_client = APIClient()
    create_application_json = api_client.post_json(endpoint, payload, expected_status_code=201)
    application_id = create_application_json["id"]

    # Test - Delete the application
    delete_endpoint = f"/api/v1/applications/{application_id}"
    api_client.delete(delete_endpoint)

    # Verify it is deleted by trying to get it and expecting a 404
    get_endpoint = f"/api/v1/applications/{application_id}"
    api_client.get(get_endpoint, expected_status_code=404)

    # Should use SQL to verify the application is deleted, but for now we just check the API response.
