import sys, os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
import tempfile
import json

import todo


def test_add_task(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        tasks_file = os.path.join(tmpdir, "tasks.json")
        monkeypatch.setattr(todo, "TASKS_FILE", tasks_file)

        todo.add_task("Test task", priority="high", due="2024-01-01")

        with open(tasks_file) as f:
            tasks = json.load(f)

        assert len(tasks) == 1
        t = tasks[0]
        assert t["description"] == "Test task"
        assert t["priority"] == "high"
        assert t["due"] == "2024-01-01"
        assert t["done"] is False


def test_mark_done(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        tasks_file = os.path.join(tmpdir, "tasks.json")
        monkeypatch.setattr(todo, "TASKS_FILE", tasks_file)

        todo.add_task("Test task")
        todo.mark_done(1)

        with open(tasks_file) as f:
            tasks = json.load(f)

        assert tasks[0]["done"] is True


def test_delete_task(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        tasks_file = os.path.join(tmpdir, "tasks.json")
        monkeypatch.setattr(todo, "TASKS_FILE", tasks_file)

        todo.add_task("Test task")
        todo.delete_task(1)

        if os.path.exists(tasks_file):
            with open(tasks_file) as f:
                tasks = json.load(f)
        else:
            tasks = []

        assert tasks == []
