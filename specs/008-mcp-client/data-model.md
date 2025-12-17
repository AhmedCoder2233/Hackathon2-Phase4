# Data Model: Integrate MCP Server with OpenAI Agent

## Entity: User

### Description
Represents the authenticated user interacting with the system.

### Attributes
- `user_id`: String (Unique identifier from Better Auth)

### Relationships
- Each `Task` is associated with a `User`.

## Entity: Task

### Description
Represents a single to-do item that users can create, manage, and track. This model is defined and implemented in the `007-todo-mcp-tools` feature.

### Attributes
- `id`: Integer (Primary Key, Auto-incrementing)
- `user_id`: String (Indexed, Foreign Key to User entity, required)
- `title`: String (Required, descriptive name for the task)
- `description`: String (Optional, detailed explanation of the task)
- `completed`: Boolean (Default: `False`, indicates if the task is finished)
- `created_at`: Datetime (Auto-generated timestamp, records when the task was created)
- `updated_at`: Datetime (Auto-updated timestamp, records the last modification time)

### Validation Rules
- Operations on a `Task` must be performed by the `user_id` associated with the task.

### State Transitions
- A task is initially created with `completed` set to `False`.
- A task can transition from `completed: False` to `completed: True` via the `complete_task` operation.
- A task can be deleted at any state.
- A task's `title` or `description` can be updated at any state.
