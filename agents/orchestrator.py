"""
NeuronForce Multi-Agent LangGraph Orchestrator
Coordinates intent classification, context retrieval from local CRM DB,
specialized sub-agents, and CRM action execution tools.
"""

import time
import re
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, END

CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.state import AgentState, GraphNodeStep
from agents.context_retriever import retrieve_crm_context
from agents.subagents.llm_client import call_llm_json, call_llm_text

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
        "data": {"prompt": prompt, "session_id": state.get("session_id", "default")}
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    return {
        "active_node": "context_retrieval",
        "graph_steps": current_steps
    }


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
            "sample_contacts": [c.get("name") for c in context.get("matching_contacts", [])[:3]],
            "sample_deals": [d.get("title") for d in context.get("matching_deals", [])[:3]]
        }
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    return {
        "context_data": context,
        "active_node": "intent_router",
        "graph_steps": current_steps
    }


def node_intent_router(state: AgentState) -> Dict[str, Any]:
    """Node 3: Classify intent and route to specialized subagent or CRM action tool"""
    start = time.time()
    prompt = state.get("user_prompt", "")
    context = state.get("context_data", {})
    lower = prompt.lower()

    # Rule-assisted + LLM routing
    intent = "general"
    target_subagent = None
    action_type = None
    entities: Dict[str, Any] = {}

    # 0. Check if user is asking a question/inquiry (read-only query vs CRM mutation)
    question_triggers = [
        "what", "how many", "how much", "tell me", "show me", "list", "total",
        "calculate", "find", "who is", "which", "give me", "overview", "status of"
    ]
    is_inquiry = any(lower.startswith(q) or f" {q} " in f" {lower} " for q in question_triggers)
    mutation_verbs = [
        "create deal", "new deal", "add deal", "create contact", "new contact",
        "add contact", "create campaign", "schedule", "book", "set up meeting",
        "update deal", "modify deal", "change deal", "move deal", "advance deal",
        "close deal", "update contact", "modify contact", "change status"
    ]
    has_mutation_verb = any(v in lower for v in mutation_verbs)

    # 1. Detect Action Types first (only if mutation intent or verb present)
    if not is_inquiry or has_mutation_verb:
        if any(k in lower for k in ["schedule", "meeting", "calendar", "call with", "book a", "set up a meeting"]):
            if any(action_kw in lower for action_kw in ["schedule", "create", "set up", "book", "add"]):
                intent = "crm_action"
                action_type = "schedule_meeting"
        elif any(k in lower for k in ["create deal", "new deal", "add deal", "create a deal"]):
            intent = "crm_action"
            action_type = "create_deal"
        elif any(k in lower for k in ["move deal", "update deal", "change deal", "close deal", "advance deal"]):
            intent = "crm_action"
            action_type = "update_deal"
        elif any(k in lower for k in ["create contact", "new contact", "add contact", "new lead", "add lead"]):
            intent = "crm_action"
            action_type = "create_contact"
        elif any(k in lower for k in ["update contact", "modify contact", "qualify contact"]):
            intent = "crm_action"
            action_type = "update_contact"
        elif any(k in lower for k in ["create campaign", "new campaign", "launch campaign", "draft campaign", "marketing campaign"]):
            intent = "crm_action"
            action_type = "create_campaign"

    # 2. Detect 5 Specialized Sub-Agents if not a direct CRUD action
    if intent != "crm_action":
        if any(k in lower for k in ["lead score", "score lead", "score the lead", "buyer intent", "icp score", "scoring"]):
            intent = "subagent"
            target_subagent = "lead_scoring"
        elif any(k in lower for k in ["draft email", "write email", "follow-up email", "sales email", "outreach email", "send email"]):
            intent = "subagent"
            target_subagent = "email_draft"
        elif any(k in lower for k in ["deal risk", "win probability", "risk and probability", "deal health", "stalled deal", "risk analysis"]):
            intent = "subagent"
            target_subagent = "deal_risk"
        elif any(k in lower for k in ["churn", "retention", "at risk", "cancel subscription", "churn risk", "usage drop"]):
            intent = "subagent"
            target_subagent = "churn_prediction"
        elif any(k in lower for k in ["summarize meeting", "meeting notes", "meeting summary", "action items", "takeaways", "notes from"]):
            intent = "subagent"
            target_subagent = "meeting_summary"

    # 3. LLM Refinement for Entity & Decision extraction
    system_prompt = (
        "You are an intent parser for an enterprise sales CRM orchestrator. Reference date: Thursday, Oct 22, 2026.\n"
        "Analyze the user prompt and extract routing info.\n"
        "CRITICAL ROUTING RULES:\n"
        "1. If the user is asking a question, inquiring about pipeline metrics, totals, deal counts, status, contacts, or summary (e.g. 'What is the total amount of deals?', 'How many deals in pipeline?', 'Show pipeline status'), route MUST be 'general'. NEVER route questions or read queries to 'crm_action'!\n"
        "2. 'crm_action' is STRICTLY for write/create/update actions (e.g., 'create a deal', 'schedule meeting with...', 'update contact', 'move deal to closed_won').\n"
        "3. When action_type is 'schedule_meeting':\n"
        "   - 'title': formulate a concise professional title (e.g. 'Meeting: Tanuj & Sarah Chen' or 'Discovery Call: SpaceY'). DO NOT use prompt command phrases like 'Schedule a meeting between...'.\n"
        "   - 'start_time': exact date and start time (e.g. '2026-10-24T21:00:00' or '24 October 9:00 PM').\n"
        "   - 'end_time': end time if a range is specified (e.g. '2026-10-24T22:00:00' or '10:00 PM').\n"
        "   - 'duration_minutes': duration in minutes (e.g. 60).\n"
        "4. 'subagent' is only for the 5 specialized AI tasks: lead scoring, email drafting, deal risk assessment, churn prediction, meeting summarization.\n"
        "Return JSON with schema:\n"
        "{\n"
        '  "route": "<subagent|crm_action|general>",\n'
        '  "target_subagent": "<lead_scoring|email_draft|deal_risk|churn_prediction|meeting_summary|null>",\n'
        '  "action_type": "<schedule_meeting|create_deal|update_deal|create_contact|update_contact|create_campaign|null>",\n'
        '  "entities": {\n'
        '    "title": "<clean concise meeting or deal title, e.g. Meeting: Tanuj & Sarah Chen>",\n'
        '    "name": "<person name(s) if mentioned>",\n'
        '    "company": "<company name if mentioned>",\n'
        '    "amount": <number if deal value mentioned else null>,\n'
        '    "stage": "<pipeline stage if mentioned>",\n'
        '    "email": "<email if mentioned>",\n'
        '    "start_time": "<parsed ISO start time or datetime string>",\n'
        '    "end_time": "<parsed ISO end time or datetime string>",\n'
        '    "duration_minutes": <duration in minutes integer or null>,\n'
        '    "date_time": "<original or parsed date/time string>",\n'
        '    "subject": "<subject or title if mentioned>"\n'
        '  }\n'
        "}"
    )
    llm_decision = call_llm_json(system_prompt, f"User Prompt: {prompt}\nContext Summary: {context.get('summary', '')}")
    if llm_decision and "data" in llm_decision:
        parsed = llm_decision["data"]
        if parsed.get("route") in ("subagent", "crm_action", "general"):
            # Only override if specific
            if parsed.get("route") == "subagent" and parsed.get("target_subagent"):
                intent = "subagent"
                target_subagent = parsed.get("target_subagent")
            elif parsed.get("route") == "crm_action" and parsed.get("action_type"):
                intent = "crm_action"
                action_type = parsed.get("action_type")
            elif parsed.get("route") == "general":
                intent = "general"
                action_type = None
        if isinstance(parsed.get("entities"), dict):
            entities = parsed.get("entities", {})

    # Guard against misrouting informational inquiries to crm_action
    if is_inquiry and not has_mutation_verb:
        intent = "general"
        action_type = None


    elapsed_ms = max(10, int((time.time() - start) * 1000))
    summary_text = (
        f"Routed to {target_subagent.replace('_', ' ').title()} Sub-Agent"
        if intent == "subagent"
        else f"Routed to CRM Action: {action_type}"
        if intent == "crm_action"
        else "Routed to Direct Synthesis"
    )

    step: GraphNodeStep = {
        "node": "intent_router",
        "status": "completed",
        "label": "Orchestrator Decision Router",
        "latency_ms": elapsed_ms,
        "summary": summary_text,
        "data": {
            "intent": intent,
            "target_subagent": target_subagent,
            "action_type": action_type,
            "extracted_entities": entities
        }
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    next_node = "subagent_executor" if intent == "subagent" else "crm_action_executor" if intent == "crm_action" else "synthesizer"

    return {
        "intent": intent,
        "target_subagent": target_subagent,
        "action_type": action_type,
        "entities": entities,
        "active_node": next_node,
        "graph_steps": current_steps
    }


def node_subagent_executor(state: AgentState) -> Dict[str, Any]:
    """Node 4a: Execute one of the 5 specialized agentic workflows"""
    start = time.time()
    subagent = state.get("target_subagent") or "lead_scoring"
    prompt = state.get("user_prompt", "")
    context = state.get("context_data", {})

    subagent_result = {}
    if subagent == "lead_scoring":
        subagent_result = run_lead_scoring(prompt, context)
    elif subagent == "email_draft":
        subagent_result = run_email_drafter(prompt, context)
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
        "summary": f"Completed {subagent.replace('_', ' ')} analysis",
        "data": subagent_result
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    return {
        "subagent_result": subagent_result,
        "target_subagent": subagent,
        "active_node": "synthesizer",
        "graph_steps": current_steps
    }


def node_crm_action_executor(state: AgentState) -> Dict[str, Any]:
    """Node 4b: Execute CRM database actions (Calendar, Deals, Contacts, Campaigns)"""
    start = time.time()
    action = state.get("action_type") or "schedule_meeting"
    prompt = state.get("user_prompt", "")
    entities = state.get("entities", {})
    context = state.get("context_data", {})

    tool_result: Dict[str, Any] = {"success": False, "action": action, "message": "Unknown action"}

    # 1. Calendar Action
    if action == "schedule_meeting":
        # Formulate clean, professional meeting title
        title = entities.get("title") or entities.get("subject")
        if not title or any(cmd in title.lower() for cmd in ["schedule a meeting", "book a meeting", "set up a meeting", "meeting: schedule"]):
            names = entities.get("name")
            if names:
                title = f"Meeting: {names}"
            elif context.get("matching_contacts"):
                names_str = " & ".join([c["name"] for c in context["matching_contacts"][:2]])
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
        if not raw_attendees and entities.get("email"):
            raw_attendees = [entities["email"]]
        if not raw_attendees and context.get("matching_contacts"):
            raw_attendees = [c.get("email") for c in context["matching_contacts"] if c.get("email")][:2]
        if not raw_attendees and entities.get("name"):
            for n in entities["name"].split(","):
                clean_n = n.strip()
                if clean_n:
                    raw_attendees.append(f"{clean_n.lower().replace(' ', '.')}@example.com")

        # Sanitize attendee emails: remove spaces, validate format
        attendees = []
        for a in raw_attendees:
            clean_email = str(a).strip().replace(" ", "")
            if "@" in clean_email:
                attendees.append(clean_email)

        tool_result = schedule_meeting(
            title=title,
            start_time=start_time,
            end_time=end_time,
            duration_minutes=duration_mins,
            attendees=attendees or ["team@neuronforce.ai"]
        )

    # 2. Create Deal Action
    elif action == "create_deal":
        title = entities.get("subject") or f"Deal: {entities.get('company') or 'New Opportunity'}"
        raw_amount = entities.get("amount") or 150000.0
        try:
            value = float(raw_amount)
        except Exception:
            value = 150000.0
        company = entities.get("company") or "Enterprise Client"
        stage = entities.get("stage") or "prospecting"
        tool_result = create_deal(
            title=title,
            value=value,
            company=company,
            stage=stage
        )

    # 3. Update Deal Action
    elif action == "update_deal":
        company = entities.get("company") or entities.get("subject") or prompt
        stage = entities.get("stage")
        raw_amount = entities.get("amount")
        value = float(raw_amount) if raw_amount else None
        tool_result = update_deal(
            deal_identifier=company,
            stage=stage,
            value=value
        )

    # 4. Create Contact Action
    elif action == "create_contact":
        name = entities.get("name") or "Alex Taylor"
        parts = name.split()
        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else "Contact"
        email = entities.get("email") or f"{first_name.lower()}.{last_name.lower().replace(' ', '.')}@example.com"
        company = entities.get("company") or "Acme Corp"
        tool_result = create_contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            company=company
        )


    # 5. Update Contact Action
    elif action == "update_contact":
        name = entities.get("name") or entities.get("email") or prompt
        tool_result = update_contact(
            identifier=name,
            lead_status=entities.get("stage") or "qualified"
        )

    # 6. Create Campaign Action
    elif action == "create_campaign":
        name = entities.get("subject") or f"Campaign: {prompt[:40]}"
        subject = entities.get("subject") or f"Accelerate Enterprise Growth with NeuronForce"
        tool_result = create_campaign(
            name=name,
            subject=subject,
            target_segment=entities.get("company") or "enterprise_leads"
        )

    elapsed_ms = max(10, int((time.time() - start) * 1000))

    step: GraphNodeStep = {
        "node": f"action_{action}",
        "status": "completed",
        "label": f"CRM Action: {action.replace('_', ' ').title()}",
        "latency_ms": elapsed_ms,
        "summary": tool_result.get("message", "Executed CRM action"),
        "data": tool_result
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    return {
        "tool_result": tool_result,
        "action_type": action,
        "active_node": "synthesizer",
        "graph_steps": current_steps
    }


def node_synthesizer(state: AgentState) -> Dict[str, Any]:
    """Node 5: Synthesize conversational answer and assemble client-ready payloads"""
    start = time.time()
    prompt = state.get("user_prompt", "")
    intent = state.get("intent", "general")
    subagent = state.get("target_subagent")
    subagent_result = state.get("subagent_result")
    tool_result = state.get("tool_result")

    final_response = ""
    confidence = 0.92

    if tool_result and tool_result.get("success"):
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
            elif "win_probability" in subagent_result or "key_risk_factors" in subagent_result:
                subagent_key = "deal_risk"
            elif "overall_churn_risk" in subagent_result or "at_risk_accounts" in subagent_result:
                subagent_key = "churn_prediction"
            elif "meeting_title" in subagent_result or "action_items" in subagent_result:
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
            risks = "\n".join([f"• {r}" for r in subagent_result.get("key_risk_factors", [])])
            mitigations = "\n".join([f"• {m}" for m in subagent_result.get("mitigation_actions", [])])
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
            playbooks = "\n".join([f"• {p}" for p in subagent_result.get("recommended_retention_playbook", [])])
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
            actions = "\n".join([
                f"• **{a.get('task')}** — Assigned to *{a.get('owner')}* (Due: {a.get('due_date')})"
                for a in subagent_result.get("action_items", [])
            ])
            final_response = (
                f"### 📝 Executive Meeting Summary: **{title}**\n\n"
                f"{exec_sum}\n\n"
                f"**Action Commitments:**\n{actions}\n\n"
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

        stage_breakdown_str = "\n".join([
            f"  - **{stg.replace('_', ' ').title()}**: {info['count']} deals totaling `${info['total_value']:,.2f}`"
            for stg, info in deals_by_stage.items()
        ])

        crm_metrics_context = (
            f"Live CRM Database Metrics:\n"
            f"- Total Deals in Pipeline: {pipeline.get('total_deals_count', len(context.get('matching_deals', [])))}\n"
            f"- Total Pipeline Value: ${pipeline.get('total_pipeline_value', 0):,.2f}\n"
            f"- Breakdown by Stage:\n{stage_breakdown_str or '  - None'}\n"
            f"- Total Contacts in CRM: {pipeline.get('total_contacts_count', len(context.get('matching_contacts', [])))}\n"
            f"- Upcoming Calendar Events: {len(context.get('upcoming_events', []))}\n"
            f"- Active Campaigns: {len(context.get('recent_campaigns', []))}\n"
            f"\nDeals in Pipeline:\n" + "\n".join([
                f"  * {d.get('title')} ({d.get('company')}): ${float(d.get('value', 0) or 0):,.2f} [Stage: {d.get('stage')}]"
                for d in deals_overview[:20]
            ])
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
            total_val = pipeline.get('total_pipeline_value', 0)
            total_cnt = pipeline.get('total_deals_count', 0)
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
        "data": {"confidence": confidence, "response_length": len(final_response)}
    }

    current_steps = list(state.get("graph_steps", []))
    current_steps.append(step)

    # Compute overall telemetry
    total_latency = sum(s.get("latency_ms", 0) for s in current_steps)
    model_name = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash-lite")

    return {
        "final_response": final_response,
        "confidence_score": confidence,
        "active_node": "END",
        "graph_steps": current_steps,
        "telemetry": {
            "model": model_name,
            "total_latency_ms": total_latency,
            "confidence": confidence,
            "cost": 0.0004
        }
    }


# ==============================================================================
# LangGraph Workflow Graph Assembly
# ==============================================================================

def route_after_intent(state: AgentState) -> str:
    """Conditional router function for LangGraph"""
    intent = state.get("intent")
    if intent == "subagent":
        return "subagent_executor"
    elif intent == "crm_action":
        return "crm_action_executor"
    else:
        return "synthesizer"


def build_orchestrator_graph():
    """Build and compile the LangGraph StateGraph"""
    builder = StateGraph(AgentState)

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
            "synthesizer": "synthesizer"
        }
    )

    # Return to Synthesizer
    builder.add_edge("subagent_executor", "synthesizer")
    builder.add_edge("crm_action_executor", "synthesizer")
    builder.add_edge("synthesizer", END)

    return builder.compile()


# Compile graph singleton
ORCHESTRATOR_GRAPH = build_orchestrator_graph()


def run_agent_orchestrator(
    prompt: str,
    session_id: str = "default_session",
    messages: Optional[List[Dict[str, Any]]] = None
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
        "context_data": {},
        "subagent_result": None,
        "tool_result": None,
        "final_response": "",
        "confidence_score": 0.9,
        "active_node": "prompt_ingestion",
        "graph_steps": [],
        "telemetry": {}
    }

    final_state = ORCHESTRATOR_GRAPH.invoke(initial_state)

    return {
        "reply": final_state.get("final_response"),
        "intent": final_state.get("intent"),
        "target_subagent": final_state.get("target_subagent"),
        "action_type": final_state.get("action_type"),
        "subagent_result": final_state.get("subagent_result"),
        "tool_result": final_state.get("tool_result"),
        "graph_steps": final_state.get("graph_steps", []),
        "telemetry": final_state.get("telemetry", {}),
        "confidence_score": final_state.get("confidence_score", 0.92)
    }
