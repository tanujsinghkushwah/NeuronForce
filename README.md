# NeuronForce — AI-Native CRM Platform

> **A next-generation, AI-agent-powered CRM platform designed as an intelligent, transparent alternative to Salesforce.** Built on modern architecture principles with sub-100ms response times, cyclic LangGraph multi-agent orchestration, and explicit cost & confidence telemetry on every autonomous decision.

---

## ⚡ Why NeuronForce?

Traditional enterprise CRMs like Salesforce are **slow, monolithic, and rigid**. While tools like Agentforce introduce generative AI, they operate as opaque black boxes with high seat licenses and hidden token costs, latencies, and reasoning steps.

**NeuronForce** re-architects the CRM platform from first principles:

1. **Autonomous Multi-Agent Orchestration**: Built on LangGraph StateGraphs with cyclic execution, dynamic CRM tool routing, and multi-turn conversational session memory with semantic pronoun resolution.
2. **Cost & Confidence Transparency**: Every autonomous action exposes confidence scores, fractional-cent token costs, execution latency, and reasoning traces.
3. **Sub-100ms Performance**: Decoupled ASGI modular architecture (FastAPI + Next.js 16 App Router) eliminating legacy CRM interface bloat.
4. **Pragmatic Automation Boundary**: Strict ACID transactional guarantees for financial deals and contact records, paired with probabilistic LLMs for sales outreach, churn prediction, and scheduling.

---

## 🏗️ Repository Architecture

```
neuronforce/
├── agents/                     # Multi-Agent LangGraph Framework
│   ├── orchestrator/           # Cyclic StateGraph workflow, routing, and node execution
│   ├── subagents/              # Specialist agents (Lead Scoring, Deal Risk, Email Drafter, Churn Sentinel)
│   ├── tools/                  # CRM action executors (Contacts, Deals, Calendar, Campaigns, Outbound Email)
│   ├── evals/                  # 15-scenario benchmark evaluation suite & runner
│   ├── session_store.py        # Multi-turn conversational memory & pronoun resolution
│   └── context_retriever.py    # Cross-entity CRM dynamic context retrieval
├── backend/                    # FastAPI Modular ASGI Backend
│   ├── app/
│   │   ├── routers/            # 12 modular REST routers (Contacts, Deals, AI Agents, Search, Campaigns, etc.)
│   │   ├── models/             # SQLAlchemy 2.0 relational models (PostgreSQL / SQLite)
│   │   ├── services/           # Outbound email (Resend API + SMTP fallback) & auth services
│   │   ├── auth.py             # Google OAuth 2.0 PKCE & JWT token management
│   │   └── config.py           # Centralized typed application settings
│   ├── scripts/seed_data.py    # Autonomous realistic enterprise CRM seed engine
│   └── tests/                  # Pytest test suite (63 unit & integration tests)
├── frontend/                   # Next.js 16 (React 19) + Tailwind CSS 4
│   ├── src/app/                # App Router: Dashboard, AI Agents Studio, Contacts, Deals, Campaigns, Tickets, Calendar, Analytics
│   ├── src/components/         # Glassmorphic UI Shell, AI Workflow Visualizer, Global Omnisearch, Calendar Grid
│   └── src/lib/api.ts          # Centralized typed API client
├── docs/                       # Architectural Reference & System Design
│   └── SYSTEM_DESIGN_DECISIONS.md # 30 deep-dive architectural decisions & trade-offs
├── docker-compose.yml          # Multi-container production deployment stack
├── start_tunnel.sh             # 1-Click live public demo launcher (Cloudflare Tunnel)
└── README.md
```

---

## 📸 Product Tour & Screenshots

### 1. Revenue & Intelligence Dashboard
> Sub-100ms pipeline velocity, real-time closed revenue trajectories, and deterministic vs. AI agent workload distribution.

![NeuronForce Sales & AI Telemetry Dashboard](docs/images/dashboard.png)

### 2. Autonomous Sales Agent Studio & LangGraph Workflow
> Multi-turn conversational copilot with visual LangGraph execution tracking (Request Understanding → CRM Data Gathering → Intelligent Decision Routing → Specialized Sub-Agents / Direct CRM Actions).

![Autonomous Sales Agent Studio & LangGraph Workflow](docs/images/ai_agents_studio.png)

### 3. Interactive Deals Pipeline & Kanban Funnel
> Multi-stage opportunity funnel with AI-calibrated win probabilities, weighted revenue forecasting, and drag-and-drop stage updates.

![Deals Pipeline Kanban](docs/images/deals_pipeline.png)

### 4. Multi-Entity Global Omnisearch (`Cmd/Ctrl + K`)
> Instant token-ranked fuzzy search across contacts, deals, activities, and support tickets with keyboard navigation.

![Global Omnisearch](docs/images/global_search.png)

### 5. Contact Intelligence & AI Lead Scoring
> Complete customer lifecycle tracking with AI-powered engagement scoring (0–100), full interaction timelines, and contact guards.

![Contact Intelligence & AI Lead Scoring](docs/images/contacts_intelligence.png)

### 6. Dual-Track Authentication & Enterprise Persona Simulator
> Production Google OAuth 2.0 PKCE flow paired with a 1-click zero-friction demo persona simulator for instant testing.

![Dual-Track Authentication Guard](docs/images/auth_guard.png)

---

## ✨ Core Platform Modules

- **Autonomous Agent Studio (`/ai-agents`)**: Natural language CRM copilot with continuous multi-turn dialogue, real-time LangGraph node execution visualization, and automatic CRM action execution (booking meetings, updating stages, drafting follow-ups).
- **Global Omnisearch (`Cmd/Ctrl + K`)**: Token-ranked fuzzy multi-entity search across contacts, deals, timeline activities, and support tickets with keyboard navigation.
- **Deals & Pipeline Management (`/deals`)**: Interactive multi-stage kanban funnel (Prospecting → Qualification → Proposal → Negotiation → Closed Won/Lost) with AI win-probability calibration and deal-risk analysis.
- **Lead & Contact Intelligence (`/contacts`)**: Complete lifecycle tracking, AI-powered engagement scoring, contact deletion guards, and timeline history.
- **Multi-Channel Campaigns (`/campaigns`)**: AI-assisted campaign creation, audience segmentation, email/SMS template generation, and dispatch statistics.
- **Support Tickets (`/tickets`)**: Incident tracking, SLA priority levels, status workflows, and customer history association.
- **Google Calendar Grid (`/calendar`)**: Native time-grid schedule coordination tied directly to CRM contacts and scheduled meetings.
- **Dual-Track Authentication (`/login`)**: Production-grade Google OAuth 2.0 with dynamic origin preservation, alongside an instant 1-click Demo Persona Simulator.
- **Outbound Email Engine**: Dual-tier delivery through Resend API with automatic SMTP fallback and CRM interaction logging.

---

## 🚀 Quick Start Guide

### Option 1: 1-Click Live Public Demo (Recommended)

Launch both backend, frontend, and a public Cloudflare HTTPS tunnel with a single script:

```bash
./start_tunnel.sh
```

### Option 2: Local Development Setup

#### 1. Backend (FastAPI)

```bash
cd backend

# Activate virtual environment
source ../.venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI backend with auto-reload (seeds SQLite DB automatically on startup)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- **Swagger API Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/api/health`

#### 2. Frontend (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Run frontend development server
npm run dev
```

- **Web Application UI**: `http://localhost:3000`

---

## 🧪 Testing & Benchmark Evaluations

### Backend Unit & Integration Tests (63 Tests)

Run the isolated test suite using in-memory SQLite fixtures and mocked external APIs:

```bash
cd backend
pytest -v tests
```

### Multi-Agent Autonomous Evaluation Suite (15 Benchmark Scenarios)

NeuronForce includes a formal evaluation benchmark evaluating orchestrator routing accuracy, entity extraction, graph step consistency, and latency across 15 distinct enterprise scenarios:

```bash
python -m agents.evals.runner
```

---

## ⚙️ Environment Configuration

Create a `.env` file in the project root or `backend/` directory:

```env
# AI Gateway (OpenRouter)
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=google/gemini-2.5-flash-lite

# Dual-Tier Outbound Email
RESEND_API_KEY=your_resend_api_key          # Primary transactional email provider
SMTP_HOST=                                  # Optional SMTP fallback
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=

# Dual-Track Auth / Google SSO (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
JWT_SECRET_KEY=your_jwt_secret_key

# URLs & Database
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
DATABASE_URL=sqlite:///./neuronforce.db      # Or postgresql://user:pass@host:5432/neuronforce
```

---

## 📖 Deep-Dive System Design Documentation

For a comprehensive breakdown of all 30 system design decisions, trade-offs, scalability roadmaps, and interview pitch scripts, refer to:

👉 **[docs/SYSTEM_DESIGN_DECISIONS.md](docs/SYSTEM_DESIGN_DECISIONS.md)**
