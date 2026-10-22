"""
Execution Runner for LangGraph Multi-Agent Orchestrator
Invokes the compiled workflow graph and formats the client response payload.
"""

from typing import Dict, Any, List, Optional
from agents.state import AgentState
from agents.orchestrator.graph import ORCHESTRATOR_GRAPH
from agents.session_store import update_session


def run_agent_orchestrator(
    prompt: str,
    session_id: str = "default_session",
    messages: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Execute the compiled LangGraph workflow.
    Returns the complete state with graph steps, action result, subagent output, and synthesized text.
    """
    initial_state: AgentState = {
        "user_prompt": prompt,
        "session_id": session_id,
        "messages": messages or [{"role": "user", "content": prompt}],
        "intent": None,
        "target_subagent": None,
        "action_type": None,
        "entities": {},
        "plan": [],
        "current_step_index": 0,
        "step_results": [],
        "context_data": {},
        "subagent_result": None,
        "subagent_results": [],
        "tool_result": None,
        "tool_results": [],
        "final_response": "",
        "confidence_score": 0.9,
        "active_node": "prompt_ingestion",
        "graph_steps": [],
        "telemetry": {},
    }

    final_state = ORCHESTRATOR_GRAPH.invoke(initial_state)

    # Persist multi-turn session state, conversational history, and active entities
    try:
        update_session(
            session_id=session_id,
            user_prompt=prompt,
            assistant_reply=final_state.get("final_response", ""),
            tool_results=final_state.get("tool_results", []),
            subagent_results=final_state.get("subagent_results", []),
            extracted_entities=final_state.get("entities", {}),
        )
    except Exception:
        pass

    return {
        "reply": final_state.get("final_response"),
        "intent": final_state.get("intent"),
        "target_subagent": final_state.get("target_subagent"),
        "action_type": final_state.get("action_type"),
        "subagent_result": final_state.get("subagent_result"),
        "subagent_results": final_state.get("subagent_results", []),
        "tool_result": final_state.get("tool_result"),
        "tool_results": final_state.get("tool_results", []),
        "graph_steps": final_state.get("graph_steps", []),
        "telemetry": final_state.get("telemetry", {}),
        "confidence_score": final_state.get("confidence_score", 0.92),
    }
