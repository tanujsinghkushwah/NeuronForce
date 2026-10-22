#!/usr/bin/env python3
"""
NeuronForce Seed Script
Run this standalone to populate the database with realistic demo data.

Usage:
    cd neuronforce/backend
    python -m scripts.seed_data
    # OR directly:
    ./venv/bin/python scripts/seed_data.py
"""

import sys
import os

# Add parent directory to path so we can import from app/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from datetime import datetime, timezone, timedelta
from app.database import SessionLocal, engine, Base
from app.models import (
    Contact,
    Deal,
    Activity,
    Task,
    AIAgentTask,
    AnalyticsSnapshot,
    CalendarEvent,
    LeadStatus,
    DealStage,
    Priority,
    TaskStatus,
    ActivityType,
    AgentTaskType,
    AgentTaskStatus,
    User,
    OAuthAccount,
    UserSession,
    Ticket,
    TicketMessage,
    TicketStatus,
    TicketPriority,
    TicketCategory,
    Campaign,
    CampaignStatus,
    CampaignType,
)


def seed_users(db):
    """Seed initial Google OAuth linked user accounts."""
    if db.query(User).count() > 0:
        return

    users_data = [
        {
            "email": "alex.rivera@neuronforce.ai",
            "full_name": "Alex Rivera",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alex",
            "role": "revops_lead",
            "google_sub": "google_alex_rivera_101",
        },
        {
            "email": "sarah.jenkins@neuronforce.ai",
            "full_name": "Sarah Jenkins",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=SarahJ",
            "role": "admin",
            "google_sub": "google_sarah_jenkins_102",
        },
        {
            "email": "jordan.lee@neuronforce.ai",
            "full_name": "Jordan Lee",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Jordan",
            "role": "sales_rep",
            "google_sub": "google_jordan_lee_103",
        },
    ]

    for u_info in users_data:
        user = User(
            email=u_info["email"],
            full_name=u_info["full_name"],
            avatar_url=u_info["avatar_url"],
            role=u_info["role"],
            is_active=True,
            is_verified=True,
            last_login_at=datetime.now(timezone.utc),
        )
        db.add(user)
        db.flush()

        oauth_acc = OAuthAccount(
            user_id=user.id,
            provider="google",
            provider_user_id=u_info["google_sub"],
            email=u_info["email"],
            raw_claims={
                "email": u_info["email"],
                "name": u_info["full_name"],
                "email_verified": True,
            },
        )
        db.add(oauth_acc)

    db.commit()
    print("✅ Seeded initial Google OAuth users")


def seed_tickets(db):
    """Seed initial Service Cloud support cases & tickets."""
    if db.query(Ticket).count() > 0:
        return

    now = datetime.now(timezone.utc)
    c1 = db.query(Contact).filter(Contact.email == "sarah.chen@techcorp.io").first()
    c2 = (
        db.query(Contact)
        .filter(Contact.email == "marcus.johnson@innovateinc.com")
        .first()
    )
    c3 = (
        db.query(Contact)
        .filter(Contact.email == "elena.rodriguez@globalretail.com")
        .first()
    )

    tickets_data = [
        {
            "ticket_number": "TKT-0001",
            "title": "API Rate Limiting exceeded during bulk contact sync",
            "description": "We are experiencing 429 Too Many Requests errors when syncing our 50k customer records via the REST API integration.",
            "status": TicketStatus.IN_PROGRESS,
            "priority": TicketPriority.CRITICAL,
            "category": TicketCategory.TECHNICAL,
            "contact_id": c1.id if c1 else None,
            "assigned_to": "Alex Rivera",
            "reporter_name": "Sarah Chen",
            "reporter_email": "sarah.chen@techcorp.io",
            "sla_due_at": now + timedelta(hours=2),
            "first_response_at": now - timedelta(hours=1),
            "sentiment": "frustrated",
            "ai_triage": {
                "urgency_score": 9,
                "sentiment": "frustrated",
                "category": "technical",
                "priority": "critical",
                "escalate": True,
                "estimated_resolution_hours": 3,
            },
            "ai_suggested_response": "Hi Sarah, our engineering team has temporarily elevated your API quota limit to 5,000 req/min while we investigate the batch pipeline bottleneck.",
            "tags": ["api", "rate-limit", "enterprise-sla"],
            "messages": [
                {
                    "author_name": "Sarah Chen",
                    "author_email": "sarah.chen@techcorp.io",
                    "body": "Hi team, our bulk sync failed at 3:15 AM with HTTP 429. This is blocking our morning data replication pipeline.",
                    "is_internal": False,
                    "created_at": now - timedelta(hours=3),
                },
                {
                    "author_name": "Alex Rivera",
                    "author_email": "alex.rivera@neuronforce.ai",
                    "body": "Hi Sarah, thank you for alerting us. I have confirmed the rate limiter triggered and am temporarily lifting the throttle for your tenant key.",
                    "is_internal": False,
                    "created_at": now - timedelta(hours=1),
                },
                {
                    "author_name": "AI Agentforce",
                    "author_email": "ai@neuronforce.ai",
                    "body": "AI Triage Note: Customer is on Enterprise tier with $120k ARR deal in pipeline. Recommend priority escalation to RevOps infrastructure lead.",
                    "is_internal": True,
                    "is_ai_generated": True,
                    "created_at": now - timedelta(hours=1, minutes=5),
                },
            ],
        },
        {
            "ticket_number": "TKT-0002",
            "title": "Billing invoice discrepancy for Q3 enterprise seats",
            "description": "Invoice #INV-2026-89 shows 25 seats billed instead of contracted 20 seats.",
            "status": TicketStatus.OPEN,
            "priority": TicketPriority.HIGH,
            "category": TicketCategory.BILLING,
            "contact_id": c2.id if c2 else None,
            "assigned_to": "Sarah Jenkins",
            "reporter_name": "Marcus Johnson",
            "reporter_email": "marcus.johnson@innovateinc.com",
            "sla_due_at": now + timedelta(hours=3),
            "sentiment": "neutral",
            "ai_triage": {
                "urgency_score": 7,
                "sentiment": "neutral",
                "category": "billing",
                "priority": "high",
                "escalate": False,
                "estimated_resolution_hours": 4,
            },
            "ai_suggested_response": "Hi Marcus, I reviewed your contract terms and verified the 5 seat variance. I have issued a credit memo of $1,250 and reissued the revised invoice.",
            "tags": ["billing", "invoice", "refund"],
            "messages": [
                {
                    "author_name": "Marcus Johnson",
                    "author_email": "marcus.johnson@innovateinc.com",
                    "body": "Our accounts payable team noticed that invoice INV-2026-89 charged for 25 licenses, but order form OF-881 specifies 20. Please issue an adjusted invoice.",
                    "is_internal": False,
                    "created_at": now - timedelta(hours=2),
                }
            ],
        },
        {
            "ticket_number": "TKT-0003",
            "title": "SSO SAML configuration assistance for Okta",
            "description": "Need guidance configuring Okta SAML 2.0 metadata and attribute mapping for user provisioning.",
            "status": TicketStatus.RESOLVED,
            "priority": TicketPriority.MEDIUM,
            "category": TicketCategory.ONBOARDING,
            "contact_id": c3.id if c3 else None,
            "assigned_to": "Jordan Lee",
            "reporter_name": "Elena Rodriguez",
            "reporter_email": "elena.rodriguez@globalretail.com",
            "sla_due_at": now - timedelta(hours=5),
            "first_response_at": now - timedelta(hours=10),
            "resolved_at": now - timedelta(hours=2),
            "sentiment": "positive",
            "ai_triage": {
                "urgency_score": 4,
                "sentiment": "positive",
                "category": "onboarding",
                "priority": "medium",
                "escalate": False,
                "estimated_resolution_hours": 2,
            },
            "tags": ["sso", "saml", "okta"],
            "messages": [
                {
                    "author_name": "Elena Rodriguez",
                    "author_email": "elena.rodriguez@globalretail.com",
                    "body": "We are completing our Okta integration and need the ACS URL and entity ID for our workspace domain.",
                    "is_internal": False,
                    "created_at": now - timedelta(hours=12),
                },
                {
                    "author_name": "Jordan Lee",
                    "author_email": "jordan.lee@neuronforce.ai",
                    "body": "Hi Elena, here is our Okta metadata guide and domain configuration values. Let us know if you need a quick screen share.",
                    "is_internal": False,
                    "created_at": now - timedelta(hours=10),
                },
                {
                    "author_name": "Elena Rodriguez",
                    "author_email": "elena.rodriguez@globalretail.com",
                    "body": "That worked perfectly! All our 140 users successfully federated. Thank you!",
                    "is_internal": False,
                    "created_at": now - timedelta(hours=2),
                },
            ],
        },
        {
            "ticket_number": "TKT-0004",
            "title": "Custom field export missing in CSV download",
            "description": "When exporting contacts view with custom tags and industry filters, custom metadata columns are empty.",
            "status": TicketStatus.OPEN,
            "priority": TicketPriority.LOW,
            "category": TicketCategory.BUG,
            "assigned_to": "Alex Rivera",
            "reporter_name": "David Kim",
            "reporter_email": "david.kim@apexfinancial.com",
            "sla_due_at": now + timedelta(hours=48),
            "sentiment": "neutral",
            "ai_triage": {
                "urgency_score": 3,
                "sentiment": "neutral",
                "category": "bug",
                "priority": "low",
                "escalate": False,
                "estimated_resolution_hours": 12,
            },
            "tags": ["csv-export", "ui", "data-export"],
            "messages": [
                {
                    "author_name": "David Kim",
                    "author_email": "david.kim@apexfinancial.com",
                    "body": "Exporting contact tables to CSV currently omits JSON tags column.",
                    "is_internal": False,
                    "created_at": now - timedelta(hours=6),
                }
            ],
        },
    ]

    for t_data in tickets_data:
        msgs = t_data.pop("messages", [])
        ticket = Ticket(**t_data)
        db.add(ticket)
        db.flush()

        for m_data in msgs:
            msg = TicketMessage(ticket_id=ticket.id, **m_data)
            db.add(msg)

    db.commit()
    print("✅ Seeded Service Cloud support tickets")


def seed_campaigns(db):
    """Seed initial Marketing Cloud email campaigns & journeys."""
    if db.query(Campaign).count() > 0:
        return

    now = datetime.now(timezone.utc)
    campaigns_data = [
        {
            "name": "Q4 Enterprise AI Transformation Webinar",
            "type": CampaignType.EMAIL,
            "status": CampaignStatus.ACTIVE,
            "description": "Exclusive invitation to VP and C-level revenue leaders exploring AI-driven sales orchestration.",
            "subject": "Exclusive Invite: Scaling Revenue Operations with Autonomous AI Agents",
            "preview_text": "Join 500+ RevOps executives on Nov 12 for live pipeline automation benchmarks.",
            "body_html": "<p>Hi {{first_name}},</p><p>Enterprise sales teams are eliminating 80% of manual CRM data entry using autonomous agents.</p><p><a href='#'>Register for the live briefing &rarr;</a></p>",
            "body_text": "Hi {{first_name}},\n\nEnterprise sales teams are eliminating 80% of manual CRM data entry using autonomous agents.\n\nRegister for the live briefing: https://neuronforce.ai/webinar-q4",
            "from_name": "Alex Rivera",
            "from_email": "alex.rivera@neuronforce.ai",
            "audience_filter": {"industry": "Technology", "lead_status": "qualified"},
            "recipient_count": 1240,
            "sent_at": now - timedelta(days=2),
            "emails_sent": 1240,
            "emails_delivered": 1215,
            "emails_opened": 476,
            "emails_clicked": 148,
            "emails_bounced": 25,
            "emails_unsubscribed": 3,
            "open_rate": 0.3918,
            "click_rate": 0.1218,
            "conversion_rate": 0.052,
            "revenue_attributed": 48500.0,
            "ai_score": 94,
            "ai_insights": {
                "strengths": [
                    "Personalized subject line",
                    "High executive engagement",
                    "Above-benchmark open rate (+14%)",
                ],
                "recommendation": "Deploy automated 48-hour follow-up to attendees who clicked the registration link.",
            },
            "tags": ["webinar", "q4-pipeline", "enterprise", "c-level"],
        },
        {
            "name": "Re-engagement: Closed-Lost Pipeline Nurture",
            "type": CampaignType.NURTURE_SEQUENCE,
            "status": CampaignStatus.COMPLETED,
            "description": "Automated nurture campaign for deals marked closed-lost in the past 6 months.",
            "subject": "What's new in NeuronForce 2.0: Real-time autonomous pipeline intelligence",
            "preview_text": "See how our new release addresses integration bottlenecks.",
            "body_html": "<p>Hi {{first_name}},</p><p>We recently shipped our Gemini-powered Agentforce layer with automatic SLA triaging and 1-click quoting.</p>",
            "body_text": "Hi {{first_name}},\n\nWe recently shipped our Gemini-powered Agentforce layer with automatic SLA triaging and 1-click quoting.",
            "from_name": "Sarah Jenkins",
            "from_email": "sarah.jenkins@neuronforce.ai",
            "audience_filter": {"lead_status": "contacted"},
            "recipient_count": 480,
            "sent_at": now - timedelta(days=14),
            "completed_at": now - timedelta(days=7),
            "emails_sent": 480,
            "emails_delivered": 472,
            "emails_opened": 142,
            "emails_clicked": 41,
            "emails_bounced": 8,
            "emails_unsubscribed": 2,
            "open_rate": 0.3008,
            "click_rate": 0.0869,
            "conversion_rate": 0.041,
            "revenue_attributed": 24000.0,
            "ai_score": 87,
            "ai_insights": {
                "strengths": ["Strong value proposition for previous evaluators"],
                "recommendation": "Add customer case study video link in body to boost click-through by ~18%.",
            },
            "tags": ["nurture", "re-engagement", "closed-lost"],
        },
        {
            "name": "Spring 2026 Product Release: Autonomous Agentforce",
            "type": CampaignType.ANNOUNCEMENT,
            "status": CampaignStatus.SCHEDULED,
            "description": "Global announcement for general availability of autonomous AI agent workflows.",
            "subject": "Announcing NeuronForce Agentforce: AI that doesn't just suggest — it executes",
            "preview_text": "Next-generation autonomous revenue orchestration is now live.",
            "body_html": "<p>Meet Agentforce: The first AI sales platform with real-time Gemini reasoning and self-healing pipelines.</p>",
            "body_text": "Meet Agentforce: The first AI sales platform with real-time Gemini reasoning and self-healing pipelines.",
            "from_name": "NeuronForce Team",
            "from_email": "product@neuronforce.ai",
            "audience_filter": {},
            "recipient_count": 3500,
            "scheduled_at": now + timedelta(days=3),
            "ai_score": 92,
            "ai_insights": {
                "strengths": ["Compelling hook", "Clear product positioning"],
                "recommendation": "Set up A/B subject line test between product-led vs. outcome-led headline.",
            },
            "ab_test_enabled": True,
            "ab_variant_subject": "How top revenue teams are automating 65% of customer workflows with AI",
            "tags": ["product-launch", "announcement", "agentforce"],
        },
        {
            "name": "Mid-Market Growth Plan: 20% Annual Upgrade",
            "type": CampaignType.PROMOTIONAL,
            "status": CampaignStatus.ACTIVE,
            "description": "Targeted upgrade incentives for mid-market monthly accounts switching to annual billing.",
            "subject": "Upgrade your team's pipeline velocity: Save 20% on Annual Pro",
            "preview_text": "Lock in your 2026 pricing and unlock unlimited AI agent tasks.",
            "body_html": "<p>Hi {{first_name}},</p><p>Switch to Annual Pro today and get unlimited Agentforce execution plus dedicated SLA support.</p>",
            "body_text": "Hi {{first_name}},\n\nSwitch to Annual Pro today and get unlimited Agentforce execution plus dedicated SLA support.",
            "from_name": "Jordan Lee",
            "from_email": "jordan.lee@neuronforce.ai",
            "audience_filter": {"industry": "Finance"},
            "recipient_count": 860,
            "sent_at": now - timedelta(days=5),
            "emails_sent": 860,
            "emails_delivered": 845,
            "emails_opened": 358,
            "emails_clicked": 134,
            "emails_bounced": 15,
            "emails_unsubscribed": 4,
            "open_rate": 0.4237,
            "click_rate": 0.1586,
            "conversion_rate": 0.082,
            "revenue_attributed": 64200.0,
            "ai_score": 96,
            "ai_insights": {
                "strengths": [
                    "High conversion rate",
                    "Clear ROI proposition",
                    "Strong click-to-open ratio",
                ],
                "recommendation": "Expand audience segment to Healthcare and Retail verticals.",
            },
            "tags": ["promotional", "upgrade", "annual-plan"],
        },
    ]

    for c_data in campaignss_data if "campaignss_data" in locals() else campaigns_data:
        campaign = Campaign(**c_data)
        db.add(campaign)

    db.commit()
    print("✅ Seeded Marketing Cloud campaigns")


def seed_analytics_snapshots(db, force: bool = False):
    """Seed comprehensive 180-day (6-month) revenue trajectory and telemetry snapshots."""
    existing_count = db.query(AnalyticsSnapshot).count()
    if existing_count >= 60 and not force:
        return

    if existing_count > 0:
        db.query(AnalyticsSnapshot).delete()
        db.flush()

    now = datetime.now(timezone.utc)
    start_revenue = 185000.0
    end_revenue = 520000.0
    total_days = 180

    for i in range(total_days):
        date = now - timedelta(days=total_days - 1 - i)
        progress = i / float(total_days - 1) if total_days > 1 else 1.0
        base_revenue = start_revenue + (end_revenue - start_revenue) * (progress**1.25)
        if i == total_days - 1:
            rev = end_revenue
        else:
            rev = round(base_revenue + random.uniform(-1500, 1500), 2)

        base_pipeline = 1800000.0 + 550000.0 * (progress**0.8)
        pipe_val = round(base_pipeline + random.uniform(-40000, 40000), 2)

        snapshot = AnalyticsSnapshot(
            date=date,
            total_revenue=rev,
            deals_won=1 if i in [25, 60, 95, 130, 165, 179] else 0,
            deals_lost=1 if i in [45, 115] else 0,
            new_contacts=random.randint(1, 6),
            active_deals=random.randint(6, 11),
            pipeline_value=pipe_val,
            conversion_rate=round(random.uniform(35.0, 52.0), 1),
            avg_deal_size=round(random.uniform(180000, 520000), 2),
            ai_tasks_run=random.randint(8, 28),
            ai_total_cost=round(random.uniform(0.04, 0.35), 4),
            created_at=date,
        )
        db.add(snapshot)

    db.commit()
    print(f"✅ Seeded {total_days} daily analytics snapshots for revenue trajectory")


def seed_database(db):
    """Populate the database with realistic demo data."""
    # Ensure users exist
    seed_users(db)

    # Ensure Service Cloud, Marketing Cloud, and Analytics Snapshots are populated
    seed_tickets(db)
    seed_campaigns(db)
    seed_analytics_snapshots(db)

    # Check if contact data already exists
    if db.query(Contact).count() > 0:
        print("ℹ️  Database already seeded — skipping contacts/deals.")
        return

    # --- CONTACTS ---
    contacts_data = [
        {
            "first_name": "Sarah",
            "last_name": "Chen",
            "email": "sarah.chen@techcorp.io",
            "phone": "+1-415-555-0101",
            "company": "TechCorp Solutions",
            "job_title": "VP of Engineering",
            "department": "Engineering",
            "industry": "Technology",
            "city": "San Francisco",
            "state": "CA",
            "country": "USA",
            "lead_status": LeadStatus.QUALIFIED,
            "lead_score": 92,
            "source": "LinkedIn",
            "tags": ["enterprise", "tech", "hot-lead"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah",
        },
        {
            "first_name": "Marcus",
            "last_name": "Johnson",
            "email": "marcus.j@innovate.com",
            "phone": "+1-212-555-0202",
            "company": "Innovate Inc",
            "job_title": "CTO",
            "department": "Technology",
            "industry": "SaaS",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "lead_status": LeadStatus.CONTACTED,
            "lead_score": 78,
            "source": "Referral",
            "tags": ["startup", "saas", "decision-maker"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Marcus",
        },
        {
            "first_name": "Elena",
            "last_name": "Rodriguez",
            "email": "elena.r@globalretail.com",
            "phone": "+1-305-555-0303",
            "company": "Global Retail Group",
            "job_title": "Director of Operations",
            "department": "Operations",
            "industry": "Retail",
            "city": "Miami",
            "state": "FL",
            "country": "USA",
            "lead_status": LeadStatus.QUALIFIED,
            "lead_score": 85,
            "source": "Website",
            "tags": ["retail", "enterprise", "warm-lead"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Elena",
        },
        {
            "first_name": "James",
            "last_name": "Park",
            "email": "james.park@finova.io",
            "phone": "+1-312-555-0404",
            "company": "Finova Financial",
            "job_title": "CFO",
            "department": "Finance",
            "industry": "Finance",
            "city": "Chicago",
            "state": "IL",
            "country": "USA",
            "lead_status": LeadStatus.NEW,
            "lead_score": 65,
            "source": "Conference",
            "tags": ["finance", "enterprise", "new-lead"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=James",
        },
        {
            "first_name": "Aisha",
            "last_name": "Patel",
            "email": "aisha.p@healthtech.io",
            "phone": "+1-617-555-0505",
            "company": "HealthTech Solutions",
            "job_title": "CEO",
            "department": "Executive",
            "industry": "Healthcare",
            "city": "Boston",
            "state": "MA",
            "country": "USA",
            "lead_status": LeadStatus.QUALIFIED,
            "lead_score": 95,
            "source": "Referral",
            "tags": ["healthcare", "startup", "hot-lead"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Aisha",
        },
        {
            "first_name": "David",
            "last_name": "Kim",
            "email": "david.kim@cloudops.com",
            "phone": "+1-206-555-0606",
            "company": "CloudOps Platform",
            "job_title": "Head of DevOps",
            "department": "Engineering",
            "industry": "Cloud Computing",
            "city": "Seattle",
            "state": "WA",
            "country": "USA",
            "lead_status": LeadStatus.CONTACTED,
            "lead_score": 72,
            "source": "Website",
            "tags": ["cloud", "devops", "mid-market"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=David",
        },
        {
            "first_name": "Maria",
            "last_name": "Santos",
            "email": "maria.santos@edulearn.com",
            "phone": "+1-512-555-0707",
            "company": "EduLearn Platform",
            "job_title": "VP of Product",
            "department": "Product",
            "industry": "EdTech",
            "city": "Austin",
            "state": "TX",
            "country": "USA",
            "lead_status": LeadStatus.NEW,
            "lead_score": 58,
            "source": "LinkedIn",
            "tags": ["edtech", "startup"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Maria",
        },
        {
            "first_name": "Robert",
            "last_name": "Williams",
            "email": "robert.w@megacorp.com",
            "phone": "+1-404-555-0808",
            "company": "MegaCorp Industries",
            "job_title": "VP of Sales",
            "department": "Sales",
            "industry": "Manufacturing",
            "city": "Atlanta",
            "state": "GA",
            "country": "USA",
            "lead_status": LeadStatus.CONVERTED,
            "lead_score": 88,
            "source": "Conference",
            "tags": ["manufacturing", "enterprise", "customer"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Robert",
        },
        {
            "first_name": "Lisa",
            "last_name": "Thompson",
            "email": "lisa.t@datawise.ai",
            "phone": "+1-720-555-0909",
            "company": "DataWise AI",
            "job_title": "Head of AI/ML",
            "department": "Engineering",
            "industry": "AI/ML",
            "city": "Denver",
            "state": "CO",
            "country": "USA",
            "lead_status": LeadStatus.QUALIFIED,
            "lead_score": 90,
            "source": "Referral",
            "tags": ["ai", "startup", "hot-lead"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Lisa",
        },
        {
            "first_name": "Michael",
            "last_name": "Chang",
            "email": "michael.c@cyberguard.io",
            "phone": "+1-571-555-1010",
            "company": "CyberGuard Security",
            "job_title": "CISO",
            "department": "Security",
            "industry": "Cybersecurity",
            "city": "Washington",
            "state": "DC",
            "country": "USA",
            "lead_status": LeadStatus.CONTACTED,
            "lead_score": 76,
            "source": "Website",
            "tags": ["security", "enterprise", "warm-lead"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Michael",
        },
        {
            "first_name": "Priya",
            "last_name": "Sharma",
            "email": "priya.s@greenergy.com",
            "phone": "+1-503-555-1111",
            "company": "GreenErgy Solutions",
            "job_title": "COO",
            "department": "Operations",
            "industry": "Clean Energy",
            "city": "Portland",
            "state": "OR",
            "country": "USA",
            "lead_status": LeadStatus.NEW,
            "lead_score": 62,
            "source": "LinkedIn",
            "tags": ["energy", "sustainability"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Priya",
        },
        {
            "first_name": "Tom",
            "last_name": "Anderson",
            "email": "tom.a@logisticspro.com",
            "phone": "+1-901-555-1212",
            "company": "LogisticsPro",
            "job_title": "Director of Supply Chain",
            "department": "Logistics",
            "industry": "Logistics",
            "city": "Memphis",
            "state": "TN",
            "country": "USA",
            "lead_status": LeadStatus.UNQUALIFIED,
            "lead_score": 35,
            "source": "Cold Call",
            "tags": ["logistics", "mid-market"],
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Tom",
        },
    ]

    contacts = []
    now = datetime.now(timezone.utc)
    for cd in contacts_data:
        cd["last_contacted"] = now - timedelta(days=random.randint(0, 30))
        cd["created_at"] = now - timedelta(days=random.randint(30, 180))
        cd["updated_at"] = now - timedelta(days=random.randint(0, 10))
        contact = Contact(**cd)
        db.add(contact)
        contacts.append(contact)

    db.flush()

    # --- DEALS ---
    deals_data = [
        {
            "title": "TechCorp Enterprise Platform License",
            "value": 450000,
            "stage": DealStage.NEGOTIATION,
            "probability": 75,
            "expected_close_date": now + timedelta(days=14),
            "company": "TechCorp Solutions",
            "owner": "Alex Rivera",
            "priority": Priority.HIGH,
            "tags": ["enterprise", "annual"],
            "ai_win_probability": 0.78,
            "ai_insights": {
                "risk_factors": ["Competitor pricing pressure"],
                "recommended_actions": [
                    "Schedule executive meeting",
                    "Prepare ROI analysis",
                ],
                "sentiment": "positive",
            },
        },
        {
            "title": "Innovate Inc SaaS Migration",
            "value": 180000,
            "stage": DealStage.PROPOSAL,
            "probability": 50,
            "expected_close_date": now + timedelta(days=30),
            "company": "Innovate Inc",
            "owner": "Alex Rivera",
            "priority": Priority.MEDIUM,
            "tags": ["saas", "migration"],
            "ai_win_probability": 0.55,
            "ai_insights": {
                "risk_factors": ["Budget constraints in Q4"],
                "recommended_actions": [
                    "Offer phased implementation",
                    "Provide case studies",
                ],
                "sentiment": "neutral",
            },
        },
        {
            "title": "Global Retail POS Integration",
            "value": 320000,
            "stage": DealStage.QUALIFICATION,
            "probability": 35,
            "expected_close_date": now + timedelta(days=60),
            "company": "Global Retail Group",
            "owner": "Jordan Lee",
            "priority": Priority.HIGH,
            "tags": ["retail", "integration"],
            "ai_win_probability": 0.42,
            "ai_insights": {
                "risk_factors": [
                    "Complex integration requirements",
                    "Multiple stakeholders",
                ],
                "recommended_actions": ["Technical POC", "Stakeholder mapping"],
                "sentiment": "cautious",
            },
        },
        {
            "title": "Finova Compliance Automation Suite",
            "value": 95000,
            "stage": DealStage.PROSPECTING,
            "probability": 15,
            "expected_close_date": now + timedelta(days=90),
            "company": "Finova Financial",
            "owner": "Jordan Lee",
            "priority": Priority.LOW,
            "tags": ["finance", "compliance"],
            "ai_win_probability": 0.20,
            "ai_insights": {
                "risk_factors": ["Early stage", "Budget not allocated"],
                "recommended_actions": ["Discovery call", "Industry benchmark report"],
                "sentiment": "early",
            },
        },
        {
            "title": "HealthTech AI Diagnostics Platform",
            "value": 780000,
            "stage": DealStage.NEGOTIATION,
            "probability": 80,
            "expected_close_date": now + timedelta(days=7),
            "company": "HealthTech Solutions",
            "owner": "Alex Rivera",
            "priority": Priority.CRITICAL,
            "tags": ["healthcare", "ai", "priority"],
            "ai_win_probability": 0.88,
            "ai_insights": {
                "risk_factors": ["Legal review pending"],
                "recommended_actions": [
                    "Fast-track legal review",
                    "Prepare implementation plan",
                ],
                "sentiment": "very positive",
            },
        },
        {
            "title": "CloudOps Infrastructure Deal",
            "value": 210000,
            "stage": DealStage.PROPOSAL,
            "probability": 45,
            "expected_close_date": now + timedelta(days=45),
            "company": "CloudOps Platform",
            "owner": "Sam Taylor",
            "priority": Priority.MEDIUM,
            "tags": ["cloud", "infrastructure"],
            "ai_win_probability": 0.52,
            "ai_insights": {
                "risk_factors": ["Technical evaluation ongoing"],
                "recommended_actions": [
                    "Arrange technical deep-dive",
                    "Competitive analysis",
                ],
                "sentiment": "neutral",
            },
        },
        {
            "title": "MegaCorp Manufacturing Suite",
            "value": 520000,
            "stage": DealStage.CLOSED_WON,
            "probability": 100,
            "expected_close_date": now - timedelta(days=15),
            "actual_close_date": now - timedelta(days=12),
            "company": "MegaCorp Industries",
            "owner": "Alex Rivera",
            "priority": Priority.HIGH,
            "tags": ["manufacturing", "won"],
            "ai_win_probability": 1.0,
            "ai_insights": {
                "win_factors": [
                    "Strong executive sponsorship",
                    "Clear ROI demonstrated",
                ],
                "sentiment": "closed",
            },
        },
        {
            "title": "DataWise ML Pipeline License",
            "value": 165000,
            "stage": DealStage.QUALIFICATION,
            "probability": 40,
            "expected_close_date": now + timedelta(days=55),
            "company": "DataWise AI",
            "owner": "Sam Taylor",
            "priority": Priority.MEDIUM,
            "tags": ["ai", "data"],
            "ai_win_probability": 0.45,
            "ai_insights": {
                "risk_factors": ["Evaluating alternatives"],
                "recommended_actions": [
                    "Differentiation presentation",
                    "Free trial offer",
                ],
                "sentiment": "competitive",
            },
        },
        {
            "title": "CyberGuard Security Audit Platform",
            "value": 290000,
            "stage": DealStage.CLOSED_LOST,
            "probability": 0,
            "expected_close_date": now - timedelta(days=20),
            "actual_close_date": now - timedelta(days=18),
            "company": "CyberGuard Security",
            "owner": "Jordan Lee",
            "priority": Priority.MEDIUM,
            "tags": ["security", "lost"],
            "ai_win_probability": 0.0,
            "ai_insights": {
                "loss_factors": [
                    "Price too high",
                    "Competitor offered bundled solution",
                ],
                "sentiment": "lost",
            },
        },
        {
            "title": "EduLearn Content Management System",
            "value": 75000,
            "stage": DealStage.PROSPECTING,
            "probability": 20,
            "expected_close_date": now + timedelta(days=75),
            "company": "EduLearn Platform",
            "owner": "Sam Taylor",
            "priority": Priority.LOW,
            "tags": ["edtech", "content"],
            "ai_win_probability": 0.25,
            "ai_insights": {
                "risk_factors": ["Small budget", "Long decision cycle"],
                "recommended_actions": ["Starter package proposal", "ROI calculator"],
                "sentiment": "early",
            },
        },
    ]

    contact_deal_mapping = {
        0: [0],
        1: [1],
        2: [2],
        3: [3],
        4: [4],
        5: [5],
        7: [6],
        8: [7],
        9: [8],
        6: [9],
    }

    deals = []
    for dd in deals_data:
        dd["created_at"] = now - timedelta(days=random.randint(15, 120))
        dd["updated_at"] = now - timedelta(days=random.randint(0, 7))
        deal = Deal(**dd)
        db.add(deal)
        deals.append(deal)

    db.flush()

    # Associate contacts with deals
    for contact_idx, deal_indices in contact_deal_mapping.items():
        for deal_idx in deal_indices:
            if contact_idx < len(contacts) and deal_idx < len(deals):
                deals[deal_idx].contacts.append(contacts[contact_idx])

    db.flush()

    # --- ACTIVITIES ---
    activity_types = [
        ActivityType.CALL,
        ActivityType.EMAIL,
        ActivityType.MEETING,
        ActivityType.NOTE,
    ]
    activity_subjects = {
        ActivityType.CALL: [
            "Discovery call",
            "Follow-up call",
            "Pricing discussion",
            "Technical Q&A",
            "Check-in call",
        ],
        ActivityType.EMAIL: [
            "Proposal sent",
            "Follow-up email",
            "Pricing update",
            "Meeting request",
            "Case study shared",
        ],
        ActivityType.MEETING: [
            "Demo presentation",
            "Contract review",
            "Technical deep-dive",
            "Executive briefing",
            "Quarterly review",
        ],
        ActivityType.NOTE: [
            "Competitor intel",
            "Budget update",
            "Decision timeline",
            "Stakeholder feedback",
            "Requirements update",
        ],
    }

    for i in range(40):
        atype = random.choice(activity_types)
        subject = random.choice(activity_subjects[atype])
        contact = random.choice(contacts)
        deal = random.choice(deals) if random.random() > 0.3 else None
        activity = Activity(
            type=atype,
            subject=subject,
            description=f"Activity: {subject} with {contact.first_name} {contact.last_name}",
            contact_id=contact.id,
            deal_id=deal.id if deal else None,
            duration_minutes=(
                random.randint(5, 60)
                if atype in [ActivityType.CALL, ActivityType.MEETING]
                else None
            ),
            outcome=(
                random.choice(
                    ["Positive", "Neutral", "Follow-up needed", "No response"]
                )
                if atype != ActivityType.NOTE
                else None
            ),
            scheduled_at=now
            - timedelta(days=random.randint(0, 60), hours=random.randint(0, 8)),
            completed_at=(
                now - timedelta(days=random.randint(0, 55))
                if random.random() > 0.2
                else None
            ),
            created_at=now - timedelta(days=random.randint(0, 60)),
        )
        db.add(activity)

    # --- TASKS ---
    task_titles = [
        "Follow up with client on proposal",
        "Prepare Q4 forecast report",
        "Schedule demo for new feature",
        "Update CRM records",
        "Send contract for review",
        "Prepare competitive analysis",
        "Call to discuss pricing",
        "Set up onboarding meeting",
        "Review customer feedback",
        "Create ROI presentation",
        "Update pipeline forecast",
        "Send meeting notes",
        "Research competitor offerings",
        "Prepare case study",
        "Schedule quarterly review",
    ]
    assignees = ["Alex Rivera", "Jordan Lee", "Sam Taylor"]

    for i, title in enumerate(task_titles):
        contact = random.choice(contacts)
        status = random.choice(
            [
                TaskStatus.TODO,
                TaskStatus.TODO,
                TaskStatus.IN_PROGRESS,
                TaskStatus.COMPLETED,
            ]
        )
        task = Task(
            title=title,
            description=f"Task related to {contact.company}",
            status=status,
            priority=random.choice(
                [Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.CRITICAL]
            ),
            due_date=now + timedelta(days=random.randint(-5, 30)),
            contact_id=contact.id,
            assigned_to=random.choice(assignees),
            completed_at=(
                now - timedelta(days=random.randint(0, 10))
                if status == TaskStatus.COMPLETED
                else None
            ),
            created_at=now - timedelta(days=random.randint(0, 30)),
            updated_at=now - timedelta(days=random.randint(0, 5)),
        )
        db.add(task)

    # --- AI AGENT TASKS ---
    ai_tasks_data = [
        {
            "task_type": AgentTaskType.LEAD_SCORING,
            "status": AgentTaskStatus.COMPLETED,
            "input_data": {
                "contact_id": 1,
                "features": ["engagement_high", "budget_confirmed"],
            },
            "output_data": {
                "score": 92,
                "factors": [
                    "High email engagement rate",
                    "Budget confirmed",
                    "Decision maker",
                ],
                "recommendation": "Prioritize for immediate outreach",
            },
            "confidence_score": 0.94,
            "cost_estimate": 0.002,
            "actual_cost": 0.0018,
            "latency_ms": 245,
            "triggered_by": "automation",
        },
        {
            "task_type": AgentTaskType.EMAIL_DRAFT,
            "status": AgentTaskStatus.COMPLETED,
            "input_data": {
                "contact_id": 2,
                "context": "follow_up_proposal",
                "tone": "professional",
            },
            "output_data": {
                "subject": "Following Up: Innovate Inc Partnership Proposal",
                "body": "Dear Marcus,\n\nI hope this message finds you well...",
                "alternatives": 3,
            },
            "confidence_score": 0.87,
            "cost_estimate": 0.008,
            "actual_cost": 0.0072,
            "latency_ms": 1840,
            "triggered_by": "user",
        },
        {
            "task_type": AgentTaskType.DEAL_ANALYSIS,
            "status": AgentTaskStatus.COMPLETED,
            "input_data": {"deal_id": 1, "analysis_type": "risk_assessment"},
            "output_data": {
                "risk_level": "medium",
                "win_probability": 0.78,
                "key_risks": ["Competitor undercutting", "Budget freeze risk"],
                "mitigation_strategies": [
                    "Demonstrate unique value prop",
                    "Offer flexible payment terms",
                ],
            },
            "confidence_score": 0.82,
            "cost_estimate": 0.015,
            "actual_cost": 0.013,
            "latency_ms": 3200,
            "triggered_by": "user",
        },
        {
            "task_type": AgentTaskType.CHURN_PREDICTION,
            "status": AgentTaskStatus.COMPLETED,
            "input_data": {"customer_segment": "enterprise", "time_horizon": "90_days"},
            "output_data": {
                "at_risk_accounts": [
                    {
                        "company": "CloudOps Platform",
                        "churn_probability": 0.35,
                        "signals": ["Decreased usage", "Support ticket spike"],
                    }
                ],
                "total_revenue_at_risk": 501000,
            },
            "confidence_score": 0.79,
            "cost_estimate": 0.025,
            "actual_cost": 0.022,
            "latency_ms": 4500,
            "triggered_by": "schedule",
        },
        {
            "task_type": AgentTaskType.FORECAST,
            "status": AgentTaskStatus.COMPLETED,
            "input_data": {"period": "Q4_2026", "model": "ensemble"},
            "output_data": {
                "predicted_revenue": 2850000,
                "confidence_interval": [2420000, 3280000],
                "key_drivers": ["HealthTech deal close", "TechCorp expansion"],
                "risk_adjusted_forecast": 2650000,
            },
            "confidence_score": 0.76,
            "cost_estimate": 0.05,
            "actual_cost": 0.045,
            "latency_ms": 8900,
            "triggered_by": "schedule",
        },
        {
            "task_type": AgentTaskType.MEETING_SUMMARY,
            "status": AgentTaskStatus.RUNNING,
            "input_data": {
                "meeting_id": "mtg_2026_q4_review",
                "participants": ["Sarah Chen", "Alex Rivera"],
            },
            "output_data": {},
            "confidence_score": None,
            "cost_estimate": 0.012,
            "actual_cost": None,
            "latency_ms": None,
            "triggered_by": "automation",
        },
    ]

    for atd in ai_tasks_data:
        atd["created_at"] = now - timedelta(hours=random.randint(0, 72))
        atd["completed_at"] = (
            now - timedelta(hours=random.randint(0, 24))
            if atd["status"] == AgentTaskStatus.COMPLETED
            else None
        )
        ai_task = AIAgentTask(**atd)
        db.add(ai_task)

    # --- ANALYTICS SNAPSHOTS ---
    seed_analytics_snapshots(db)

    # --- CALENDAR EVENTS ---
    calendar_events = [
        {
            "title": "TechCorp Contract Negotiation",
            "description": "Final contract terms discussion with Sarah Chen",
            "start_time": now + timedelta(days=1, hours=2),
            "end_time": now + timedelta(days=1, hours=3),
            "location": "Zoom Meeting",
            "event_type": "meeting",
            "attendees": ["Sarah Chen", "Alex Rivera"],
            "color": "#6366f1",
        },
        {
            "title": "HealthTech Demo Call",
            "description": "Product demo for AI Diagnostics Platform",
            "start_time": now + timedelta(days=2, hours=4),
            "end_time": now + timedelta(days=2, hours=5, minutes=30),
            "location": "Google Meet",
            "event_type": "demo",
            "attendees": ["Aisha Patel", "Alex Rivera", "Jordan Lee"],
            "color": "#f59e0b",
        },
        {
            "title": "Pipeline Review",
            "description": "Weekly pipeline review with sales team",
            "start_time": now + timedelta(days=3, hours=1),
            "end_time": now + timedelta(days=3, hours=2),
            "location": "Conference Room A",
            "event_type": "meeting",
            "attendees": ["Alex Rivera", "Jordan Lee", "Sam Taylor"],
            "color": "#6366f1",
        },
        {
            "title": "Follow-up: Innovate Inc",
            "description": "Follow up on SaaS migration proposal",
            "start_time": now + timedelta(days=1, hours=5),
            "end_time": now + timedelta(days=1, hours=5, minutes=30),
            "location": "Phone",
            "event_type": "call",
            "attendees": ["Marcus Johnson"],
            "color": "#10b981",
        },
        {
            "title": "Global Retail POC Planning",
            "description": "Technical POC scope and timeline",
            "start_time": now + timedelta(days=4, hours=3),
            "end_time": now + timedelta(days=4, hours=4, minutes=30),
            "location": "Teams Meeting",
            "event_type": "meeting",
            "attendees": ["Elena Rodriguez", "Jordan Lee"],
            "color": "#6366f1",
        },
        {
            "title": "Q4 Forecast Review",
            "description": "Quarterly forecast discussion with leadership",
            "start_time": now + timedelta(days=5, hours=2),
            "end_time": now + timedelta(days=5, hours=3),
            "location": "Executive Board Room",
            "event_type": "meeting",
            "attendees": ["Alex Rivera", "Jordan Lee", "Sam Taylor", "VP Sales"],
            "color": "#8b5cf6",
        },
        {
            "title": "DataWise Follow-up",
            "description": "Technical deep-dive and differentiation discussion",
            "start_time": now + timedelta(days=2, hours=1),
            "end_time": now + timedelta(days=2, hours=2),
            "location": "Zoom Meeting",
            "event_type": "follow_up",
            "attendees": ["Lisa Thompson", "Sam Taylor"],
            "color": "#ef4444",
        },
        {
            "title": "Customer Success Alignment: HyperScale",
            "description": "Quarterly enterprise onboarding review and SLA checkpoint with account team.",
            "start_time": now.replace(hour=11, minute=0, second=0),
            "end_time": now.replace(hour=12, minute=0, second=0),
            "location": "Google Meet",
            "event_type": "meeting",
            "attendees": ["elena@hyperscale.ai", "alex@neuronforce.ai"],
            "color": "#10b981",
        },
        {
            "title": "AI Agent Mesh Cost Optimization Sync",
            "description": "Evaluating token consumption and sub-100ms routing efficiency across models.",
            "start_time": now.replace(hour=14, minute=30, second=0),
            "end_time": now.replace(hour=15, minute=30, second=0),
            "location": "Zoom Meeting",
            "event_type": "demo",
            "attendees": ["jordan@neuronforce.ai", "alex@neuronforce.ai"],
            "color": "#8b5cf6",
        },
        {
            "title": "CyberGuard Security Governance Sign-off",
            "description": "Final SOC2 Type II compliance audit review and enterprise DPA sign-off.",
            "start_time": (now + timedelta(days=1)).replace(
                hour=9, minute=30, second=0
            ),
            "end_time": (now + timedelta(days=1)).replace(hour=10, minute=30, second=0),
            "location": "Teams Meeting",
            "event_type": "review",
            "attendees": ["ciso@cyberguard.io", "legal@neuronforce.ai"],
            "color": "#ef4444",
        },
        {
            "title": "Weekly Sales Leadership Standup",
            "description": "Pipeline acceleration metrics, deal probability rankings, and quarterly targets.",
            "start_time": (now + timedelta(days=1)).replace(
                hour=11, minute=30, second=0
            ),
            "end_time": (now + timedelta(days=1)).replace(hour=12, minute=30, second=0),
            "location": "Executive Board Room",
            "event_type": "meeting",
            "attendees": [
                "alex@neuronforce.ai",
                "jordan@neuronforce.ai",
                "sam@neuronforce.ai",
            ],
            "color": "#06b6d4",
        },
        {
            "title": "Finova Compliance Architecture Review",
            "description": "Technical architecture validation for automated audit workflows.",
            "start_time": (now - timedelta(days=1)).replace(
                hour=10, minute=0, second=0
            ),
            "end_time": (now - timedelta(days=1)).replace(hour=11, minute=0, second=0),
            "location": "Zoom Meeting",
            "event_type": "presentation",
            "attendees": ["james.park@finova.io", "alex@neuronforce.ai"],
            "color": "#6366f1",
        },
    ]

    for ced in calendar_events:
        ced["created_at"] = now - timedelta(days=random.randint(1, 7))
        ced["updated_at"] = now
        event = CalendarEvent(**ced)
        db.add(event)

    db.commit()
    print("✅ Database seeded with NeuronForce demo data!")


if __name__ == "__main__":
    print("🚀 Seeding NeuronForce database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    print("Done!")
