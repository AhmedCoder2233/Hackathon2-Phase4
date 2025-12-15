# Tasks: JWT Authentication & User ID Retrieval

**Branch**: `006-jwt-auth` | **Date**: December 14, 2025 | **Spec**: `specs/006-jwt-auth/spec.md`
**Input**: Feature specification from `/specs/006-jwt-auth/spec.md`

## Summary

This document outlines the tasks required to implement JWT token validation and user identification for the `/support/chatkit` endpoint in the FastAPI backend. Tasks are organized into phases corresponding to user stories and foundational setup.

## Task Generation Rules Reference

Tasks are formatted as: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- `[P?]`: Indicates a parallelizable task.
- `[Story?]`: E.g., `[US1]`, `[US2]`, maps to user stories from `spec.md`.

## Phase 1: Setup

This phase involves setting up the environment and installing necessary dependencies.

*   - [x] T001 Install `python-jose[cryptography]` `sqlalchemy` `psycopg2-binary` in `backend/` (via `pip install`)
*   - [x] T002 Configure environment variables for `DATABASE_URL`, `BETTER_AUTH_SECRET`, `BETTER_AUTH_ISSUER` (add to `.env` in `backend/`)

## Phase 2: Foundational

This phase covers tasks that are prerequisites for all user stories, primarily database models and JWT validation utility.

*   - [x] T003 Create SQLAlchemy models for `User` and `Session` entities in `backend/app/database.py`
*   - [x] T004 Define the relationship between `User` and `Session` models in `backend/app/database.py`
*   - [x] T005 Setup database connection and session management in `backend/app/database.py`
*   - [x] T006 Implement JWT decode and validation function in `backend/app/auth.py`
*   - [x] T007 Handle Better Auth JWT token format and extract email from token payload in `backend/app/auth.py`

## Phase 3: User Story 1 - Authenticated ChatKit Request (Priority: P1)

**Story Goal**: As an authenticated user, I want to send a message to the `/support/chatkit` endpoint, and have my JWT token validated and my user ID retrieved, so that the ChatKit service can identify me.
**Independent Test**: Send an authorized request to `/support/chatkit` and verify the user ID is correctly processed internally and appropriate errors (401) are returned for invalid tokens.

*   - [x] T008 [P] [US1] Extract JWT token from `Authorization` header in `backend/app/main.py`
*   - [x] T009 [P] [US1] Integrate JWT validation utility into `/support/chatkit` endpoint in `backend/app/main.py`
*   - [x] T010 [US1] Query database for `User` by email extracted from JWT in `backend/app/main.py`
*   - [x] T011 [US1] Access sessions relationship of the found `User` in `backend/app/main.py`
*   - [x] T012 [US1] Retrieve `user_id` from an active session in `backend/app/main.py`
*   - [x] T013 [US1] Implement 401 Unauthorized response for invalid/expired tokens (FR-007) in `backend/app/main.py`
*   - [x] T014 [US1] Log authentication attempts (FR-012) in `backend/app/main.py`

## Phase 4: User Story 2 - User Not Found (Priority: P2)

**Story Goal**: As a user, if my email extracted from a valid JWT does not correspond to an existing user in the database, I want the system to handle this gracefully, so that it does not proceed with chat processing for an unknown user.
**Independent Test**: Send a valid JWT for an email not present in the database and verify a 404 error with the specific message.

*   - [x] T015 [US2] Implement 404 Not Found response for user not found (FR-008) in `backend/app/main.py`

## Phase 5: User Story 3 - No Active Sessions (Priority: P2)

**Story Goal**: As a user, if my authenticated account has no active sessions, I want the system to indicate this, so that it does not attempt to retrieve a `user_id` from a non-existent session.
**Independent Test**: Send a valid JWT for a user who has no associated sessions in the database and verify a 404 error with the specific message.

*   - [x] T016 [US3] Implement 404 Not Found response for no active sessions (FR-009) in `backend/app/main.py`

## Phase 6: Polish & Cross-Cutting Concerns

This phase includes cross-cutting concerns and ensures the feature is robust.

*   - [x] T017 [P] Ensure existing ChatKit functionality remains unaffected (FR-010) in `backend/app/main.py`
*   - [x] T018 [P] Make user context (including `user_id`) available for downstream processing (FR-011) in `backend/app/main.py`
*   - [x] T019 Implement robust error handling for database connection issues (Edge Case) in `backend/app/main.py`
*   - [x] T020 Review and update `quickstart.md` with final API details and example usage.

## Dependency Graph (User Story Completion Order)

1.  Phase 3: User Story 1 - Authenticated ChatKit Request (P1)
2.  Phase 4: User Story 2 - User Not Found (P2)
3.  Phase 5: User Story 3 - No Active Sessions (P2)

(Note: User Story 2 and 3 can be developed in parallel or in any order after User Story 1's foundational components are in place, as they depend on the core JWT validation and user lookup established in Story 1).

## Parallel Execution Examples (within each User Story)

*   **User Story 1**: Tasks T008 (extract token) and T009 (integrate validation) can be worked on in parallel with setting up the initial endpoint structure.
*   **User Story 2**: Task T015 is largely independent once the basic user lookup from US1 is functional.
*   **User Story 3**: Task T016 is largely independent once the basic user lookup from US1 is functional.
*   **Polish Phase**: Tasks T017 (ChatKit functionality check) and T018 (user context availability) can be worked on in parallel.

## Suggested MVP Scope

The Suggested MVP Scope is **User Story 1 - Authenticated ChatKit Request (Priority: P1)**.
This encompasses the core functionality of JWT validation and user identification, which provides the primary value proposition of the feature.

## Implementation Strategy

The implementation will follow an iterative approach, starting with the MVP (User Story 1) and then sequentially addressing User Stories 2 and 3. Cross-cutting concerns and polish will be handled in the final phase. This ensures incremental delivery and allows for early testing of core authentication features.

