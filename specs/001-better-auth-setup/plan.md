# Implementation Plan: Better Auth Setup

**Branch**: `001-better-auth-setup` | **Date**: 2025-12-13 | **Spec**: [specs/001-better-auth-setup/spec.md](specs/001-better-auth-setup/spec.md)

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The primary requirement is to implement a robust email/password authentication system for a Next.js application, featuring auto-generated unique user IDs, secure password hashing, comprehensive session management, and protected routes. The technical approach involves leveraging the `better-auth` library for Next.js, backed by a PostgreSQL database for user and session persistence.

## Technical Context

**Language/Version**: TypeScript/JavaScript (Next.js), SQL (PostgreSQL)
**Primary Dependencies**: Next.js, better-auth, pg
**Storage**: PostgreSQL
**Testing**: Jest (Unit/Integration), Playwright (E2E)
**Target Platform**: Web (Next.js application)
**Project Type**: Web application (full-stack with Next.js API routes)
**Performance Goals**: P95 login/signup < 500ms, P95 session validation < 100ms
**Constraints**: Secure password hashing (bcrypt), unique user ID generation (nanoid), session management, protected routes, minimum password length (8 characters).
**Scale/Scope**: Initial setup for a single user, scalable to multiple users within the application's overall context.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Review

*   **Stateless Architecture**: **OK**. The plan for `better-auth` using database-backed sessions aligns with stateless server design.
*   **MCP Tool-Based Design**: **N/A**. This principle applies to the AI agent's interaction, not directly to this authentication feature's implementation details.
*   **Single Endpoint Pattern**: **VIOLATION**. The authentication feature introduces `/api/auth/[...all]` endpoints, deviating from the `POST /api/{user_id}/chat` rule.
    *   **Justification**: Authentication is a fundamental cross-cutting concern requiring dedicated endpoints, which are standard for modern web frameworks and not directly part of the chat endpoint's core function. These endpoints are distinct and serve a different purpose, handling user sessions and credentials.
*   **Conversation Persistence**: **N/A**. This principle applies to chat conversations, not directly to user authentication. User session persistence will be handled by `better-auth` and the database.
*   **Core Technology Stack**:
    *   Frontend: Next.js (TypeScript/JavaScript) is proposed for frontend. Constitution mentions `OpenAI ChatKit`. **VIOLATION**.
        *   **Justification**: Next.js provides a complete framework for building full-stack web applications, including server-side rendering, routing, and API routes, which is necessary for a user authentication flow (e.g., login/signup forms, protected routes). OpenAI ChatKit is primarily a UI library for chat interfaces and does not offer the necessary framework capabilities for a full authentication system. The authentication system needs a more general-purpose frontend framework.
    *   Backend: Next.js API routes (TypeScript/JavaScript) are used for authentication backend logic. Constitution mentions `Python FastAPI`. **VIOLATION**.
        *   **Justification**: Using Next.js API routes keeps the authentication logic within a single, coherent Next.js application, reducing complexity, improving developer experience, and enabling seamless integration between frontend and backend authentication concerns (e.g., setting HTTP-only cookies). Introducing a separate FastAPI backend solely for authentication would add unnecessary architectural overhead given Next.js's capabilities.
    *   ORM: `better-auth` abstracts the ORM, potentially not using `SQLModel`. Constitution specifies `SQLModel`. **VIOLATION**.
        *   **Justification**: `better-auth` is chosen for its comprehensive authentication features and ease of integration with Next.js and PostgreSQL. Its internal ORM or database interaction strategy is part of its design, and overriding it to specifically use `SQLModel` might lead to significant customization effort or break `better-auth`'s functionality. The benefit of using `better-auth` outweighs the strict adherence to `SQLModel` for this specific module, especially since it interacts with PostgreSQL, which is a constitutional database.
    *   Database: Neon Serverless PostgreSQL is in constitution. Plan uses PostgreSQL, which is compatible. **OK**.
    *   Authentication: Better Auth is in constitution. Plan uses `Better Auth`. **OK**.

### Data Models
*   **ADDITION**: The feature introduces `session` and `account` data models (tables) in addition to the existing `Task`, `Conversation`, and `Message` models. This is expected and necessary for authentication. The `user` model is consistent.

### API Contract (Fixed Interface)
*   **VIOLATION**: Introduction of `/api/auth/[...all]` endpoints for authentication, which is a deviation from the single `/api/{user_id}/chat` endpoint defined in the constitution. This is directly related to the "Single Endpoint Pattern" violation above.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
