"""
NeuronForce - AI-Powered CRM Platform Backend
FastAPI application entrypoint with lifespan context, CORS middleware, and modular routers.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, get_db, Base
from app.routers import register_routers
from scripts.seed_data import seed_database

# Ensure database tables exist
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager: seed database on startup."""
    db = next(get_db())
    try:
        seed_database(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="NeuronForce API",
    description="AI-Powered CRM Platform - Alternative to Salesforce",
    version="1.0.0",
    lifespan=lifespan,
)

from app.config import settings

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=r"^https:\/\/.*\.trycloudflare\.com$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all modular domain routers
register_routers(app)
