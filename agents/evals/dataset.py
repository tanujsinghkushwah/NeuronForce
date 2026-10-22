"""
NeuronForce Autonomous Agent Evaluation Dataset
Defines 15 comprehensive evaluation scenarios across General Queries,
CRM Mutations, Specialist Sub-Agents, and Compound Multi-Step Workflows.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class EvalScenario:
    id: str
    name: str
    category: str  # 'general_query' | 'crm_action' | 'subagent' | 'compound_workflow'
    prompt: str
    expected_intent: str  # 'general' | 'crm_action' | 'subagent' | 'compound'
    expected_action_type: Optional[str] = None
    expected_subagent: Optional[str] = None
    expected_entities: Dict[str, Any] = field(default_factory=dict)
    required_steps: List[str] = field(default_factory=list)
    min_confidence: float = 0.85
    expected_reply_keywords: List[str] = field(default_factory=list)


EVAL_SCENARIOS: List[EvalScenario] = [
    # --------------------------------------------------------------------------
    # 1. General Inquiries (Read-Only Analytics & Information Lookups)
    # --------------------------------------------------------------------------
    EvalScenario(
        id="eval_01_general_pipeline_metrics",
        name="Pipeline Metrics & Deal Totals",
        category="general_query",
        prompt="What is the total amount of deals currently in our sales pipeline?",
        expected_intent="general",
        expected_action_type=None,
        expected_subagent=None,
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "synthesizer",
        ],
        min_confidence=0.88,
        expected_reply_keywords=["deal", "pipeline"],
    ),
    EvalScenario(
        id="eval_02_general_contact_directory",
        name="Enterprise Contact Directory Search",
        category="general_query",
        prompt="Show me our key contacts at SpaceY and what their roles are",
        expected_intent="general",
        expected_action_type=None,
        expected_subagent=None,
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "synthesizer",
        ],
        min_confidence=0.85,
        expected_reply_keywords=["SpaceY"],
    ),
    # --------------------------------------------------------------------------
    # 2. Direct CRM Actions (Calendar, Deals, Contacts, Campaigns)
    # --------------------------------------------------------------------------
    EvalScenario(
        id="eval_03_crm_schedule_meeting",
        name="Calendar Executive Meeting Booking",
        category="crm_action",
        prompt="Schedule an executive sales demo with Sarah Chen for 24 October at 9:00 PM",
        expected_intent="crm_action",
        expected_action_type="schedule_meeting",
        expected_subagent=None,
        expected_entities={"name": "Sarah Chen"},
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "action_schedule_meeting",
            "synthesizer",
        ],
        min_confidence=0.90,
        expected_reply_keywords=["Meeting", "Scheduled"],
    ),
    EvalScenario(
        id="eval_04_crm_create_deal",
        name="Create High-Value Pipeline Opportunity",
        category="crm_action",
        prompt="Create a new deal for Cyberdyne Systems worth $250,000 in proposal stage",
        expected_intent="crm_action",
        expected_action_type="create_deal",
        expected_subagent=None,
        expected_entities={
            "company": "Cyberdyne Systems",
            "amount": 250000.0,
            "stage": "proposal",
        },
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "action_create_deal",
            "synthesizer",
        ],
        min_confidence=0.90,
        expected_reply_keywords=["Cyberdyne Systems", "250"],
    ),
    EvalScenario(
        id="eval_05_crm_update_deal_stage",
        name="Advance Deal to Closed Won",
        category="crm_action",
        prompt="Move deal for Quantum Leap Corp to closed_won stage",
        expected_intent="crm_action",
        expected_action_type="update_deal",
        expected_subagent=None,
        expected_entities={"company": "Quantum Leap Corp", "stage": "closed_won"},
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "action_update_deal",
            "synthesizer",
        ],
        min_confidence=0.90,
        expected_reply_keywords=["Quantum Leap Corp"],
    ),
    EvalScenario(
        id="eval_06_crm_create_contact",
        name="Add New Enterprise Contact Record",
        category="crm_action",
        prompt="Create a new contact named Marcus Vance with email marcus.vance@vanceindustries.com",
        expected_intent="crm_action",
        expected_action_type="create_contact",
        expected_subagent=None,
        expected_entities={
            "name": "Marcus Vance",
            "email": "marcus.vance@vanceindustries.com",
        },
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "action_create_contact",
            "synthesizer",
        ],
        min_confidence=0.90,
        expected_reply_keywords=["Marcus Vance", "marcus.vance@vanceindustries.com"],
    ),
    EvalScenario(
        id="eval_07_crm_update_contact_email",
        name="Update Existing Contact Email Details",
        category="crm_action",
        prompt="Update email for Marcus Vance to marcus.updated@vanceindustries.com",
        expected_intent="crm_action",
        expected_action_type="update_contact",
        expected_subagent=None,
        expected_entities={
            "name": "Marcus Vance",
            "email": "marcus.updated@vanceindustries.com",
        },
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "action_update_contact",
            "synthesizer",
        ],
        min_confidence=0.90,
        expected_reply_keywords=["marcus.updated@vanceindustries.com"],
    ),
    EvalScenario(
        id="eval_08_crm_create_campaign",
        name="Launch Enterprise Outreach Campaign",
        category="crm_action",
        prompt="Create a marketing campaign for Enterprise AI Acceleration targeting enterprise_leads",
        expected_intent="crm_action",
        expected_action_type="create_campaign",
        expected_subagent=None,
        expected_entities={"subject": "Enterprise AI Acceleration"},
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "action_create_campaign",
            "synthesizer",
        ],
        min_confidence=0.90,
        expected_reply_keywords=["Campaign"],
    ),
    # --------------------------------------------------------------------------
    # 3. Specialized Sub-Agents (Lead Scoring, Email, Risk, Churn, Summary)
    # --------------------------------------------------------------------------
    EvalScenario(
        id="eval_09_subagent_lead_scoring",
        name="Buyer Intent & ICP Lead Scoring",
        category="subagent",
        prompt="Score lead for Dr. Aris Thorne at Neural Dynamics based on high buyer intent signals",
        expected_intent="subagent",
        expected_action_type=None,
        expected_subagent="lead_scoring",
        expected_entities={"name": "Dr. Aris Thorne", "company": "Neural Dynamics"},
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "subagent_lead_scoring",
            "synthesizer",
        ],
        min_confidence=0.90,
        expected_reply_keywords=["Lead Scoring", "Buyer Intent"],
    ),
    EvalScenario(
        id="eval_10_subagent_email_draft",
        name="Hyper-Personalized Sales Email Drafter",
        category="subagent",
        prompt="Draft a personalized sales follow-up email to Sarah Chen about NeuronForce autonomous agents",
        expected_intent="subagent",
        expected_action_type=None,
        expected_subagent="email_draft",
        expected_entities={"name": "Sarah Chen"},
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "subagent_email_draft",
            "synthesizer",
        ],
        min_confidence=0.90,
        expected_reply_keywords=["Subject:", "NeuronForce"],
    ),
    EvalScenario(
        id="eval_11_subagent_deal_risk",
        name="Deal Health & Win Probability Assessment",
        category="subagent",
        prompt="Analyze deal risk and win probability for our SpaceY negotiation",
        expected_intent="subagent",
        expected_action_type=None,
        expected_subagent="deal_risk",
        expected_entities={"company": "SpaceY"},
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "subagent_deal_risk",
            "synthesizer",
        ],
        min_confidence=0.90,
        expected_reply_keywords=["Win Probability", "Risk"],
    ),
    EvalScenario(
        id="eval_12_subagent_churn_sentinel",
        name="Account Churn & Retention Sentinel",
        category="subagent",
        prompt="Analyze customer churn risk for Enterprise Cloud Corp due to dropping usage and tickets",
        expected_intent="subagent",
        expected_action_type=None,
        expected_subagent="churn_prediction",
        expected_entities={"company": "Enterprise Cloud Corp"},
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "subagent_churn_prediction",
            "synthesizer",
        ],
        min_confidence=0.90,
        expected_reply_keywords=["Churn", "ARR"],
    ),
    EvalScenario(
        id="eval_13_subagent_meeting_summary",
        name="Executive Call & Notes Summarizer",
        category="subagent",
        prompt="Summarize meeting notes: Discussed Q4 budget with CFO, agreed on $150k pricing tier, action item to dispatch security compliance checklist",
        expected_intent="subagent",
        expected_action_type=None,
        expected_subagent="meeting_summary",
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "subagent_meeting_summary",
            "synthesizer",
        ],
        min_confidence=0.90,
        expected_reply_keywords=["Action Items", "Key Decisions"],
    ),
    # --------------------------------------------------------------------------
    # 4. Compound Multi-Step Workflows (CRM Mutation + Sub-Agent Execution)
    # --------------------------------------------------------------------------
    EvalScenario(
        id="eval_14_compound_create_contact_and_email",
        name="Create Contact & Auto-Dispatch Specialized Email",
        category="compound_workflow",
        prompt="Create a new contact named Elena Rostova with email elena@heliosenergy.com and send specialized email promoting NeuronForce",
        expected_intent="compound",
        expected_action_type="create_contact",
        expected_subagent="email_draft",
        expected_entities={"name": "Elena Rostova", "email": "elena@heliosenergy.com"},
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "action_create_contact",
            "subagent_email_draft",
            "synthesizer",
        ],
        min_confidence=0.92,
        expected_reply_keywords=["elena@heliosenergy.com", "Subject:"],
    ),
    EvalScenario(
        id="eval_15_compound_update_contact_and_email",
        name="Update Contact Details & Sequentially Send Outreach",
        category="compound_workflow",
        prompt="Update email for Elena Rostova to elena.rostova@heliosenergy.com and then send specialized email promoting NeuronForce",
        expected_intent="compound",
        expected_action_type="update_contact",
        expected_subagent="email_draft",
        expected_entities={
            "name": "Elena Rostova",
            "email": "elena.rostova@heliosenergy.com",
        },
        required_steps=[
            "prompt_ingestion",
            "context_retrieval",
            "intent_router",
            "action_update_contact",
            "subagent_email_draft",
            "synthesizer",
        ],
        min_confidence=0.92,
        expected_reply_keywords=["elena.rostova@heliosenergy.com", "Subject:"],
    ),
]
