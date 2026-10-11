import requests


def test_verify_public_demo_stats_endpoint():
    """
Example response body:
    {
      "total_seeded_applications": 4,
      "status_counts": {
        "potential": 2,
        "applied": 1,
        "in_progress": 1,
        "final_stage": 0,
        "hired": 0,
        "rejected": 0,
        "withdrawn": 0,
        "total": 4
      }
    }
    """
    # make the call to the public demo stats endpoint
    url = "http://127.0.0.1:3050/api/v1/public/demo-stats"
    response = requests.get(url)

    # verify the status code
    status_code = response.status_code
    assert status_code == 200, f"Expected status code 200, but got {status_code}"

    # verify the body of the response
    response_body = response.json()

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
