"""
Tests for Global Unified Search Endpoint
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_global_search_empty_query(client):
    """Empty query should return default discovery/navigation items."""
    res = client.get("/api/search")
    assert res.status_code == 200
    data = res.json()
    assert "categories" in data
    assert "contacts" in data["categories"]
    assert "deals" in data["categories"]
    assert "agents" in data["categories"]
    assert "navigation" in data["categories"]
    assert data["total"] > 0


def test_global_search_multi_word_query(client):
    """Multi-token query with stop-words like 'Tanuj and Robert' should find both."""
    res = client.get("/api/search?q=Tanuj and Robert")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    found_contacts = [c["title"] for c in data["categories"]["contacts"]]
    assert any("Robert" in name or "Tanuj" in name for name in found_contacts)


def test_global_search_deals_and_companies(client):
    """Searching company or deal title should return deals."""
    res = client.get("/api/search?q=TechCorp")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    deal_titles = [d["title"] for d in data["categories"]["deals"]]
    contact_companies = [
        c.get("meta", {}).get("company", "") for c in data["categories"]["contacts"]
    ]
    assert any("TechCorp" in t for t in deal_titles) or any(
        "TechCorp" in comp for comp in contact_companies
    )


def test_global_search_ai_agents(client):
    """Searching agent capabilities or agent names should return fleet agents."""
    res = client.get("/api/search?q=lead scoring")
    assert res.status_code == 200
    data = res.json()
    agent_names = [a["title"] for a in data["categories"]["agents"]]
    assert any("Lead Scoring Agent" in name for name in agent_names)


def test_global_search_navigation(client):
    """Searching platform features should surface navigation links."""
    res = client.get("/api/search?q=pipeline")
    assert res.status_code == 200
    data = res.json()
    nav_titles = [n["title"] for n in data["categories"]["navigation"]]
    assert any("Deals Pipeline" in name for name in nav_titles)
