"""
NeuronForce LangGraph Workflow Graph Assembly
Compiles the StateGraph orchestrator connecting ingestion, retrieval, routing,
execution nodes, and synthesis.
"""

from typing import Any
from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.orchestrator.nodes import (
    node_prompt_ingestion,
    node_context_retrieval,
    node_intent_router,
    node_subagent_executor,
    node_crm_action_executor,
    node_synthesizer,
)
from agents.orchestrator.routing import route_after_intent, route_after_step


def build_orchestrator_graph() -> Any:
    """Build and compile the LangGraph StateGraph."""
    builder: Any = StateGraph(AgentState)  # type: ignore

    # Add Nodes
    builder.add_node("prompt_ingestion", node_prompt_ingestion)
    builder.add_node("context_retrieval", node_context_retrieval)
    builder.add_node("intent_router", node_intent_router)
    builder.add_node("subagent_executor", node_subagent_executor)
    builder.add_node("crm_action_executor", node_crm_action_executor)
    builder.add_node("synthesizer", node_synthesizer)

    # Add Edges
    builder.set_entry_point("prompt_ingestion")
    builder.add_edge("prompt_ingestion", "context_retrieval")
    builder.add_edge("context_retrieval", "intent_router")

    # Conditional Branching from Router
    builder.add_conditional_edges(
        "intent_router",
        route_after_intent,
        {
            "subagent_executor": "subagent_executor",
            "crm_action_executor": "crm_action_executor",
            "synthesizer": "synthesizer",
        },
    )

    # Conditional Branching after CRM Action (for multi-step workflows)
    builder.add_conditional_edges(
        "crm_action_executor",
        route_after_step,
        {
            "crm_action_executor": "crm_action_executor",
            "subagent_executor": "subagent_executor",
            "synthesizer": "synthesizer",
        },
    )

    # Conditional Branching after Subagent (for multi-step workflows)
    builder.add_conditional_edges(
        "subagent_executor",
        route_after_step,
        {
            "crm_action_executor": "crm_action_executor",
            "subagent_executor": "subagent_executor",
            "synthesizer": "synthesizer",
        },
    )

    # Final transition from synthesizer to END
    builder.add_edge("synthesizer", END)

    return builder.compile()


# Compiled graph singleton
ORCHESTRATOR_GRAPH = build_orchestrator_graph()
