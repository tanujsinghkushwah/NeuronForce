"""
Unit Tests for Contacts API
Tests CRUD operations, searching, filtering, and validation.
"""

def test_create_and_get_contact(client):
    """Test creating a contact and retrieving it by ID."""
    payload = {
        "first_name": "Elena",
        "last_name": "Rostova",
        "email": "elena.rostova@acme.ai",
        "phone": "+1-555-0199",
        "company": "Acme AI Corp",
        "job_title": "VP of Engineering",
        "department": "Engineering",
        "industry": "Artificial Intelligence",
        "lead_status": "qualified",
        "lead_score": 85,
        "source": "referral",
        "tags": ["enterprise", "decision-maker"],
        "notes": "Met at AI Summit 2026."
    }
    create_res = client.post("/api/contacts", json=payload)
    assert create_res.status_code == 200
    contact = create_res.json()
    assert contact["id"] is not None
    assert contact["first_name"] == "Elena"
    assert contact["last_name"] == "Rostova"
    assert contact["lead_status"] == "qualified"
    assert contact["lead_score"] == 85
    contact_id = contact["id"]

    # Retrieve by ID
    get_res = client.get(f"/api/contacts/{contact_id}")
    assert get_res.status_code == 200
    retrieved = get_res.json()
    assert retrieved["id"] == contact_id
    assert retrieved["email"] == "elena.rostova@acme.ai"
    assert "enterprise" in retrieved["tags"]


def test_list_contacts_with_search_and_filter(client):
    """Test listing contacts with search text and lead status filtering."""
    # Seed 2 contacts
    client.post("/api/contacts", json={
        "first_name": "Marcus",
        "last_name": "Vance",
        "email": "marcus@vancetech.io",
        "company": "Vance Technologies",
        "lead_status": "new",
        "lead_score": 30
    })
    client.post("/api/contacts", json={
        "first_name": "Sarah",
        "last_name": "Connor",
        "email": "sarah@cyberdyne.org",
        "company": "Cyberdyne Systems",
        "lead_status": "converted",
        "lead_score": 95
    })

    # List all
    all_res = client.get("/api/contacts")
    assert all_res.status_code == 200
    contacts = all_res.json()
    assert len(contacts) >= 2

    # Search by query
    search_res = client.get("/api/contacts?search=Cyberdyne")
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert len(search_data) == 1
    assert search_data[0]["company"] == "Cyberdyne Systems"

    # Filter by lead_status
    filter_res = client.get("/api/contacts?status=converted")
    assert filter_res.status_code == 200
    filter_data = filter_res.json()
    assert all(c["lead_status"] == "converted" for c in filter_data)


def test_update_contact(client):
    """Test updating fields on an existing contact."""
    create_res = client.post("/api/contacts", json={
        "first_name": "Dev",
        "last_name": "Patel",
        "email": "dev@fintech.co",
        "company": "Fintech Global",
        "lead_status": "new",
        "lead_score": 40
    })
    contact_id = create_res.json()["id"]

    update_payload = {
        "job_title": "Chief Technology Officer",
        "lead_status": "qualified",
        "lead_score": 90
    }
    update_res = client.put(f"/api/contacts/{contact_id}", json=update_payload)
    assert update_res.status_code == 200
    updated = update_res.json()
    assert updated["job_title"] == "Chief Technology Officer"
    assert updated["lead_status"] == "qualified"
    assert updated["lead_score"] == 90
    assert updated["first_name"] == "Dev"  # unchanged


def test_delete_contact(client):
    """Test deleting a contact."""
    create_res = client.post("/api/contacts", json={
        "first_name": "Delete",
        "last_name": "Me",
        "email": "delete.me@test.com"
    })
    contact_id = create_res.json()["id"]

    # Delete
    del_res = client.delete(f"/api/contacts/{contact_id}")
    assert del_res.status_code == 200
    assert del_res.json()["message"] == "Contact deleted"

    # Verify 404
    get_res = client.get(f"/api/contacts/{contact_id}")
    assert get_res.status_code == 404


def test_contact_not_found_errors(client):
    """Test 404 responses for non-existent contacts."""
    assert client.get("/api/contacts/99999").status_code == 404
    assert client.put("/api/contacts/99999", json={"first_name": "Test"}).status_code == 404
    assert client.delete("/api/contacts/99999").status_code == 404
