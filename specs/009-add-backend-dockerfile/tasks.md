# Tasks: Add Dockerfile for Backend

**Input**: Design documents from `/specs/009-add-backend-dockerfile/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: No tests were requested for this feature.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup
- [x] T001 Verify Docker is installed and the Docker daemon is running.

---

## Phase 2: Foundational Tasks
(No foundational tasks are required for this feature.)

---

## Phase 3: User Story 1 - Build Backend Docker Image (Priority: P1) 🎯 MVP

**Goal**: Create a `Dockerfile` to build a container image for the backend application, enabling standardized development and deployment.

**Independent Test**: The `Dockerfile` can be used to successfully build a Docker image, and a container started from that image runs the application without errors. This can be verified using the commands in `quickstart.md`.

### Implementation for User Story 1

- [x] T002 [US1] Create the initial `backend/Dockerfile` with the `python:3.13-slim-bookworm` base image and define the builder and final stages for a multi-stage build.
- [x] T003 [US1] In the builder stage of `backend/Dockerfile`, install `uv` and copy the `pyproject.toml` and `uv.lock` files.
- [x] T004 [US1] In the builder stage of `backend/Dockerfile`, install all Python dependencies using `uv sync`.
- [x] T005 [US1] In the final stage of `backend/Dockerfile`, copy the installed Python environment from the builder stage.
- [x] T006 [US1] In the final stage of `backend/Dockerfile`, copy the backend application code into the image.
- [x] T007 [US1] In the final stage of `backend/Dockerfile`, expose port 8000 for the application.
- [x] T008 [US1] In the final stage of `backend/Dockerfile`, set the default command to `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently by building and running the Docker image.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final verification of the feature.

- [ ] T009 Manually build the Docker image using the command from `quickstart.md` to ensure it builds successfully within the 5-minute performance goal.
- [ ] T010 Manually run the Docker container using the command from `quickstart.md` and verify the application is accessible at http://localhost:8000.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **User Story 1 (Phase 3)**: Depends on Setup completion.
- **Polish (Phase 4)**: Depends on User Story 1 completion.

### Within User Story 1

- The tasks T002-T008 should be executed sequentially as they each modify the same `backend/Dockerfile`.

### Parallel Opportunities

- No parallel opportunities exist within this feature, as it primarily involves the sequential construction of a single file.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 3: User Story 1
3. Complete Phase 4: Polish
4. **STOP and VALIDATE**: The `Dockerfile` should successfully build an image that runs the application. This completes the feature.
