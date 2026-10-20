from clients.api_client import APIClient
from clients.sql_client import SQLClient


def test_verify_api_key_is_not_stored_as_plain_text():
    """
    Verify newly created API keys are hashed in the database, not stored in plain text.
    """
    api_client = APIClient()
    sql_client = SQLClient()

    # make a call to create a new api key
    create_api_key_endpoint = "/api/v1/api-keys"
    create_api_key_payload = {
                "name": "API Testing Automation"
                }

    create_key_json = api_client.post_json(create_api_key_endpoint, create_api_key_payload)
    api_key = create_key_json["api_key"]
    key_prefix = create_key_json["key_prefix"]
    key_id = create_key_json["id"]

    assert api_key.startswith("jt_live_")
    assert key_prefix.startswith("jt_live_")
    assert api_key.startswith(key_prefix)

    # go to api-keys database and verify the key is not stored as plain text
    query = f"""
            SELECT hashed_key, key_prefix
            FROM api_keys
            WHERE id = {key_id}
            ORDER BY id DESC;
        """

    db_rows = sql_client.execute_query(query)
    db_row = db_rows[0] if db_rows else None
    assert db_row is not None, f"No database row found for API key ID: {key_id}"
    assert db_row['key_prefix'] == key_prefix
    assert db_row['hashed_key'] != api_key