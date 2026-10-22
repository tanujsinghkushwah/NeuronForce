"""
Unit tests for Service Cloud (Support Tickets & Cases) endpoints.
"""

import pytest


def test_create_and_get_ticket(client):
    """Test creating a support ticket and retrieving it."""
    payload = {
        "title": "High latency on webhook deliveries",
        "description": "Outbound webhook notifications take > 15 seconds to acknowledge.",
        "priority": "high",
        "category": "technical",
        "reporter_name": "Sarah Connor",
        "reporter_email": "sarah.connor@cyberdyne.io",
        "tags": ["webhooks", "latency"],
        "ai_triage": True,
    }
    response = client.post("/api/tickets", json=payload)
    assert response.status_code == 200
    ticket = response.json()
    assert ticket["title"] == payload["title"]
    assert ticket["priority"] == "high"
    assert ticket["category"] == "technical"
    assert ticket["ticket_number"].startswith("TKT-")
    assert ticket["sla_due_at"] is not None
    assert "ai_triage" in ticket
    assert ticket["status"] == "open"
    ticket_id = ticket["id"]

    # Retrieve ticket
    get_res = client.get(f"/api/tickets/{ticket_id}")
    assert get_res.status_code == 200
    fetched = get_res.json()
    assert fetched["id"] == ticket_id
    assert fetched["reporter_email"] == "sarah.connor@cyberdyne.io"


def test_list_tickets_and_filter(client):
    """Test listing tickets with filtering by status and priority."""
    # Create critical ticket
    client.post(
        "/api/tickets",
        json={
            "title": "Production outage in auth service",
            "priority": "critical",
            "category": "bug",
        },
    )
    # Create low ticket
    client.post(
        "/api/tickets",
        json={
            "title": "Dark mode theme toggle request",
            "priority": "low",
            "category": "feature_request",
        },
    )

    # List all
    res = client.get("/api/tickets")
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 2

    # Filter by priority=critical
    crit_res = client.get("/api/tickets?priority=critical")
    assert crit_res.status_code == 200
    crit_items = crit_res.json()
    assert all(t["priority"] == "critical" for t in crit_items)


def test_update_ticket_status(client):
    """Test updating ticket status and assigning an agent."""
    create_res = client.post(
        "/api/tickets",
        json={
            "title": "SSO certificate renewal",
            "priority": "medium",
        },
    )
    t_id = create_res.json()["id"]

    update_res = client.patch(
        f"/api/tickets/{t_id}",
        json={
            "status": "in_progress",
            "assigned_to": "Alex Rivera",
            "internal_notes": "Assigned to Alex; awaiting vendor renewal cert.",
        },
    )
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["status"] == "in_progress"
    assert updated["assigned_to"] == "Alex Rivera"
    assert (
        updated["internal_notes"] == "Assigned to Alex; awaiting vendor renewal cert."
    )


def test_ticket_messages_thread(client):
    """Test adding conversation messages to a ticket."""
    create_res = client.post(
        "/api/tickets",
        json={
            "title": "Custom report generation issue",
            "priority": "medium",
        },
    )
    t_id = create_res.json()["id"]

    msg_payload = {
        "author_name": "Jordan Lee",
        "author_email": "jordan.lee@neuronforce.ai",
        "body": "Could you provide the date range for which the export failed?",
        "is_internal": False,
    }
    msg_res = client.post(f"/api/tickets/{t_id}/messages", json=msg_payload)
    assert msg_res.status_code == 200
    msg = msg_res.json()
    assert msg["body"] == msg_payload["body"]
    assert msg["author_name"] == "Jordan Lee"

    # Verify message in ticket detail
    t_detail = client.get(f"/api/tickets/{t_id}").json()
    assert len(t_detail["messages"]) >= 1
    assert t_detail["messages"][0]["body"] == msg_payload["body"]


def test_ticket_stats(client):
    """Test the ticket metrics and SLA stats endpoint."""
    res = client.get("/api/tickets/stats")
    assert res.status_code == 200
    stats = res.json()
    assert "total_tickets" in stats
    assert "open_tickets" in stats
    assert "in_progress_tickets" in stats
    assert "resolved_tickets" in stats
    assert "sla_breached" in stats
    assert "by_priority" in stats
    assert "by_category" in stats
