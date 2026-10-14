from clients.api_client import APIClient


def test_verify_user_can_create_application():
    """Verify an authenticated user can create a new application."""
    # create a payload with the token in the header
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

    # verify the api response body
    assert post_response_body, f"POST applications api response body is empty. Endpoint: {create_application_endpoint}"
    assert isinstance(post_response_body, dict), f"Expected a dict, but got {type(post_response_body)}"
    assert post_response_body["company_name"] == payload["company_name"], f"Expected company_name to be {payload['company_name']}, but got {post_response_body.get('company_name')}"
    assert post_response_body["job_url"] == payload["job_url"], f"Expected job_url to be {payload['job_url']}, but got {post_response_body.get('job_url')}"
    assert post_response_body["location"] == payload["location"], f"Expected location to be {payload['location']}, but got {post_response_body.get('location')}"
    assert post_response_body["next_action"] == payload["next_action"], f"Expected next_action to be {payload['next_action']}, but got {post_response_body.get('next_action')}"
    assert post_response_body["notes"] == payload["notes"], f"Expected notes to be {payload['notes']}, but got {post_response_body.get('notes')}"
    assert post_response_body["remote_type"] == payload["remote_type"], f"Expected remote_type to be {payload['remote_type']}, but got {post_response_body.get('remote_type')}"
    assert post_response_body["role_title"] == payload["role_title"], f"Expected role_title to be {payload['role_title']}, but got {post_response_body.get('role_title')}"
    assert post_response_body["salary_range"] == payload["salary_range"], f"Expected salary_range to be {payload['salary_range']}, but got {post_response_body.get('salary_range')}"
    assert post_response_body["status"] == payload["status"], f"Expected status to be {payload['status']}, but got {post_response_body.get('status')}"
    assert post_response_body["description"] is None, f"Expected description to be None, but got {post_response_body.get('description')}"

    assert post_response_body["id"], "Expected an 'id' field in the response body, but it was missing."
    assert isinstance(post_response_body["id"], int), f"Expected 'id' to be an integer, but got {type(post_response_body['id'])}"
    assert post_response_body["id"] > 0, f"Expected 'id' to be greater than 0, but got {post_response_body['id']}"
    assert post_response_body["created_at"], "Expected a 'created_at' field in the response body, but it was missing."
    assert post_response_body["updated_at"], "Expected an 'updated_at' field in the response body, but it was missing."

    # do a GET call and verify the item is actually created
    application_id = post_response_body["id"]
    get_application_endpoint = f"/api/v1/applications/{application_id}"
    get_response_body = api_client.get_json(get_application_endpoint)

    assert post_response_body["id"] == get_response_body["id"], f"Expected id to be {post_response_body['id']}, but got {get_response_body.get('id')}"
    assert get_response_body["company_name"] == payload["company_name"], f"Expected company_name to be {payload['company_name']}, but got {get_response_body.get('company_name')}"
    assert get_response_body["job_url"] == payload["job_url"], f"Expected job_url to be {payload['job_url']}, but got {get_response_body.get('job_url')}"
    assert get_response_body["location"] == payload["location"], f"Expected location to be {payload['location']}, but got {get_response_body.get('location')}"
    assert get_response_body["next_action"] == payload["next_action"], f"Expected next_action to be {payload['next_action']}, but got {get_response_body.get('next_action')}"
    assert get_response_body["notes"] == payload["notes"], f"Expected notes to be {payload['notes']}, but got {get_response_body.get('notes')}"
    assert get_response_body["remote_type"] == payload["remote_type"], f"Expected remote_type to be {payload['remote_type']}, but got {get_response_body.get('remote_type')}"
    assert get_response_body["role_title"] == payload["role_title"], f"Expected role_title to be {payload['role_title']}, but got {get_response_body.get('role_title')}"
    assert get_response_body["salary_range"] == payload["salary_range"], f"Expected salary_range to be {payload['salary_range']}, but got {get_response_body.get('salary_range')}"
    assert get_response_body["status"] == payload["status"], f"Expected status to be {payload['status']}, but got {get_response_body.get('status')}"
    assert get_response_body["description"] is None, f"Expected description to be None, but got {get_response_body.get('description')}"

    # clean up / teardown: delete the created application
    delete_application_endpoint = f"/api/v1/applications/{application_id}"
    # we just make the call, the client verifies 204
    api_client.delete(delete_application_endpoint, expected_status_code=204)