# Data Model: Todo MCP Tools Implementation

## Entity: Task

### Description
Represents a single to-do item that users can create, manage, and track.

### Attributes
- `id`: Integer (Primary Key, Auto-incrementing)
- `user_id`: String (Indexed, Foreign Key to User entity, required)
- `title`: String (Required, descriptive name for the task)
- `description`: String (Optional, detailed explanation of the task)
- `completed`: Boolean (Default: `False`, indicates if the task is finished)
- `created_at`: Datetime (Auto-generated timestamp, records when the task was created)
- `updated_at`: Datetime (Auto-updated timestamp, records the last modification time)

### Relationships
- **User**: Each `Task` belongs to a `User` (identified by `user_id`).

### Validation Rules
- `user_id` must be provided.
- `title` must be provided and cannot be empty.
- `task_id` must exist for `complete_task`, `delete_task`, and `update_task` operations.
- Operations on a `Task` must be performed by the `user_id` associated with the task.

### State Transitions
- A task is initially created with `completed` set to `False`.
- A task can transition from `completed: False` to `completed: True` via the `complete_task` operation.
- A task can be deleted at any state.
- A task's `title` or `description` can be updated at any state.
