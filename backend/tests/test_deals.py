"""
Unit Tests for Deals & Pipeline API
Tests deal creation, contact associations, pipeline grouping, updates, and deletion.
"""


def test_create_and_get_deal(client):
    """Test creating a deal with associated contacts and retrieving it."""
    # First create a contact to associate
    c_res = client.post(
        "/api/contacts",
        json={
            "first_name": "Alexander",
            "last_name": "Pierce",
            "company": "Stark Industries",
            "email": "pierce@stark.com",
        },
    )
    contact_id = c_res.json()["id"]

    deal_payload = {
        "title": "Stark Enterprise AI Platform",
        "value": 150000.0,
        "currency": "USD",
        "stage": "proposal",
        "probability": 60,
        "company": "Stark Industries",
        "owner": "Alex Rivera",
        "priority": "high",
        "tags": ["enterprise", "ai"],
        "contact_ids": [contact_id],
    }
    create_res = client.post("/api/deals", json=deal_payload)
    assert create_res.status_code == 200
    deal = create_res.json()
    assert deal["id"] is not None
    assert deal["title"] == "Stark Enterprise AI Platform"
    assert deal["value"] == 150000.0
    assert deal["stage"] == "proposal"
    assert len(deal["contacts"]) == 1
    assert deal["contacts"][0]["id"] == contact_id

    # Retrieve by ID
    get_res = client.get(f"/api/deals/{deal['id']}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == "Stark Enterprise AI Platform"


def test_deals_pipeline_view(client):
    """Test GET /api/deals/pipeline correctly categorizes stages and computes totals."""
    # Create deals in different stages
    client.post(
        "/api/deals",
        json={
            "title": "Deal In Prospecting",
            "value": 10000.0,
            "stage": "prospecting",
            "probability": 10,
        },
    )
    client.post(
        "/api/deals",
        json={
            "title": "Deal In Proposal",
            "value": 50000.0,
            "stage": "proposal",
            "probability": 50,
        },
    )

    pipeline_res = client.get("/api/deals/pipeline")
    assert pipeline_res.status_code == 200
    pipeline = pipeline_res.json()
    assert "stages" in pipeline
    assert "total_value" in pipeline
    assert "weighted_value" in pipeline

    # Verify stages present
    stages = pipeline["stages"]
    assert "prospecting" in stages
    assert "proposal" in stages
    assert "closed_won" in stages

    # Check that total_value includes active deals (10k + 50k = 60k)
    assert pipeline["total_value"] >= 60000.0
    # Weighted: 10000 * 0.10 + 50000 * 0.50 = 1000 + 25000 = 26000
    assert pipeline["weighted_value"] >= 26000.0


def test_update_deal_stage(client):
    """Test updating deal stage and probability."""
    create_res = client.post(
        "/api/deals",
        json={
            "title": "Negotiation Deal",
            "value": 80000.0,
            "stage": "proposal",
            "probability": 50,
        },
    )
    deal_id = create_res.json()["id"]

    update_res = client.put(
        f"/api/deals/{deal_id}", json={"stage": "negotiation", "probability": 80}
    )
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["stage"] == "negotiation"
    assert updated["probability"] == 80


def test_delete_deal(client):
    """Test deleting a deal."""
    create_res = client.post(
        "/api/deals", json={"title": "Temporary Deal", "value": 5000.0}
    )
    deal_id = create_res.json()["id"]

    del_res = client.delete(f"/api/deals/{deal_id}")
    assert del_res.status_code == 200
    assert del_res.json()["message"] == "Deal deleted"

    get_res = client.get(f"/api/deals/{deal_id}")
    assert get_res.status_code == 404


def test_deal_not_found_errors(client):
    """Test 404s for non-existent deals."""
    assert client.get("/api/deals/99999").status_code == 404
    assert client.put("/api/deals/99999", json={"title": "Test"}).status_code == 404
    assert client.delete("/api/deals/99999").status_code == 404
