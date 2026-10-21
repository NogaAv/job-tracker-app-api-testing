
def verify_error_response(response_json, expected_code, expected_message):

    assert response_json["error"], f"Expecting failure response but did not het any error. Actual: {response_json}"
    assert response_json["error"]["code"] == expected_code
    assert response_json["error"]["message"] == expected_message
    assert response_json["error"]["details"] or response_json["error"]["details"] == []
    assert isinstance(response_json["error"]["details"], list), f"Error response expected to have a list in 'details' but it did not. Actual: {response_json}"