"""
Unit Tests for Health Check & Dashboard API
"""


def test_health_check(client):
    """Test /api/health endpoint returns 200 and healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"
    assert "timestamp" in data


def test_dashboard_empty_db(client):
    """Test /api/dashboard returns complete dashboard structure."""
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "total_contacts" in data
    assert "total_deals" in data
    assert "total_revenue" in data
    assert "pipeline_value" in data
    assert "conversion_rate" in data
    assert "deals_won" in data
    assert "deals_lost" in data
    assert "revenue_trend" in data
    assert "pipeline_by_stage" in data
    assert "top_deals" in data
    assert "recent_activities" in data
    assert "lead_sources" in data
