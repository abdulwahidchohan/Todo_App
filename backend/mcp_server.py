"""
MCP (Model Context Protocol) Server for the Todo application.
Exposes tools for AI agents to interact with the todo system.
"""

import asyncio
from mcp.server import Server
from mcp.server.exceptions import RequestCancelledException
from mcp.types import Tool, Argument, Prompt, PromptMessage, TextContent, EmbeddedResource, ResourceContents, ListPromptsResult, CallToolResult
from typing import Dict, Any, List, Optional
import json
from datetime import datetime

# Import CRUD functions from existing backend logic
from todo_logic import create_task_logic, get_tasks_logic, toggle_task_status_logic
from models import TaskCreate
from database import engine
from models import Task
from sqlmodel import Session, select


# Initialize the MCP server
mcp_server = Server("todo-mcp-server")


@mcp_server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """
    List all available tools provided by this server.
    """
    return [
        Tool(
            name="add_task",
            description="Creates a new task with the provided title and description",
            input_schema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title of the task to be created"},
                    "description": {"type": "string", "description": "Additional details about the task (optional)"}
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="Retrieves a list of tasks filtered by status",
            input_schema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "incomplete", "complete"],
                        "description": "Filter tasks by status. Default is 'all'",
                        "default": "all"
                    }
                }
            }
        ),
        Tool(
            name="complete_task",
            description="Marks a task as complete by its ID",
            input_schema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "The unique identifier of the task to mark as complete"}
                },
                "required": ["task_id"]
            }
        )
    ]


@mcp_server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """
    Handle tool calls from the MCP client.
    """
    try:
        if name == "add_task":
            return await handle_add_task(arguments)
        elif name == "list_tasks":
            return await handle_list_tasks(arguments)
        elif name == "complete_task":
            return await handle_complete_task(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        # Return error result
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error executing tool {name}: {str(e)}"
                )
            ],
            isError=True
        )


async def handle_add_task(arguments: Dict[str, Any]) -> CallToolResult:
    """
    Handle the add_task tool call.
    """
    title = arguments.get("title")
    description = arguments.get("description", "")

    if not title:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="Error: Title is required for add_task"
                )
            ],
            isError=True
        )

    # Create task data
    task_data = TaskCreate(title=title, description=description)

    # Use the existing database session
    with Session(engine) as session:
        # Use the shared business logic
        task = create_task_logic(session, task_data, "mock-user-uuid")

        # Format the response
        result = {
            "task_id": task.id,
            "success": True,
            "message": f"Task '{task.title}' created successfully"
        }

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=json.dumps(result)
            )
        ]
    )


async def handle_list_tasks(arguments: Dict[str, Any]) -> CallToolResult:
    """
    Handle the list_tasks tool call.
    """
    status_filter = arguments.get("status", "all")

    # Use the existing database session
    with Session(engine) as session:
        # Use the shared business logic
        tasks = get_tasks_logic(session, "mock-user-uuid", status_filter)

        # Format the response
        task_list = []
        for task in tasks:
            task_list.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status
            })

        result = {
            "tasks": task_list,
            "count": len(task_list),
            "success": True,
            "message": f"Retrieved {len(task_list)} {status_filter} tasks"
        }

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=json.dumps(result)
            )
        ]
    )


async def handle_complete_task(arguments: Dict[str, Any]) -> CallToolResult:
    """
    Handle the complete_task tool call.
    """
    task_id = arguments.get("task_id")

    if not task_id:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text="Error: task_id is required for complete_task"
                )
            ],
            isError=True
        )

    # Use the existing database session
    with Session(engine) as session:
        # Use the shared business logic
        task = toggle_task_status_logic(session, task_id, "mock-user-uuid")

        if not task:
            result = {
                "success": False,
                "message": f"Task with ID {task_id} not found"
            }
        else:
            result = {
                "success": True,
                "message": f"Task '{task.title}' marked as {task.status}",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status
                }
            }

    return CallToolResult(
        content=[
            TextContent(
                type="text",
                text=json.dumps(result)
            )
        ]
    )


# Run the server if this file is executed directly
if __name__ == "__main__":
    import sys
    import logging
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Run the server
    if len(sys.argv) > 1:
        # If arguments are provided, run in LSP mode
        from mcp.server.stdio import stdio_server
        with stdio_server() as server:
            mcp_server.run(server)
    else:
        # Otherwise, run in HTTP mode for testing
        print("Starting MCP server on http://localhost:3000...")
        import uvicorn
        uvicorn.run(mcp_server, host="0.0.0.0", port=3000)