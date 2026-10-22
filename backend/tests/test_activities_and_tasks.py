"""
Unit Tests for Activities & Tasks API
Tests activity logging, associations with contacts/deals, task creation, and updates.
"""


def test_create_and_list_activity(client):
    """Test creating an activity for a contact and deal, then listing it."""
    # Create contact and deal
    c_res = client.post(
        "/api/contacts", json={"first_name": "Tony", "last_name": "Stark"}
    )
    contact_id = c_res.json()["id"]

    d_res = client.post(
        "/api/deals", json={"title": "Arc Reactor Supply", "value": 500000.0}
    )
    deal_id = d_res.json()["id"]

    activity_payload = {
        "type": "meeting",
        "subject": "Product Architecture Review",
        "description": "Reviewed enterprise security requirements and multi-agent workflow.",
        "contact_id": contact_id,
        "deal_id": deal_id,
        "duration_minutes": 45,
        "outcome": "positive",
    }
    act_res = client.post("/api/activities", json=activity_payload)
    assert act_res.status_code == 200
    act_data = act_res.json()
    assert act_data["id"] is not None
    assert act_data["subject"] == "Product Architecture Review"
    assert act_data["contact_id"] == contact_id
    assert act_data["deal_id"] == deal_id

    # List activities filtered by contact_id
    filter_res = client.get(f"/api/activities?contact_id={contact_id}")
    assert filter_res.status_code == 200
    activities = filter_res.json()
    assert len(activities) >= 1
    assert activities[0]["subject"] == "Product Architecture Review"


def test_create_and_update_task(client):
    """Test task lifecycle: creation, listing with filter, and updating status."""
    task_payload = {
        "title": "Send MSA and SOC2 documentation",
        "description": "Enterprise security team requested latest compliance pack.",
        "status": "todo",
        "priority": "high",
        "assigned_to": "Sarah Connor",
    }
    create_res = client.post("/api/tasks", json=task_payload)
    assert create_res.status_code == 200
    task = create_res.json()
    task_id = task["id"]
    assert task["title"] == "Send MSA and SOC2 documentation"
    assert task["status"] == "todo"

    # List tasks with status=todo
    list_res = client.get("/api/tasks?status=todo")
    assert list_res.status_code == 200
    tasks = list_res.json()
    assert any(t["id"] == task_id for t in tasks)

    # Update task to completed
    update_res = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": "Send MSA and SOC2 documentation",
            "status": "completed",
            "priority": "high",
            "assigned_to": "Sarah Connor",
        },
    )
    assert update_res.status_code == 200
    updated_task = update_res.json()
    assert updated_task["status"] == "completed"

    # Verify 404 for updating non-existent task
    assert (
        client.put("/api/tasks/99999", json={"title": "Non-existent"}).status_code
        == 404
    )
