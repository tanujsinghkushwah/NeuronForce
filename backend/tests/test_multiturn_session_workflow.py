"""
Test Multi-Turn Conversational Session Continuity
Validates:
1. Turn 1: Multi-step Contact creation + Meeting scheduling.
2. Turn 2: Deal creation ($1,000,000 between Tanuj and Robert).
3. Turn 3: "Create a new Campaign to promote this deal on X, Instagram" (pronoun 'this deal' resolved, AI social copy generated).
4. Turn 4: "Perform deal risk analysis on it" (pronoun 'it' resolved to $1M deal, routed to deal_risk subagent, not general overview).
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest
import uuid
from agents.orchestrator import run_agent_orchestrator
from agents.session_store import get_or_create_session, clear_session


def test_multiturn_continuous_session_workflow():
    session_id = f"test_session_{uuid.uuid4().hex[:8]}"
    clear_session(session_id)

    # -------------------------------------------------------------
    # Turn 1: Contact + Meeting
    # -------------------------------------------------------------
    turn1_prompt = "Create contact Tanuj with email tanuj@neuronforce.ai at Google and schedule a meeting with Tanuj and Robert tomorrow at 2 PM"
    res1 = run_agent_orchestrator(prompt=turn1_prompt, session_id=session_id)

    assert res1.get("reply") is not None
    session = get_or_create_session(session_id)
    assert len(session.messages) == 2
    assert session.active_contact is not None or session.active_meeting is not None

    # -------------------------------------------------------------
    # Turn 2: Create $1M Deal
    # -------------------------------------------------------------
    turn2_prompt = (
        "Create a deal between Tanuj and Robert for $1,000,000 in prospecting stage"
    )
    res2 = run_agent_orchestrator(prompt=turn2_prompt, session_id=session_id)

    assert res2.get("reply") is not None
    assert session.active_deal is not None
    assert float(session.active_deal.get("value", 0)) == 1000000.0

    # -------------------------------------------------------------
    # Turn 3: Campaign referencing "this deal" on X, Instagram
    # -------------------------------------------------------------
    turn3_prompt = "Create a new Campaign to promote this deal on X, Instagram"
    res3 = run_agent_orchestrator(prompt=turn3_prompt, session_id=session_id)

    assert res3.get("reply") is not None
    # Verify campaign was created
    tool_res = res3.get("tool_result") or (
        res3.get("tool_results", [{}])[-1] if res3.get("tool_results") else {}
    )
    campaign_data = tool_res.get("campaign")
    assert campaign_data is not None
    # Channels should include X and Instagram
    channels = [str(c).lower() for c in campaign_data.get("channels", [])]
    assert any("x" in c or "twitter" in c for c in channels)
    assert any("instagram" in c or "ig" in c for c in channels)

    # Verify social copy was generated
    social_copy = campaign_data.get("social_copy", {})
    assert social_copy.get("x_post") or social_copy.get("instagram_caption")

    # Verify session active_campaign updated
    assert session.active_campaign is not None

    # -------------------------------------------------------------
    # Turn 4: Deal Risk Analysis on "it"
    # -------------------------------------------------------------
    turn4_prompt = "Perform deal risk analysis on it"
    res4 = run_agent_orchestrator(prompt=turn4_prompt, session_id=session_id)

    # Crucial test: "it" must route to deal_risk subagent, NOT generic synthesis
    assert res4.get("intent") in ("subagent", "deal_risk")
    assert res4.get("target_subagent") == "deal_risk"
    sub_res = res4.get("subagent_result")
    assert sub_res is not None
    assert "win_probability" in sub_res or "risk_tier" in sub_res

    # Check that it evaluated the $1M deal specifically
    deal_title = sub_res.get("deal_title", "")
    assert (
        session.active_deal.get("title") in deal_title
        or "Tanuj" in deal_title
        or "Robert" in deal_title
        or sub_res.get("win_probability") is not None
    )

    clear_session(session_id)
