import requests
from configs.settings import BASE_URL
from helpers.auth_helper import login_user


def test_verify_authenticated_user_can_get_applications():
    """
    verify an authenticated user can retrieve the applications list
    """
    # get JWT token: login with user and get the token from the response
    # Make the call
    token = login_user()

    # make the api call with the token in the header
    get_applications_url = f"{BASE_URL}/api/v1/applications"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(get_applications_url, headers=headers)

    # verify the api status code
    assert response.status_code == 200, f"GET applications api response expected to have status code 200, but got {response.status_code}. Endpoint: {get_applications_url}"

    # verify the api response body
    response_body = response.json()
    assert response_body, f"GET applications api response body is empty. Endpoint: {get_applications_url}"
    assert isinstance(response_body, list), f"Expected a list, but got {type(response_body)}"
