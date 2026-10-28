import pytest
from clients.api_client import APIClient
from helpers.application_helper import build_create_application_payload, create_application, delete_application, \
    get_application, get_applications_list
from helpers.error_helper import verify_error_response


@pytest.mark.tcid("TC-016")
def test_verify_create_application_required_company_name():

    api_client = APIClient()

    # Create application with missing "company_name" in the req payload
    payload = build_create_application_payload()
    payload.pop("company_name")

    # Send post request expecting an error
    response_json = create_application(api_client, payload, expected_status_code=422)

    # Verify the error response
    verify_error_response(response_json, "VALIDATION_ERROR", "Request validation failed")
    # Verify the error returns the missing field
    assert "company_name" in response_json["error"]["details"][0]["loc"]


@pytest.mark.tcid("TC-017")
def test_verify_create_application_rejects_invalid_status():
    api_client = APIClient()
    # create application with invalid status
    payload = build_create_application_payload(status="not_exist")

    # Send post request expecting an error
    response_json = create_application(api_client, payload, expected_status_code=422)

    # Verify the error response
    verify_error_response(response_json, "VALIDATION_ERROR", "Request validation failed")
    # Verify the error returns the missing field
    assert "status" in response_json["error"]["details"][0]["loc"]


@pytest.mark.tcid("TC-018")
def test_verify_get_nonexisting_application_returns_not_found():
    api_client = APIClient()
    nonexisting_app_id = 99999999

    # make a get call with nonexistent id expecting a 404
    response_json = get_application(api_client, nonexisting_app_id, expected_status_code=404)
    # Verify the error response
    verify_error_response(response_json, "NOT_FOUND", "Application not found")
    # Verify the error returns empty "details" field
    assert response_json["error"]["details"] == []


@pytest.mark.tcid("TC-019")
def test_verify_applications_list_requires_authentication():

    # create unauthenticated client
    api_client = APIClient(authenticated=False)
    # make a get call with authentication expecting error 401
    response_json = get_applications_list(api_client, expected_status_code=401)

    # Verify the error response
    verify_error_response(response_json, "AUTHENTICATION_REQUIRED", "Authentication required")
    # Verify the error returns empty "details" field
    assert response_json["error"]["details"] == []
