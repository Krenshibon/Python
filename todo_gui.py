import tkinter as tk
from tkinter import messagebox
import todo

class TodoApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Todo App")

        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        entry_frame = tk.Frame(root)
        entry_frame.pack(fill=tk.X, padx=10)

        self.entry = tk.Entry(entry_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(entry_frame, text="Add", command=self.add_task).pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(btn_frame, text="Mark Done", command=self.mark_done).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Delete", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_tasks).pack(side=tk.LEFT)

        self.load_tasks()

    def load_tasks(self):
        self.listbox.delete(0, tk.END)
        tasks = todo.load_tasks()
        for t in tasks:
            status = "[x]" if t.get("done") else "[ ]"
            self.listbox.insert(tk.END, f"{t['id']} {status} {t['description']}")

    def add_task(self):
        desc = self.entry.get().strip()
        if not desc:
            messagebox.showwarning("Input Error", "Please enter a task description")
            return
        todo.add_task(desc)
        self.entry.delete(0, tk.END)
        self.load_tasks()

    def _selected_task_id(self):
        selection = self.listbox.curselection()
        if not selection:
            return None
        item = self.listbox.get(selection[0])
        return int(item.split()[0])

    def mark_done(self):
        task_id = self._selected_task_id()
        if task_id is None:
            messagebox.showwarning("Selection Error", "Please select a task")
            return
        todo.mark_done(task_id)
        self.load_tasks()

    def delete_task(self):
        task_id = self._selected_task_id()
        if task_id is None:
            messagebox.showwarning("Selection Error", "Please select a task")
            return
        todo.delete_task(task_id)
        self.load_tasks()

    def clear_tasks(self):
        if messagebox.askyesno("Confirm", "Clear all tasks?"):
            todo.clear_tasks()
            self.load_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()
