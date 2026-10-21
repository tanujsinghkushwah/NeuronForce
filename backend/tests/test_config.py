"""
Unit Tests for Application Configuration (backend/app/config.py)
Tests default settings, environment loading, and CORS parsing.
"""

import os
import pytest
from app.config import settings, Settings


def test_default_settings():
    """Verify that default settings load with expected defaults."""
    assert settings.DATABASE_URL.startswith("sqlite") or "postgres" in settings.DATABASE_URL
    assert settings.JWT_ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0
    assert isinstance(settings.cors_origins, list)
    assert len(settings.cors_origins) >= 1
    assert "http://localhost:3000" in settings.cors_origins


def test_cors_origins_property(monkeypatch):
    """Test custom CORS_ORIGINS parsing from comma-separated string."""
    monkeypatch.setenv("CORS_ORIGINS", "https://app.neuronforce.ai, https://admin.neuronforce.ai ")
    s = Settings()
    assert s.cors_origins == ["https://app.neuronforce.ai", "https://admin.neuronforce.ai"]


def test_environment_override(monkeypatch):
    """Test environment variable overrides on Settings."""
    monkeypatch.setenv("ENVIRONMENT", "staging")
    monkeypatch.setenv("JWT_SECRET_KEY", "custom-test-secret-key-123")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    s = Settings()
    assert s.ENVIRONMENT == "staging"
    assert s.JWT_SECRET_KEY == "custom-test-secret-key-123"
    assert s.ACCESS_TOKEN_EXPIRE_MINUTES == 60
