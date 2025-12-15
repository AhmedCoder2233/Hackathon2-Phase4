# Tasks for Todo MCP Tools Implementation

## Feature Branch: `007-todo-mcp-tools`

## Implementation Strategy:

This implementation will follow an MVP-first approach, prioritizing core task management functionalities. Each user story will be developed in a separate phase, allowing for independent testing and incremental delivery.

## Dependencies

-   User Story 1: Add a new task (P1)
-   User Story 2: List my tasks (P1)
-   User Story 3: Mark a task as completed (P1)
-   User Story 4: Delete a task (P2)
-   User Story 5: Update a task (P2)

## Parallel Execution Opportunities:

Within each User Story phase, tasks are generally sequential. However, some tasks might be parallelizable if they operate on different files or have no direct dependencies on other incomplete tasks within that phase. The `[P]` tag indicates potential for parallel execution.

---

## Phase 1: Setup

### Goal: Prepare the development environment for the feature.

- [X] T001 Create `backend/app/mcp_tools.py` file.

---

## Phase 2: Foundational - Implement Task Model

### Goal: Establish the core data model for tasks.

-   [X] T002 Add `Task` model to `backend/app/database.py` based on `data-model.md`.
-   [X] T003 Ensure `Task` model is correctly imported where needed in `backend/app/database.py`.

---

## Phase 3: User Story 1 - Add a new task (Priority: P1)

### Goal: Allow users to create new tasks.
### Independent Test Criteria:
A user can successfully add a task, and it appears in their task list.

### Implementation Tasks:
-   [X] T004 [US1] Implement `add_task` function in `backend/app/mcp_tools.py` as defined in `contracts/auth-api.yaml`.
-   [X] T005 [US1] Ensure `add_task` correctly saves new tasks to the database.

---

## Phase 4: User Story 2 - List my tasks (Priority: P1)

### Goal: Allow users to view their tasks.
### Independent Test Criteria:
A user can retrieve a list of their tasks, and the list accurately reflects the tasks they have added and their statuses.

### Implementation Tasks:
-   [X] T006 [US2] Implement `list_tasks` function in `backend/app/mcp_tools.py` as defined in `contracts/auth-api.yaml`.
-   [X] T007 [US2] Ensure `list_tasks` correctly filters by status ("all", "pending", "completed").

---

## Phase 5: User Story 3 - Mark a task as completed (Priority: P1)

### Goal: Allow users to mark tasks as completed.
### Independent Test Criteria:
A user can mark a specific task as completed, and its status is updated accordingly.

### Implementation Tasks:
-   [X] T008 [US3] Implement `complete_task` function in `backend/app/mcp_tools.py` as defined in `contracts/auth-api.yaml`.
-   [X] T009 [US3] Ensure `complete_task` correctly updates the `completed` status and `updated_at` timestamp in the database.

---

## Phase 6: User Story 4 - Delete a task (Priority: P2)

### Goal: Allow users to remove tasks.
### Independent Test Criteria:
A user can delete a task, and it no longer appears in their task list.

### Implementation Tasks:
-   [X] T010 [US4] Implement `delete_task` function in `backend/app/mcp_tools.py` as defined in `contracts/auth-api.yaml`.
-   [X] T011 [US4] Ensure `delete_task` correctly removes the task from the database.

---

## Phase 7: User Story 5 - Update a task (Priority: P2)

### Goal: Allow users to modify task details.
### Independent Test Criteria:
A user can modify the details of an existing task, and the changes are reflected.

### Implementation Tasks:
-   [X] T012 [US5] Implement `update_task` function in `backend/app/mcp_tools.py` as defined in `contracts/auth-api.yaml`.
-   [X] T013 [US5] Ensure `update_task` correctly modifies the title, description, and `updated_at` timestamp in the database.

---

## Final Phase: Polish & Cross-Cutting Concerns

### Goal: Integrate MCP tools and ensure overall system quality.

-   [X] T014 Register FastMCP instance and tools in `backend/app/mcp_tools.py`.
-   [X] T015 Integrate `backend/app/mcp_tools.py` into the FastAPI application (e.g., in `backend/app/main.py`).
-   [X] T016 Implement comprehensive error handling for all MCP tools, including `ValueError` for task not found scenarios.
-   [X] T017 Verify all operations (`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`) correctly associate tasks with the `user_id`.
