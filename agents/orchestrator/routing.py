"""
LangGraph Conditional Routing Logic for Multi-Agent Orchestrator
"""

from typing import Dict, Any
from agents.state import AgentState


def route_after_intent(state: AgentState) -> str:
    """Conditional router function for LangGraph branching."""
    intent = state.get("intent")
    if intent == "subagent":
        return "subagent_executor"
    elif intent == "crm_action":
        return "crm_action_executor"
    else:
        return "synthesizer"
