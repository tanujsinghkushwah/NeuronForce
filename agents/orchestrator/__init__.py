"""
NeuronForce Multi-Agent LangGraph Orchestrator Package
Decomposed into modular submodules:
- nodes: LangGraph node implementations
- routing: Branching conditions & intent edges
- graph: StateGraph construction and compilation
- runner: Workflow execution & result synthesis
"""

from agents.orchestrator.nodes import (
    node_prompt_ingestion,
    node_context_retrieval,
    node_intent_router,
    node_subagent_executor,
    node_crm_action_executor,
    node_synthesizer,
)
from agents.orchestrator.routing import route_after_intent
from agents.orchestrator.graph import build_orchestrator_graph, ORCHESTRATOR_GRAPH
from agents.orchestrator.runner import run_agent_orchestrator

__all__ = [
    "run_agent_orchestrator",
    "build_orchestrator_graph",
    "ORCHESTRATOR_GRAPH",
    "node_prompt_ingestion",
    "node_context_retrieval",
    "node_intent_router",
    "node_subagent_executor",
    "node_crm_action_executor",
    "node_synthesizer",
    "route_after_intent",
]
