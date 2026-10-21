"""
NeuronForce API Routers Package
Aggregates all modular route handlers.
"""

from fastapi import FastAPI

from app.routers.dashboard import router as dashboard_router
from app.routers.contacts import router as contacts_router
from app.routers.deals import router as deals_router
from app.routers.activities import router as activities_router
from app.routers.ai_agents import router as ai_agents_router
from app.routers.calendar import router as calendar_router
from app.routers.analytics import router as analytics_router
from app.routers.settings import router as settings_router
from app.routers.auth import router as auth_router
from app.routers.tickets import router as tickets_router
from app.routers.campaigns import router as campaigns_router

all_routers = [
    dashboard_router,
    contacts_router,
    deals_router,
    activities_router,
    ai_agents_router,
    calendar_router,
    analytics_router,
    settings_router,
    auth_router,
    tickets_router,
    campaigns_router,
]


def register_routers(app: FastAPI) -> None:
    """Register all domain routers with the FastAPI application instance."""
    for router in all_routers:
        app.include_router(router)
