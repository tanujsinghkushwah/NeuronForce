---
description: Enterprise security, secrets management, authentication, input sanitization, and OWASP best practices.
globs: ["**/*"]
alwaysApply: true
---

# Security & Secrets Management Rule

## 1. Secrets & Credentials Policy
- **NEVER hardcode secrets**: Do not hardcode API keys, passwords, database credentials, OAuth client secrets, or JWT encryption keys in source code.
- **Environment variables**: Always source configuration and sensitive credentials via environment variables (`os.getenv(...)`) or validated Pydantic settings.
- **Git protection**: Verify that `.env`, `.env.local`, `.pem`, `.key`, and credential files are included in `.gitignore` and never committed to version control. Maintain `.env.example` with placeholder values for setup.

## 2. Authentication & Authorization (RBAC)
- **Token security**: Sign JWTs with secure keys and algorithms (`HS256` or `RS256`). Always configure explicit token expiration (`exp`) and issuance (`iat`) claims.
- **Session verification**: Check active session validity and revocation status in the database on sensitive requests.
- **Role-Based Access Control (RBAC)**: Validate user roles (`admin`, `revops_lead`, `sales_rep`) on endpoints modifying company settings, executing privileged AI agent workflows, or viewing global financial telemetry.
- **Explicit HTTP status codes**:
  - Return `401 Unauthorized` for missing, expired, or revoked authentication credentials.
  - Return `403 Forbidden` when an authenticated user lacks permissions for a resource.

## 3. Input Validation & OWASP Defenses
- **Strict schema validation**: Validate all request parameters, query strings, and payloads using strict Pydantic schemas with typed fields and length constraints.
- **SQL Injection prevention**: Strictly use SQLAlchemy ORM or parameterized queries. **NEVER** use string formatting (f-strings, `.format()`, `%`) to construct SQL queries.
- **XSS prevention**: Avoid `dangerouslySetInnerHTML` in frontend React components without explicit sanitization (e.g. DOMPurify). Ensure React automatic string escaping is preserved.
- **CORS configuration**: In production, restrict `allow_origins` to trusted domain origins; never combine wildcard `allow_origins=["*"]` with `allow_credentials=True`.

## 4. AI Agent Safety & Data Privacy
- **PII sanitization**: Redact sensitive customer PII (passwords, auth tokens, credit card numbers, SSNs) before sending prompts to external AI models or persisting AI task execution inputs.
- **Log hygiene**: Never log credentials, raw tokens, or sensitive customer records. Always include `exc_info=True` in exception logs without echoing sensitive user input.
- **Model output verification**: Parse and validate non-deterministic LLM agent responses through structured schemas before executing deterministic database writes or automated actions.

## 5. Dependency & Supply Chain Integrity
- Pin dependency versions in `requirements.txt` and `package.json`.
- Do not use deprecated packages or unmaintained third-party utilities.
