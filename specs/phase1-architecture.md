# Phase I: Python Console Todo App Architecture Plan

## Overview
This document outlines the architectural design for the Python Console Todo Application. It defines the core components, their responsibilities, and how they interact to fulfill the requirements specified in `specs/features/phase1-console.md`.

## Architecture Components

### 1. Task Model
The `Task` class will represent a single todo item with all its properties.

#### Class Definition
```python
class Task:
    def __init__(self, task_id: int, title: str, description: str = "", status: str = "incomplete"):
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status  # "incomplete" or "complete"
```

#### Properties
- `id`: Unique identifier for the task (integer)
- `title`: Task title (string, required)
- `description`: Task description (string, optional)
- `status`: Completion status ("incomplete" or "complete")

#### Responsibilities
- Store task data in a structured format
- Provide methods for updating task properties if needed

### 2. TodoManager Class
The `TodoManager` class will handle all business logic related to task management.

#### Class Definition
```python
class TodoManager:
    def __init__(self):
        self.tasks = []  # List of Task objects
        self.next_id = 1  # Auto-incrementing ID counter
```

#### Methods

##### `add_task(title: str, description: str = "") -> int`
- Creates a new Task object with the next available ID
- Adds the task to the tasks list
- Increments the next_id counter
- Returns the ID of the newly created task

##### `delete_task(task_id: int) -> bool`
- Finds the task with the given ID in the tasks list
- Removes the task if found
- Returns True if successful, False if task not found

##### `update_task(task_id: int, title: str = None, description: str = None) -> bool`
- Finds the task with the given ID in the tasks list
- Updates the specified fields if the task exists
- Returns True if successful, False if task not found

##### `get_all_tasks() -> List[Task]`
- Returns a copy of the tasks list
- Enables safe read access to the task data

##### `toggle_task_status(task_id: int) -> bool`
- Finds the task with the given ID in the tasks list
- Toggles the status between "incomplete" and "complete"
- Returns True if successful, False if task not found

##### `get_next_id() -> int`
- Returns the next available ID for a new task
- Used internally to maintain unique IDs

#### Responsibilities
- Manage the collection of tasks in memory
- Handle all CRUD operations on tasks
- Maintain unique IDs for tasks
- Provide data access methods for the CLI interface

### 3. CLI Interface
The command-line interface will handle user input and output, orchestrating interactions between the user and the TodoManager.

#### Main Loop Structure
```python
def main():
    todo_manager = TodoManager()
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == "1":
            handle_add_task(todo_manager)
        elif choice == "2":
            handle_delete_task(todo_manager)
        elif choice == "3":
            handle_update_task(todo_manager)
        elif choice == "4":
            handle_view_tasks(todo_manager)
        elif choice == "5":
            handle_toggle_status(todo_manager)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
```

#### Menu Display
- Shows the main menu options to the user
- Formats the menu in a readable way

#### User Input Handlers
Each menu option will have a dedicated handler function:
- `handle_add_task(todo_manager)`
- `handle_delete_task(todo_manager)`
- `handle_update_task(todo_manager)`
- `handle_view_tasks(todo_manager)`
- `handle_toggle_status(todo_manager)`

#### Responsibilities
- Present the user interface
- Handle user input and validation
- Call appropriate TodoManager methods
- Display results and error messages to the user

## Error Handling Strategy

### Input Validation
- Validate user input for expected data types (e.g., ensure task IDs are integers)
- Check for required fields (e.g., task title cannot be empty when adding a task)
- Provide clear error messages for invalid input

### Task ID Validation
- Before any operation requiring a task ID, verify that the task exists
- Implement helper methods to check if a task ID exists before operations
- Return appropriate error messages when a non-existent ID is referenced

### Exception Handling
- Wrap potentially problematic operations in try-catch blocks
- Handle ValueError exceptions when converting user input to integers
- Provide graceful fallbacks for unexpected errors

### Specific Error Scenarios
1. **Deleting non-existent task**: Display error message "Task with ID X not found"
2. **Updating non-existent task**: Display error message "Task with ID X not found"
3. **Toggling status of non-existent task**: Display error message "Task with ID X not found"
4. **Invalid menu choice**: Display error message and prompt again
5. **Invalid task ID input**: Display error message and prompt again

## Data Flow

### Task Creation Flow
1. User selects "Add Task" from menu
2. CLI prompts for title and description
3. CLI calls `todo_manager.add_task(title, description)`
4. TodoManager creates new Task object with next available ID
5. TodoManager adds task to tasks list
6. Method returns new task ID
7. CLI displays confirmation with task ID

### Task Retrieval Flow
1. User selects "View Task List" from menu
2. CLI calls `todo_manager.get_all_tasks()`
3. TodoManager returns copy of tasks list
4. CLI formats and displays tasks

### Task Modification Flow
1. User selects operation (Update, Delete, Toggle Status)
2. CLI prompts for task ID
3. CLI validates input and calls appropriate TodoManager method
4. TodoManager performs operation and returns success status
5. CLI displays appropriate confirmation or error message

## Implementation Considerations

### Memory Management
- Since data is stored in-memory only, all data will be lost when the application exits
- No need for complex data persistence mechanisms
- Simple list structure is sufficient for the requirements

### Thread Safety
- Not required since this is a single-user console application
- No concurrent access to data structures

### Extensibility
- Design allows for easy addition of new features
- Separation of concerns enables independent testing of components
- Data model is separate from business logic and UI

## Testing Strategy

### Unit Tests
- Test each method in TodoManager class independently
- Test Task model initialization and properties
- Test error handling scenarios

### Integration Tests
- Test the interaction between CLI and TodoManager
- Test complete user workflows

### Error Condition Tests
- Test operations with non-existent task IDs
- Test input validation
- Test boundary conditions