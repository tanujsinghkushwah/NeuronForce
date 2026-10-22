"""
LangGraph Conditional Routing Logic for Multi-Agent Orchestrator
"""

from typing import Dict, Any
from agents.state import AgentState


def route_after_intent(state: AgentState) -> str:
    """Conditional router function for LangGraph branching from intent_router."""
    intent = state.get("intent")
    action_type = state.get("action_type")
    target_subagent = state.get("target_subagent")

    # If the LLM planned a CRM mutation (or compound workflow), execute the CRM action first
    if action_type or intent in ("crm_action", "compound"):
        return "crm_action_executor"
    elif target_subagent or intent == "subagent":
        return "subagent_executor"
    else:
        return "synthesizer"


def route_after_crm_action(state: AgentState) -> str:
    """Conditional router function after CRM action execution."""
    # If a specialist subagent was planned as part of a compound workflow (e.g. email outreach),
    # route sequentially to subagent_executor so it executes as an observable, first-class graph node.
    if state.get("target_subagent"):
        return "subagent_executor"
    return "synthesizer"
