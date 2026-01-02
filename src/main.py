"""
Python Console Todo App
Main application logic with CLI interface.
"""

from typing import List, Optional
from models import Task


class TodoManager:
    """
    Manages the collection of tasks in memory.
    Handles all CRUD operations on tasks.
    """
    
    def __init__(self):
        """
        Initialize the TodoManager with an empty task list and ID counter.
        """
        self.tasks: List[Task] = []
        self.next_id: int = 1
    
    def add_task(self, title: str, description: str = "") -> int:
        """
        Creates a new Task object with the next available ID and adds it to the tasks list.
        
        Args:
            title (str): Task title (required)
            description (str): Task description (optional)
            
        Returns:
            int: The ID of the newly created task
        """
        new_task = Task(task_id=self.next_id, title=title, description=description)
        self.tasks.append(new_task)
        task_id = self.next_id
        self.next_id += 1
        return task_id
    
    def delete_task(self, task_id: int) -> bool:
        """
        Finds the task with the given ID in the tasks list and removes it.
        
        Args:
            task_id (int): The ID of the task to delete
            
        Returns:
            bool: True if successful, False if task not found
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False
    
    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Finds the task with the given ID in the tasks list and updates the specified fields.
        
        Args:
            task_id (int): The ID of the task to update
            title (Optional[str]): New title (if provided)
            description (Optional[str]): New description (if provided)
            
        Returns:
            bool: True if successful, False if task not found
        """
        for task in self.tasks:
            if task.id == task_id:
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                return True
        return False
    
    def get_all_tasks(self) -> List[Task]:
        """
        Returns a copy of the tasks list for safe read access.
        
        Returns:
            List[Task]: Copy of the tasks list
        """
        return self.tasks.copy()
    
    def toggle_task_status(self, task_id: int) -> bool:
        """
        Finds the task with the given ID and toggles its status between "incomplete" and "complete".
        
        Args:
            task_id (int): The ID of the task to toggle
            
        Returns:
            bool: True if successful, False if task not found
        """
        for task in self.tasks:
            if task.id == task_id:
                if task.status == "incomplete":
                    task.status = "complete"
                else:
                    task.status = "incomplete"
                return True
        return False


def display_menu():
    """
    Shows the main menu options to the user in a formatted way.
    """
    print("\nPython Console Todo App")
    print("=======================")
    print("1. Add Task")
    print("2. Delete Task")
    print("3. Update Task")
    print("4. View Task List")
    print("5. Mark Task as Complete")
    print("6. Exit")
    print()


def get_user_choice() -> str:
    """
    Gets and validates the user's menu choice.
    
    Returns:
        str: The user's menu choice
    """
    while True:
        try:
            choice = input("Enter your choice (1-6): ").strip()
            if choice in ["1", "2", "3", "4", "5", "6"]:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            exit()


def handle_add_task(todo_manager: TodoManager):
    """
    Handles the Add Task operation.
    
    Args:
        todo_manager (TodoManager): The TodoManager instance to use
    """
    print("\n--- Add Task ---")
    title = input("Enter task title: ").strip()
    
    if not title:
        print("Error: Task title cannot be empty.")
        return
    
    description = input("Enter task description (optional): ").strip()
    task_id = todo_manager.add_task(title, description)
    print(f"Task added successfully with ID: {task_id}")


def handle_delete_task(todo_manager: TodoManager):
    """
    Handles the Delete Task operation.
    
    Args:
        todo_manager (TodoManager): The TodoManager instance to use
    """
    print("\n--- Delete Task ---")
    tasks = todo_manager.get_all_tasks()
    
    if not tasks:
        print("No tasks available to delete.")
        return
    
    print("Current tasks:")
    display_tasks(tasks)
    
    try:
        task_id = int(input("Enter the ID of the task to delete: "))
        if todo_manager.delete_task(task_id):
            print(f"Task with ID {task_id} deleted successfully.")
        else:
            print(f"Error: Task with ID {task_id} not found.")
    except ValueError:
        print("Error: Please enter a valid task ID (integer).")


def handle_update_task(todo_manager: TodoManager):
    """
    Handles the Update Task operation.
    
    Args:
        todo_manager (TodoManager): The TodoManager instance to use
    """
    print("\n--- Update Task ---")
    tasks = todo_manager.get_all_tasks()
    
    if not tasks:
        print("No tasks available to update.")
        return
    
    print("Current tasks:")
    display_tasks(tasks)
    
    try:
        task_id = int(input("Enter the ID of the task to update: "))
        
        # Check if task exists
        task_exists = any(task.id == task_id for task in tasks)
        if not task_exists:
            print(f"Error: Task with ID {task_id} not found.")
            return
        
        current_task = next(task for task in tasks if task.id == task_id)
        
        new_title = input(f"Enter new title (current: '{current_task.title}', press Enter to keep current): ").strip()
        new_description = input(f"Enter new description (current: '{current_task.description}', press Enter to keep current): ").strip()
        
        # Prepare update parameters
        title_update = new_title if new_title else None
        description_update = new_description if new_description else None
        
        if todo_manager.update_task(task_id, title_update, description_update):
            print(f"Task with ID {task_id} updated successfully.")
        else:
            print(f"Error: Task with ID {task_id} not found.")
    except ValueError:
        print("Error: Please enter a valid task ID (integer).")


def handle_view_tasks(todo_manager: TodoManager):
    """
    Handles the View Task List operation.
    
    Args:
        todo_manager (TodoManager): The TodoManager instance to use
    """
    print("\n--- Task List ---")
    tasks = todo_manager.get_all_tasks()
    
    if not tasks:
        print("No tasks available.")
        return
    
    display_tasks(tasks)


def display_tasks(tasks: List[Task]):
    """
    Displays a formatted list of tasks.
    
    Args:
        tasks (List[Task]): List of tasks to display
    """
    print(f"{'ID':<5} {'Title':<20} {'Status':<12}")
    print("-" * 40)
    for task in tasks:
        status = "✓ Complete" if task.status == "complete" else "○ Incomplete"
        print(f"{task.id:<5} {task.title[:19]:<20} {status:<12}")


def handle_toggle_status(todo_manager: TodoManager):
    """
    Handles the Mark Task as Complete operation.
    
    Args:
        todo_manager (TodoManager): The TodoManager instance to use
    """
    print("\n--- Mark Task as Complete ---")
    tasks = todo_manager.get_all_tasks()
    
    if not tasks:
        print("No tasks available.")
        return
    
    print("Current tasks:")
    display_tasks(tasks)
    
    try:
        task_id = int(input("Enter the ID of the task to toggle: "))
        if todo_manager.toggle_task_status(task_id):
            task = next((t for t in tasks if t.id == task_id), None)
            if task:
                new_status = "complete" if task.status == "complete" else "incomplete"
                print(f"Task with ID {task_id} marked as {new_status}.")
        else:
            print(f"Error: Task with ID {task_id} not found.")
    except ValueError:
        print("Error: Please enter a valid task ID (integer).")


def main():
    """
    Main application loop that orchestrates the CLI interface.
    """
    todo_manager = TodoManager()
    
    print("Welcome to the Python Console Todo App!")
    
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


if __name__ == "__main__":
    main()