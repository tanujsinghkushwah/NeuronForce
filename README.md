# NeuronForce — AI-Native CRM Platform

> **A next-generation, AI-agent-powered CRM platform designed as an intelligent alternative to Salesforce.** Built on modern architecture principles with non-deterministic AI decisions where cost, reliability, and business impact justify automation.

---

## ⚡ Core Philosophy: Why NeuronForce?

Traditional enterprise CRMs like Salesforce are often **bloated, slow, and constrained by rigid, deterministic rules** (e.g., legacy Flow Builder / Process Builder). While Salesforce introduced Agentforce, it remains opaque in its cost, latency, and reasoning.

**NeuronForce** re-architects CRM from the ground up:
1. **AI Agents with Cost & Confidence Visibility**: Every autonomous action (lead scoring, deal risk analysis, predictive forecasting, email drafting) exposes its confidence score, estimated/actual token cost, and execution latency.
2. **Sub-100ms Performance**: Lightweight, modular stack with FastAPI and Next.js, eliminating legacy CRM interface lag.
3. **Transparent Automation Boundary**: Clear demarcation between deterministic business logic (ACID transactional guarantees for deals and contacts) and non-deterministic probabilistic intelligence (AI agents).
4. **CP System Architecture**: Built with PostgreSQL/ACID compliance at the foundation to guarantee transactional integrity across pipeline and revenue states.

---

## 🏗️ Repository Architecture

The project is structured as a clean monorepo:

```
neuronforce/
├── frontend/               # Next.js 16 + TypeScript + Tailwind CSS 4
│   ├── src/
│   │   ├── app/            # App Router: Dashboard (/), Contacts, Deals, AI Agents, Analytics, Calendar, Settings
│   │   ├── components/     # UI Shell (Sidebar, Header)
│   │   ├── lib/            # Centralized API client (api.ts)
│   │   └── types/          # Full TypeScript domain contracts (crm.ts)
│   ├── package.json        # Dependencies (Recharts, Lucide React, clsx)
│   └── ...
├── backend/                # FastAPI + Python 3.14 + SQLAlchemy 2.1
│   ├── app/
│   │   ├── database.py     # SQLAlchemy 2.0 DeclarativeBase, session manager, CP rationale
│   │   ├── models.py       # 7 core data models (Contacts, Deals, Activities, Tasks, AI, Analytics, Calendar)
│   │   ├── schemas.py      # Pydantic v2 schemas with ConfigDict
│   │   └── main.py         # 25+ REST endpoints with CORS, lifespan handler
│   ├── scripts/
│   │   └── seed_data.py    # Standalone runnable enterprise demo dataset seed script
│   ├── tests/              # Comprehensive Pytest test suite (22 unit tests)
│   │   ├── conftest.py     # Isolated in-memory SQLite fixtures & TestClient
│   │   ├── test_health_and_dashboard.py
│   │   ├── test_contacts.py
│   │   ├── test_deals.py
│   │   ├── test_activities_and_tasks.py
│   │   ├── test_ai_agents.py
│   │   └── test_calendar_analytics_settings.py
│   ├── neuronforce.db      # SQLite database (auto-created on startup)
│   └── requirements.txt    # Backend dependencies including pytest & httpx
├── .gitignore              # Monorepo-wide ignore rules
├── PLAN.md                 # Architecture roadmap & specifications
└── README.md               # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Backend (FastAPI)

```bash
cd backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt  # or: pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic pydantic python-dateutil

# Run backend development server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run standalone database seeder (optional, runs on startup)
python -m scripts.seed_data

# Run full backend unit test suite (22 tests)
pytest -v tests
```
- API Swagger Documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`

### 2. Frontend (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Run frontend development server
npm run dev
```
- Application Web UI: `http://localhost:3000`

---

## 📊 Modules & API Coverage

- **Dashboard**: High-level sales KPIs, revenue trends, pipeline funnel, recent activities, AI cost metrics.
- **Contacts**: Full lead lifecycle tracking, contact records, lead score categorization, source attribution.
- **Deals Pipeline**: Multi-stage deal funnel (Prospecting → Negotiation → Closed Won/Lost), win probability, AI risk insights.
- **AI Agent Automation**: Autonomous task runner for Lead Scoring, Email Drafting, Deal Risk Analysis, Churn Prediction, and Revenue Forecasting.
- **Activities & Tasks**: CRM interactions timeline (calls, meetings, emails) and task management.
- **Calendar**: Meeting & schedule coordination tied directly to contacts and deals.
- **Analytics**: Historical snapshots, team leaderboards, conversion rates, and AI ROI calculator.
- **Settings**: AI thresholds, budget controls, and pipeline stage configuration.
