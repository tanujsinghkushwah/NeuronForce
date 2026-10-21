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
├── frontend/               # Next.js 15 + TypeScript + Tailwind CSS
│   ├── src/
│   │   └── app/            # App Router pages and layouts
│   ├── package.json        # Dependencies (Recharts, Lucide, date-fns)
│   └── ...
├── backend/                # FastAPI + Python 3.14 + SQLAlchemy 2.1
│   ├── app/
│   │   ├── __init__.py     # Package init
│   │   ├── database.py     # SQLAlchemy engine, session management, CP rationale
│   │   ├── models.py       # 7 core data models (Contacts, Deals, Activities, Tasks, AI, Analytics, Calendar)
│   │   ├── schemas.py      # Pydantic v2 schemas for all requests and responses
│   │   ├── seed_data.py    # Realistic enterprise demo dataset
│   │   └── main.py         # 25+ REST endpoints with CORS and auto-seeding
│   ├── neuronforce.db      # SQLite database (auto-created on startup)
│   └── venv/               # Python virtual environment (ignored in git)
├── .gitignore              # Monorepo-wide ignore rules
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
