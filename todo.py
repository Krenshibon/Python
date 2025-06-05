import argparse
import json
import os
from typing import List, Dict

TASKS_FILE = "tasks.json"

def load_tasks() -> List[Dict]:
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks: List[Dict]):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(description: str, priority: str = None, due: str = None):
    tasks = load_tasks()
    task_id = max([t["id"] for t in tasks], default=0) + 1
    task = {"id": task_id, "description": description, "done": False}
    if priority:
        task["priority"] = priority
    if due:
        task["due"] = due
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task {task_id}: {description}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    show_priority = any("priority" in t for t in tasks)
    show_due = any("due" in t for t in tasks)

    header_parts = ["ID", "Status"]
    if show_priority:
        header_parts.append("Priority")
    if show_due:
        header_parts.append("Due")
    header_parts.append("Description")
    print(" ".join(header_parts))

    for t in tasks:
        parts = [str(t["id"]), "[x]" if t.get("done") else "[ ]"]
        if show_priority:
            parts.append(str(t.get("priority", "-")))
        if show_due:
            parts.append(str(t.get("due", "-")))
        parts.append(t["description"])
        print(" ".join(parts))

def mark_done(task_id: int):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            if t.get("done"):
                print(f"Task {task_id} is already completed.")
            else:
                t["done"] = True
                save_tasks(tasks)
                print(f"Marked task {task_id} as done.")
            return
    print(f"Task {task_id} not found.")

def delete_task(task_id: int):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Task {task_id} not found.")
    else:
        save_tasks(new_tasks)
        print(f"Deleted task {task_id}.")

def clear_tasks():
    save_tasks([])
    print("Cleared all tasks.")

def main():
    parser = argparse.ArgumentParser(description="Simple todo app")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("description", help="Task description")
    add_p.add_argument(
        "--priority",
        help="Task priority",
    )
    add_p.add_argument(
        "--due",
        help="Due date in YYYY-MM-DD format",
    )

    list_p = subparsers.add_parser("list", help="List tasks")

    done_p = subparsers.add_parser("done", help="Mark a task as done")
    done_p.add_argument("task_id", type=int)

    del_p = subparsers.add_parser("delete", help="Delete a task")
    del_p.add_argument("task_id", type=int)

    clear_p = subparsers.add_parser("clear", help="Clear all tasks")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description, priority=args.priority, due=args.due)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        mark_done(args.task_id)
    elif args.command == "delete":
        delete_task(args.task_id)
    elif args.command == "clear":
        clear_tasks()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
