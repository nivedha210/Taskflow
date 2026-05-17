
import json
import os
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

FILE_NAME = "tasks.json"


# ----------------------------
# CLEAR SCREEN
# ----------------------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# ----------------------------
# PAUSE SCREEN
# ----------------------------
def pause():
    input("\nPress Enter to continue...")


# ----------------------------
# LOAD TASKS
# ----------------------------
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return []


# ----------------------------
# SAVE TASKS
# ----------------------------
def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


# ----------------------------
# ADD TASK
# ----------------------------
def add_task(tasks):
    clear_screen()

    print(Fore.CYAN + "\n=== ADD NEW TASK ===")

    title = input("Enter task title: ").strip()

    if not title:
        print(Fore.RED + "Task title cannot be empty!")
        pause()
        return

    category = input("Enter category: ").strip()

    priority = input("Enter priority (High/Medium/Low): ").capitalize()

    if priority not in ["High", "Medium", "Low"]:
        print(Fore.RED + "Invalid priority!")
        pause()
        return

    due_date = input("Enter due date (YYYY-MM-DD): ")

    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except:
        print(Fore.RED + "Invalid date format!")
        pause()
        return

    task = {
        "title": title,
        "category": category,
        "priority": priority,
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }

    tasks.append(task)
    save_tasks(tasks)

    print(Fore.GREEN + "\nTask added successfully!")
    pause()


# ----------------------------
# VIEW TASKS
# ----------------------------
def view_tasks(tasks):
    clear_screen()

    print(Fore.YELLOW + "\n=== ALL TASKS ===")

    if not tasks:
        print(Fore.RED + "\nNo tasks found!")
        pause()
        return

    today = datetime.today().date()

    for index, task in enumerate(tasks, start=1):

        due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()

        status = "Completed" if task["completed"] else "Pending"

        if not task["completed"] and due < today:
            status = "Overdue"

        if task['priority'] == "High":
            color = Fore.RED

        elif task['priority'] == "Medium":
            color = Fore.YELLOW

        else:
            color = Fore.GREEN

        print(color + f"""
------------------------------------
Task #{index}
------------------------------------
Title      : {task['title']}
Category   : {task['category']}
Priority   : {task['priority']}
Due Date   : {task['due_date']}
Status     : {status}
Created On : {task['created_at']}
""")

    pause()


# ----------------------------
# MARK TASK COMPLETED
# ----------------------------
def mark_completed(tasks):
    clear_screen()

    if not tasks:
        print(Fore.RED + "No tasks available!")
        pause()
        return

    view_tasks_without_pause(tasks)

    try:
        task_no = int(input("\nEnter task number to mark completed: "))

        if 1 <= task_no <= len(tasks):
            tasks[task_no - 1]["completed"] = True
            save_tasks(tasks)

            print(Fore.GREEN + "\nTask marked as completed!")

        else:
            print(Fore.RED + "\nInvalid task number!")

    except:
        print(Fore.RED + "\nPlease enter a valid number!")

    pause()


# ----------------------------
# DELETE TASK
# ----------------------------
def delete_task(tasks):
    clear_screen()

    if not tasks:
        print(Fore.RED + "No tasks available!")
        pause()
        return

    view_tasks_without_pause(tasks)

    try:
        task_no = int(input("\nEnter task number to delete: "))

        if 1 <= task_no <= len(tasks):
            deleted = tasks.pop(task_no - 1)
            save_tasks(tasks)

            print(Fore.GREEN + f"\nDeleted task: {deleted['title']}")

        else:
            print(Fore.RED + "\nInvalid task number!")

    except:
        print(Fore.RED + "\nInvalid input!")

    pause()


# ----------------------------
# EDIT TASK
# ----------------------------
def edit_task(tasks):
    clear_screen()

    if not tasks:
        print(Fore.RED + "No tasks available!")
        pause()
        return

    view_tasks_without_pause(tasks)

    try:
        task_no = int(input("\nEnter task number to edit: "))

        if 1 <= task_no <= len(tasks):

            task = tasks[task_no - 1]

            print("\nLeave blank to keep old value.\n")

            new_title = input(f"New title ({task['title']}): ")
            new_category = input(f"New category ({task['category']}): ")
            new_priority = input(f"New priority ({task['priority']}): ")
            new_due = input(f"New due date ({task['due_date']}): ")

            if new_title:
                task['title'] = new_title

            if new_category:
                task['category'] = new_category

            if new_priority:
                new_priority = new_priority.capitalize()

                if new_priority in ["High", "Medium", "Low"]:
                    task['priority'] = new_priority
                else:
                    print(Fore.RED + "\nInvalid priority! Keeping old value.")

            if new_due:
                try:
                    datetime.strptime(new_due, "%Y-%m-%d")
                    task['due_date'] = new_due
                except:
                    print(Fore.RED + "\nInvalid date! Keeping old value.")

            save_tasks(tasks)

            print(Fore.GREEN + "\nTask updated successfully!")

        else:
            print(Fore.RED + "\nInvalid task number!")

    except:
        print(Fore.RED + "\nInvalid input!")

    pause()


# ----------------------------
# SEARCH TASKS
# ----------------------------
def search_tasks(tasks):
    clear_screen()

    keyword = input("Enter keyword to search: ").lower()

    found = False

    for index, task in enumerate(tasks, start=1):
        if keyword in task['title'].lower():

            found = True

            print(Fore.CYAN + f"""
------------------------------------
Task #{index}
------------------------------------
Title    : {task['title']}
Category : {task['category']}
Priority : {task['priority']}
Status   : {'Completed' if task['completed'] else 'Pending'}
""")

    if not found:
        print(Fore.RED + "\nNo matching tasks found!")

    pause()


# ----------------------------
# PRODUCTIVITY ANALYTICS
# ----------------------------
def analytics(tasks):
    clear_screen()

    total = len(tasks)

    completed = len([t for t in tasks if t['completed']])

    pending = total - completed

    productivity = 0

    if total > 0:
        productivity = (completed / total) * 100

    print(Fore.MAGENTA + "\n=== PRODUCTIVITY ANALYTICS ===")

    print(f"\nTotal Tasks       : {total}")
    print(f"Completed Tasks   : {completed}")
    print(f"Pending Tasks     : {pending}")
    print(f"Productivity      : {productivity:.2f}%")

    today = datetime.today().strftime("%Y-%m-%d")

    daily_completed = len([
        t for t in tasks
        if t['completed'] and t['created_at'] == today
    ])

    print(f"Today's Completed : {daily_completed}")

    pause()


# ----------------------------
# VIEW TASKS WITHOUT PAUSE
# ----------------------------
def view_tasks_without_pause(tasks):

    print(Fore.YELLOW + "\n=== ALL TASKS ===")

    today = datetime.today().date()

    for index, task in enumerate(tasks, start=1):

        due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()

        status = "Completed" if task["completed"] else "Pending"

        if not task["completed"] and due < today:
            status = "Overdue"

        if task['priority'] == "High":
            color = Fore.RED
        elif task['priority'] == "Medium":
            color = Fore.YELLOW
        else:
            color = Fore.GREEN

        print(color + f"""
------------------------------------
Task #{index}
------------------------------------
Title      : {task['title']}
Category   : {task['category']}
Priority   : {task['priority']}
Due Date   : {task['due_date']}
Status     : {status}
Created On : {task['created_at']}
""")


# ----------------------------
# MAIN MENU
# ----------------------------
def menu():

    tasks = load_tasks()

    while True:

        clear_screen()

        print(Fore.BLUE + """
====================================
      TASKFLOW PRO
 Smart Productivity Manager
====================================

1. Add Task
2. View Tasks
3. Edit Task
4. Delete Task
5. Mark Task Completed
6. Search Tasks
7. Productivity Analytics
8. Exit
""")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task(tasks)

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            edit_task(tasks)

        elif choice == "4":
            delete_task(tasks)

        elif choice == "5":
            mark_completed(tasks)

        elif choice == "6":
            search_tasks(tasks)

        elif choice == "7":
            analytics(tasks)

        elif choice == "8":
            clear_screen()
            print(Fore.GREEN + "Thank you for using TaskFlow Pro!")
            break

        else:
            print(Fore.RED + "\nInvalid choice!")
            pause()


# ----------------------------
# START PROGRAM
# ----------------------------
menu()


