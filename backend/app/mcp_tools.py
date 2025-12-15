from fastmcp import FastMCP
from sqlmodel import Session, select
from app.database import Task, get_session, engine
from datetime import datetime, timezone

mcp = FastMCP("Todo Tools", stateless_http=True)

@mcp.tool()
def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Create a new task"""
    with Session(engine) as session:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"task_id": task.id, "status": "created", "title": task.title}

@mcp.tool()
def list_tasks(user_id: str, status: str = "all") -> dict:
    """List user's tasks. Status: all, pending, or completed"""
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == user_id)
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        tasks = session.exec(query).all()
        return {
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "created_at": t.created_at.isoformat()
                } for t in tasks
            ]
        }

@mcp.tool()
def complete_task(user_id: str, task_id: int) -> dict:
    """Mark task as completed"""
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()
        if not task:
            raise ValueError(f"Task {task_id} not found")
        task.completed = True
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        return {"task_id": task.id, "status": "completed", "title": task.title}

@mcp.tool()
def delete_task(user_id: str, task_id: int) -> dict:
    """Delete a task"""
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()
        if not task:
            raise ValueError(f"Task {task_id} not found")
        title = task.title
        session.delete(task)
        session.commit()
        return {"task_id": task_id, "status": "deleted", "title": title}

@mcp.tool()
def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> dict:
    """Update task title or description"""
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()
        if not task:
            raise ValueError(f"Task {task_id} not found")
        if title:
            task.title = title
        if description is not None:
            task.description = description
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        return {"task_id": task.id, "status": "updated", "title": task.title}