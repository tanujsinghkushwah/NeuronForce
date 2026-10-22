"""
NeuronForce Multi-Agent LangGraph Orchestrator Nodes
Implements individual execution nodes for prompt ingestion, CRM retrieval,
intent routing, sub-agent delegation, CRM mutation execution, and synthesis.
"""

import time
import re
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

CURRENT_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = CURRENT_DIR.parent
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.state import AgentState, GraphNodeStep
from agents.context_retriever import retrieve_crm_context
from agents.subagents.llm_client import call_llm_json, call_llm_text
from agents.orchestrator.routing import route_after_intent, route_after_step

# Specialized Sub-Agents
from agents.subagents.lead_scoring import run_lead_scoring
from agents.subagents.email_drafter import run_email_drafter
from agents.subagents.deal_risk import run_deal_risk_analysis
from agents.subagents.churn_sentinel import run_churn_sentinel
from agents.subagents.meeting_summarizer import run_meeting_summarizer

# CRM Execution Tools
from agents.tools.calendar_tools import schedule_meeting, update_meeting
from agents.tools.deal_tools import create_deal, update_deal
from agents.tools.contact_tools import create_contact, update_contact
from agents.tools.campaign_tools import create_campaign
from agents.tools.email_tools import send_email_message

# ==============================================================================
# LangGraph Node Implementations
# ==============================================================================


def node_prompt_ingestion(state: AgentState) -> Dict[str, Any]:
    """Node 1: Prompt Ingestion and Sanitization"""
    start = time.time()
    prompt = state.get("user_prompt", "").strip()

    step: GraphNodeStep = {
        "node": "prompt_ingestion",
        "status": "completed",
        "label": "Prompt Ingestion",
        "latency_ms": max(1, int((time.time() - start) * 1000)),
        "summary": f"Ingested prompt ({len(prompt.split())} words)",
        "data": {"prompt": prompt, "session_id": state.get("session_id", "default")},
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    return {"active_node": "context_retrieval", "graph_steps": current_steps}


def node_context_retrieval(state: AgentState) -> Dict[str, Any]:
    """Node 2: Retrieve local DB data matching prompt entities"""
    start = time.time()
    prompt = state.get("user_prompt", "")
    context = retrieve_crm_context(prompt)
    elapsed_ms = max(5, int((time.time() - start) * 1000))

    step: GraphNodeStep = {
        "node": "context_retrieval",
        "status": "completed",
        "label": "CRM Context Retrieval",
        "latency_ms": elapsed_ms,
        "summary": context.get("summary", "Context retrieved from SQLite database"),
        "data": {
            "matching_contacts_count": len(context.get("matching_contacts", [])),
            "matching_deals_count": len(context.get("matching_deals", [])),
            "upcoming_events_count": len(context.get("upcoming_events", [])),
            "sample_contacts": [
                c.get("name") for c in context.get("matching_contacts", [])[:3]
            ],
            "sample_deals": [
                d.get("title") for d in context.get("matching_deals", [])[:3]
            ],
        },
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    return {
        "context_data": context,
        "active_node": "intent_router",
        "graph_steps": current_steps,
    }


def _fallback_offline_planner(
    prompt: str,
) -> tuple[str, Optional[str], Optional[str], Dict[str, Any], List[Dict[str, Any]]]:
    """
    Lightweight, resilient fallback planner invoked ONLY when the LLM service is offline or unconfigured.
    Supports single-step and multi-step plan decomposition.
    """
    lower = prompt.lower()
    intent = "general"
    action_type = None
    target_subagent = None
    entities: Dict[str, Any] = {}
    plan: List[Dict[str, Any]] = []

    # Extract email if present
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", prompt)
    if email_match:
        entities["email"] = email_match.group(0)

    # Question triggers guard
    question_triggers = [
        "what",
        "how many",
        "how much",
        "tell me",
        "show me",
        "list",
        "total",
        "calculate",
        "find",
        "who is",
        "which",
        "give me",
        "overview",
        "status of",
    ]
    is_inquiry = any(
        lower.startswith(q) or f" {q} " in f" {lower} " for q in question_triggers
    )

    detected_actions: List[str] = []
    detected_subagents: List[str] = []

    if not is_inquiry:
        if any(
            k in lower
            for k in [
                "create contact",
                "new contact",
                "add contact",
                "new lead",
                "add lead",
            ]
        ):
            detected_actions.append("create_contact")
        if any(
            k in lower for k in ["update contact", "modify contact", "update email"]
        ):
            detected_actions.append("update_contact")
        if any(
            k in lower
            for k in [
                "schedule",
                "book a",
                "calendar",
                "call with",
                "set up a meeting",
            ]
        ):
            detected_actions.append("schedule_meeting")
        if any(k in lower for k in ["create deal", "new deal", "add deal"]):
            detected_actions.append("create_deal")
        if any(
            k in lower
            for k in ["update deal", "move deal", "advance deal", "close deal"]
        ):
            detected_actions.append("update_deal")
        if any(
            k in lower for k in ["create campaign", "new campaign", "launch campaign"]
        ):
            detected_actions.append("create_campaign")

    # Subagent detection
    if any(
        k in lower
        for k in [
            "lead score",
            "score lead",
            "score the lead",
            "buyer intent",
            "icp score",
            "scoring",
        ]
    ):
        detected_subagents.append("lead_scoring")
    if any(
        k in lower
        for k in [
            "draft email",
            "send email",
            "write email",
            "specialized email",
            "personalized email",
            "sales email",
            "outreach email",
            "outreach message",
            "follow-up email",
        ]
    ) or (
        not is_inquiry
        and any(w in lower for w in ["draft", "outreach", "follow-up"])
        and "email" in lower
        and not any(k in lower for k in ["with email", "email is", "email id"])
    ):
        detected_subagents.append("email_draft")
    if any(
        k in lower
        for k in [
            "deal risk",
            "win probability",
            "deal health",
            "stalled deal",
            "risk analysis",
        ]
    ):
        detected_subagents.append("deal_risk")
    if any(
        k in lower for k in ["churn", "retention", "cancel subscription", "churn risk"]
    ):
        detected_subagents.append("churn_prediction")
    if any(
        k in lower
        for k in [
            "meeting notes",
            "summarize meeting",
            "meeting summary",
            "action items",
        ]
    ):
        detected_subagents.append("meeting_summary")

    # Name extraction fallback
    name_match = re.search(
        r"\b(?:named|for|of)\s+([A-Za-z]+(?:\s+[A-Za-z]+)*?)(?:\s+(?:with|to|email|at|and|worth)|$)",
        prompt,
        re.IGNORECASE,
    )
    if name_match:
        candidate = name_match.group(1).strip()
        if candidate.lower() not in (
            "email",
            "contact",
            "lead",
            "a",
            "the",
            "new",
            "closed_won",
            "closed_lost",
            "proposal",
        ):
            entities["name"] = candidate

    # Deal value extraction fallback
    amount_match = re.search(r"\$([0-9,]+(?:\.[0-9]{2})?)", prompt)
    if amount_match:
        try:
            entities["amount"] = float(amount_match.group(1).replace(",", ""))
        except Exception:
            pass

    # Company extraction fallback
    comp_match = re.search(
        r"(?:for|at)\s+([A-Za-z0-9]+(?:\s+[A-Za-z0-9]+)*?)(?:\s+(?:worth|in|stage|\$)|$)",
        prompt,
    )
    if comp_match:
        cand_comp = comp_match.group(1).strip()
        if cand_comp.lower() not in (
            "email",
            "contact",
            "lead",
            "a",
            "the",
            "new",
            "closed_won",
            "closed_lost",
            "proposal",
            "qualification",
        ):
            entities["company"] = cand_comp

    # Build ordered plan based on appearance position in prompt
    step_candidates = []
    for act in detected_actions:
        keys = [act.replace("_", " ")]
        if act == "schedule_meeting":
            keys = ["schedule", "meeting", "calendar"]
        elif act == "create_contact":
            keys = ["create contact", "add contact", "new contact"]
        pos_list = [lower.find(k) for k in keys if lower.find(k) != -1]
        pos = min(pos_list) if pos_list else 0

        step_ent = dict(entities)
        if act == "schedule_meeting":
            time_m = re.search(r"(tomorrow.*?)(?:\.|$)", prompt, re.IGNORECASE)
            if time_m:
                step_ent["start_time"] = time_m.group(1).strip()
            title_m = re.search(
                r"(?:for|with)\s+([A-Za-z\s&,]+?)(?:\s+for|\s+tomorrow|\s+at|\s+on|$)",
                prompt,
                re.IGNORECASE,
            )
            if title_m:
                step_ent["name"] = title_m.group(1).strip()
                step_ent["title"] = f"Meeting: {step_ent['name']}"
            step_ent["duration_minutes"] = 60

        step_candidates.append(
            (
                pos,
                {
                    "step_id": 0,
                    "type": "crm_action",
                    "action_type": act,
                    "target_subagent": None,
                    "description": f"Execute CRM action: {act.replace('_', ' ').title()}",
                    "entities": step_ent,
                },
            )
        )

    for sub in detected_subagents:
        keys = [sub.replace("_", " ")]
        if sub == "email_draft":
            keys = ["draft email", "send email", "personalized email", "email"]
        pos_list = [lower.find(k) for k in keys if lower.find(k) != -1]
        pos = min(pos_list) if pos_list else 0
        step_candidates.append(
            (
                pos,
                {
                    "step_id": 0,
                    "type": "subagent",
                    "action_type": None,
                    "target_subagent": sub,
                    "description": f"Execute Sub-Agent: {sub.replace('_', ' ').title()}",
                    "entities": dict(entities),
                },
            )
        )

    step_candidates.sort(key=lambda x: x[0])
    plan = [s[1] for s in step_candidates]
    for idx, s in enumerate(plan):
        s["step_id"] = idx + 1

    if len(plan) > 1:
        intent = "compound"
        action_type = next(
            (s["action_type"] for s in plan if s.get("action_type")), None
        )
        target_subagent = next(
            (s["target_subagent"] for s in plan if s.get("target_subagent")), None
        )
    elif len(plan) == 1:
        first = plan[0]
        if first.get("type") == "crm_action":
            intent = "crm_action"
            action_type = first.get("action_type")
        else:
            intent = "subagent"
            target_subagent = first.get("target_subagent")
    else:
        intent = "general"

    return intent, action_type, target_subagent, entities, plan


def node_intent_router(state: AgentState) -> Dict[str, Any]:
    """Node 3: Classify intent and formulate execution plan using structured LLM inference"""
    start = time.time()
    prompt = state.get("user_prompt", "")
    context = state.get("context_data", {})
    current_date_str = datetime.now().strftime("%A, %b %d, %Y")

    system_prompt = (
        "You are the central Autonomous Agent Orchestrator & Planner for NeuronForce Enterprise Sales CRM.\n"
        f"Reference current date: {current_date_str}.\n\n"
        "Analyze the user prompt and context to construct a structured, ordered multi-step execution plan.\n\n"
        "ROUTING CAPABILITIES:\n"
        "1. 'general': Read-only questions, pipeline metrics, totals, deal counts, status inquiries, or summaries.\n"
        "   - Read queries and inquiries MUST ALWAYS be routed to 'general'. Never route questions to write actions!\n\n"
        "2. 'crm_action': Direct single CRM database write/mutation actions:\n"
        "   - 'create_contact': Adding a new contact or lead.\n"
        "   - 'update_contact': Modifying contact details (email, status, lifecycle stage, job title).\n"
        "   - 'schedule_meeting': Booking or scheduling calendar events or calls.\n"
        "   - 'create_deal': Adding an opportunity/deal to the pipeline.\n"
        "   - 'update_deal': Advancing or moving deal stage, updating deal value, closing won/lost.\n"
        "   - 'create_campaign': Creating sales or marketing outreach campaign.\n\n"
        "3. 'subagent': Executing a single specialized AI agent workflow:\n"
        "   - 'email_draft': Drafting or dispatching personalized sales outreach, follow-ups, or cold pitch emails.\n"
        "   - 'lead_scoring': Calculating buyer intent score, ICP fit, qualification analysis, and priority tier.\n"
        "   - 'deal_risk': Analyzing win probability, stall risk, deal health, and risk mitigations.\n"
        "   - 'churn_prediction': Customer retention risk, usage drops, renewal likelihood, account health.\n"
        "   - 'meeting_summary': Extracting action items, key decisions, and takeaways from notes or calls.\n\n"
        "4. 'compound': Multi-step workflows requesting ANY combination of CRM actions and/or specialized sub-agents.\n"
        "   CRITICAL: If the user prompt requests multiple actions or steps, you MUST set route='compound' and "
        "   provide an ordered 'plan' array containing every step in sequence!\n\n"
        "   Multi-step examples:\n"
        "   - 'Create contact Tanuj (email: tanuj@...) then schedule a meeting for Tanuj and Sarah tomorrow 12-1 PM'\n"
        "     -> route: 'compound'\n"
        "     -> plan: [\n"
        '          {"step_id": 1, "type": "crm_action", "action_type": "create_contact", "entities": {"name": "Tanuj", "email": "tanuj@..."}},\n'
        '          {"step_id": 2, "type": "crm_action", "action_type": "schedule_meeting", "entities": {"title": "Meeting: Tanuj & Sarah", "name": "Tanuj, Sarah", "start_time": "tomorrow 12 PM-1 PM", "duration_minutes": 60}}\n'
        "        ]\n"
        "   - 'Create a contact for Alice (alice@...) and send her a specialized outreach email'\n"
        "     -> route: 'compound'\n"
        "     -> plan: [\n"
        '          {"step_id": 1, "type": "crm_action", "action_type": "create_contact", "entities": {"name": "Alice", "email": "alice@..."}},\n'
        '          {"step_id": 2, "type": "subagent", "target_subagent": "email_draft", "entities": {"name": "Alice", "email": "alice@..."}}\n'
        "        ]\n"
        "   - 'Add a new deal for Acme Corp ($80,000 in proposal stage) and evaluate deal risk'\n"
        "     -> route: 'compound'\n"
        "     -> plan: [\n"
        '          {"step_id": 1, "type": "crm_action", "action_type": "create_deal", "entities": {"company": "Acme Corp", "amount": 80000, "stage": "proposal"}},\n'
        '          {"step_id": 2, "type": "subagent", "target_subagent": "deal_risk", "entities": {"company": "Acme Corp"}}\n'
        "        ]\n\n"
        "ENTITY EXTRACTION GUIDELINES:\n"
        "- 'name': Person's name (e.g. 'Tanuj', 'Sarah Chen'). Do not include noise words like 'contact', 'new', 'lead'.\n"
        "- 'email': Valid email address (e.g. 'user@example.com').\n"
        "- 'company': Company name (e.g. 'SpaceY', 'Acme Corp').\n"
        "- 'job_title': Professional title or role.\n"
        "- 'amount': Numeric deal value (e.g. 50000).\n"
        "- 'stage': Pipeline stage (qualification, discovery, proposal, negotiation, closed_won, closed_lost).\n"
        "- 'title': Professional meeting or deal title (e.g. 'Meeting: Tanuj & Sarah Chen').\n"
        "- 'start_time': Parsed datetime ISO string or natural time (e.g. 'tomorrow 12 PM-1 PM').\n"
        "- 'end_time': Parsed datetime ISO string or natural time.\n"
        "- 'duration_minutes': Integer minutes.\n"
        "- 'attendees': List of emails or names.\n"
        "- 'subject': Email subject or campaign title.\n\n"
        "OUTPUT FORMAT (STRICT JSON ONLY):\n"
        "{\n"
        '  "route": "general" | "crm_action" | "subagent" | "compound",\n'
        '  "plan": [\n'
        "    {\n"
        '      "step_id": 1,\n'
        '      "type": "crm_action" | "subagent",\n'
        '      "action_type": "create_contact" | "update_contact" | "schedule_meeting" | "create_deal" | "update_deal" | "create_campaign" | null,\n'
        '      "target_subagent": "email_draft" | "lead_scoring" | "deal_risk" | "churn_prediction" | "meeting_summary" | null,\n'
        '      "description": "<string summary>",\n'
        '      "entities": {\n'
        '        "name": "<string or null>",\n'
        '        "email": "<string or null>",\n'
        '        "company": "<string or null>",\n'
        '        "job_title": "<string or null>",\n'
        '        "amount": <number or null>,\n'
        '        "stage": "<string or null>",\n'
        '        "title": "<string or null>",\n'
        '        "start_time": "<string or null>",\n'
        '        "end_time": "<string or null>",\n'
        '        "duration_minutes": <number or null>,\n'
        '        "subject": "<string or null>"\n'
        "      }\n"
        "    }\n"
        "  ],\n"
        '  "action_type": "<first action or null>",\n'
        '  "target_subagent": "<first subagent or null>",\n'
        '  "entities": {\n'
        '    "name": "<string or null>",\n'
        '    "email": "<string or null>",\n'
        '    "company": "<string or null>",\n'
        '    "job_title": "<string or null>",\n'
        '    "amount": <number or null>,\n'
        '    "stage": "<string or null>",\n'
        '    "title": "<string or null>",\n'
        '    "start_time": "<string or null>",\n'
        '    "end_time": "<string or null>",\n'
        '    "duration_minutes": <number or null>,\n'
        '    "subject": "<string or null>"\n'
        "  },\n"
        '  "reasoning": "<short explanation>"\n'
        "}"
    )

    llm_decision = call_llm_json(
        system_prompt,
        f"User Prompt: {prompt}\nContext Summary: {context.get('summary', '')}",
    )

    plan: List[Dict[str, Any]] = []

    if (
        llm_decision
        and "data" in llm_decision
        and isinstance(llm_decision["data"], dict)
        and llm_decision["data"].get("route")
        in ("general", "crm_action", "subagent", "compound")
    ):
        parsed = llm_decision["data"]
        route = parsed.get("route", "general")
        action_type = parsed.get("action_type")
        target_subagent = parsed.get("target_subagent")
        entities = (
            parsed.get("entities") if isinstance(parsed.get("entities"), dict) else {}
        )
        raw_plan = parsed.get("plan")

        # Normalize LLM confusion where a CRM action was assigned to target_subagent
        crm_action_names = (
            "schedule_meeting",
            "create_contact",
            "update_contact",
            "create_deal",
            "update_deal",
            "create_campaign",
        )
        subagent_names = (
            "email_draft",
            "lead_scoring",
            "deal_risk",
            "churn_prediction",
            "meeting_summary",
        )

        if target_subagent in crm_action_names:
            if not action_type:
                action_type = target_subagent
                target_subagent = None
            else:
                second_action = target_subagent
                target_subagent = None
                route = "compound"
                if not raw_plan or len(raw_plan) < 2:
                    raw_plan = [
                        {
                            "step_id": 1,
                            "type": "crm_action",
                            "action_type": action_type,
                            "entities": entities,
                        },
                        {
                            "step_id": 2,
                            "type": "crm_action",
                            "action_type": second_action,
                            "entities": entities,
                        },
                    ]

        # Parse and sanitize raw_plan
        if isinstance(raw_plan, list) and len(raw_plan) > 0:
            for idx, p_step in enumerate(raw_plan):
                if not isinstance(p_step, dict):
                    continue
                st_type = p_step.get("type")
                act = p_step.get("action_type")
                sub = p_step.get("target_subagent")

                if sub in crm_action_names:
                    st_type = "crm_action"
                    act = sub
                    sub = None
                elif act in subagent_names:
                    st_type = "subagent"
                    sub = act
                    act = None
                elif not st_type:
                    st_type = "crm_action" if act else "subagent"

                st_ent = {**entities, **(p_step.get("entities") or {})}
                plan.append(
                    {
                        "step_id": idx + 1,
                        "type": st_type,
                        "action_type": act,
                        "target_subagent": sub,
                        "description": p_step.get("description")
                        or f"Execute {act or sub}",
                        "entities": st_ent,
                    }
                )

        if not plan:
            if action_type and target_subagent:
                route = "compound"
                plan = [
                    {
                        "step_id": 1,
                        "type": "crm_action",
                        "action_type": action_type,
                        "entities": entities,
                    },
                    {
                        "step_id": 2,
                        "type": "subagent",
                        "target_subagent": target_subagent,
                        "entities": entities,
                    },
                ]
            elif action_type:
                plan = [
                    {
                        "step_id": 1,
                        "type": "crm_action",
                        "action_type": action_type,
                        "entities": entities,
                    }
                ]
            elif target_subagent:
                plan = [
                    {
                        "step_id": 1,
                        "type": "subagent",
                        "target_subagent": target_subagent,
                        "entities": entities,
                    }
                ]

        if len(plan) > 1:
            route = "compound"
            if not action_type:
                action_type = next(
                    (s["action_type"] for s in plan if s.get("action_type")), None
                )
            if not target_subagent:
                target_subagent = next(
                    (s["target_subagent"] for s in plan if s.get("target_subagent")),
                    None,
                )

        intent = route
    else:
        # Graceful fallback for offline tests or when LLM API is unconfigured
        intent, action_type, target_subagent, entities, plan = (
            _fallback_offline_planner(prompt)
        )

    elapsed_ms = max(10, int((time.time() - start) * 1000))

    if len(plan) > 1:
        step_names = [
            f"{s.get('action_type') or s.get('target_subagent') or 'step'}".replace(
                "_", " "
            ).title()
            for s in plan
        ]
        summary_text = f"Multi-Step Workflow: {' ➔ '.join(step_names)}"
    elif intent == "compound":
        summary_text = f"Compound Execution Plan: CRM {action_type} ➔ {str(target_subagent).replace('_', ' ').title()} Sub-Agent"
    elif intent == "subagent":
        summary_text = f"Routed to {(target_subagent or 'agent').replace('_', ' ').title()} Sub-Agent"
    elif intent == "crm_action":
        summary_text = f"Routed to CRM Action: {action_type}"
    else:
        summary_text = "Routed to Direct Synthesis"

    step: GraphNodeStep = {
        "node": "intent_router",
        "status": "completed",
        "label": "Intent Router & Semantic Planner",
        "latency_ms": elapsed_ms,
        "summary": summary_text,
        "data": {
            "intent": intent,
            "target_subagent": target_subagent,
            "action_type": action_type,
            "extracted_entities": entities,
            "plan_steps_count": len(plan),
            "plan": plan,
        },
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    temp_state: Any = {
        **state,
        "intent": intent,
        "target_subagent": target_subagent,
        "action_type": action_type,
        "entities": entities,
        "plan": plan,
        "current_step_index": 0,
    }
    next_node = route_after_intent(temp_state)

    return {
        "intent": intent,
        "target_subagent": target_subagent,
        "action_type": action_type,
        "entities": entities,
        "plan": plan,
        "current_step_index": 0,
        "step_results": [],
        "tool_results": [],
        "subagent_results": [],
        "active_node": next_node,
        "graph_steps": current_steps,
    }


def node_subagent_executor(state: AgentState) -> Dict[str, Any]:
    """Node 4a: Execute one of the 5 specialized agentic workflows in a multi-step sequence"""
    start = time.time()
    plan = list(state.get("plan") or [])
    current_idx = state.get("current_step_index", 0)
    step_results = list(state.get("step_results") or [])
    subagent_results = list(state.get("subagent_results") or [])

    step_info = plan[current_idx] if (plan and current_idx < len(plan)) else {}
    subagent = (
        step_info.get("target_subagent")
        or state.get("target_subagent")
        or "lead_scoring"
    )
    prompt = state.get("user_prompt", "")
    context = dict(state.get("context_data", {}))
    entities = {**state.get("entities", {}), **(step_info.get("entities") or {})}

    subagent_result: Dict[str, Any] = {}
    if subagent == "lead_scoring":
        subagent_result = run_lead_scoring(prompt, context)
    elif subagent == "email_draft":
        # Check context or preceding tool_result for target contact details
        target_contact = context.get("target_contact")
        if (
            not target_contact
            and state.get("tool_result")
            and isinstance(state["tool_result"], dict)
        ):
            target_contact = state["tool_result"].get("contact")

        drafter_context = dict(context)
        if target_contact and isinstance(target_contact, dict):
            drafter_context["target_contact"] = target_contact
            if target_contact.get("name"):
                drafter_context["recipient_name"] = target_contact["name"]
            if target_contact.get("email"):
                drafter_context["recipient_email"] = target_contact["email"]

        subagent_result = run_email_drafter(prompt, drafter_context)

        target_email = entities.get("email")
        if not target_email and target_contact:
            target_email = target_contact.get("email")
        if not target_email and drafter_context.get("recipient_email"):
            target_email = drafter_context.get("recipient_email")
        if not target_email:
            em = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", prompt)
            if em:
                target_email = em.group(0)
        if not target_email and context.get("matching_contacts"):
            target_email = context["matching_contacts"][0].get("email")

        recipient_name = (
            (target_contact.get("name") if target_contact else None)
            or subagent_result.get("recipient")
            or entities.get("name")
            or "Valued Contact"
        )
        if target_contact and target_contact.get("company"):
            comp_str = f" ({target_contact.get('company')})"
            if comp_str not in recipient_name:
                recipient_name = f"{recipient_name}{comp_str}"
        subagent_result["recipient"] = recipient_name

        if target_email:
            subagent_result["email_address"] = target_email
            contact_id = (target_contact.get("id") if target_contact else None) or (
                context.get("matching_contacts") or [{}]
            )[0].get("id")
            dispatch_res = send_email_message(
                to_email=target_email,
                subject=subagent_result.get("subject", "Personalized Sales Outreach"),
                body=subagent_result.get("body", ""),
                to_name=recipient_name,
                contact_id=contact_id,
            )
            subagent_result["dispatch_status"] = dispatch_res
            subagent_result["dispatch_info"] = dispatch_res.get("delivery_status")
    elif subagent == "deal_risk":
        subagent_result = run_deal_risk_analysis(prompt, context)
    elif subagent == "churn_prediction":
        subagent_result = run_churn_sentinel(prompt, context)
    elif subagent == "meeting_summary":
        subagent_result = run_meeting_summarizer(prompt, context)

    elapsed_ms = max(15, int((time.time() - start) * 1000))

    step: GraphNodeStep = {
        "node": f"subagent_{subagent}",
        "status": "completed",
        "label": f"{subagent.replace('_', ' ').title()} Sub-Agent",
        "latency_ms": elapsed_ms,
        "summary": (
            f"Personalized email {('delivered live via Resend' if subagent_result.get('dispatch_status', {}).get('sent_live') else 'logged in CRM activities')} for {subagent_result.get('email_address')}"
            if subagent == "email_draft" and subagent_result.get("email_address")
            else f"Completed {subagent.replace('_', ' ')} analysis"
        ),
        "data": subagent_result,
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    subagent_results.append(subagent_result)
    step_results.append(
        {"type": "subagent", "agent": subagent, "result": subagent_result}
    )
    next_idx = current_idx + 1

    temp_state: AgentState = {
        **state,
        "subagent_result": subagent_result,
        "subagent_results": subagent_results,
        "step_results": step_results,
        "current_step_index": next_idx,
    }
    next_node = route_after_step(temp_state)

    return {
        "subagent_result": subagent_result,
        "subagent_results": subagent_results,
        "step_results": step_results,
        "target_subagent": subagent,
        "current_step_index": next_idx,
        "context_data": context,
        "active_node": next_node,
        "graph_steps": current_steps,
    }


def node_crm_action_executor(state: AgentState) -> Dict[str, Any]:
    """Node 4b: Execute CRM database actions (Calendar, Deals, Contacts, Campaigns) in a multi-step sequence"""
    start = time.time()
    plan = list(state.get("plan") or [])
    current_idx = state.get("current_step_index", 0)
    step_results = list(state.get("step_results") or [])
    tool_results = list(state.get("tool_results") or [])

    step_info = plan[current_idx] if (plan and current_idx < len(plan)) else {}
    action = (
        step_info.get("action_type") or state.get("action_type") or "schedule_meeting"
    )
    prompt = state.get("user_prompt", "")
    entities = {**state.get("entities", {}), **(step_info.get("entities") or {})}
    context = dict(state.get("context_data", {}))

    tool_result: Dict[str, Any] = {
        "success": False,
        "action": action,
        "message": "Unknown action",
    }

    # 1. Calendar Action
    if action == "schedule_meeting":
        # Formulate clean, professional meeting title
        title = entities.get("title") or entities.get("subject")
        if not title or any(
            cmd in title.lower()
            for cmd in [
                "schedule a meeting",
                "book a meeting",
                "set up a meeting",
                "meeting: schedule",
            ]
        ):
            names = entities.get("name")
            if names:
                title = f"Meeting: {names}"
            elif context.get("target_contact") and context.get("matching_contacts"):
                target_n = context["target_contact"].get("name")
                other_n = context["matching_contacts"][0].get("name")
                title = f"Meeting: {target_n} & {other_n}"
            elif context.get("matching_contacts"):
                names_str = " & ".join(
                    [c["name"] for c in context["matching_contacts"][:2]]
                )
                title = f"Meeting: {names_str}"
            else:
                title = "Executive Sales Alignment Meeting"

        start_time = entities.get("start_time") or entities.get("date_time")
        end_time = entities.get("end_time")
        duration = entities.get("duration_minutes")
        try:
            duration_mins = int(duration) if duration else None
        except Exception:
            duration_mins = None

        # Build clean attendees list
        raw_attendees = entities.get("attendees") or []
        if isinstance(raw_attendees, str):
            raw_attendees = [a.strip() for a in raw_attendees.split(",") if a.strip()]

        attendees = []
        for a in raw_attendees:
            clean_email = str(a).strip().replace(" ", "")
            if "@" in clean_email and clean_email not in attendees:
                attendees.append(clean_email)

        # Include email from target_contact created in prior step
        if context.get("target_contact") and context["target_contact"].get("email"):
            tc_email = str(context["target_contact"]["email"]).strip().replace(" ", "")
            if "@" in tc_email and tc_email not in attendees:
                attendees.append(tc_email)

        if entities.get("email"):
            ent_email = str(entities["email"]).strip().replace(" ", "")
            if "@" in ent_email and ent_email not in attendees:
                attendees.append(ent_email)

        # Look up names in CRM Contacts database
        names_to_lookup = []
        if entities.get("name"):
            for part in re.split(r"[,&/]| and ", str(entities["name"])):
                p_clean = part.strip()
                if p_clean and p_clean.lower() not in (
                    "meeting",
                    "schedule",
                    "tomorrow",
                    "today",
                ):
                    names_to_lookup.append(p_clean)

        # Also extract proper capitalized names from prompt
        for word in re.findall(r"\b[A-Z][a-z]+\b", prompt):
            if word.lower() not in (
                "create",
                "then",
                "schedule",
                "meeting",
                "contact",
                "new",
                "tomorrow",
                "today",
                "pm",
                "am",
            ):
                if word not in names_to_lookup:
                    names_to_lookup.append(word)

        from app.database import SessionLocal
        from app.models.contact import Contact

        db = SessionLocal()
        matched_contact_id = None
        try:
            for cand_name in names_to_lookup:
                c_row = (
                    db.query(Contact)
                    .filter(
                        (Contact.first_name.ilike(f"%{cand_name}%"))
                        | (Contact.last_name.ilike(f"%{cand_name}%"))
                    )
                    .first()
                )
                if c_row:
                    if not matched_contact_id and hasattr(c_row, "id"):
                        matched_contact_id = int(getattr(c_row, "id"))
                    if c_row.email:
                        c_email = str(c_row.email).strip().replace(" ", "")
                        if "@" in c_email and c_email not in attendees:
                            attendees.append(c_email)
        except Exception:
            pass
        finally:
            db.close()

        if not attendees and context.get("matching_contacts"):
            attendees = [
                c.get("email") for c in context["matching_contacts"] if c.get("email")
            ][:2]

        if not attendees:
            attendees = ["team@neuronforce.ai"]

        raw_cid: Any = (
            context.get("target_contact", {}).get("id")
            or matched_contact_id
            or (context.get("matching_contacts", [{}])[0].get("id"))
        )
        contact_id_for_event: Optional[int] = int(raw_cid) if raw_cid else None

        tool_result = schedule_meeting(
            title=title,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration_mins,
            attendees=attendees,
            contact_id=contact_id_for_event,
        )
        if tool_result.get("success") and tool_result.get("event"):
            context["target_event"] = tool_result["event"]

    # 2. Create Deal Action
    elif action == "create_deal":
        title = (
            entities.get("subject")
            or f"Deal: {entities.get('company') or 'New Opportunity'}"
        )
        raw_amount = entities.get("amount") or 150000.0
        try:
            value = float(raw_amount)
        except Exception:
            value = 150000.0
        company = entities.get("company") or "Enterprise Client"
        stage = entities.get("stage") or "prospecting"
        tool_result = create_deal(
            title=title, value=value, company=company, stage=stage
        )
        if tool_result.get("success") and tool_result.get("deal"):
            context["target_deal"] = tool_result["deal"]

    # 3. Update Deal Action
    elif action == "update_deal":
        company = entities.get("company") or entities.get("subject") or prompt
        stage = entities.get("stage")
        raw_amount = entities.get("amount")
        deal_value: Optional[float] = float(raw_amount) if raw_amount else None
        tool_result = update_deal(
            deal_identifier=company, stage=stage, value=deal_value
        )
        if tool_result.get("success") and tool_result.get("deal"):
            context["target_deal"] = tool_result["deal"]

    # 4. Create Contact Action
    elif action == "create_contact":
        name = entities.get("name")
        if not name:
            named_m = re.search(
                r"\bnamed\s+([A-Za-z]+(?:\s+[A-Za-z]+)*?)(?:\s+(?:with|email|at|from|and)|$)",
                prompt,
                re.IGNORECASE,
            )
            if named_m:
                name = named_m.group(1).strip()
        if not name:
            name = "Alex Taylor"

        parts = name.split()
        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

        email = entities.get("email")
        if not email:
            em = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", prompt)
            if em:
                email = em.group(0)
            else:
                email = f"{first_name.lower()}.{last_name.lower().replace(' ', '.') if last_name else 'contact'}@example.com"

        company = entities.get("company") or ""
        if str(company).lower() in ("null", "none"):
            company = ""

        tool_result = create_contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            company=company,
        )
        if tool_result.get("success") and tool_result.get("contact"):
            context["target_contact"] = tool_result["contact"]
            context["recipient_name"] = tool_result["contact"].get("name")
            context["recipient_email"] = tool_result["contact"].get("email")
            # Also prepend to matching_contacts for subsequent steps
            m_contacts = list(context.get("matching_contacts", []))
            m_contacts.insert(0, tool_result["contact"])
            context["matching_contacts"] = m_contacts

    # 5. Update Contact Action
    elif action == "update_contact":
        name = entities.get("name")
        email = entities.get("email")

        # Fallback regex extraction if entities missed them
        if not email:
            em = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", prompt)
            if em:
                email = em.group(0)

        if not name:
            nm = re.search(
                r"(?:for|of)\s+([A-Za-z\s]+?)\s+(?:to|\b)",
                prompt,
                re.IGNORECASE,
            )
            if nm:
                candidate = nm.group(1).strip()
                if candidate.lower() not in (
                    "email",
                    "contact",
                    "lead",
                    "a",
                    "the",
                ):
                    name = candidate
        if not name:
            name = entities.get("identifier") or prompt

        stage = entities.get("stage")
        tool_result = update_contact(identifier=name, email=email, lead_status=stage)
        if tool_result.get("success") and tool_result.get("contact"):
            context["target_contact"] = tool_result["contact"]
            context["recipient_name"] = tool_result["contact"].get("name")
            context["recipient_email"] = tool_result["contact"].get("email")

    # 6. Create Campaign Action
    elif action == "create_campaign":
        name = entities.get("subject") or f"Campaign: {prompt[:40]}"
        subject = (
            entities.get("subject") or "Accelerate Enterprise Growth with NeuronForce"
        )
        tool_result = create_campaign(
            name=name,
            subject=subject,
            target_segment=entities.get("company") or "enterprise_leads",
        )

    elapsed_ms = max(10, int((time.time() - start) * 1000))

    step: GraphNodeStep = {
        "node": f"action_{action}",
        "status": "completed",
        "label": f"CRM Action: {action.replace('_', ' ').title()}",
        "latency_ms": elapsed_ms,
        "summary": tool_result.get("message", "Executed CRM action"),
        "data": tool_result,
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    tool_results.append(tool_result)
    step_results.append({"type": "crm_action", "action": action, "result": tool_result})
    next_idx = current_idx + 1

    temp_state: AgentState = {
        **state,
        "tool_result": tool_result,
        "tool_results": tool_results,
        "step_results": step_results,
        "current_step_index": next_idx,
    }
    next_node = route_after_step(temp_state)

    return {
        "tool_result": tool_result,
        "tool_results": tool_results,
        "step_results": step_results,
        "action_type": action,
        "current_step_index": next_idx,
        "context_data": context,
        "active_node": next_node,
        "graph_steps": current_steps,
    }


def node_synthesizer(state: AgentState) -> Dict[str, Any]:
    """Node 5: Synthesize conversational answer and assemble client-ready payloads"""
    start = time.time()
    prompt = state.get("user_prompt", "")
    intent = state.get("intent", "general")
    subagent = state.get("target_subagent")
    subagent_result = state.get("subagent_result")
    subagent_results = list(state.get("subagent_results") or [])
    tool_result = state.get("tool_result")
    tool_results = list(state.get("tool_results") or [])
    step_results = list(state.get("step_results") or [])

    final_response = ""
    confidence = 0.92

    # Case A: Multi-Action Workflow (e.g. Create Contact + Schedule Meeting)
    if len(tool_results) > 1:
        sections = []
        for i, tr in enumerate(tool_results, 1):
            act = tr.get("action")
            if act == "create_contact" and tr.get("contact"):
                c = tr["contact"]
                sections.append(
                    f"### {i}. 👤 Contact Created\n"
                    f"- **Name**: **{c.get('name')}**\n"
                    f"- **Email**: `{c.get('email')}`\n"
                    f"- **Company**: {c.get('company') or 'Enterprise'}\n"
                    f"- **Status**: Registered in CRM database"
                )
            elif act == "update_contact" and tr.get("contact"):
                c = tr["contact"]
                sections.append(
                    f"### {i}. 👤 Contact Updated\n"
                    f"- **Name**: **{c.get('name')}**\n"
                    f"- **Email**: `{c.get('email')}`\n"
                    f"- **Status**: Profile updated"
                )
            elif act == "schedule_meeting" and tr.get("event"):
                ev = tr["event"]
                time_str = (
                    tr.get("message", "").split(" on ")[-1]
                    if " on " in tr.get("message", "")
                    else f"{ev.get('start_time')} to {ev.get('end_time')}"
                )
                attendees_str = ", ".join(
                    [f"`{a}`" for a in (ev.get("attendees") or [])]
                )
                sections.append(
                    f"### {i}. 📅 Meeting Scheduled\n"
                    f"- **Title**: **{ev.get('title')}**\n"
                    f"- **Date & Time**: {time_str}\n"
                    f"- **Attendees**: {attendees_str or 'Team'}\n"
                    f"- **Location**: {ev.get('location') or 'Google Meet / Zoom'}"
                )
            elif act in ("create_deal", "update_deal") and tr.get("deal"):
                d = tr["deal"]
                sections.append(
                    f"### {i}. 💼 Deal {'Created' if act == 'create_deal' else 'Updated'}\n"
                    f"- **Title**: **{d.get('title')}**\n"
                    f"- **Value**: `${float(d.get('value', 0)):,.2f}`\n"
                    f"- **Stage**: `{d.get('stage')}`"
                )
            elif act == "create_campaign" and tr.get("campaign"):
                cmp = tr["campaign"]
                sections.append(
                    f"### {i}. 📢 Campaign Launched\n"
                    f"- **Name**: **{cmp.get('name')}**\n"
                    f"- **Subject**: `{cmp.get('subject')}`"
                )
            else:
                sections.append(f"### {i}. {tr.get('message', 'Action executed')}")

        final_response = (
            f"**Multi-Step Workflow Completed Successfully!**\n\n"
            + "\n\n".join(sections)
            + "\n\nAll pipeline models, activity logs, and calendar views have been synchronized with the latest database state."
        )
        confidence = 0.98

    # Case B: Compound CRM Action + Subagent (e.g. create contact + draft email)
    elif tool_result and tool_result.get("success") and subagent_result:
        subj = subagent_result.get("subject", "")
        body = subagent_result.get("body", "")
        recipient = subagent_result.get("recipient", "Recipient")
        email_addr = subagent_result.get("email_address") or (
            tool_result.get("contact", {}).get("email")
        )
        cta = subagent_result.get("call_to_action", "")
        dispatch_info = subagent_result.get("dispatch_info", "")

        final_response = (
            f"**Action Completed Successfully!**\n\n"
            f"{tool_result.get('message')}\n\n"
            f"### ✉️ Hyper-Personalized Sales Email Generated for **{recipient}** ({email_addr})\n\n"
            f"**Subject:** `{subj}`\n\n"
            f"---\n\n"
            f"{body}\n\n"
            f"---\n\n"
            f"**Strategic CTA**: {cta}\n\n"
            f"*{dispatch_info or 'Email logged in CRM activity history.'}*"
        )
        confidence = 0.98

    elif tool_result and tool_result.get("success"):
        final_response = (
            f"**Action Completed Successfully!**\n\n"
            f"{tool_result.get('message', 'The requested CRM action has been executed.')}\n\n"
            f"All pipeline models and calendar views have been synchronized with the latest database state."
        )
        confidence = 0.98

    elif tool_result and not tool_result.get("success"):
        final_response = (
            f"⚠️ **Action Notification**: {tool_result.get('message') or 'Unable to complete the requested update.'}\n\n"
            f"Please verify the details or existing records in the CRM database."
        )
        confidence = 0.85

    elif subagent_result:
        subagent_key = (subagent or "").lower()
        if not subagent_key:
            if "lead_name" in subagent_result or "score" in subagent_result:
                subagent_key = "lead_scoring"
            elif "subject" in subagent_result and "body" in subagent_result:
                subagent_key = "email_draft"
            elif (
                "win_probability" in subagent_result
                or "key_risk_factors" in subagent_result
            ):
                subagent_key = "deal_risk"
            elif (
                "overall_churn_risk" in subagent_result
                or "at_risk_accounts" in subagent_result
            ):
                subagent_key = "churn_prediction"
            elif (
                "meeting_title" in subagent_result or "action_items" in subagent_result
            ):
                subagent_key = "meeting_summary"
        if "lead" in subagent_key:
            name = subagent_result.get("lead_name", "Lead")
            score = subagent_result.get("score", 90)
            tier = str(subagent_result.get("tier", "hot")).upper()
            recom = subagent_result.get("recommendation", "")
            factors = "\n".join([f"• {f}" for f in subagent_result.get("factors", [])])
            final_response = (
                f"### 🎯 Lead Scoring Intelligence for **{name}**\n\n"
                f"- **Buyer Intent Score**: `{score}/100` ({tier} Priority)\n"
                f"- **ICP Alignment**: `{round(float(subagent_result.get('icp_match_score', 0.9)) * 100)}%`\n"
                f"- **Recommendation**: {recom}\n\n"
                f"**Key Behavioral & Firmographic Signals:**\n{factors}"
            )
            confidence = 0.95

        elif "email" in subagent_key:
            subj = subagent_result.get("subject", "")
            body = subagent_result.get("body", "")
            recipient = subagent_result.get("recipient", "Recipient")
            cta = subagent_result.get("call_to_action", "")
            final_response = (
                f"### ✉️ Hyper-Personalized Sales Email for **{recipient}**\n\n"
                f"**Subject:** `{subj}`\n\n"
                f"---\n\n"
                f"{body}\n\n"
                f"---\n"
                f"**Strategic CTA**: {cta}\n"
                f"*Ready to review and dispatch directly via Marketing Cloud.*"
            )
            confidence = 0.94

        elif "deal" in subagent_key or "risk" in subagent_key:
            title = subagent_result.get("deal_title", "Deal")
            prob = round(float(subagent_result.get("win_probability", 0.75)) * 100)
            risk = str(subagent_result.get("risk_tier", "medium")).upper()
            risks = "\n".join(
                [f"• {r}" for r in subagent_result.get("key_risk_factors", [])]
            )
            mitigations = "\n".join(
                [f"• {m}" for m in subagent_result.get("mitigation_actions", [])]
            )
            final_response = (
                f"### 🛡️ Deal Risk & Probability Assessment: **{title}**\n\n"
                f"- **Win Probability**: `{prob}%`\n"
                f"- **Risk Exposure Level**: `{risk}`\n"
                f"- **Timeline**: {subagent_result.get('decision_timeline', 'Closing soon')}\n\n"
                f"**Critical Risk Indicators:**\n{risks}\n\n"
                f"**Recommended Mitigations:**\n{mitigations}"
            )
            confidence = 0.93

        elif "churn" in subagent_key:
            arr = float(subagent_result.get("total_arr_at_risk", 180000.0))
            playbooks = "\n".join(
                [
                    f"• {p}"
                    for p in subagent_result.get("recommended_retention_playbook", [])
                ]
            )
            final_response = (
                f"### ⚠️ Customer Churn Sentinel Report\n\n"
                f"- **Overall Risk**: `{str(subagent_result.get('overall_churn_risk', 'moderate')).upper()}`\n"
                f"- **Total ARR at Risk**: `${arr:,.2f}`\n"
                f"- **Preventable Recovery Ratio**: `{round(float(subagent_result.get('preventable_percentage', 0.8)) * 100)}%`\n\n"
                f"**High-Priority Retention Playbook:**\n{playbooks}"
            )
            confidence = 0.91

        elif "meeting" in subagent_key or "summary" in subagent_key:
            title = subagent_result.get("meeting_title", "Meeting")
            exec_sum = subagent_result.get("executive_summary", "")
            decisions = "\n".join(
                [f"• {d}" for d in subagent_result.get("key_decisions", [])]
            )
            actions = "\n".join(
                [
                    f"• **{a.get('task')}** — Assigned to *{a.get('owner')}* (Due: {a.get('due_date')})"
                    for a in subagent_result.get("action_items", [])
                ]
            )
            final_response = (
                f"### 📝 Executive Meeting Summary: **{title}**\n\n"
                f"{exec_sum}\n\n"
                f"**Key Decisions:**\n{decisions or '• Consensus achieved on strategic scope.'}\n\n"
                f"**Action Items:**\n{actions}\n\n"
                f"**CRM Impact**: {subagent_result.get('crm_impact', 'Updated deal stages and activity log.')}"
            )
            confidence = 0.96
        else:
            final_response = f"Agent completed analysis: {subagent_result}"

    else:
        # General response synthesis using live CRM database metrics and records
        context = state.get("context_data", {})
        pipeline = context.get("pipeline_metrics", {})
        deals_overview = pipeline.get("all_deals_overview", [])
        deals_by_stage = pipeline.get("deals_by_stage", {})

        stage_breakdown_str = "\n".join(
            [
                f"  - **{stg.replace('_', ' ').title()}**: {info['count']} deals totaling `${info['total_value']:,.2f}`"
                for stg, info in deals_by_stage.items()
            ]
        )

        crm_metrics_context = (
            f"Live CRM Database Metrics:\n"
            f"- Total Deals in Pipeline: {pipeline.get('total_deals_count', len(context.get('matching_deals', [])))}\n"
            f"- Total Pipeline Value: ${pipeline.get('total_pipeline_value', 0):,.2f}\n"
            f"- Breakdown by Stage:\n{stage_breakdown_str or '  - None'}\n"
            f"- Total Contacts in CRM: {pipeline.get('total_contacts_count', len(context.get('matching_contacts', [])))}\n"
            f"- Upcoming Calendar Events: {len(context.get('upcoming_events', []))}\n"
            f"- Active Campaigns: {len(context.get('recent_campaigns', []))}\n"
            f"\nDeals in Pipeline:\n"
            + "\n".join(
                [
                    f"  * {d.get('title')} ({d.get('company')}): ${float(d.get('value', 0) or 0):,.2f} [Stage: {d.get('stage')}]"
                    for d in deals_overview[:20]
                ]
            )
        )

        sys_prompt = (
            "You are NeuronForce Autonomous AI Sales Studio. Answer the user's inquiry directly, accurately, "
            "and insightfully based strictly on the live CRM database context provided.\n"
            "Highlight exact dollar amounts, deal counts, and stage distribution in clean GitHub markdown.\n"
            "Keep the response executive, concise, and structured."
        )
        user_prompt = f"User Request: {prompt}\n\n{crm_metrics_context}"
        llm_reply = call_llm_text(sys_prompt, user_prompt)

        if llm_reply:
            final_response = llm_reply
            confidence = 0.96
        else:
            if any(
                k in prompt.lower()
                for k in ["contact", "who", "people", "team", "directory"]
            ):
                contacts = context.get("matching_contacts", [])
                contact_lines = "\n".join(
                    [
                        f"- **{c.get('name')}** ({c.get('email')}) — {c.get('job_title') or c.get('role', 'Executive')} at **{c.get('company', 'Enterprise')}**"
                        for c in contacts[:10]
                    ]
                )
                final_response = (
                    f"### 👥 Key Contacts Directory\n\n"
                    f"{contact_lines or 'No matching contacts found in CRM.'}\n\n"
                    f"*Retrieved directly from live CRM database context.*"
                )
                confidence = 0.92
            else:
                total_val = pipeline.get("total_pipeline_value", 0)
                total_cnt = pipeline.get("total_deals_count", 0)
                final_response = (
                    f"### 📊 Live CRM Pipeline Overview\n\n"
                    f"- **Total Deals in Pipeline**: `{total_cnt}`\n"
                    f"- **Total Pipeline Value**: `${total_val:,.2f}`\n\n"
                    f"**Breakdown by Stage:**\n{stage_breakdown_str or 'No active deals.'}"
                )
                confidence = 0.90

    elapsed_ms = max(5, int((time.time() - start) * 1000))

    step: GraphNodeStep = {
        "node": "synthesizer",
        "status": "completed",
        "label": "Response Synthesis & Telemetry",
        "latency_ms": elapsed_ms,
        "summary": "Synthesized executive response with telemetry payload",
        "data": {
            "confidence": confidence,
            "response_length": len(final_response),
        },
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    # Compute overall telemetry
    total_latency = sum(s.get("latency_ms", 0) for s in current_steps)
    model_name = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash-lite")

    return {
        "final_response": final_response,
        "confidence_score": confidence,
        "tool_result": tool_result or (tool_results[-1] if tool_results else None),
        "tool_results": tool_results,
        "subagent_result": subagent_result
        or (subagent_results[-1] if subagent_results else None),
        "subagent_results": subagent_results,
        "step_results": step_results,
        "active_node": "END",
        "graph_steps": current_steps,
        "telemetry": {
            "model": model_name,
            "total_latency_ms": total_latency,
            "confidence": confidence,
            "cost": 0.0004,
        },
    }
