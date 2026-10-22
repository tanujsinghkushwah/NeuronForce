"""
LangGraph Conditional Routing Logic for Multi-Agent Orchestrator
"""

from typing import Dict, Any
from agents.state import AgentState


def route_after_intent(state: AgentState) -> str:
    """Conditional router function for LangGraph branching from intent_router."""
    plan = state.get("plan") or []
    if plan:
        first_step = plan[0]
        step_type = first_step.get("type")
        if step_type == "crm_action" or first_step.get("action_type"):
            return "crm_action_executor"
        elif step_type == "subagent" or first_step.get("target_subagent"):
            return "subagent_executor"

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


def route_after_step(state: AgentState) -> str:
    """
    Conditional router function after step execution (CRM action or subagent).
    Advances to next step in multi-step plan, or routes to synthesizer once all steps complete.
    """
    plan = state.get("plan") or []
    idx = state.get("current_step_index", 0)

    if idx < len(plan):
        next_step = plan[idx]
        step_type = next_step.get("type")
        if step_type == "crm_action" or next_step.get("action_type"):
            return "crm_action_executor"
        elif step_type == "subagent" or next_step.get("target_subagent"):
            return "subagent_executor"

    # Backwards compatibility check
    if not plan and state.get("target_subagent") and not state.get("subagent_result"):
        return "subagent_executor"

    return "synthesizer"


# Backwards compatibility alias
route_after_crm_action = route_after_step
