"""
Unit Tests for Calendar, Analytics & Settings API
Tests calendar event scheduling, historical analytics snapshots, team performance, and settings.
"""

from datetime import datetime, timezone, timedelta
from app.models import AnalyticsSnapshot

def test_calendar_events_crud(client):
    """Test creating, listing, and deleting calendar events."""
    start_time = datetime.now(timezone.utc) + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)

    event_payload = {
        "title": "Quarterly Business Review with Stark Ind.",
        "description": "Present AI CRM benchmark and cost savings report.",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "location": "Zoom / Virtual",
        "event_type": "presentation",
        "attendees": ["tony@stark.com", "sales@neuronforce.ai"],
        "color": "#6366f1",
        "is_all_day": False,
        "reminder_minutes": 15
    }
    create_res = client.post("/api/calendar/events", json=event_payload)
    assert create_res.status_code == 200
    event = create_res.json()
    event_id = event["id"]
    assert event["title"] == "Quarterly Business Review with Stark Ind."
    assert "tony@stark.com" in event["attendees"]

    # List events
    list_res = client.get("/api/calendar/events")
    assert list_res.status_code == 200
    events = list_res.json()
    assert any(e["id"] == event_id for e in events)

    # Delete event
    del_res = client.delete(f"/api/calendar/events/{event_id}")
    assert del_res.status_code == 200
    assert del_res.json()["message"] == "Event deleted"

    # Delete non-existent event 404
    assert client.delete("/api/calendar/events/99999").status_code == 404


def test_analytics_revenue(client, db_session):
    """Test /api/analytics/revenue returns time-series snapshots."""
    # Seed a snapshot directly into the session
    today = datetime.now(timezone.utc)
    snapshot = AnalyticsSnapshot(
        date=today,
        total_revenue=250000.0,
        pipeline_value=890000.0,
        deals_won=8,
        deals_lost=2,
        conversion_rate=80.0,
        avg_deal_size=31250.0,
        new_contacts=15,
        ai_tasks_run=42,
        ai_total_cost=0.1850
    )
    db_session.add(snapshot)
    db_session.commit()

    res = client.get("/api/analytics/revenue?days=7")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 1
    assert data[-1]["total_revenue"] == 250000.0
    assert data[-1]["ai_tasks_run"] == 42


def test_analytics_performance(client):
    """Test /api/analytics/performance returns team performance and pipeline metrics."""
    # Seed a deal with an owner
    client.post("/api/deals", json={
        "title": "Performance Test Deal",
        "value": 120000.0,
        "stage": "closed_won",
        "owner": "Alex Rivera"
    })

    res = client.get("/api/analytics/performance")
    assert res.status_code == 200
    data = res.json()
    assert "team_performance" in data
    assert "overall" in data
    assert any(t["owner"] == "Alex Rivera" for t in data["team_performance"])
    assert data["overall"]["total_revenue"] >= 120000.0


def test_app_settings(client):
    """Test /api/settings returns company, AI agent config, and pipeline stages."""
    res = client.get("/api/settings")
    assert res.status_code == 200
    data = res.json()
    assert data["company"]["name"] == "NeuronForce"
    assert data["ai_config"]["auto_lead_scoring"] is True
    assert data["ai_config"]["confidence_threshold"] == 0.7
    assert len(data["pipeline_stages"]) == 6
