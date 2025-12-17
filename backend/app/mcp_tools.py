from mcp.server.fastmcp import FastMCP
from sqlmodel import Session, select
from datetime import datetime, timezone
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from .database import Task, get_session, engine
except ImportError:
    from database import Task, get_session, engine

mcp = FastMCP("Todo Tools")

@mcp.tool()
def add_task(user_id: str, title: str, description: str = "") -> str:
    """Create a new task"""
    logger.info(f"🔧 add_task called: user_id={user_id}, title={title}")
    
    session = Session(engine)
    
    try:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        
        # Return simple string message for better agent understanding
        result_msg = f"✅ Task created successfully! ID: {task.id}, Title: '{task.title}'"
        if task.description:
            result_msg += f", Description: '{task.description}'"
        
        logger.info(f"✅ Task created: ID={task.id}")
        return result_msg
        
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Error creating task: {e}")
        return f"❌ Error: Could not create task - {str(e)}"
        
    finally:
        session.close()

@mcp.tool()
def list_tasks(user_id: str, status: str = "all") -> str:
    """List user's tasks. Status: all, pending, or completed"""
    logger.info(f"🔧 list_tasks called: user_id={user_id}, status={status}")
    
    session = Session(engine)
    
    try:
        query = select(Task).where(Task.user_id == user_id)
        
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
            
        tasks = session.exec(query).all()
        
        if not tasks:
            return f"📭 No {status} tasks found."
        
        # Format as readable string
        result_lines = [f"📋 Your {status} tasks ({len(tasks)} total):"]
        for t in tasks:
            status_icon = "✅" if t.completed else "⏳"
            task_line = f"\n{status_icon} [ID: {t.id}] {t.title}"
            if t.description:
                task_line += f" - {t.description}"
            result_lines.append(task_line)
        
        result_msg = "".join(result_lines)
        logger.info(f"✅ Listed {len(tasks)} tasks")
        return result_msg
        
    except Exception as e:
        logger.error(f"❌ Error listing tasks: {e}")
        return f"❌ Error: Could not list tasks - {str(e)}"
        
    finally:
        session.close()

@mcp.tool()
def complete_task(user_id: str, task_id: int) -> str:
    """Mark task as completed"""
    logger.info(f"🔧 complete_task called: user_id={user_id}, task_id={task_id}")
    
    session = Session(engine)
    
    try:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()
        
        if not task:
            return f"❌ Task {task_id} not found for this user"
            
        task.completed = True
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)
        
        result_msg = f"✅ Marked '{task.title}' as completed!"
        logger.info(f"✅ Task {task_id} completed")
        return result_msg
        
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Error completing task: {e}")
        return f"❌ Error: Could not complete task - {str(e)}"
        
    finally:
        session.close()

@mcp.tool()
def delete_task(user_id: str, task_id: int) -> str:
    """Delete a task"""
    logger.info(f"🔧 delete_task called: user_id={user_id}, task_id={task_id}")
    
    session = Session(engine)
    
    try:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()
        
        if not task:
            return f"❌ Task {task_id} not found for this user"
            
        title = task.title
        session.delete(task)
        session.commit()
        
        result_msg = f"🗑️ Deleted '{title}' successfully!"
        logger.info(f"✅ Task {task_id} deleted")
        return result_msg
        
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Error deleting task: {e}")
        return f"❌ Error: Could not delete task - {str(e)}"
        
    finally:
        session.close()

@mcp.tool()
def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> str:
    """Update task title or description"""
    logger.info(f"🔧 update_task called: user_id={user_id}, task_id={task_id}")
    
    session = Session(engine)
    
    try:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()
        
        if not task:
            return f"❌ Task {task_id} not found for this user"
            
        changes = []
        if title:
            old_title = task.title
            task.title = title
            changes.append(f"title from '{old_title}' to '{title}'")
        if description is not None:
            task.description = description
            changes.append(f"description to '{description}'")
            
        task.updated_at = datetime.now(timezone.utc)
        session.add(task)
        session.commit()
        session.refresh(task)
        
        result_msg = f"✏️ Updated {', '.join(changes)} for task '{task.title}'"
        logger.info(f"✅ Task {task_id} updated")
        return result_msg
        
    except Exception as e:
        session.rollback()
        logger.error(f"❌ Error updating task: {e}")
        return f"❌ Error: Could not update task - {str(e)}"
        
    finally:
        session.close()

# Create app
mcp_app = mcp.streamable_http_app()

logger.info("🚀 MCP Todo Tools Server Started!")