---
description: Prefer incremental development of features with unit testing and sequential commits.
globs: ["**/*"]
alwaysApply: true
---

# Incremental Development & Testing Rule

- Develop features incrementally in isolated, logical phases rather than large monolithic changes.
- For every new feature, API endpoint, or refactor, implement or update unit tests to verify the individual functionality before proceeding to subsequent steps.
- Always run the relevant test suites (e.g. `pytest backend/tests` for backend, `npm run build` for frontend) to confirm zero regressions and verify clean execution.
- Commit and push changes sequentially for each individual feature or verified milestone with clear, descriptive commit messages.
- Early bug detection: test individual parts in isolation before connecting them into end-to-end workflows.
