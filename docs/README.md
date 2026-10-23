# NeuronForce — Architecture & Documentation Hub

Welcome to the **NeuronForce Architectural Reference & Documentation Hub**. This directory contains the complete technical design specifications, high-level diagrams, and trade-off rationales for the platform.

---

## 📚 Core System Design & Architecture Documents

| Document | Primary Focus | Key Content & Diagrams |
|---|---|---|
| 🤖 [**Agentic System High-Level Design (HLD)**](HLD_AGENTIC_SYSTEM.md) | LangGraph Multi-Agent Orchestration | • Cyclic StateGraph architecture & node topology<br/>• Multi-turn session memory & semantic pronoun resolution<br/>• Specialist sub-agent mesh (Lead, Deal, Email, Churn, Summary)<br/>• Dynamic CRM entity & attendee resolution<br/>• OpenRouter gateway & deterministic offline fallback<br/>• 15-scenario evaluation harness (`agents/evals/`) |
| ⚡ [**Backend System High-Level Design (HLD)**](HLD_BACKEND_SYSTEM.md) | ASGI Modular Monolith Architecture | • FastAPI request/response lifecycle & middleware pipeline<br/>• Complete Relational Entity-Relationship (ER) diagram<br/>• Dual-Track Auth (Google OAuth 2.0 PKCE + Demo Persona Simulator)<br/>• Dual-tier outbound email delivery (Resend HTTP + SMTP fallback)<br/>• Sub-15ms token-ranked global omnisearch engine<br/>• 1M DAU horizontal scale-out topology |
| ⚖️ [**System Design Decisions & Trade-Offs**](SYSTEM_DESIGN_DECISIONS.md) | Architectural Decisions Matrix | • 30 deep-dive technical decisions with alternatives evaluated<br/>• Pros, cons, and mitigations for each architectural choice<br/>• Demo pitch scripts for technical evaluations & system design interviews<br/>• CAP theorem justification (Relational CP vs. NoSQL) |
| 🎯 [**Initial Platform Vision & Plan**](PLAN.md) | MVP Vision & Foundation | • Foundational thesis: AI-agent CRM vs. legacy Salesforce<br/>• Cost and confidence transparency philosophy<br/>• Initial MVP scope and phase breakdown |

---

## 🎨 Demo-Ready Presentation Diagrams & Draw.io Assets

For live product demonstrations, architecture pitches, and visual walkthroughs:

| Asset | Format | Purpose & Description |
|---|---|---|
| 🤖 **Agentic Flow Diagram (PNG)** | [`images/hld_agentic_system.png`](images/hld_agentic_system.png) | Ultra-crisp 2560×1520 PNG showing LangGraph cyclic execution, session store, pronoun resolution, subagents & OpenRouter. |
| 🤖 **Agentic Flow Draw.io File** | [`hld_agentic_system.drawio`](hld_agentic_system.drawio) | Native Draw.io XML file ready to import/edit in [diagrams.net](https://app.diagrams.net). |
| ⚡ **Backend Architecture Diagram (PNG)** | [`images/hld_backend_system.png`](images/hld_backend_system.png) | Ultra-crisp 2560×1520 PNG highlighting Modular Monolith, Relational CP Consistency (CAP Theorem), Dual-Track Auth, and 1M Scale. |
| ⚡ **Backend Architecture Draw.io File** | [`hld_backend_system.drawio`](hld_backend_system.drawio) | Native Draw.io XML file ready to import/edit in [diagrams.net](https://app.diagrams.net). |
| 🖥️ **Agentic Fullscreen Presentation** | [`hld_agentic_system.html`](hld_agentic_system.html) | Standalone responsive dark-theme HTML diagram. |
| 🖥️ **Backend Fullscreen Presentation** | [`hld_backend_system.html`](hld_backend_system.html) | Standalone responsive dark-theme HTML diagram. |

---

## 🗺️ Architectural Visualizations Directory

Product tour screenshots and UI cockpit visual references are stored in:
- [`images/`](images/): High-resolution UI captures of the Sales & AI Telemetry Dashboard, Autonomous Agent Studio, Deals Pipeline Kanban, Global Omnisearch, Contact Intelligence, and Dual-Track Auth Guard.
