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
    assert "ai_model" in stats


def test_openrouter_inference_and_dynamic_model(client, monkeypatch):
    """Test that OpenRouter API is called with custom OPENROUTER_MODEL and processed properly."""
    import httpx
    from app.config import settings

    custom_model = "anthropic/claude-3.5-sonnet"
    monkeypatch.setattr(settings, "OPENROUTER_API_KEY", "sk-or-test-mock-key")
    monkeypatch.setattr(settings, "OPENROUTER_MODEL", custom_model)

    mock_response_data = {
        "id": "gen-test-12345",
        "model": custom_model,
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": '{"score": 96, "tier": "hot", "factors": ["High engagement", "Decision maker"], "recommendation": "Book demo today", "icp_match": 0.95}'
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 150,
            "completion_tokens": 60,
            "total_tokens": 210
        }
    }

    recorded_requests = []
    orig_post = httpx.Client.post

    def mock_post(self, url, *args, **kwargs):
        if "openrouter.ai" in str(url):
            recorded_requests.append({"url": str(url), "json": kwargs.get("json"), "headers": kwargs.get("headers")})
            req = httpx.Request("POST", str(url))
            return httpx.Response(200, json=mock_response_data, request=req)
        return orig_post(self, url, *args, **kwargs)

    monkeypatch.setattr(httpx.Client, "post", mock_post)

    payload = {
        "task_type": "lead_scoring",
        "input_data": {"contact_name": "Satya Nadella", "company": "Microsoft"}
    }
    response = client.post("/api/ai-agents/tasks", json=payload)
    assert response.status_code == 200
    task = response.json()
    assert task["task_type"] == "lead_scoring"
    assert task["output_data"]["score"] == 96
    assert task["output_data"]["_meta"]["model"] == custom_model
    assert task["output_data"]["_meta"]["is_real_ai"] is True
    assert len(recorded_requests) == 1
    assert recorded_requests[0]["json"]["model"] == custom_model
    assert "Bearer sk-or-test-mock-key" in recorded_requests[0]["headers"]["Authorization"]


def test_ai_agents_chat_endpoint(client):
    """Test AI agents chat studio endpoint for general inquiry routing."""
    payload = {"message": "What is the total amount of deals currently in pipeline?"}
    response = client.post("/api/ai-agents/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["intent"] == "general"
    assert len(data.get("graph_steps", [])) >= 3
    assert data.get("confidence_score") is not None


def test_calendar_meeting_parser():
    """Test natural language calendar meeting date/time and range parsing."""
    import sys
    from pathlib import Path
    repo_root = Path(__file__).resolve().parent.parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    from agents.tools.calendar_tools import parse_meeting_datetime

    # Range test
    st, en, dur = parse_meeting_datetime("9 PM-10 PM 24 October")
    assert st.year == 2026
    assert st.month == 10
    assert st.day == 24
    assert st.hour == 21
    assert en.hour == 22
    assert dur == 60

    # Relative test
    st2, en2, dur2 = parse_meeting_datetime("tomorrow at 3pm")
    assert st2.hour == 15
    assert dur2 == 45

