"""
Data models for the Todo application.
"""

from typing import Dict, Any


class Task:
    """
    Represents a single todo task with its properties.
    """
    
    def __init__(self, task_id: int, title: str, description: str = "", status: str = "incomplete"):
        """
        Initialize a new Task instance.
        
        Args:
            task_id (int): Unique identifier for the task
            title (str): Task title (required)
            description (str): Task description (optional)
            status (str): Completion status ("incomplete" or "complete")
        """
        self.id: int = task_id
        self.title: str = title
        self.description: str = description
        self.status: str = status  # "incomplete" or "complete"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Task object to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status
        }
    
    def __repr__(self) -> str:
        """
        String representation of the Task object.
        
        Returns:
            str: String representation
        """
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', status='{self.status}')"