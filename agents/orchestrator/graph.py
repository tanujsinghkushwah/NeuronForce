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
from agents.orchestrator.routing import route_after_intent


def build_orchestrator_graph():
    """Build and compile the LangGraph StateGraph."""
    builder: Any = StateGraph(AgentState)

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

    # Return to Synthesizer
    builder.add_edge("subagent_executor", "synthesizer")
    builder.add_edge("crm_action_executor", "synthesizer")
    builder.add_edge("synthesizer", END)

    return builder.compile()


# Compiled graph singleton
ORCHESTRATOR_GRAPH = build_orchestrator_graph()
