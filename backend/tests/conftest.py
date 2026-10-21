"""
NeuronForce Pytest Configuration & Test Fixtures
Provides isolated in-memory database and FastAPI TestClient for unit tests.
"""

import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Ensure backend root is on sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.database import Base, get_db
import app.database as app_db
from app.main import app

# In-memory test database with StaticPool to keep state across threads/connections
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db(monkeypatch_session=None):
    """Create all tables in memory once for the test session."""
    # Ensure startup event in tests seeds the in-memory DB or skips file DB
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    """Provides a clean, isolated database transaction for each test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session, monkeypatch):
    """Provides a FastAPI TestClient connected to the isolated test session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Override get_db in dependency overrides and in the module
    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.setattr(app_db, "get_db", override_get_db)
    monkeypatch.setattr(app_db, "SessionLocal", lambda: db_session)

    with TestClient(app, raise_server_exceptions=True) as test_client:
        yield test_client

    app.dependency_overrides.clear()
