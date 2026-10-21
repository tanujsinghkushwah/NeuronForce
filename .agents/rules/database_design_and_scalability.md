---
description: Create proper data models following database design best practices with scalability and reliability.
globs: ["backend/app/models/**", "backend/app/database.py", "backend/app/schemas/**"]
alwaysApply: true
---

# Database Design, Scalability & Reliability Rule

## Data Modeling Best Practices
- Separate data models into dedicated modules within the `models/` package (e.g. `models/user.py`, `models/deal.py`, `models/oauth.py`) instead of maintaining a monolithic models file.
- Follow relational normalization standards:
  - Isolate authentication and OAuth provider records (`oauth_accounts`) and active tokens/sessions (`user_sessions`) from the core `users` entity.
  - Define explicit foreign keys with suitable `ondelete` cascade rules (e.g. `CASCADE` for user-dependent sessions/tokens).
  - Add database indexes on all lookup columns, foreign keys, unique identifiers, and frequently filtered fields (`email`, `user_id`, `provider_user_id`, `stage`, etc.).

## Scalability & Production Readiness
- Design database schemas and connections to easily scale from SQLite in local development to PostgreSQL in production environments.
- Maintain connection pooling best practices (e.g. `pool_pre_ping=True`, proper connection limits).
- Use timezone-aware UTC timestamps (`datetime.now(timezone.utc)`) across all timestamp columns.

## System Reliability & Data Integrity
- Ensure ACID compliance across state transitions and financial/pipeline calculations.
- Validate all incoming data using strict Pydantic schemas before persisting to the database.
- Use atomic transactions and proper rollback handling (`db.rollback()`) within database session scopes.
