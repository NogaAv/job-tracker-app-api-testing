import pytest
from clients.api_client import APIClient
from clients.sql_client import SQLClient


@pytest.mark.tcid("TC-015")
def test_verify_delete_application_writes_to_audit_logs():
    """
    Verify deleting an application records a ``deleted`` audit log via SQLClient.
    """
    status_before = "potential"
    status_after = None

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
            "status": status_before
            }

    # make the api call to create (test setup)
    endpoint = "/api/v1/applications"
    api_client = APIClient()
    create_application_json = api_client.post_json(endpoint, payload, expected_status_code=201)
    application_id = create_application_json["id"]

    # make api call to delete
    delete_endpoint = f"/api/v1/applications/{application_id}"
    api_client.delete(delete_endpoint)

    # verify the log table using SQLClient
    sql_client = SQLClient()
    query = f"""SELECT * 
            FROM application_audit_logs
            WHERE application_id = {application_id}
            ORDER BY id DESC
            LIMIT 1;"""
    audit_log_rows = sql_client.execute_query(query)

    assert audit_log_rows, f"Expected rows in audit log for application id: {application_id}"
    audit_log = audit_log_rows[0]
    assert audit_log["application_id"] == application_id
    assert audit_log["action"] == "deleted"
    assert audit_log["old_status"] == status_before
    assert audit_log["new_status"] == status_after
