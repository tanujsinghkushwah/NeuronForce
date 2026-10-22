"""
Global Search API Router
Provides multi-entity unified searching across contacts, deals, AI agents,
tickets, campaigns, and platform navigation with multi-token fuzzy ranking.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import re

from app.database import get_db
from app.models.contact import Contact
from app.models.deal import Deal
from app.models.ticket import Ticket
from app.models.campaign import Campaign
from app.models.agent import AIAgentTask
from app.models.user import User

router = APIRouter(prefix="/api/search", tags=["Global Search"])

STOP_WORDS = {
    "and",
    "or",
    "the",
    "in",
    "with",
    "&",
    "a",
    "an",
    "to",
    "for",
    "of",
    "on",
    "at",
    "by",
    "from",
}

BUILTIN_AGENTS = [
    {
        "id": "lead_scoring",
        "name": "Lead Scoring Agent",
        "description": "Predicts buyer intent using multi-factor signals (engagement, ICP alignment, tech stack).",
        "category": "Sales Automation",
        "badge": "Active",
        "badge_color": "indigo",
        "keywords": [
            "lead",
            "score",
            "scoring",
            "intent",
            "buyer",
            "icp",
            "qualification",
        ],
    },
    {
        "id": "email_draft",
        "name": "Personalized Email Drafter",
        "description": "Generates context-aware, hyper-personalized sales follow-ups addressing buyer objections.",
        "category": "Content Generation",
        "badge": "Active",
        "badge_color": "purple",
        "keywords": ["email", "draft", "outreach", "followup", "mail", "personalized"],
    },
    {
        "id": "deal_risk",
        "name": "Deal Risk & Win Probability",
        "description": "Detects competitor undercutting, budget freezes, and missing champions across deal records.",
        "category": "Revenue Intelligence",
        "badge": "Active",
        "badge_color": "cyan",
        "keywords": [
            "deal",
            "risk",
            "win",
            "probability",
            "forecast",
            "revenue",
            "competitor",
        ],
    },
    {
        "id": "churn_prediction",
        "name": "Customer Churn Sentinel",
        "description": "Identifies enterprise accounts exhibiting usage drop-offs and recommends retention interventions.",
        "category": "Retention Intelligence",
        "badge": "Active",
        "badge_color": "rose",
        "keywords": ["churn", "retention", "dropoff", "customer", "sentinel", "risk"],
    },
    {
        "id": "meeting_summary",
        "name": "Executive Meeting Summarizer",
        "description": "Extracts action items, timeline commitments, sentiment, and CRM deal updates from meeting notes.",
        "category": "Meeting Intelligence",
        "badge": "Active",
        "badge_color": "amber",
        "keywords": [
            "meeting",
            "summary",
            "notes",
            "action",
            "commitments",
            "call",
            "calendar",
        ],
    },
    {
        "id": "forecast",
        "name": "Pipeline Revenue Forecaster",
        "description": "Runs ensemble Bayesian forecast calculations with risk-adjusted confidence intervals.",
        "category": "Executive Forecasting",
        "badge": "Ensemble AI",
        "badge_color": "emerald",
        "keywords": ["forecast", "pipeline", "revenue", "bayesian", "q4", "projection"],
    },
    {
        "id": "ticket_triage",
        "name": "Service Cloud Triage Agent",
        "description": "Autonomous case classification, SLA urgency prediction, customer sentiment, and rapid response drafting.",
        "category": "Service Automation",
        "badge": "Service AI",
        "badge_color": "blue",
        "keywords": ["ticket", "triage", "sla", "support", "case", "service"],
    },
    {
        "id": "campaign_optimize",
        "name": "Marketing Campaign Optimizer",
        "description": "Predicts email open & click-through rates, scores subject line hooks, and suggests high-converting A/B variants.",
        "category": "Marketing Intelligence",
        "badge": "Marketing AI",
        "badge_color": "pink",
        "keywords": [
            "campaign",
            "marketing",
            "optimize",
            "email",
            "open",
            "click",
            "variant",
        ],
    },
]

NAVIGATION_ITEMS = [
    {
        "id": "nav-dashboard",
        "title": "Dashboard",
        "subtitle": "Enterprise sales telemetry, revenue trajectory, and pipeline stages",
        "href": "/",
        "keywords": [
            "dashboard",
            "home",
            "telemetry",
            "overview",
            "metrics",
            "revenue",
            "stats",
        ],
        "badge": "Core",
    },
    {
        "id": "nav-contacts",
        "title": "Contacts Directory",
        "subtitle": "Manage enterprise leads, decision makers, and prospect accounts",
        "href": "/contacts",
        "keywords": [
            "contacts",
            "leads",
            "people",
            "prospects",
            "accounts",
            "customers",
        ],
        "badge": "CRM",
    },
    {
        "id": "nav-deals",
        "title": "Deals Pipeline",
        "subtitle": "Kanban board tracking opportunities, pipeline velocity, and deal stages",
        "href": "/deals",
        "keywords": [
            "deals",
            "pipeline",
            "kanban",
            "opportunities",
            "sales",
            "revenue",
        ],
        "badge": "Pipeline",
    },
    {
        "id": "nav-agents",
        "title": "AI Agents Fleet",
        "subtitle": "Interactive AI agent studio, graph orchestration, and autonomous execution",
        "href": "/ai-agents",
        "keywords": [
            "agents",
            "ai",
            "autonomous",
            "fleet",
            "studio",
            "chat",
            "langgraph",
            "workflow",
        ],
        "badge": "AI Fleet",
    },
    {
        "id": "nav-campaigns",
        "title": "Marketing Campaigns",
        "subtitle": "Email sequences, audience targeting, open rates, and outreach analytics",
        "href": "/campaigns",
        "keywords": [
            "campaigns",
            "marketing",
            "email",
            "sequences",
            "outreach",
            "templates",
        ],
        "badge": "Marketing",
    },
    {
        "id": "nav-tickets",
        "title": "Service Cases & Support",
        "subtitle": "Customer support tickets, SLA tracking, and autonomous AI triage",
        "href": "/tickets",
        "keywords": ["tickets", "cases", "service", "support", "sla", "issues", "bugs"],
        "badge": "Service",
    },
    {
        "id": "nav-analytics",
        "title": "Analytics & BI",
        "subtitle": "Revenue forecasting, conversion funnels, and executive reporting",
        "href": "/analytics",
        "keywords": [
            "analytics",
            "bi",
            "reporting",
            "forecast",
            "funnel",
            "charts",
            "metrics",
        ],
        "badge": "BI",
    },
    {
        "id": "nav-calendar",
        "title": "Calendar & Scheduling",
        "subtitle": "Sales meetings, client demos, and autonomous meeting scheduler",
        "href": "/calendar",
        "keywords": [
            "calendar",
            "scheduling",
            "meetings",
            "events",
            "demos",
            "appointments",
        ],
        "badge": "Schedule",
    },
    {
        "id": "nav-settings",
        "title": "Platform Settings",
        "subtitle": "Workspace configuration, security rules, Google SSO, and integrations",
        "href": "/settings",
        "keywords": ["settings", "preferences", "config", "auth", "sso", "profile"],
        "badge": "Admin",
    },
]


class SearchItem(BaseModel):
    id: str
    type: str  # "contact", "deal", "agent", "ticket", "campaign", "navigation"
    title: str
    subtitle: Optional[str] = None
    badge: Optional[str] = None
    badge_color: Optional[str] = "indigo"
    href: str
    meta: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    query: str
    total: int
    items: List[SearchItem]
    categories: Dict[str, List[SearchItem]]


def tokenize(query_str: str) -> List[str]:
    """Tokenize query into lowercase words with stop words removed."""
    raw = [
        w.strip()
        for w in re.findall(r"[\w-]+", query_str.lower())
        if len(w.strip()) >= 2
    ]
    sig = [w for w in raw if w not in STOP_WORDS]
    return sig if sig else raw


def score_item(
    tokens: List[str], raw_q: str, primary_text: str, secondary_text: str = ""
) -> int:
    """Calculate relevance score for an item based on full query and tokens."""
    score = 0
    full_haystack = f"{primary_text} {secondary_text}".lower()

    # 1. Exact raw query match (highest)
    if raw_q and raw_q in full_haystack:
        score += 100
        if raw_q in primary_text.lower():
            score += 50

    # 2. Token matches
    matched_count = 0
    for t in tokens:
        if t in primary_text.lower():
            score += 30
            matched_count += 1
        elif secondary_text and t in secondary_text.lower():
            score += 15
            matched_count += 1

    # Bonus if all search tokens matched
    if tokens and matched_count == len(tokens):
        score += 40

    return score


@router.get("", response_model=SearchResponse)
def global_search(
    q: str = Query("", description="Search term for global CRM search"),
    limit: int = Query(
        20, ge=1, le=50, description="Max results to return per category"
    ),
    db: Session = Depends(get_db),
):
    """
    Search across contacts, deals, AI agents, service tickets, campaigns, and navigation.
    Supports multi-word queries like 'Tanuj and Robert' or partial tokens.
    """
    raw_q = q.strip().lower()
    tokens = tokenize(raw_q)
    is_empty = len(raw_q) == 0

    results_by_cat: Dict[str, List[SearchItem]] = {
        "contacts": [],
        "deals": [],
        "agents": [],
        "tickets": [],
        "campaigns": [],
        "navigation": [],
    }

    # ─── 1. Contacts Search ──────────────────────────────────────────────────
    contact_scores = []
    contacts = db.query(Contact).all()
    for c in contacts:
        full_name = f"{c.first_name} {c.last_name}".strip()
        comp = c.company or ""
        email = c.email or ""
        job = c.job_title or ""
        tags = (
            " ".join(c.tags)
            if isinstance(c.tags, list)
            else (str(c.tags) if c.tags else "")
        )

        if is_empty:
            score = 1
        else:
            score = score_item(
                tokens, raw_q, f"{full_name} {comp}", f"{email} {job} {tags}"
            )

        if score > 0:
            subtitle_parts = []
            if job:
                subtitle_parts.append(job)
            if comp:
                subtitle_parts.append(comp)
            elif email:
                subtitle_parts.append(email)
            subtitle = " · ".join(subtitle_parts) or email or "Lead"

            badge_str = (
                c.lead_status.value.upper()
                if hasattr(c.lead_status, "value")
                else str(c.lead_status).upper()
            )
            contact_scores.append(
                (
                    score,
                    SearchItem(
                        id=f"contact-{c.id}",
                        type="contact",
                        title=full_name,
                        subtitle=subtitle,
                        badge=badge_str,
                        badge_color=(
                            "emerald"
                            if badge_str in ["QUALIFIED", "CONVERTED"]
                            else "indigo"
                        ),
                        href=f"/contacts?search={full_name}",
                        meta={
                            "id": c.id,
                            "email": c.email,
                            "company": c.company,
                            "avatar_url": c.avatar_url,
                            "score": c.lead_score,
                        },
                    ),
                )
            )

    contact_scores.sort(key=lambda x: x[0], reverse=True)
    results_by_cat["contacts"] = [item for _, item in contact_scores[:limit]]

    # ─── 2. Deals Search ─────────────────────────────────────────────────────
    deal_scores = []
    deals = db.query(Deal).all()
    for d in deals:
        title = d.title or ""
        comp = d.company or ""
        owner = d.owner or ""
        desc = d.description or ""
        stage_str = (
            d.stage.value.upper() if hasattr(d.stage, "value") else str(d.stage).upper()
        )

        if is_empty:
            score = 1
        else:
            score = score_item(
                tokens, raw_q, f"{title} {comp}", f"{owner} {desc} {stage_str}"
            )

        if score > 0:
            val_str = f"${int(d.value):,}" if d.value else "$0"
            sub = f"{val_str} · {comp}" if comp else val_str
            deal_scores.append(
                (
                    score,
                    SearchItem(
                        id=f"deal-{d.id}",
                        type="deal",
                        title=title,
                        subtitle=sub,
                        badge=stage_str.replace("_", " "),
                        badge_color=(
                            "purple"
                            if "WON" in stage_str
                            else ("rose" if "LOST" in stage_str else "indigo")
                        ),
                        href=f"/deals?search={title}",
                        meta={
                            "id": d.id,
                            "value": d.value,
                            "stage": stage_str,
                            "company": d.company,
                        },
                    ),
                )
            )

    deal_scores.sort(key=lambda x: x[0], reverse=True)
    results_by_cat["deals"] = [item for _, item in deal_scores[:limit]]

    # ─── 3. AI Agents Search ─────────────────────────────────────────────────
    agent_scores = []
    for agent in BUILTIN_AGENTS:
        name = agent["name"]
        desc = agent["description"]
        cat = agent["category"]
        kws = " ".join(agent["keywords"])

        if is_empty:
            score = 1
        else:
            score = score_item(tokens, raw_q, name, f"{desc} {cat} {kws}")

        if score > 0:
            agent_scores.append(
                (
                    score,
                    SearchItem(
                        id=f"agent-{agent['id']}",
                        type="agent",
                        title=name,
                        subtitle=desc,
                        badge=agent["badge"],
                        badge_color=agent["badge_color"],
                        href=f"/ai-agents?agent={agent['id']}",
                        meta={"agent_id": agent["id"], "category": cat},
                    ),
                )
            )

    agent_scores.sort(key=lambda x: x[0], reverse=True)
    results_by_cat["agents"] = [item for _, item in agent_scores[:limit]]

    # ─── 4. Support Tickets Search ───────────────────────────────────────────
    ticket_scores = []
    tickets = db.query(Ticket).all()
    for t in tickets:
        title = t.title or ""
        num = t.ticket_number or f"TKT-{t.id}"
        desc = t.description or ""
        stat = (
            t.status.value.upper()
            if hasattr(t.status, "value")
            else str(t.status).upper()
        )
        prio = (
            t.priority.value.upper()
            if hasattr(t.priority, "value")
            else str(t.priority).upper()
        )

        if is_empty:
            score = 1
        else:
            score = score_item(tokens, raw_q, f"{num} {title}", f"{desc} {stat} {prio}")

        if score > 0:
            ticket_scores.append(
                (
                    score,
                    SearchItem(
                        id=f"ticket-{t.id}",
                        type="ticket",
                        title=f"{num}: {title}",
                        subtitle=f"Status: {stat} · Priority: {prio}",
                        badge=prio,
                        badge_color=(
                            "rose"
                            if prio == "CRITICAL"
                            else ("amber" if prio == "HIGH" else "blue")
                        ),
                        href=f"/tickets?search={title}",
                        meta={"id": t.id, "ticket_number": num, "status": stat},
                    ),
                )
            )

    ticket_scores.sort(key=lambda x: x[0], reverse=True)
    results_by_cat["tickets"] = [item for _, item in ticket_scores[:limit]]

    # ─── 5. Marketing Campaigns Search ───────────────────────────────────────
    campaign_scores = []
    campaigns = db.query(Campaign).all()
    for camp in campaigns:
        name = camp.name or ""
        subj = camp.subject or ""
        desc = camp.description or ""
        stat = (
            camp.status.value.upper()
            if hasattr(camp.status, "value")
            else str(camp.status).upper()
        )

        if is_empty:
            score = 1
        else:
            score = score_item(tokens, raw_q, name, f"{subj} {desc} {stat}")

        if score > 0:
            campaign_scores.append(
                (
                    score,
                    SearchItem(
                        id=f"campaign-{camp.id}",
                        type="campaign",
                        title=name,
                        subtitle=subj or desc or "Email campaign",
                        badge=stat,
                        badge_color="emerald" if stat == "ACTIVE" else "slate",
                        href=f"/campaigns?search={name}",
                        meta={"id": camp.id, "status": stat},
                    ),
                )
            )

    campaign_scores.sort(key=lambda x: x[0], reverse=True)
    results_by_cat["campaigns"] = [item for _, item in campaign_scores[:limit]]

    # ─── 6. Navigation Search ────────────────────────────────────────────────
    nav_scores = []
    for nav in NAVIGATION_ITEMS:
        title = nav["title"]
        sub = nav["subtitle"]
        kws = " ".join(nav["keywords"])

        if is_empty:
            score = 1
        else:
            score = score_item(tokens, raw_q, title, f"{sub} {kws}")

        if score > 0:
            nav_scores.append(
                (
                    score,
                    SearchItem(
                        id=nav["id"],
                        type="navigation",
                        title=title,
                        subtitle=sub,
                        badge=nav["badge"],
                        badge_color="slate",
                        href=nav["href"],
                    ),
                )
            )

    nav_scores.sort(key=lambda x: x[0], reverse=True)
    results_by_cat["navigation"] = [item for _, item in nav_scores[:limit]]

    # Compile flat items list preserving category ordering
    all_flat_items: List[SearchItem] = []
    for cat in ["contacts", "deals", "agents", "tickets", "campaigns", "navigation"]:
        all_flat_items.extend(results_by_cat[cat])

    total_count = len(all_flat_items)

    return SearchResponse(
        query=q,
        total=total_count,
        items=all_flat_items,
        categories=results_by_cat,
    )
