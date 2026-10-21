---
description: Next.js, React, and TypeScript development standards.
globs: ["frontend/src/**.ts", "frontend/src/**.tsx"]
alwaysApply: true
---

# Next.js & Frontend Standards

- Mark client-interactive components explicitly with `'use client'`.
- Avoid hydration mismatches: do not initialize client date objects (e.g. `Date.now()`, `new Date()`) directly in root client component state without hydration guards or `useEffect`.
- Use TypeScript strictly for all component props, API responses, and state models.
- Reuse established design system tokens and glassmorphism styles (`glass-card`, `glass-panel`, `glass-panel-interactive`).
- For icons, always use `lucide-react` icons (verify icon availability, e.g. `Kanban` rather than `Trello`).
- Verify production compilation with `npm run build` in `frontend/` before pushing commits.
