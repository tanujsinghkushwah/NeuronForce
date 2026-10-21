---
description: Break large monolithic files into cohesive sub-folder sections and modular routers.
globs: ["backend/**", "frontend/**"]
alwaysApply: true
---

# Modular File Organization Rule

## Break Large Monolithic Files
- Avoid maintaining large, multi-responsibility files. When a file grows beyond a cohesive size (e.g. >200-300 lines or handling multiple resource domains), break it down into modular sub-folder sections.

## Backend Modular Architecture
- **Routes & Endpoints**: Separate large entrypoint files like `backend/app/main.py` into dedicated domain modules in `backend/app/routes/` or `backend/app/routers/` using FastAPI `APIRouter` (e.g. `routes/auth.py`, `routes/contacts.py`, `routes/deals.py`, `routes/ai_agents.py`, `routes/analytics.py`, `routes/calendar.py`, `routes/settings.py`).
- **Models**: Group related entities inside `backend/app/models/` with an `__init__.py` barrel export so external imports remain clean and backward compatible.
- **Schemas**: Split request/response models into modular domain files under `backend/app/schemas/` when schemas expand.
- **Business Logic & Services**: Separate core business logic, AI orchestration, and external integrations into dedicated `services/` or `utils/` modules.

## Frontend Modular Architecture
- Break large page components into focused, reusable subcomponents in `components/`.
- Isolate state logic into custom hooks or context providers (`context/`) rather than bloating page views.
