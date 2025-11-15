from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import Iterable, List, Optional, Sequence


ISO_TIMESTAMP = "%Y-%m-%dT%H:%M:%S.%fZ"


class ValidationError(ValueError):
    """Raised for invalid user input."""


class TaskNotFoundError(LookupError):
    """Raised when a task ID does not exist."""


class TaskAlreadyCompletedError(ValueError):
    """Raised when attempting to complete an already completed task."""


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @classmethod
    def from_string(cls, value: Optional[str]) -> "Priority":
        if value is None:
            return cls.MEDIUM
        normalized = value.strip().lower()
        try:
            return cls(normalized)
        except ValueError as exc:
            raise ValidationError(
                f"Priority must be one of: {', '.join(p.value for p in cls)}"
            ) from exc

    @property
    def sort_value(self) -> int:
        order = {Priority.HIGH: 2, Priority.MEDIUM: 1, Priority.LOW: 0}
        return order[self]


@dataclass
class Task:
    id: int
    description: str
    created_at: datetime
    priority: Priority = Priority.MEDIUM
    due: Optional[date] = None
    completed: bool = False
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "created_at": self.created_at.strftime(ISO_TIMESTAMP),
            "priority": self.priority.value,
            "due": self.due.isoformat() if self.due else None,
            "completed": self.completed,
            "completed_at": self.completed_at.strftime(ISO_TIMESTAMP)
            if self.completed_at
            else None,
        }

    @classmethod
    def from_dict(cls, payload: dict) -> "Task":
        try:
            created_at = datetime.strptime(payload["created_at"], ISO_TIMESTAMP)
        except (KeyError, ValueError) as exc:
            raise ValidationError("Task payload missing valid created_at timestamp") from exc

        due_value = payload.get("due")
        due = datetime.strptime(due_value, "%Y-%m-%d").date() if due_value else None

        completed_value = payload.get("completed_at")
        completed_at = (
            datetime.strptime(completed_value, ISO_TIMESTAMP) if completed_value else None
        )
        return cls(
            id=int(payload["id"]),
            description=payload["description"],
            created_at=created_at.replace(tzinfo=timezone.utc),
            priority=Priority.from_string(payload.get("priority")),
            due=due,
            completed=bool(payload.get("completed", False)),
            completed_at=completed_at.replace(tzinfo=timezone.utc)
            if completed_at
            else None,
        )


def _ensure_description(description: str) -> str:
    if not description or not description.strip():
        raise ValidationError("Description cannot be empty.")
    return description.strip()


def parse_due_date(value: Optional[str]) -> Optional[date]:
    if value is None:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValidationError("Due date must use YYYY-MM-DD format.") from exc


def next_task_id(tasks: Sequence[Task]) -> int:
    if not tasks:
        return 1
    return max(task.id for task in tasks) + 1


def create_task(
    description: str,
    priority: Optional[str],
    due: Optional[str],
    existing_tasks: Sequence[Task],
) -> Task:
    clean_description = _ensure_description(description)
    priority_value = Priority.from_string(priority)
    due_value = parse_due_date(due)
    created_at = datetime.now(timezone.utc)
    return Task(
        id=next_task_id(existing_tasks),
        description=clean_description,
        created_at=created_at,
        priority=priority_value,
        due=due_value,
    )


def find_task(tasks: Sequence[Task], task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task
    raise TaskNotFoundError(f"Task {task_id} not found.")


def mark_task_complete(task: Task) -> Task:
    if task.completed:
        raise TaskAlreadyCompletedError(f"Task {task.id} is already completed.")
    task.completed = True
    task.completed_at = datetime.now(timezone.utc)
    return task


def delete_task(tasks: Sequence[Task], task_id: int) -> tuple[Task, List[Task]]:
    task = find_task(tasks, task_id)
    remaining = [candidate for candidate in tasks if candidate.id != task_id]
    return task, remaining


def filter_tasks(tasks: Sequence[Task], view: str) -> List[Task]:
    if view == "all":
        return list(tasks)
    if view == "completed":
        return [task for task in tasks if task.completed]
    return [task for task in tasks if not task.completed]


def sort_tasks(tasks: List[Task], sort_key: Optional[str]) -> List[Task]:
    if sort_key == "priority":
        return sorted(tasks, key=lambda t: t.priority.sort_value, reverse=True)
    if sort_key == "due":
        return sorted(
            tasks,
            key=lambda t: (t.due is None, t.due or date.max, t.created_at),
        )
    return sorted(tasks, key=lambda t: t.created_at)


def update_task_collection(tasks: List[Task], updated_task: Task) -> List[Task]:
    return [updated_task if task.id == updated_task.id else task for task in tasks]


def tasks_to_payload(tasks: Iterable[Task]) -> List[dict]:
    return [task.to_dict() for task in tasks]


def payload_to_tasks(payload: Iterable[dict]) -> List[Task]:
    return [Task.from_dict(item) for item in payload]
