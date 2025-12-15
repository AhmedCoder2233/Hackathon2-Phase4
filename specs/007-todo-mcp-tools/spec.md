# Feature Specification: Todo MCP Tools Implementation

**Feature Branch**: `007-todo-mcp-tools`  
**Created**: 2025-12-15  
**Status**: Draft  
**Input**: User description: "Todo MCP Tools Implementation ## Task Create `backend/app/mcp_tools.py` file with FastMCP todo management tools that connect to database. ## Requirements ### 1. Add Task Model to `database.py` ```python class Task(SQLModel, table=True): __tablename__ = "task" id: Optional[int] = Field(default=None, primary_key=True) user_id: str = Field(index=True) title: str description: Optional[str] = None completed: bool = Field(default=False) created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) ``` ### 2. Create `backend/app/mcp_tools.py` **Import FastMCP and database:** ```python from fastmcp import FastMCP from sqlmodel import Session, select from app.database import Task, get_session, engine ``` **Create FastMCP instance:** ```python mcp = FastMCP("Todo Tools") ``` **Implement 5 tools:** #### Tool 1: add_task ```python @mcp.tool() def add_task(user_id: str, title: str, description: str = "") -> dict: """Create a new task""" with Session(engine) as session: task = Task(user_id=user_id, title=title, description=description) session.add(task) session.commit() session.refresh(task) return {"task_id": task.id, "status": "created", "title": task.title} ``` #### Tool 2: list_tasks ```python @mcp.tool() def list_tasks(user_id: str, status: str = "all") -> dict: """List user's tasks. Status: all, pending, or completed""" with Session(engine) as session: query = select(Task).where(Task.user_id == user_id) if status == "pending": query = query.where(Task.completed == False) elif status == "completed": query = query.where(Task.completed == True) tasks = session.exec(query).all() return { "tasks": [ { "id": t.id, "title": t.title, "description": t.description, "completed": t.completed, "created_at": t.created_at.isoformat() } for t in tasks ] } ``` #### Tool 3: complete_task ```python @mcp.tool() def complete_task(user_id: str, task_id: int) -> dict: """Mark task as completed""" with Session(engine) as session: task = session.exec( select(Task).where(Task.id == task_id, Task.user_id == user_id) ).first() if not task: raise ValueError(f"Task {task_id} not found") task.completed = True task.updated_at = datetime.now(timezone.utc) session.add(task) session.commit() return {"task_id": task.id, "status": "completed", "title": task.title} ``` #### Tool 4: delete_task ```python @mcp.tool() def delete_task(user_id: str, task_id: int) -> dict: """Delete a task""" with Session(engine) as session: task = session.exec( select(Task).where(Task.id == task_id, Task.user_id == user_id) ).first() if not task: raise ValueError(f"Task {task_id} not found") title = task.title session.delete(task) session.commit() return {"task_id": task_id, "status": "deleted", "title": title} ``` #### Tool 5: update_task ```python @mcp.tool() def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> dict: """Update task title or description""" with Session(engine) as session: task = session.exec( select(Task).where(Task.id == task_id, Task.user_id == user_id) ).first() if not task: raise ValueError(f"Task {task_id} not found") if title: task.title = title if description is not None: task.description = description task.updated_at = datetime.now(timezone.utc) session.add(task) session.commit() return {"task_id": task.id, "status": "updated", "title": task.title} ``` ## That's It! - Add Task model to `database.py` - Create `mcp_tools.py` with 5 tools - All tools connect to database using existing `engine` and `Session`"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add a new task (Priority: P1)
- **Description**: As a user, I want to be able to create new tasks so that I can keep track of my to-do items.
- **Why this priority**: Core functionality for a todo application.
- **Independent Test**: A user can successfully add a task, and it appears in their task list.
- **Acceptance Scenarios**:
    1. **Given** I am a registered user, **When** I provide a title and optional description for a new task, **Then** a new task is created with a unique ID, status "created", and the provided title.

### User Story 2 - List my tasks (Priority: P1)
- **Description**: As a user, I want to see a list of my tasks, optionally filtered by status (pending or completed), so I can view my progress.
- **Why this priority**: Essential for managing tasks.
- **Independent Test**: A user can retrieve a list of their tasks, and the list accurately reflects the tasks they have added and their statuses.
- **Acceptance Scenarios**:
    1. **Given** I have existing tasks, **When** I request to list my tasks with no status filter, **Then** I receive a list of all my tasks including their ID, title, description, completed status, and creation timestamp.
    2. **Given** I have existing tasks, **When** I request to list my tasks filtered by "pending", **Then** I receive a list of only my incomplete tasks.
    3. **Given** I have existing tasks, **When** I request to list my tasks filtered by "completed", **Then** I receive a list of only my completed tasks.

### User Story 3 - Mark a task as completed (Priority: P1)
- **Description**: As a user, I want to mark a task as completed so that I can track my accomplishments.
- **Why this priority**: Fundamental task management action.
- **Independent Test**: A user can mark a specific task as completed, and its status is updated accordingly.
- **Acceptance Scenarios**:
    1. **Given** I have an incomplete task, **When** I provide the ID of that task, **Then** the task's status is updated to "completed", its `updated_at` timestamp is set, and the system confirms the update.
    2. **Given** I provide an invalid task ID, **When** I attempt to mark it as completed, **Then** the system returns an error indicating the task was not found.

### User Story 4 - Delete a task (Priority: P2)
- **Description**: As a user, I want to delete a task that is no longer relevant.
- **Why this priority**: Allows for cleaning up task lists.
- **Independent Test**: A user can delete a task, and it no longer appears in their task list.
- **Acceptance Scenarios**:
    1. **Given** I have an existing task, **When** I provide the ID of that task, **Then** the task is permanently removed from the system, and the system confirms the deletion.
    2. **Given** I provide an invalid task ID, **When** I attempt to delete it, **Then** the system returns an error indicating the task was not found.

### User Story 5 - Update a task (Priority: P2)
- **Description**: As a user, I want to update the title or description of an existing task.
- **Why this priority**: Allows for correcting or refining task details.
- **Independent Test**: A user can modify the details of an existing task, and the changes are reflected.
- **Acceptance Scenarios**:
    1. **Given** I have an existing task, **When** I provide the task ID and a new title, **Then** the task's title is updated, its `updated_at` timestamp is set, and the system confirms the update.
    2. **Given** I have an existing task, **When** I provide the task ID and a new description, **Then** the task's description is updated, its `updated_at` timestamp is set, and the system confirms the update.
    3. **Given** I have an existing task, **When** I provide the task ID and both a new title and description, **Then** both are updated, its `updated_at` timestamp is set, and the system confirms the update.
    4. **Given** I provide an invalid task ID, **When** I attempt to update it, **Then** the system returns an error indicating the task was not found.

### Edge Cases
- What happens when a user tries to complete/delete/update a task that belongs to another user? (Expected: Error - Task not found or Unauthorized)
- How does the system handle an empty title for a new task? (Expected: Validation error)

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The system MUST allow users to create a new task with a title and optional description.
- **FR-002**: The system MUST allow users to retrieve a list of their tasks, with optional filtering by status (all, pending, completed).
- **FR-003**: The system MUST allow users to mark an existing task as completed.
- **FR-004**: The system MUST allow users to delete an existing task.
- **FR-005**: The system MUST allow users to update the title and/or description of an existing task.
- **FR-006**: The system MUST associate tasks with a specific user (`user_id`).
- **FR-007**: The system MUST provide an error when attempting to perform an action on a non-existent task or a task that does not belong to the user.
- **FR-008**: The system MUST record the creation and last update timestamps for each task.

### Key Entities *(include if feature involves data)*
- **Task**: Represents a single to-do item.
    - Attributes: `id` (unique identifier), `user_id` (owner), `title` (task description), `description` (optional detailed description), `completed` (boolean status), `created_at` (timestamp), `updated_at` (timestamp).

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: Users can successfully create, list, complete, delete, and update tasks with 100% success rate under normal operating conditions.
- **SC-002**: A user's task list (up to 100 tasks) loads in under 1 second.
- **SC-003**: Task creation, completion, deletion, and update operations complete in under 500ms.
- **SC-004**: The system correctly associates tasks with the creating user, preventing unauthorized access.