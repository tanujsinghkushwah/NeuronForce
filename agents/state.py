"""
NeuronForce Multi-Agent State Definition for LangGraph
"""

from typing import TypedDict, List, Dict, Any, Optional


class GraphNodeStep(TypedDict):
    node: str
    status: str  # 'idle' | 'running' | 'completed' | 'skipped' | 'failed'
    label: str
    latency_ms: int
    summary: str
    data: Optional[Dict[str, Any]]


class AgentState(TypedDict):
    """
    State passed through all LangGraph nodes in the orchestration workflow.
    """

    # User message & conversation
    user_prompt: str
    session_id: str
    messages: List[Dict[str, Any]]

    # Routing and classification
    intent: Optional[
        str
    ]  # 'lead_scoring' | 'email_draft' | 'deal_risk' | 'churn_prediction' | 'meeting_summary' | 'crm_action' | 'general'
    target_subagent: Optional[
        str
    ]  # 'lead_scoring' | 'email_draft' | 'deal_risk' | 'churn_prediction' | 'meeting_summary'
    action_type: Optional[
        str
    ]  # 'schedule_meeting' | 'create_deal' | 'update_deal' | 'create_contact' | 'update_contact' | 'create_campaign' | 'update_campaign'
    entities: Dict[str, Any]

    # Data Context retrieved from DB / APIs
    context_data: Dict[str, Any]

    # Sub-agent and tool results
    subagent_result: Optional[Dict[str, Any]]
    tool_result: Optional[Dict[str, Any]]

    # Final synthesized answer
    final_response: str
    confidence_score: float

    # Execution telemetry & visualization steps
    active_node: str
    graph_steps: List[GraphNodeStep]
    telemetry: Dict[str, Any]
