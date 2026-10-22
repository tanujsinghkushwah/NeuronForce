"""
Pytest integration for NeuronForce Autonomous Multi-Agent Evaluation Suite.
Parametrizes across all 15 benchmark scenarios to verify reliability of orchestrator,
CRM actions, specialist sub-agents, and sequential compound flows.
"""

import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.evals.dataset import EVAL_SCENARIOS, EvalScenario
from agents.evals.runner import run_eval_scenario


@pytest.fixture(autouse=True)
def mock_emails_in_evals(monkeypatch):
    """Ensure email sending is mocked during evaluation test runs."""
    from unittest.mock import MagicMock
    import resend
    import smtplib

    mock_send = MagicMock(return_value={"id": "mock_eval_resend_id"})
    monkeypatch.setattr(resend.Emails, "send", mock_send)

    mock_smtp_inst = MagicMock()
    mock_smtp_class = MagicMock(return_value=mock_smtp_inst)
    mock_smtp_inst.__enter__.return_value = mock_smtp_inst
    monkeypatch.setattr(smtplib, "SMTP", mock_smtp_class)

    yield


@pytest.mark.parametrize(
    "scenario",
    EVAL_SCENARIOS,
    ids=[s.id for s in EVAL_SCENARIOS],
)
def test_agent_eval_scenario(scenario: EvalScenario):
    """
    Execute each evaluation scenario through LangGraph and verify routing,
    execution steps, and synthesized results.
    """
    res = run_eval_scenario(scenario)
    assert res.passed, (
        f"Evaluation scenario '{scenario.id}' failed!\n"
        f"Errors: {res.errors}\n"
        f"Executed steps: {res.executed_steps}\n"
        f"Reply preview: {res.reply_preview}"
    )
