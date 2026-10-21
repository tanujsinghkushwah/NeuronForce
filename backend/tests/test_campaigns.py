"""
Unit tests for Marketing Cloud (Campaigns & Email Marketing) endpoints.
"""

import pytest


def test_list_templates(client):
    """Test retrieving pre-designed high-converting email templates."""
    response = client.get("/api/campaigns/templates")
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) >= 3
    assert any(t["id"] == "enterprise_webinar" for t in templates)
    assert any(t["id"] == "closed_lost_nurture" for t in templates)


def test_create_and_get_campaign(client):
    """Test creating an email campaign and fetching it."""
    payload = {
        "name": "Mid-Year Security Compliance Briefing",
        "type": "email",
        "description": "SOC2 and HIPAA certification briefing for security leads",
        "subject": "NeuronForce SOC2 Type II Certification & Enterprise Compliance",
        "preview_text": "Download our audit report and compliance matrix",
        "body_html": "<p>Hi {{first_name}}, our updated SOC2 compliance package is available.</p>",
        "body_text": "Hi {{first_name}}, our updated SOC2 compliance package is available.",
        "audience_filter": {"industry": "Finance"},
        "tags": ["security", "compliance", "enterprise"],
    }
    response = client.post("/api/campaigns", json=payload)
    assert response.status_code == 200
    campaign = response.json()
    assert campaign["name"] == payload["name"]
    assert campaign["status"] == "draft"
    assert campaign["ai_score"] is not None
    c_id = campaign["id"]

    # Fetch details
    detail_res = client.get(f"/api/campaigns/{c_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["id"] == c_id
    assert detail["subject"] == payload["subject"]


def test_simulate_send_campaign(client):
    """Test launching and tracking metrics for a campaign."""
    create_res = client.post("/api/campaigns", json={
        "name": "Q3 Executive Summit",
        "type": "email",
        "subject": "Join us at the Executive Summit",
    })
    c_id = create_res.json()["id"]

    send_res = client.post(f"/api/campaigns/{c_id}/send")
    assert send_res.status_code == 200
    result = send_res.json()
    assert result["status"] in ("active", "completed")
    assert result["emails_sent"] > 0
    assert result["emails_delivered"] > 0
    assert result["open_rate"] >= 0
    assert result["click_rate"] >= 0


def test_ai_optimize_campaign(client):
    """Test triggering AI campaign optimization advice."""
    create_res = client.post("/api/campaigns", json={
        "name": "Product Launch Announcement",
        "type": "email",
        "subject": "Check out our newest features!",
    })
    c_id = create_res.json()["id"]

    opt_res = client.post(f"/api/campaigns/{c_id}/ai-optimize")
    assert opt_res.status_code == 200
    optimized = opt_res.json()
    assert "ai_score" in optimized
    assert "ai_insights" in optimized


def test_campaign_stats(client):
    """Test retrieving global marketing campaign analytics."""
    res = client.get("/api/campaigns/stats")
    assert res.status_code == 200
    stats = res.json()
    assert "total_campaigns" in stats
    assert "active_campaigns" in stats
    assert "total_emails_sent" in stats
    assert "total_revenue_attributed" in stats
    assert "avg_open_rate" in stats
    assert "avg_click_rate" in stats
