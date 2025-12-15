# Implementation Plan: JWT Authentication & User ID Retrieval

**Branch**: `006-jwt-auth` | **Date**: December 14, 2025 | **Spec**: `specs/006-jwt-auth/spec.md`
**Input**: Feature specification from `/specs/006-jwt-auth/spec.md`

## Summary

This feature implements JWT token validation and a user identification system for the `/support/chatkit` endpoint in the FastAPI backend. The technical approach involves validating Better Auth JWT tokens, extracting user information (specifically email), querying the database for the corresponding user and associated sessions, and finally retrieving the `user_id` from an active session. This ensures that only authenticated and identified users can interact with the ChatKit service.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: FastAPI, python-jose[cryptography], sqlalchemy, psycopg2-binary  
**Storage**: Neon Serverless PostgreSQL  
**Testing**: pytest  
**Target Platform**: Linux server  
**Project Type**: Web application (Backend component)  
**Performance Goals**: User retrieval from the database based on email completes within 100 milliseconds for 99% of requests.  
**Constraints**:
*   JWT validation must happen before any ChatKit processing.
*   User context (including `user_id`) must be available for downstream processing within the `/support/chatkit` endpoint.
*   Existing ChatKit functionality must remain intact and unaffected by the new authentication layer.
*   All implementation must adhere to the "no manual coding allowed" principle, utilizing Claude Code or similar agent-driven development.
**Scale/Scope**: This initial implementation focuses solely on securing and identifying users for the `/support/chatkit` endpoint.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   **Stateless Architecture**: PASS - The feature implements JWT validation and user lookup per-request, fetching user data from the database, aligning with stateless server design.
*   **MCP Tool-Based Design**: PASS - This foundational security feature integrates with the backend API, which will be exposed via MCP tools. The JWT validation is a necessary preceding step for MCP tool invocation.
*   **Single Endpoint Pattern**: PASS - The feature specifically targets and enhances a single endpoint, `/support/chatkit`, maintaining the single endpoint pattern.
*   **Conversation Persistence**: PASS - Although not directly related to JWT auth, the user lookup from the database via sessions aligns with the principle of conversation persistence by relying on a persistent store for user data.
*   **Core Technology Stack**: PASS -
    *   **Backend**: Utilizes Python FastAPI, Neon Serverless PostgreSQL, and integrates with Better Auth, all aligned with the defined stack.
*   **No manual coding allowed**: PASS - This plan adheres to the constraint that all implementation will be agent-driven.
*   **Repository Structure**: PASS - The plan involves creating/modifying files within `backend/app/` and `specs/`, consistent with the "Web application" structure.
*   **Functional Requirements**: PASS - The feature directly addresses functional requirements by adding robust authentication and user identification.
*   **Documentation Requirements**: PASS - The planning process will generate `research.md`, `data-model.md`, `quickstart.md`, and API `contracts/`, fulfilling documentation needs.

All Constitution gates pass. No violations detected.

## Project Structure

### Documentation (this feature)

```text
specs/006-jwt-auth/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── app/
│   │   ├── main.py       # Update /support/chatkit endpoint
│   │   ├── database.py   # New file for database models
│   │   └── auth.py       # New file for JWT validation utility
│   └── tests/
│
├── tests/
└── ... (existing files)
```

**Structure Decision**: The project uses a web application structure with separate `backend/` and `frontend/` directories. This feature adds new files and modifies an existing endpoint within the `backend/app/` directory, adhering to the established structure.

## Complexity Tracking

> **N/A - No Constitution Check violations that require justification.**