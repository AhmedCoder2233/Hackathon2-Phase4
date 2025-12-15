# Tasks: ChatKit UI Integration

**Feature Branch**: `003-chatkit-ui` | **Date**: 2025-12-13 | **Spec**: `specs/003-chatkit-ui/spec.md`
**Plan**: `specs/003-chatkit-ui/plan.md`

## Summary

This document outlines the actionable tasks for implementing the ChatKit UI integration feature, organized by user story and priority. The implementation will focus on frontend-only changes, integrating the ChatKit component, and enhancing the authentication flow to support user identification and redirection.

## Implementation Strategy

The feature will be delivered incrementally, prioritizing core user journeys first (MVP approach). User Story 1 (User Signup and Chat Access) forms the MVP, ensuring basic functionality and integration are in place. User Story 2 (Modern UI Experience) will follow to refine the aesthetic and responsiveness.

## Dependencies

The user stories are largely independent, but User Story 1 forms the foundational functionality upon which User Story 2 builds for visual refinement.

-   **User Story 1** (P1) -> **User Story 2** (P2) (for UI refinement of the chat page)

## Parallel Execution Opportunities

-   **User Story 1** tasks can be done sequentially.
-   **User Story 2** tasks, particularly related to styling, can be initiated once the core components are in place from User Story 1. Specific styling tasks for auth pages can potentially run in parallel with early ChatKit integration if separate developers are assigned.

## Phase 1: Setup

**Goal**: Prepare the frontend project for ChatKit integration.

- [x] T001 Install `@openai/chatkit-react` package in `frontend/package.json`

## Phase 2: Foundational (Authentication Updates)

**Goal**: Implement `user_id` generation and auto-redirection in the authentication flow.
**Independent Test Criteria**: New users can sign up with a generated `user_id`, and both signup/login redirect to `/chat`.

- [x] T002 Implement unique `user_id` generation (e.g., using `nanoid` or `UUID`) in `frontend/app/lib/auth.ts` or a new utility file.
- [x] T003 Update signup logic to save the generated `user_id` along with email and password in `frontend/app/api/auth/[...all]/route.ts` (if applicable) and client-side auth handlers (`frontend/app/lib/auth-client.ts`).
- [x] T004 Implement automatic redirection to `/chat` route upon successful signup in `frontend/app/auth/sign-in/page.tsx` or `frontend/app/auth/layout.tsx`.
- [x] T005 Implement automatic redirection to `/chat` route upon successful login in `frontend/app/auth/sign-in/page.tsx` or `frontend/app/auth/layout.tsx`.

## Phase 3: User Story 1 - User Signup and Chat Access (P1)

**Goal**: Enable new users to sign up, log in, and access a functional ChatKit interface.
**Independent Test Criteria**: A user can register, log in, and see a functional, basic ChatKit component on the `/chat` page.

- [x] T006 [US1] Create the chat page component at `frontend/app/chat/page.tsx`.
- [x] T007 [US1] Create the ChatkitWrapper component at `frontend/components/chatkit-ui/ChatkitWrapper.tsx`.
- [x] T008 [US1] Integrate `ChatkitWrapper.tsx` into `frontend/app/chat/page.tsx`.
- [x] T009 [US1] Configure the `useChatKit` hook within `frontend/components/chatkit-ui/ChatkitWrapper.tsx` with `api { url, domainKey }`, theme, start screen, and composer placeholder.
- [x] T010 [US1] Render the `<ChatKit control={chatkit.control} />` component within `frontend/components/chatkit-ui/ChatkitWrapper.tsx`.

## Phase 4: User Story 2 - Modern UI Experience (P2)

**Goal**: Ensure authentication pages and the chat interface have a modern, clean, and responsive design, with the ChatKit component utilizing full viewport dimensions.
**Independent Test Criteria**: Visual inspection confirms modern design, responsiveness, and correct sizing of the ChatKit component across various devices.

- [x] T011 [P] [US2] Review and refine styling for authentication pages (`frontend/app/auth/sign-in/page.tsx`, `frontend/app/auth/layout.tsx`) to ensure a modern aesthetic.
- [x] T012 [P] [US2] Apply CSS to ensure the ChatKit component (rendered via `frontend/components/chatkit-ui/ChatkitWrapper.tsx` and displayed in `frontend/app/chat/page.tsx`) takes full viewport height and width.
- [x] T013 [P] [US2] Verify and adjust global styles (`frontend/app/globals.css`) or component-specific styles to ensure overall clean and responsive design across the application.

## Final Phase: Polish & Cross-Cutting Concerns

**Goal**: Address any remaining minor issues, ensure code quality, and prepare for testing.

- [x] T014 Review and clean up any temporary code or console logs.
- [x] T015 Ensure all new and modified files adhere to project coding standards and linting rules.
- [x] T016 Verify environment variable loading for ChatKit configuration.
