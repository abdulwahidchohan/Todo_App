"""
FastAPI application for the Todo backend with CRUD endpoints.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from datetime import datetime
import uuid

from database import get_session
from models import Task, TaskCreate, TaskUpdate, TaskPublic
from todo_logic import (
    create_task_logic,
    get_tasks_logic,
    update_task_logic,
    delete_task_logic,
    toggle_task_status_logic
)

app = FastAPI(title="Todo API", version="1.0.0")


# Mock user ID for now - in a real implementation, this would come from JWT middleware
MOCK_USER_ID = "mock-user-uuid"


# JWT Middleware placeholder - in a real implementation, this would validate JWT tokens
def get_current_user_id():
    """
    Placeholder for JWT authentication middleware.
    In a real implementation, this would extract and validate the user ID from the JWT token.
    For now, it returns a mock user ID.
    """
    return MOCK_USER_ID


@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Todo API"}


@app.get("/api/tasks", response_model=List[TaskPublic])
def get_tasks(
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks for the authenticated user.

    Args:
        current_user_id: The ID of the current authenticated user
        session: Database session

    Returns:
        List of tasks for the user
    """
    tasks = get_tasks_logic(session, current_user_id)
    return tasks


@app.post("/api/tasks", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data
        current_user_id: The ID of the current authenticated user
        session: Database session

    Returns:
        Created task object
    """
    task = create_task_logic(session, task_data, current_user_id)
    return task


@app.put("/api/tasks/{id}", response_model=TaskPublic)
def update_task(
    id: int,
    task_data: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update an existing task for the authenticated user.

    Args:
        id: Task ID to update
        task_data: Task update data
        current_user_id: The ID of the current authenticated user
        session: Database session

    Returns:
        Updated task object
    """
    updated_task = update_task_logic(
        session,
        id,
        current_user_id,
        title=task_data.title,
        description=task_data.description
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


@app.delete("/api/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a task for the authenticated user.

    Args:
        id: Task ID to delete
        current_user_id: The ID of the current authenticated user
        session: Database session
    """
    deleted = delete_task_logic(session, id, current_user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return


@app.patch("/api/tasks/{id}/complete", response_model=TaskPublic)
def toggle_task_status(
    id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task for the authenticated user.

    Args:
        id: Task ID to toggle
        current_user_id: The ID of the current authenticated user
        session: Database session

    Returns:
        Updated task object with toggled status
    """
    updated_task = toggle_task_status_logic(session, id, current_user_id)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


# Include the database creation function for initialization
def create_db_and_tables():
    """
    Create database tables.
    This function should be called during application startup.
    """
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


# Event handler for startup
@app.on_event("startup")
def on_startup():
    """
    Event handler for application startup.
    Creates database tables if they don't exist.
    """
    import time
    import logging
    from sqlalchemy.exc import OperationalError
    from sqlmodel import SQLModel

    # Retry connecting to the database with exponential backoff
    max_retries = 10
    for attempt in range(max_retries):
        try:
            # Try to connect to the database
            from database import engine
            SQLModel.metadata.create_all(bind=engine)
            logging.info("Database connection established successfully")
            break
        except OperationalError as e:
            logging.warning(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                logging.error("Failed to connect to database after maximum retries")
                raise e
            time.sleep(2 ** attempt)  # Exponential backoff


# Chat endpoint
@app.post("/api/chat")
async def chat(message: str, userId: str = None):
    """
    Chat endpoint that receives user messages, sends them to the OpenAI Agent
    which uses our MCP tools, and returns the AI's response.

    Args:
        message: The user's message
        userId: The ID of the user (for authentication purposes)

    Returns:
        JSON response with the AI's reply
    """
    # In a real implementation, this would:
    # 1. Authenticate the user (using the userId parameter)
    # 2. Send the message to an OpenAI-compatible agent
    # 3. The agent would use our MCP tools based on the natural language
    # 4. Return the agent's response

    # For now, we'll simulate the agent's response
    # In a real implementation, we would connect to an actual agent that uses our MCP tools
    # This would involve connecting to the MCP server and using the tools defined there

    # In a real implementation, we would connect to the MCP server here
    # For now, we'll call our simulation function
    response = await process_with_mcp_agent(message, userId)

    return {"response": response}


async def process_with_mcp_agent(message: str, userId: str) -> str:
    """
    Process the user's message with an agent that uses MCP tools.
    This is a placeholder implementation that simulates the agent behavior.

    Args:
        message: The user's message
        userId: The ID of the user

    Returns:
        The agent's response
    """
    # In a real implementation, this would:
    # 1. Connect to the MCP server
    # 2. Send the message to an AI agent
    # 3. The agent would determine which MCP tools to call based on the message
    # 4. Execute the appropriate tools
    # 5. Return the formatted response

    # For now, we'll simulate the agent's behavior
    # Parse the message to determine intent
    message_lower = message.lower()

    if any(word in message_lower for word in ["add", "create", "new task"]):
        # Simulate calling add_task tool
        # Extract task title and description from message
        import re
        # Simple extraction - in reality, an LLM would parse this more sophisticatedly
        title_match = re.search(r"(?:to|that|for) ([^.!?]+)", message_lower)
        if not title_match:
            title_match = re.search(r"(?:add|create) ([^.!?]+)", message_lower)

        title = title_match.group(1).strip() if title_match else "New task"

        # Simulate calling the add_task tool
        # In a real implementation, we would call the MCP server
        return f"I've added the task '{title}' for you. What else can I help with?"

    elif any(word in message_lower for word in ["list", "show", "what", "my tasks"]):
        # Simulate calling list_tasks tool
        # In a real implementation, we would call the MCP server
        return "Here are your tasks: 1. Buy groceries (incomplete), 2. Call mom (incomplete)."

    elif any(word in message_lower for word in ["complete", "done", "finish", "mark"]):
        # Simulate calling complete_task tool
        # Extract task ID if mentioned
        import re
        id_match = re.search(r"#?(\d+)", message)
        task_id = id_match.group(1) if id_match else "the task"

        # Simulate calling the complete_task tool
        # In a real implementation, we would call the MCP server
        return f"I've marked task #{task_id} as complete. Great job!"

    else:
        # Default response
        return f"I understand you said: '{message}'. How can I help you manage your tasks?"