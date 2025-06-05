# Todo App

This repository contains a simple command line todo application written in Python.

## Usage

```
python todo.py add "Buy milk" --priority high --due 2024-05-01  # Add a new task
python todo.py list                 # List all tasks
python todo.py done 1               # Mark task 1 as done
python todo.py delete 1             # Delete task 1
python todo.py clear                # Remove all tasks
```

The `add` command accepts optional `--priority` and `--due YYYY-MM-DD` arguments to
specify a priority level and due date for the task. Tasks are stored in
`tasks.json` in the same directory.
