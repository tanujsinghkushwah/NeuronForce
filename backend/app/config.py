"""
NeuronForce - Centralized Application Configuration
Loads environment variables from .env and exposes typed application settings.
"""

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = BASE_DIR.parent

# Load .env file from backend directory or project root
dotenv_path = BASE_DIR / ".env"
if not dotenv_path.exists():
    dotenv_path = REPO_ROOT / ".env"

if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    load_dotenv()


class Settings:
    """Centralized typed application settings."""

    def __init__(self):
        # Environment & Diagnostics
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        self.DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

        # Database Configuration
        raw_db_url = os.getenv("DATABASE_URL", "sqlite:///./neuronforce.db")
        if raw_db_url.startswith("sqlite:///."):
            rel = raw_db_url.replace("sqlite:///.", "").lstrip("/")
            self.DATABASE_URL: str = f"sqlite:///{BASE_DIR / rel}"
        else:
            self.DATABASE_URL: str = raw_db_url

        # Security & JWT Configuration
        self.JWT_SECRET_KEY: str = os.getenv(
            "JWT_SECRET_KEY", "neuronforce-enterprise-jwt-secret-key-prod-2026"
        )
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080")
        )  # 7 days

        # Google OAuth 2.0 / SSO Configuration
        self.GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
        self.GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")

        # Network & URLs
        self.FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
        self.BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")

        # OpenRouter AI Configuration
        self.OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
        self.OPENROUTER_MODEL: str = os.getenv(
            "OPENROUTER_MODEL", "google/gemini-2.5-flash-lite"
        )
        self.OPENROUTER_BASE_URL: str = os.getenv(
            "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
        )

        # Optional Firebase Configuration
        self.FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")

        # Outbound Email Dispatch Configuration (Resend free API key)
        self.RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
        self.SMTP_HOST: str = os.getenv("SMTP_HOST", "")
        self.SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
        self.SMTP_USER: str = os.getenv("SMTP_USER", "")
        self.SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
        self.SMTP_FROM_EMAIL: str = os.getenv(
            "SMTP_FROM_EMAIL", "NeuronForce <onboarding@resend.dev>"
        )

    # CORS Allowed Origins
    @property
    def cors_origins(self) -> List[str]:
        raw_origins = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000",
        )
        return [o.strip() for o in raw_origins.split(",") if o.strip()]


settings = Settings()
