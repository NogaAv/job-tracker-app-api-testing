from clients.api_client import APIClient


def create_application(api_client, payload = None, expected_status_code=201):
    """
    Creates a new application with default values.
    Returns the application data as a dictionary.
    """
    if payload is None:
        payload = build_create_application_payload()

    # make the api call
    endpoint = "/api/v1/applications"
    create_application_json = api_client.post_json(endpoint, payload, expected_status_code=expected_status_code)
    return create_application_json

def get_application(api_client, application_id, expected_status_code=200):
    get_application_endpoint = f"/api/v1/applications/{application_id}"
    return api_client.get_json(get_application_endpoint, expected_status_code=expected_status_code)

def get_applications_list(api_client, expected_status_code=200):
    get_application_endpoint = f"/api/v1/applications"
    return api_client.get_json(get_application_endpoint, expected_status_code=expected_status_code)

def delete_application(api_client, application_id, expected_status_code=204):
    delete_application_endpoint = f"/api/v1/applications/{application_id}"
    return api_client.delete(delete_application_endpoint, expected_status_code=expected_status_code)

def build_create_application_payload(**kwargs):
    """
    Builds a default payload for creating an application.
    Returns the payload as a dictionary.
    """
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
    payload.update(kwargs)
    return payload