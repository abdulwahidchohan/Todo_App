"""
Data models for the Todo application using SQLModel.
"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    """
    Base model for Task with common fields.
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: str = Field(default="incomplete", regex="^(incomplete|complete)$")


class Task(TaskBase, table=True):
    """
    Task model representing the tasks table in the database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=255)  # UUID as string from Better Auth
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    """
    Model for creating new tasks.
    """
    pass


class TaskUpdate(SQLModel):
    """
    Model for updating existing tasks.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskPublic(TaskBase):
    """
    Public model for tasks with ID and timestamps.
    """
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime