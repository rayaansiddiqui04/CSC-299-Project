from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.models import Priority, Task
from storage import TaskStorage


def make_task(task_id: int) -> Task:
    return Task(
        id=task_id,
        description=f"Task {task_id}",
        created_at=datetime.now(timezone.utc),
        priority=Priority.MEDIUM,
    )


def test_load_missing_file_returns_empty(tmp_path: Path):
    storage = TaskStorage(tmp_path / "missing.json")
    assert storage.load_tasks() == []


def test_save_and_load_round_trip(tmp_path: Path):
    target = tmp_path / "tasks.json"
    storage = TaskStorage(target)
    task = make_task(1)
    task.due = datetime(2024, 3, 20, tzinfo=timezone.utc).date()
    storage.save_tasks([task])

    loaded = storage.load_tasks()
    assert len(loaded) == 1
    assert loaded[0].description == "Task 1"
    assert loaded[0].due.isoformat() == "2024-03-20"
    assert target.exists()


def test_corrupt_file_raises(tmp_path: Path):
    target = tmp_path / "tasks.json"
    target.write_text("{}")
    storage = TaskStorage(target)
    with pytest.raises(ValueError):
        storage.load_tasks()
