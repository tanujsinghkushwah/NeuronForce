"""
NeuronForce Seed Data
Realistic demo data for the CRM platform.
"""

import random
from datetime import datetime, timezone, timedelta
from .models import (
    Contact, Deal, Activity, Task, AIAgentTask, AnalyticsSnapshot,
    CalendarEvent, LeadStatus, DealStage, Priority, TaskStatus,
    ActivityType, AgentTaskType, AgentTaskStatus
)


def seed_database(db):
    """Populate the database with realistic demo data."""

    # Check if data already exists
    if db.query(Contact).count() > 0:
        return

    # --- CONTACTS ---
    contacts_data = [
        {"first_name": "Sarah", "last_name": "Chen", "email": "sarah.chen@techcorp.io",
         "phone": "+1-415-555-0101", "company": "TechCorp Solutions", "job_title": "VP of Engineering",
         "department": "Engineering", "industry": "Technology", "city": "San Francisco", "state": "CA",
         "country": "USA", "lead_status": LeadStatus.QUALIFIED, "lead_score": 92,
         "source": "LinkedIn", "tags": ["enterprise", "tech", "hot-lead"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah"},
        {"first_name": "Marcus", "last_name": "Johnson", "email": "marcus.j@innovate.com",
         "phone": "+1-212-555-0202", "company": "Innovate Inc", "job_title": "CTO",
         "department": "Technology", "industry": "SaaS", "city": "New York", "state": "NY",
         "country": "USA", "lead_status": LeadStatus.CONTACTED, "lead_score": 78,
         "source": "Referral", "tags": ["startup", "saas", "decision-maker"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Marcus"},
        {"first_name": "Elena", "last_name": "Rodriguez", "email": "elena.r@globalretail.com",
         "phone": "+1-305-555-0303", "company": "Global Retail Group", "job_title": "Director of Operations",
         "department": "Operations", "industry": "Retail", "city": "Miami", "state": "FL",
         "country": "USA", "lead_status": LeadStatus.QUALIFIED, "lead_score": 85,
         "source": "Website", "tags": ["retail", "enterprise", "warm-lead"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Elena"},
        {"first_name": "James", "last_name": "Park", "email": "james.park@finova.io",
         "phone": "+1-312-555-0404", "company": "Finova Financial", "job_title": "CFO",
         "department": "Finance", "industry": "Finance", "city": "Chicago", "state": "IL",
         "country": "USA", "lead_status": LeadStatus.NEW, "lead_score": 65,
         "source": "Conference", "tags": ["finance", "enterprise", "new-lead"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=James"},
        {"first_name": "Aisha", "last_name": "Patel", "email": "aisha.p@healthtech.io",
         "phone": "+1-617-555-0505", "company": "HealthTech Solutions", "job_title": "CEO",
         "department": "Executive", "industry": "Healthcare", "city": "Boston", "state": "MA",
         "country": "USA", "lead_status": LeadStatus.QUALIFIED, "lead_score": 95,
         "source": "Referral", "tags": ["healthcare", "startup", "hot-lead"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Aisha"},
        {"first_name": "David", "last_name": "Kim", "email": "david.kim@cloudops.com",
         "phone": "+1-206-555-0606", "company": "CloudOps Platform", "job_title": "Head of DevOps",
         "department": "Engineering", "industry": "Cloud Computing", "city": "Seattle", "state": "WA",
         "country": "USA", "lead_status": LeadStatus.CONTACTED, "lead_score": 72,
         "source": "Website", "tags": ["cloud", "devops", "mid-market"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=David"},
        {"first_name": "Maria", "last_name": "Santos", "email": "maria.santos@edulearn.com",
         "phone": "+1-512-555-0707", "company": "EduLearn Platform", "job_title": "VP of Product",
         "department": "Product", "industry": "EdTech", "city": "Austin", "state": "TX",
         "country": "USA", "lead_status": LeadStatus.NEW, "lead_score": 58,
         "source": "LinkedIn", "tags": ["edtech", "startup"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Maria"},
        {"first_name": "Robert", "last_name": "Williams", "email": "robert.w@megacorp.com",
         "phone": "+1-404-555-0808", "company": "MegaCorp Industries", "job_title": "VP of Sales",
         "department": "Sales", "industry": "Manufacturing", "city": "Atlanta", "state": "GA",
         "country": "USA", "lead_status": LeadStatus.CONVERTED, "lead_score": 88,
         "source": "Conference", "tags": ["manufacturing", "enterprise", "customer"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Robert"},
        {"first_name": "Lisa", "last_name": "Thompson", "email": "lisa.t@datawise.ai",
         "phone": "+1-720-555-0909", "company": "DataWise AI", "job_title": "Head of AI/ML",
         "department": "Engineering", "industry": "AI/ML", "city": "Denver", "state": "CO",
         "country": "USA", "lead_status": LeadStatus.QUALIFIED, "lead_score": 90,
         "source": "Referral", "tags": ["ai", "startup", "hot-lead"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Lisa"},
        {"first_name": "Michael", "last_name": "Chang", "email": "michael.c@cyberguard.io",
         "phone": "+1-571-555-1010", "company": "CyberGuard Security", "job_title": "CISO",
         "department": "Security", "industry": "Cybersecurity", "city": "Washington", "state": "DC",
         "country": "USA", "lead_status": LeadStatus.CONTACTED, "lead_score": 76,
         "source": "Website", "tags": ["security", "enterprise", "warm-lead"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Michael"},
        {"first_name": "Priya", "last_name": "Sharma", "email": "priya.s@greenergy.com",
         "phone": "+1-503-555-1111", "company": "GreenErgy Solutions", "job_title": "COO",
         "department": "Operations", "industry": "Clean Energy", "city": "Portland", "state": "OR",
         "country": "USA", "lead_status": LeadStatus.NEW, "lead_score": 62,
         "source": "LinkedIn", "tags": ["energy", "sustainability"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Priya"},
        {"first_name": "Tom", "last_name": "Anderson", "email": "tom.a@logisticspro.com",
         "phone": "+1-901-555-1212", "company": "LogisticsPro", "job_title": "Director of Supply Chain",
         "department": "Logistics", "industry": "Logistics", "city": "Memphis", "state": "TN",
         "country": "USA", "lead_status": LeadStatus.UNQUALIFIED, "lead_score": 35,
         "source": "Cold Call", "tags": ["logistics", "mid-market"],
         "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Tom"},
    ]

    contacts = []
    now = datetime.now(timezone.utc)
    for i, cd in enumerate(contacts_data):
        cd["last_contacted"] = now - timedelta(days=random.randint(0, 30))
        cd["created_at"] = now - timedelta(days=random.randint(30, 180))
        cd["updated_at"] = now - timedelta(days=random.randint(0, 10))
        contact = Contact(**cd)
        db.add(contact)
        contacts.append(contact)

    db.flush()

    # --- DEALS ---
    deals_data = [
        {"title": "TechCorp Enterprise Platform License", "value": 450000,
         "stage": DealStage.NEGOTIATION, "probability": 75,
         "expected_close_date": now + timedelta(days=14), "company": "TechCorp Solutions",
         "owner": "Alex Rivera", "priority": Priority.HIGH,
         "tags": ["enterprise", "annual"], "ai_win_probability": 0.78,
         "ai_insights": {"risk_factors": ["Competitor pricing pressure"], "recommended_actions": ["Schedule executive meeting", "Prepare ROI analysis"], "sentiment": "positive"}},
        {"title": "Innovate Inc SaaS Migration", "value": 180000,
         "stage": DealStage.PROPOSAL, "probability": 50,
         "expected_close_date": now + timedelta(days=30), "company": "Innovate Inc",
         "owner": "Alex Rivera", "priority": Priority.MEDIUM,
         "tags": ["saas", "migration"], "ai_win_probability": 0.55,
         "ai_insights": {"risk_factors": ["Budget constraints in Q4"], "recommended_actions": ["Offer phased implementation", "Provide case studies"], "sentiment": "neutral"}},
        {"title": "Global Retail POS Integration", "value": 320000,
         "stage": DealStage.QUALIFICATION, "probability": 35,
         "expected_close_date": now + timedelta(days=60), "company": "Global Retail Group",
         "owner": "Jordan Lee", "priority": Priority.HIGH,
         "tags": ["retail", "integration"], "ai_win_probability": 0.42,
         "ai_insights": {"risk_factors": ["Complex integration requirements", "Multiple stakeholders"], "recommended_actions": ["Technical POC", "Stakeholder mapping"], "sentiment": "cautious"}},
        {"title": "Finova Compliance Automation Suite", "value": 95000,
         "stage": DealStage.PROSPECTING, "probability": 15,
         "expected_close_date": now + timedelta(days=90), "company": "Finova Financial",
         "owner": "Jordan Lee", "priority": Priority.LOW,
         "tags": ["finance", "compliance"], "ai_win_probability": 0.20,
         "ai_insights": {"risk_factors": ["Early stage", "Budget not allocated"], "recommended_actions": ["Discovery call", "Industry benchmark report"], "sentiment": "early"}},
        {"title": "HealthTech AI Diagnostics Platform", "value": 780000,
         "stage": DealStage.NEGOTIATION, "probability": 80,
         "expected_close_date": now + timedelta(days=7), "company": "HealthTech Solutions",
         "owner": "Alex Rivera", "priority": Priority.CRITICAL,
         "tags": ["healthcare", "ai", "priority"], "ai_win_probability": 0.88,
         "ai_insights": {"risk_factors": ["Legal review pending"], "recommended_actions": ["Fast-track legal review", "Prepare implementation plan"], "sentiment": "very positive"}},
        {"title": "CloudOps Infrastructure Deal", "value": 210000,
         "stage": DealStage.PROPOSAL, "probability": 45,
         "expected_close_date": now + timedelta(days=45), "company": "CloudOps Platform",
         "owner": "Sam Taylor", "priority": Priority.MEDIUM,
         "tags": ["cloud", "infrastructure"], "ai_win_probability": 0.52,
         "ai_insights": {"risk_factors": ["Technical evaluation ongoing"], "recommended_actions": ["Arrange technical deep-dive", "Competitive analysis"], "sentiment": "neutral"}},
        {"title": "MegaCorp Manufacturing Suite", "value": 520000,
         "stage": DealStage.CLOSED_WON, "probability": 100,
         "expected_close_date": now - timedelta(days=15), "actual_close_date": now - timedelta(days=12),
         "company": "MegaCorp Industries", "owner": "Alex Rivera", "priority": Priority.HIGH,
         "tags": ["manufacturing", "won"], "ai_win_probability": 1.0,
         "ai_insights": {"win_factors": ["Strong executive sponsorship", "Clear ROI demonstrated"], "sentiment": "closed"}},
        {"title": "DataWise ML Pipeline License", "value": 165000,
         "stage": DealStage.QUALIFICATION, "probability": 40,
         "expected_close_date": now + timedelta(days=55), "company": "DataWise AI",
         "owner": "Sam Taylor", "priority": Priority.MEDIUM,
         "tags": ["ai", "data"], "ai_win_probability": 0.45,
         "ai_insights": {"risk_factors": ["Evaluating alternatives"], "recommended_actions": ["Differentiation presentation", "Free trial offer"], "sentiment": "competitive"}},
        {"title": "CyberGuard Security Audit Platform", "value": 290000,
         "stage": DealStage.CLOSED_LOST, "probability": 0,
         "expected_close_date": now - timedelta(days=20), "actual_close_date": now - timedelta(days=18),
         "company": "CyberGuard Security", "owner": "Jordan Lee", "priority": Priority.MEDIUM,
         "tags": ["security", "lost"], "ai_win_probability": 0.0,
         "ai_insights": {"loss_factors": ["Price too high", "Competitor offered bundled solution"], "sentiment": "lost"}},
        {"title": "EduLearn Content Management System", "value": 75000,
         "stage": DealStage.PROSPECTING, "probability": 20,
         "expected_close_date": now + timedelta(days=75), "company": "EduLearn Platform",
         "owner": "Sam Taylor", "priority": Priority.LOW,
         "tags": ["edtech", "content"], "ai_win_probability": 0.25,
         "ai_insights": {"risk_factors": ["Small budget", "Long decision cycle"], "recommended_actions": ["Starter package proposal", "ROI calculator"], "sentiment": "early"}},
    ]

    contact_deal_mapping = {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5], 7: [6], 8: [7], 9: [8], 6: [9]}

    deals = []
    for i, dd in enumerate(deals_data):
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
    activity_types = [ActivityType.CALL, ActivityType.EMAIL, ActivityType.MEETING, ActivityType.NOTE]
    activity_subjects = {
        ActivityType.CALL: ["Discovery call", "Follow-up call", "Pricing discussion", "Technical Q&A", "Check-in call"],
        ActivityType.EMAIL: ["Proposal sent", "Follow-up email", "Pricing update", "Meeting request", "Case study shared"],
        ActivityType.MEETING: ["Demo presentation", "Contract review", "Technical deep-dive", "Executive briefing", "Quarterly review"],
        ActivityType.NOTE: ["Competitor intel", "Budget update", "Decision timeline", "Stakeholder feedback", "Requirements update"],
    }

    for i in range(40):
        atype = random.choice(activity_types)
        subject = random.choice(activity_subjects[atype])
        contact = random.choice(contacts)
        deal = random.choice(deals) if random.random() > 0.3 else None
        activity = Activity(
            type=atype,
            subject=subject,
            description=f"Auto-generated activity: {subject} with {contact.first_name} {contact.last_name}",
            contact_id=contact.id,
            deal_id=deal.id if deal else None,
            duration_minutes=random.randint(5, 60) if atype in [ActivityType.CALL, ActivityType.MEETING] else None,
            outcome=random.choice(["Positive", "Neutral", "Follow-up needed", "No response"]) if atype != ActivityType.NOTE else None,
            scheduled_at=now - timedelta(days=random.randint(0, 60), hours=random.randint(0, 8)),
            completed_at=now - timedelta(days=random.randint(0, 55)) if random.random() > 0.2 else None,
            created_at=now - timedelta(days=random.randint(0, 60)),
        )
        db.add(activity)

    # --- TASKS ---
    task_titles = [
        "Follow up with client on proposal", "Prepare Q4 forecast report",
        "Schedule demo for new feature", "Update CRM records",
        "Send contract for review", "Prepare competitive analysis",
        "Call to discuss pricing", "Set up onboarding meeting",
        "Review customer feedback", "Create ROI presentation",
        "Update pipeline forecast", "Send meeting notes",
        "Research competitor offerings", "Prepare case study",
        "Schedule quarterly review",
    ]
    assignees = ["Alex Rivera", "Jordan Lee", "Sam Taylor"]

    for i, title in enumerate(task_titles):
        contact = random.choice(contacts)
        status = random.choice([TaskStatus.TODO, TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED])
        task = Task(
            title=title,
            description=f"Task related to {contact.company}",
            status=status,
            priority=random.choice([Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.CRITICAL]),
            due_date=now + timedelta(days=random.randint(-5, 30)),
            contact_id=contact.id,
            assigned_to=random.choice(assignees),
            completed_at=now - timedelta(days=random.randint(0, 10)) if status == TaskStatus.COMPLETED else None,
            created_at=now - timedelta(days=random.randint(0, 30)),
            updated_at=now - timedelta(days=random.randint(0, 5)),
        )
        db.add(task)

    # --- AI AGENT TASKS ---
    ai_tasks_data = [
        {"task_type": AgentTaskType.LEAD_SCORING, "status": AgentTaskStatus.COMPLETED,
         "input_data": {"contact_id": 1, "features": ["engagement_high", "budget_confirmed"]},
         "output_data": {"score": 92, "factors": ["High email engagement rate", "Budget confirmed", "Decision maker"], "recommendation": "Prioritize for immediate outreach"},
         "confidence_score": 0.94, "cost_estimate": 0.002, "actual_cost": 0.0018, "latency_ms": 245,
         "triggered_by": "automation"},
        {"task_type": AgentTaskType.EMAIL_DRAFT, "status": AgentTaskStatus.COMPLETED,
         "input_data": {"contact_id": 2, "context": "follow_up_proposal", "tone": "professional"},
         "output_data": {"subject": "Following Up: Innovate Inc Partnership Proposal", "body": "Dear Marcus,\n\nI hope this message finds you well. I wanted to follow up on our recent discussion regarding the SaaS migration project...", "alternatives": 3},
         "confidence_score": 0.87, "cost_estimate": 0.008, "actual_cost": 0.0072, "latency_ms": 1840,
         "triggered_by": "user"},
        {"task_type": AgentTaskType.DEAL_ANALYSIS, "status": AgentTaskStatus.COMPLETED,
         "input_data": {"deal_id": 1, "analysis_type": "risk_assessment"},
         "output_data": {"risk_level": "medium", "win_probability": 0.78, "key_risks": ["Competitor undercutting", "Budget freeze risk"], "mitigation_strategies": ["Demonstrate unique value prop", "Offer flexible payment terms"]},
         "confidence_score": 0.82, "cost_estimate": 0.015, "actual_cost": 0.013, "latency_ms": 3200,
         "triggered_by": "user"},
        {"task_type": AgentTaskType.CHURN_PREDICTION, "status": AgentTaskStatus.COMPLETED,
         "input_data": {"customer_segment": "enterprise", "time_horizon": "90_days"},
         "output_data": {"at_risk_accounts": [{"company": "CloudOps Platform", "churn_probability": 0.35, "signals": ["Decreased usage", "Support ticket spike"]}, {"company": "CyberGuard Security", "churn_probability": 0.62, "signals": ["No login in 30 days", "Contract renewal approaching"]}], "total_revenue_at_risk": 501000},
         "confidence_score": 0.79, "cost_estimate": 0.025, "actual_cost": 0.022, "latency_ms": 4500,
         "triggered_by": "schedule"},
        {"task_type": AgentTaskType.FORECAST, "status": AgentTaskStatus.COMPLETED,
         "input_data": {"period": "Q4_2026", "model": "ensemble"},
         "output_data": {"predicted_revenue": 2850000, "confidence_interval": [2420000, 3280000], "key_drivers": ["HealthTech deal close", "TechCorp expansion", "New pipeline from conference leads"], "risk_adjusted_forecast": 2650000},
         "confidence_score": 0.76, "cost_estimate": 0.05, "actual_cost": 0.045, "latency_ms": 8900,
         "triggered_by": "schedule"},
        {"task_type": AgentTaskType.MEETING_SUMMARY, "status": AgentTaskStatus.RUNNING,
         "input_data": {"meeting_id": "mtg_2026_q4_review", "participants": ["Sarah Chen", "Alex Rivera"]},
         "output_data": {},
         "confidence_score": None, "cost_estimate": 0.012, "actual_cost": None, "latency_ms": None,
         "triggered_by": "automation"},
    ]

    for atd in ai_tasks_data:
        atd["created_at"] = now - timedelta(hours=random.randint(0, 72))
        atd["completed_at"] = now - timedelta(hours=random.randint(0, 24)) if atd["status"] == AgentTaskStatus.COMPLETED else None
        ai_task = AIAgentTask(**atd)
        db.add(ai_task)

    # --- ANALYTICS SNAPSHOTS ---
    for i in range(30):
        date = now - timedelta(days=29 - i)
        snapshot = AnalyticsSnapshot(
            date=date,
            total_revenue=random.uniform(80000, 150000) + (i * 3000),
            deals_won=random.randint(0, 3),
            deals_lost=random.randint(0, 2),
            new_contacts=random.randint(1, 8),
            active_deals=random.randint(5, 12),
            pipeline_value=random.uniform(1500000, 3500000),
            conversion_rate=random.uniform(15, 35),
            avg_deal_size=random.uniform(100000, 300000),
            ai_tasks_run=random.randint(5, 25),
            ai_total_cost=random.uniform(0.05, 0.50),
            created_at=date,
        )
        db.add(snapshot)

    # --- CALENDAR EVENTS ---
    event_types = ["meeting", "call", "demo", "follow_up"]
    event_colors = {"meeting": "#6366f1", "call": "#10b981", "demo": "#f59e0b", "follow_up": "#ef4444"}

    calendar_events = [
        {"title": "TechCorp Contract Negotiation", "description": "Final contract terms discussion with Sarah Chen",
         "start_time": now + timedelta(days=1, hours=2), "end_time": now + timedelta(days=1, hours=3),
         "location": "Zoom Meeting", "event_type": "meeting", "attendees": ["Sarah Chen", "Alex Rivera"],
         "color": "#6366f1"},
        {"title": "HealthTech Demo Call", "description": "Product demo for AI Diagnostics Platform",
         "start_time": now + timedelta(days=2, hours=4), "end_time": now + timedelta(days=2, hours=5, minutes=30),
         "location": "Google Meet", "event_type": "demo", "attendees": ["Aisha Patel", "Alex Rivera", "Jordan Lee"],
         "color": "#f59e0b"},
        {"title": "Pipeline Review", "description": "Weekly pipeline review with sales team",
         "start_time": now + timedelta(days=3, hours=1), "end_time": now + timedelta(days=3, hours=2),
         "location": "Conference Room A", "event_type": "meeting", "attendees": ["Alex Rivera", "Jordan Lee", "Sam Taylor"],
         "color": "#6366f1"},
        {"title": "Follow-up: Innovate Inc", "description": "Follow up on SaaS migration proposal",
         "start_time": now + timedelta(days=1, hours=5), "end_time": now + timedelta(days=1, hours=5, minutes=30),
         "location": "Phone", "event_type": "call", "attendees": ["Marcus Johnson"],
         "color": "#10b981"},
        {"title": "Global Retail POC Planning", "description": "Technical POC scope and timeline",
         "start_time": now + timedelta(days=4, hours=3), "end_time": now + timedelta(days=4, hours=4, minutes=30),
         "location": "Teams Meeting", "event_type": "meeting", "attendees": ["Elena Rodriguez", "Jordan Lee"],
         "color": "#6366f1"},
        {"title": "Q4 Forecast Review", "description": "Quarterly forecast discussion with leadership",
         "start_time": now + timedelta(days=5, hours=2), "end_time": now + timedelta(days=5, hours=3),
         "location": "Executive Board Room", "event_type": "meeting",
         "attendees": ["Alex Rivera", "Jordan Lee", "Sam Taylor", "VP Sales"],
         "color": "#8b5cf6"},
        {"title": "DataWise Follow-up", "description": "Technical deep-dive and differentiation discussion",
         "start_time": now + timedelta(days=2, hours=1), "end_time": now + timedelta(days=2, hours=2),
         "location": "Zoom Meeting", "event_type": "follow_up", "attendees": ["Lisa Thompson", "Sam Taylor"],
         "color": "#ef4444"},
    ]

    for ced in calendar_events:
        ced["created_at"] = now - timedelta(days=random.randint(1, 7))
        ced["updated_at"] = now
        event = CalendarEvent(**ced)
        db.add(event)

    db.commit()
    print("✅ Database seeded with demo data!")
