from __future__ import annotations

from datetime import date, datetime, timezone

import pytest

from app import models


def build_task(description: str, task_id: int, completed: bool = False) -> models.Task:
    task = models.Task(
        id=task_id,
        description=description,
        created_at=datetime.now(timezone.utc),
        priority=models.Priority.MEDIUM,
        due=None,
        completed=completed,
    )
    return task


def test_create_task_assigns_ids_and_trims_description():
    first = models.create_task("First task", "high", None, [])
    second = models.create_task("  Second  ", None, "2024-03-20", [first])

    assert first.id == 1
    assert second.id == 2
    assert second.description == "Second"
    assert second.priority == models.Priority.MEDIUM
    assert second.due == date(2024, 3, 20)


def test_create_task_validates_priority_and_due():
    with pytest.raises(models.ValidationError):
        models.create_task("bad", "urgent", None, [])

    with pytest.raises(models.ValidationError):
        models.create_task("bad date", None, "2024-31-01", [])


def test_mark_task_complete_sets_timestamp_and_guard():
    task = build_task("hello", task_id=1)
    models.mark_task_complete(task)
    assert task.completed
    assert task.completed_at is not None

    with pytest.raises(models.TaskAlreadyCompletedError):
        models.mark_task_complete(task)


def test_filter_and_sort_helpers():
    tasks = [
        build_task("low", 1),
        build_task("done", 2, completed=True),
        build_task("mid", 3),
    ]
    tasks[0].priority = models.Priority.LOW
    tasks[2].priority = models.Priority.HIGH
    pending = models.filter_tasks(tasks, "pending")
    assert [task.id for task in pending] == [1, 3]

    completed = models.filter_tasks(tasks, "completed")
    assert [task.id for task in completed] == [2]

    sorted_by_priority = models.sort_tasks(tasks, "priority")
    assert [task.id for task in sorted_by_priority][:2] == [3, 2]


def test_delete_task_returns_removed_and_remaining():
    tasks = [build_task("one", 1), build_task("two", 2)]
    deleted, remaining = models.delete_task(tasks, 1)
    assert deleted.description == "one"
    assert [task.id for task in remaining] == [2]
