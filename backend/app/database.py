"""
NeuronForce Database Configuration
Uses SQLite for MVP demo (easily swappable to PostgreSQL for production).
SQLite is ACID-compliant and suitable for demo/dev; PostgreSQL recommended for production
as a CP system under CAP theorem (consistency + partition tolerance).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# For MVP, use SQLite. For production, swap to PostgreSQL:
# DATABASE_URL = "postgresql://user:password@localhost:5432/neuronforce"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./neuronforce.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency injection for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
