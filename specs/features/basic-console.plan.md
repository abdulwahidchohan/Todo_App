# Basic Console Todo App - Architecture Plan

## Overview
This document outlines the architecture plan for implementing the Basic Console Todo App as specified in `basic-console.md`. The application will be built using Python with in-memory storage and a console-based user interface.

## Architecture Components

### 1. Data Model
The application will use a simple dictionary-based data structure to store todo items in memory:

```python
# Internal storage structure
todos: Dict[int, Dict[str, Union[str, bool]]] = {
    id: {
        "id": int,
        "title": str,
        "completed": bool
    }
}
```

- Key: Unique integer ID (auto-incrementing)
- Value: Dictionary containing the todo item properties
- Next ID: Will track the next available ID for new items

### 2. Class Structure

#### TodoApp Class
The main application class that will handle all business logic:

```python
class TodoApp:
    def __init__(self):
        """Initialize the app with empty todos dict and next_id counter"""
        
    def add_todo(self, title: str) -> int:
        """Add a new todo item with the given title, return the assigned ID"""
        
    def get_todo(self, todo_id: int) -> Optional[Dict]:
        """Retrieve a todo item by its ID"""
        
    def get_all_todos(self) -> List[Dict]:
        """Retrieve all todo items"""
        
    def update_todo(self, todo_id: int, title: str) -> bool:
        """Update the title of an existing todo item, return success status"""
        
    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item by its ID, return success status"""
        
    def toggle_completion(self, todo_id: int) -> bool:
        """Toggle the completion status of a todo item, return success status"""
        
    def validate_todo_id(self, todo_id: int) -> bool:
        """Check if a given ID exists in the todos dictionary"""
```

#### TodoCLI Class
A separate class to handle the console interface:

```python
class TodoCLI:
    def __init__(self, todo_app: TodoApp):
        """Initialize with a TodoApp instance"""
        
    def display_menu(self):
        """Display the main menu options"""
        
    def get_user_input(self, prompt: str) -> str:
        """Get input from the user with a given prompt"""
        
    def display_todos(self, todos: List[Dict]):
        """Format and display the list of todos"""
        
    def display_message(self, message: str):
        """Display a message to the user"""
        
    def run(self):
        """Main loop to run the CLI interface"""
```

## Main Loop Logic

The main application flow will follow this pattern:

```
1. Initialize TodoApp and TodoCLI instances
2. Display welcome message
3. Main loop:
   a. Display menu options
   b. Get user choice
   c. Based on choice:
      - 1: Add new todo
      - 2: View all todos
      - 3: Update a todo
      - 4: Delete a todo
      - 5: Mark todo as complete/incomplete
      - 6: Exit
   d. Handle user input and call appropriate methods
   e. Display results
   f. Continue until user chooses to exit
4. Exit message
```

## Implementation Details

### Data Management
- Use a dictionary for O(1) lookup by ID
- Maintain a counter for the next available ID
- Implement validation to ensure IDs exist before operations

### Error Handling
- Validate user input (e.g., numeric IDs)
- Handle cases where requested IDs don't exist
- Handle empty input for todo titles
- Provide clear error messages to the user

### User Interface
- Clean, numbered menu system
- Clear prompts for user input
- Formatted display of todo items
- Confirmation for destructive operations (delete)

## File Structure
```
src/
└── todo_app.py          # Contains TodoApp and TodoCLI classes
```

## Dependencies
- Standard Python library only (no external dependencies)

## Performance Considerations
- Dictionary lookup for O(1) access by ID
- Simple data structure to handle up to 1000 items efficiently
- Minimal memory footprint

## Security Considerations
- Input validation to prevent injection or unexpected behavior
- No persistent storage to eliminate data persistence risks

## Testing Strategy
- Unit tests for each method in TodoApp
- Integration tests for CLI functionality
- Error case testing for invalid inputs