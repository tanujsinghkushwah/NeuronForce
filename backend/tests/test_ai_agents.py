"""
Unit Tests for AI Agent Engine API
Tests autonomous agent execution (lead scoring, churn prediction, email draft, deal analysis),
cost/latency tracking, confidence scoring, and performance analytics.
"""

def test_execute_lead_scoring_agent(client):
    """Test AI agent executing lead scoring with confidence and cost tracking."""
    payload = {
        "task_type": "lead_scoring",
        "input_data": {
            "contact_name": "Dr. Aris Thorne",
            "company": "Neural Dynamics",
            "email_opens": 14,
            "page_visits": 28
        },
        "triggered_by": "test-runner"
    }
    response = client.post("/api/ai-agents/tasks", json=payload)
    assert response.status_code == 200
    task = response.json()
    assert task["id"] is not None
    assert task["task_type"] == "lead_scoring"
    assert task["status"] == "completed"
    assert "score" in task["output_data"]
    assert "factors" in task["output_data"]
    assert "recommendation" in task["output_data"]
    assert 0.0 <= task["confidence_score"] <= 1.0
    assert task["actual_cost"] > 0
    assert task["latency_ms"] > 0
    assert task["triggered_by"] == "test-runner"


def test_execute_churn_prediction_agent(client):
    """Test AI agent predicting churn risk."""
    payload = {
        "task_type": "churn_prediction",
        "input_data": {
            "account": "Enterprise Cloud Corp",
            "nps_score": 6,
            "tickets_last_30d": 9
        }
    }
    response = client.post("/api/ai-agents/tasks", json=payload)
    assert response.status_code == 200
    task = response.json()
    assert task["task_type"] == "churn_prediction"
    assert "at_risk_accounts" in task["output_data"]
    assert "total_revenue_at_risk" in task["output_data"]
    assert "recommended_interventions" in task["output_data"]
    assert len(task["output_data"]["at_risk_accounts"]) > 0


def test_execute_email_draft_agent(client):
    """Test AI agent generating personalized sales follow-up email."""
    payload = {
        "task_type": "email_draft",
        "input_data": {
            "recipient": "Sarah Chen",
            "context": "Follow-up after product demo"
        }
    }
    response = client.post("/api/ai-agents/tasks", json=payload)
    assert response.status_code == 200
    task = response.json()
    assert task["task_type"] == "email_draft"
    assert "subject" in task["output_data"]
    assert "body" in task["output_data"]


def test_ai_agent_stats_and_filtering(client):
    """Test listing AI tasks by task_type and verifying aggregate cost/performance stats."""
    # Execute two tasks
    client.post("/api/ai-agents/tasks", json={"task_type": "deal_analysis", "input_data": {"deal_id": 1}})
    client.post("/api/ai-agents/tasks", json={"task_type": "meeting_summary", "input_data": {"notes": "Call recap"}})

    # List tasks filtering by task_type
    filtered_res = client.get("/api/ai-agents/tasks?task_type=deal_analysis")
    assert filtered_res.status_code == 200
    tasks = filtered_res.json()
    assert len(tasks) >= 1
    assert all(t["task_type"] == "deal_analysis" for t in tasks)

    # Get stats
    stats_res = client.get("/api/ai-agents/stats")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["total_tasks"] >= 2
    assert stats["completed"] >= 2
    assert stats["total_cost"] >= 0.0
    assert "cost_efficiency" in stats
    assert "roi_estimate" in stats["cost_efficiency"]
    assert "time_saved_hours" in stats["cost_efficiency"]
