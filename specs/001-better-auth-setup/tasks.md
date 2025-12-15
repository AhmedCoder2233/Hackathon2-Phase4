# Tasks: Better Auth Setup

**Input**: Design documents from `/specs/001-better-auth-setup/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: This plan does NOT include test tasks, as they were not explicitly requested in the feature specification. However, the research document (`research.md`) outlines testing strategies (Jest for Unit/Integration, Playwright for E2E) that can be incorporated into future tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/` assumed to be the root of the Next.js project.
- Paths shown below assume `app/` is within the Next.js project root.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic configuration.

- [ ] T001 Install `better-auth` and `pg` dependencies in `frontend/package.json`.
- [ ] T002 Configure `.env.local` with `DATABASE_URL`, `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`, and `NEXT_PUBLIC_APP_URL` in `frontend/.env.local`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core authentication infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 Create `app/api/auth/[...all]/route.ts` for Better Auth API routes in `frontend/app/api/auth/[...all]/route.ts`.
- [ ] T004 Create `app/lib/auth.ts` for Better Auth server-side configuration in `frontend/app/lib/auth.ts`.
- [ ] T005 Create `app/lib/auth-client.ts` for Better Auth client-side utilities in `frontend/app/lib/auth-client.ts`.
- [ ] T006 Verify database connection and initial table creation (user, session, account) by running the app.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - User Sign Up (Priority: P1) 🎯 MVP

**Goal**: A new user can successfully create an account using email and password.

**Independent Test**: A user can navigate to the login/signup page, fill out the sign-up form with valid credentials, and be redirected to the dashboard upon successful account creation.

### Implementation for User Story 1

- [ ] T007 [P] [US1] Create the login/signup UI component (initial structure with email, password, name fields, and toggle) in `frontend/app/page.tsx`.
- [ ] T008 [US1] Implement sign-up logic within `frontend/app/page.tsx` using `authClient.signUp.email`.
- [ ] T009 [US1] Add form validation for email, password, and name fields in `frontend/app/page.tsx`.
- [ ] T010 [US1] Handle sign-up success, including redirection to `/dashboard` in `frontend/app/page.tsx`.
- [ ] T011 [US1] Display error messages for sign-up failures (e.g., email already exists, weak password) in `frontend/app/page.tsx`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - User Login (Priority: P1)

**Goal**: An existing user can successfully log into their account using email and password.

**Independent Test**: A user can navigate to the login/signup page, fill out the login form with registered credentials, and be redirected to the dashboard upon successful login.

### Implementation for User Story 2

- [ ] T012 [P] [US2] Implement login UI within the existing `frontend/app/page.tsx` (re-use fields, ensure toggle works).
- [ ] T013 [US2] Implement login logic within `frontend/app/page.tsx` using `authClient.signIn.email`.
- [ ] T014 [US2] Handle login success, including redirection to `/dashboard` in `frontend/app/page.tsx`.
- [ ] T015 [US2] Display error messages for login failures (e.g., invalid credentials) in `frontend/app/page.tsx`.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Access Protected Dashboard (Priority: P1)

**Goal**: An authenticated user can view their personalized dashboard, and unauthenticated users are redirected from protected routes.

**Independent Test**:
1.  Verify a logged-in user can access `/dashboard` and see their user information.
2.  Verify a logged-out user attempting to access `/dashboard` is redirected to `/`.

### Implementation for User Story 3

- [ ] T016 [P] [US3] Create the dashboard page component in `frontend/app/dashboard/page.tsx`.
- [ ] T017 [US3] Implement session checking and protection logic in `frontend/app/dashboard/page.tsx` using `authClient.useSession`.
- [ ] T018 [US3] Redirect unauthenticated users from `/dashboard` to `/` in `frontend/app/dashboard/page.tsx`.
- [ ] T019 [US3] Display authenticated user's ID, email, and name on the dashboard in `frontend/app/dashboard/page.tsx`.

**Checkpoint**: All user stories implemented so far should be independently functional.

---

## Phase 6: User Story 4 - User Logout (Priority: P1)

**Goal**: An authenticated user can log out of their session.

**Independent Test**: A logged-in user can click a "Logout" button on the dashboard, which terminates their session and redirects them to the login page.

### Implementation for User Story 4

- [ ] T020 [P] [US4] Add a "Logout" button to the dashboard UI in `frontend/app/dashboard/page.tsx`.
- [ ] T021 [US4] Implement logout logic in `frontend/app/dashboard/page.tsx` using `authClient.signOut`.
- [ ] T022 [US4] Handle successful logout, including redirection to `/` in `frontend/app/dashboard/page.tsx`.

**Checkpoint**: All user stories should now be independently functional.

---
---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately.
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
-   **User Stories (Phase 3-6)**: All depend on Foundational phase completion.
    *   User stories can proceed in parallel (if staffed) or sequentially in priority order (all P1).

### User Story Dependencies

-   **User Story 1 (P1 - Sign Up)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
-   **User Story 2 (P1 - Login)**: Can start after Foundational (Phase 2) - No dependencies on other stories.
-   **User Story 3 (P1 - Access Dashboard)**: Can start after Foundational (Phase 2) - Requires a logged-in user (implicitly depends on US1 or US2).
-   **User Story 4 (P1 - Logout)**: Can start after Foundational (Phase 2) - Requires an active session (implicitly depends on US1 or US2).

### Within Each User Story

-   UI component creation can often be parallelized with logic implementation if separate files.
-   Core logic implementation (e.g., signup) should precede handling redirections and error messages within the same component.
-   Dashboard UI creation can be parallelized with protection logic.

### Parallel Opportunities

-   All Setup tasks marked [P] can run in parallel.
-   Within User Story phases, tasks marked [P] can run in parallel.
-   Once the Foundational phase completes, User Stories 1, 2, 3, and 4 can be worked on in parallel by different team members.

---

## Parallel Example: User Story 1 (Sign Up)

```bash
# Launch UI and initial logic together:
Task: "T007 [P] [US1] Create the login/signup UI component in frontend/app/page.tsx"
Task: "T008 [US1] Implement sign-up logic within frontend/app/page.tsx using authClient.signUp.email"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1 (Sign Up)
4.  **STOP and VALIDATE**: Test User Story 1 independently.
5.  Deploy/demo if ready.

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready.
2.  Add User Story 1 (Sign Up) → Test independently → Deploy/Demo (MVP!).
3.  Add User Story 2 (Login) → Test independently → Deploy/Demo.
4.  Add User Story 3 (Access Dashboard) → Test independently → Deploy/Demo.
5.  Add User Story 4 (Logout) → Test independently → Deploy/Demo.
6.  Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together.
2.  Once Foundational is done:
    *   Developer A: User Story 1 (Sign Up)
    *   Developer B: User Story 2 (Login)
    *   Developer C: User Story 3 (Access Dashboard)
    *   Developer D: User Story 4 (Logout)
3.  Stories complete and integrate independently.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
