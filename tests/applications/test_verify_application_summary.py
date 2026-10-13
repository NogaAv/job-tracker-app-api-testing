
from clients.api_client import APIClient


def test_verify_authenticated_user_can_access_application_summary():
    """
    Example response body for the applications summary api:
    {
      "potential": 2,
      "applied": 1,
      "in_progress": 1,
      "final_stage": 0,
      "hired": 0,
      "rejected": 0,
      "withdrawn": 0,
      "total": 4
    }
    """

    # make the call with the JWT token in header
    applications_summary_endpoint = f"/api/v1/applications/summary"
    api_client = APIClient()
    response_body = api_client.get_json(applications_summary_endpoint)

    # verify the api response body
    assert response_body, f"GET applications summary api response body is empty. Endpoint: {applications_summary_endpoint}"
    assert len(response_body.keys()) > 0, f"Expected a dictionary with keys, but got {type(response_body)}"

    assert isinstance(response_body["potential"], int), f"Expected integer, but got {type(response_body['potential'])}"
    assert isinstance(response_body["applied"], int), f"Expected integer, but got {type(response_body['applied'])}"
    assert isinstance(response_body["in_progress"], int), f"Expected integer, but got {type(response_body['in_progress'])}"
    assert isinstance(response_body["final_stage"], int), f"Expected integer, but got {type(response_body['final_stage'])}"
    assert isinstance(response_body["hired"], int), f"Expected integer, but got {type(response_body['hired'])}"
    assert isinstance(response_body["rejected"], int), f"Expected integer, but got {type(response_body['rejected'])}"
    assert isinstance(response_body["withdrawn"], int), f"Expected integer, but got {type(response_body['withdrawn'])}"
    assert isinstance(response_body["total"], int), f"Expected integer, but got {type(response_body['total'])}"

    assert response_body["total"] == sum([
        response_body["potential"],
        response_body["applied"],
        response_body["in_progress"],
        response_body["final_stage"],
        response_body["hired"],
        response_body["rejected"],
        response_body["withdrawn"]
    ]), f"Expected total to be the sum of all other values, but got {response_body['total']}"

    # for k, v in response_body.items():
    #     assert isinstance(v, int), f"Expected value for key '{k}' to be an integer, but got {type(v)}"