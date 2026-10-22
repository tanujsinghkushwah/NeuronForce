"""
Unit tests for Tableau/BI reports, funnel, revenue forecast, and CSV exports.
"""

import pytest


def test_funnel_analytics(client):
    """Test full lead-to-revenue conversion funnel endpoint."""
    response = client.get("/api/analytics/funnel")
    assert response.status_code == 200
    data = response.json()
    assert "funnel" in data
    assert len(data["funnel"]) == 4
    stages = [f["stage"] for f in data["funnel"]]
    assert "Total Leads" in stages
    assert "Qualified Leads" in stages
    assert "Deals Created" in stages
    assert "Deals Won" in stages
    assert "total_revenue" in data
    assert "overall_conversion" in data


def test_revenue_forecast(client):
    """Test AI-powered weighted revenue pipeline forecast."""
    response = client.get("/api/analytics/forecast")
    assert response.status_code == 200
    data = response.json()
    assert "total_pipeline" in data
    assert "weighted_forecast" in data
    assert "ai_weighted_forecast" in data
    assert "by_stage" in data


def test_tickets_report(client):
    """Test service ticket resolution and SLA breakdown report."""
    response = client.get("/api/analytics/reports/tickets")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "by_priority" in data
    assert "by_category" in data
    assert "resolution_rate" in data["summary"]


def test_campaigns_report(client):
    """Test marketing campaign performance and revenue attribution report."""
    response = client.get("/api/analytics/reports/campaigns")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "records" in data


def test_export_deals_csv(client):
    """Test exporting deals data as CSV format."""
    response = client.get("/api/analytics/export/deals")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert (
        "attachment; filename=deals_export.csv"
        in response.headers["content-disposition"]
    )
    content = response.text
    assert "ID,Title,Value,Stage" in content


def test_export_contacts_csv(client):
    """Test exporting contacts data as CSV format."""
    response = client.get("/api/analytics/export/contacts")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert (
        "attachment; filename=contacts_export.csv"
        in response.headers["content-disposition"]
    )
    content = response.text
    assert "ID,First Name,Last Name,Email" in content
