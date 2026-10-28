import pytest
from clients.api_client import APIClient
from helpers.application_helper import create_application, get_application, delete_application, \
    build_create_application_payload

api_client = APIClient()

@pytest.mark.tcid("TC-009")
def test_verify_user_can_update_applications_notes():
    """Verify that a user can update the notes of an existing application."""
    # setup: create an application with the default payload
    create_application_json = create_application(api_client)
    application_id = create_application_json["id"]
    notes_before = create_application_json["notes"]

    # Test
    # update the fields of the application
    update_application_endpoint = f"/api/v1/applications/{application_id}"
    update_payload = {
        "notes": "API Automated Testing Updating Notes",
    }
    update_response = api_client.patch_json(update_application_endpoint, data=update_payload)
    #validate
    assert update_response["notes"] == update_payload["notes"]
    assert notes_before != update_response["notes"]

    # fetch the application and verify update is saved
    get_application_response = get_application(api_client, application_id)
    assert get_application_response["notes"] == update_payload["notes"]

    # Teardown / Cleanup
    # delete the application created for the test
    delete_application(api_client, application_id)


@pytest.mark.tcid("TC-010")
def test_verify_user_can_update_application_remote_type():

    old_remote_type = "on_site"
    new_remote_type = "hybrid"

    # setup: create application
    payload = build_create_application_payload(remote_type=old_remote_type)
    application_info = create_application(api_client, payload)
    application_id = application_info["id"]

    # update remote_type = "hybrid"
    update_application_endpoint = f"/api/v1/applications/{application_id}"
    update_payload = {
        "remote_type": new_remote_type,
    }
    update_response = api_client.patch_json(update_application_endpoint, data=update_payload)
    # validate
    assert update_response["remote_type"] == new_remote_type
    assert update_response["remote_type"] != old_remote_type

    # fetch the application and verify update is saved
    get_application_response = get_application(api_client, application_id)
    assert get_application_response["remote_type"] == new_remote_type

    # Teardown / Cleanup
    # delete the application created for the test
    delete_application(api_client, application_id)

@pytest.mark.tcid("TC-011")
def test_verify_user_can_update_application_salary_range():

    old_salary_range = "$200k - $350k"
    new_salary_range = "450k - 500k"

    # setup: create application
    payload = build_create_application_payload(salary_range=old_salary_range)
    application_info = create_application(api_client, payload)
    application_id = application_info["id"]

    # update salary_range = "450k - 500k"
    update_application_endpoint = f"/api/v1/applications/{application_id}"
    update_payload = {
        "salary_range": new_salary_range,
    }
    update_response = api_client.patch_json(update_application_endpoint, data=update_payload)
    # validate
    assert update_response["salary_range"] == new_salary_range
    assert update_response["salary_range"] != old_salary_range

    # fetch the application and verify update is saved
    get_application_response = get_application(api_client, application_id)
    assert get_application_response["salary_range"] == new_salary_range

    # Teardown / Cleanup
    # delete the application created for the test
    delete_application(api_client, application_id)
