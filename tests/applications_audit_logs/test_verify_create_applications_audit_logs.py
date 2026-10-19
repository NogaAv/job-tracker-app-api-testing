from clients.api_client import APIClient
from clients.sql_client import SQLClient


def test_verify_create_application_writes_to_audit_logs():
    """
    Verify creating an application records a ``created`` audit log via SQLClient.
    Same scenario as the V1 test above, using the shared database helper.
    """
    # make 'applications' call -> create application
    payload = {
            "company_name": "SuperSQA",
            "job_url": "https://supersqa.com/jobs/us-test-engineer",
            "location": "Remote",
            "next_action": "Follow up with manager",
            "notes": "Submitted through api testing.",
            "remote_type": "remote",
            "role_title": "API Test Engineer",
            "salary_range": "$170k - $200k",
            "status": "potential"
            }

    # make the api call
    endpoint = "/api/v1/applications"
    api_client = APIClient()
    create_application_json = api_client.post_json(endpoint, payload, expected_status_code=201)
    application_id = create_application_json["id"]

    # verify the log table using SQLClient
    sql_client = SQLClient()
    query = f"""SELECT * 
            FROM application_audit_logs
            WHERE application_id = {application_id};"""
    audit_log_rows = sql_client.execute_query(query)

    assert audit_log_rows, f"Expected rows in audit log for application id: {application_id}"
    audit_log = audit_log_rows[0] # selecting the first row for verification, which is the last created log entry
    assert audit_log["application_id"] == application_id
    assert audit_log["action"] == "created"
    assert audit_log["user_id"]

    # clean up / teardown: delete the created application
    delete_application_endpoint = f"/api/v1/applications/{application_id}"
    # we just make the call, the client verifies 204
    api_client.delete(delete_application_endpoint, expected_status_code=204)