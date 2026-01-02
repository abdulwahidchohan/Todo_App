"""
Business logic for the Todo application.
Contains CRUD operations that can be used by both the API and MCP server.
"""

from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from models import Task, TaskCreate


def create_task_logic(session: Session, task_data: TaskCreate, user_id: str) -> Task:
    """
    Create a new task in the database.
    
    Args:
        session: Database session
        task_data: Task creation data
        user_id: ID of the user creating the task
        
    Returns:
        Created Task object
    """
    task = Task(
        title=task_data.title,
        description=task_data.description,
        status="incomplete",  # Default status
        user_id=user_id
    )
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


def get_tasks_logic(session: Session, user_id: str, status_filter: Optional[str] = None) -> List[Task]:
    """
    Retrieve tasks for a specific user with optional status filter.
    
    Args:
        session: Database session
        user_id: ID of the user whose tasks to retrieve
        status_filter: Optional status filter ("incomplete", "complete", or None for all)
        
    Returns:
        List of Task objects
    """
    statement = select(Task).where(Task.user_id == user_id)
    
    if status_filter and status_filter != "all":
        statement = statement.where(Task.status == status_filter)
    
    tasks = session.exec(statement).all()
    return tasks


def update_task_logic(
    session: Session, 
    task_id: int, 
    user_id: str, 
    title: Optional[str] = None, 
    description: Optional[str] = None
) -> Optional[Task]:
    """
    Update an existing task.
    
    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user who owns the task
        title: New title (if provided)
        description: New description (if provided)
        
    Returns:
        Updated Task object or None if not found
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    
    if not task:
        return None
    
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task


def delete_task_logic(session: Session, task_id: int, user_id: str) -> bool:
    """
    Delete a task.
    
    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user who owns the task
        
    Returns:
        True if task was deleted, False if not found
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    
    if not task:
        return False
    
    session.delete(task)
    session.commit()
    
    return True


def toggle_task_status_logic(session: Session, task_id: int, user_id: str) -> Optional[Task]:
    """
    Toggle the completion status of a task.
    
    Args:
        session: Database session
        task_id: ID of the task to toggle
        user_id: ID of the user who owns the task
        
    Returns:
        Updated Task object or None if not found
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    
    if not task:
        return None
    
    # Toggle the status
    task.status = "complete" if task.status == "incomplete" else "incomplete"
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return task