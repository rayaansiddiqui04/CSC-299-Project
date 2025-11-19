from typing import List, Dict, Any, Optional
from .storage import load_state, save_state


def add_task(
    title: str,
    priority: str = "medium",
    due_date: Optional[str] = None,
    tags: Optional[List[str]] = None,
    notes: str = "",
) -> Dict[str, Any]:
    """Create a new task, save it, and return it."""
    state = load_state()
    task_id = state.get("next_task_id", 1)

    task = {
        "id": task_id,
        "title": title,
        "status": "todo",        # todo | done
        "priority": priority,    # low | medium | high
        "due_date": due_date,    # string like "2025-11-20"
        "tags": tags or [],
        "notes": notes,
    }

    state["tasks"].append(task)
    state["next_task_id"] = task_id + 1
    save_state(state)
    return task


def list_tasks(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Return all tasks, or only tasks with a given status (todo/done).
    """
    state = load_state()
    tasks: List[Dict[str, Any]] = state.get("tasks", [])

    if status:
        tasks = [t for t in tasks if t.get("status") == status]

    return tasks


def complete_task(task_id: int) -> Optional[Dict[str, Any]]:
    """
    Mark a task as done. Returns the updated task or None if not found.
    """
    state = load_state()
    for t in state.get("tasks", []):
        if t.get("id") == task_id:
            t["status"] = "done"
            save_state(state)
            return t
    return None