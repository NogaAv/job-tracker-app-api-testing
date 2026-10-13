from clients.api_client import APIClient
from configs.settings import BASE_URL
from helpers.auth_helper import login_user


def test_verify_authenticated_user_can_get_applications():
    """
    verify an authenticated user can retrieve the applications list
    """
    # make the api call with the token in the header
    get_applications_url = f"{BASE_URL}/api/v1/applications"
    api_client = APIClient()
    response_body = api_client.get_json(get_applications_url)

    # verify the api response body
    assert response_body, f"GET applications api response body is empty. Endpoint: {get_applications_url}"
    assert isinstance(response_body, list), f"Expected a list, but got {type(response_body)}"
