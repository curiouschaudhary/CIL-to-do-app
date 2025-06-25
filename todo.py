import datetime
import json
import os
import time
from plyer import notification

notification.notify(
    title="Test Notification",
    message="This is a test alert!",
    timeout=5
)
# This script implements a simple to-do list application with the following features:


# Define the filename for storing the to-do list
TODO_FILE = "todo_list.json"

to_do_list = []

def load_tasks():
    """Loads tasks from the JSON file."""
    global to_do_list
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            try:
                to_do_list = json.load(f)
            except json.JSONDecodeError:
                print("Error decoding to-do list from file. Starting with an empty list.")
                to_do_list = []
    else:
        to_do_list = []

def save_tasks():
    """Saves the current to-do list to the JSON file."""
    with open(TODO_FILE, 'w') as f:
        json.dump(to_do_list, f, indent=4)

def show_menu():
    """Displays the to-do list menu."""
    print("\nTo-Do List Menu:")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

def add_task():
    """Adds a new task with description, priority, and due date."""
    task = input("Enter the task description: ")
    while True:
        priority = input("Enter the priority (High, Medium, Low): ").strip().capitalize()
        if priority in ["High", "Medium", "Low"]:
            break
        else:
            print("Invalid priority. Please enter High, Medium, or Low.")

    while True:
        due_date_str = input("Enter the due date (YYYY-MM-DD, leave blank for none): ").strip()
        if not due_date_str:
            due_date = None
            break
        try:
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    to_do_list.append({"task": task, "priority": priority, "due_date": str(due_date) if due_date else None, "completed": False, "created_at": timestamp})
    save_tasks()
    print(f"'{task}' with priority '{priority}' and due date '{due_date_str if due_date else 'None'}' has been added to the list.")

def view_tasks():
    """Displays the to-do list, sorted by priority and due date."""
    if not to_do_list:
        print("The to-do list is empty.")
    else:
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        sorted_tasks = sorted(
            [task for task in to_do_list if not task['completed']],
            key=lambda item: (priority_order[item["priority"]], item.get("due_date") or "9999-12-31") # Sort by priority, then due date (None last)
        )

        print("\nYour To-Do List (Prioritized, Not Completed):")
        for idx, task_data in enumerate(sorted_tasks, start=1):
            due_date_str = f" (Due: {task_data['due_date']})" if task_data['due_date'] else ""
            print(f"{idx}. [{task_data['priority']}] {task_data['task']}{due_date_str}")

        completed_tasks = [task for task in to_do_list if task['completed']]
        if completed_tasks:
            print("\nCompleted Tasks:")
            for idx, task_data in enumerate(completed_tasks, start=1):
                print(f"[X] {task_data['task']} (Completed at: {task_data['completed_at']})")

def complete_task():
    """Marks a task as completed and records the completion time."""
    view_tasks()
    incomplete_tasks = [task for task in to_do_list if not task['completed']]
    if incomplete_tasks:
        try:
            task_num = int(input("Enter the task number to mark as completed: "))
            if 1 <= task_num <= len(incomplete_tasks):
                task_to_complete = incomplete_tasks[task_num - 1]
                for task in to_do_list:
                    if task['task'] == task_to_complete['task'] and not task['completed']:
                        task['completed'] = True
                        task['completed_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_tasks()
                        print(f"'{task['task']}' has been marked as completed at {task['completed_at']}.")
                        break
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")
    elif to_do_list:
        print("No incomplete tasks to mark as completed.")
    else:
        print("The to-do list is empty.")

def delete_task():
    """Deletes a task from the to-do list."""
    view_tasks()
    if to_do_list:
        try:
            task_num = int(input("Enter the task number to delete: "))
            if 1 <= task_num <= len(to_do_list):
                deleted_task_data = to_do_list.pop(task_num - 1)
                save_tasks()
                print(f"'{deleted_task_data['task']}' has been removed.")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid number.")
    else:
        print("The to-do list is empty.")

def check_due_tasks():
    """Checks for tasks due today and sends a notification."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    upcoming_tasks = [task for task in to_do_list if task["due_date"] == today and not task["completed"]]

    for task in upcoming_tasks:
        notification.notify(
            title="Task Reminder!",
            message=f"'{task['task']}' is due today!",
            timeout=10  # Notification duration (seconds)
        )

if __name__ == "__main__":
    load_tasks()
    while True:
        check_due_tasks()  # Check for due tasks every minute
        time.sleep(60)  # Wait 60 seconds before checking again
        show_menu()
        choice = input("Choose an option (1-5): ")
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            complete_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            save_tasks()
            print("Have a nice day!")
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 5.")
