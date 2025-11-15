from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import List, Sequence

from app.models import Task, payload_to_tasks, tasks_to_payload


def _default_data_path() -> Path:
    env_override = os.environ.get("TASK_FILE")
    if env_override:
        return Path(env_override).expanduser()
    return Path.home() / ".tasks.json"


class TaskStorage:
    """JSON persistence with atomic writes."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = self._resolve_path(path)

    @staticmethod
    def _resolve_path(value: str | Path | None) -> Path:
        if value:
            return Path(value).expanduser()
        return _default_data_path()

    def load_tasks(self) -> List[Task]:
        if not self.path.exists():
            return []
        raw = self.path.read_text().strip()
        if not raw:
            return []
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("Task file is corrupt; expected a list.")
        return payload_to_tasks(data)

    def save_tasks(self, tasks: Sequence[Task]) -> None:
        payload = tasks_to_payload(tasks)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(payload, indent=2)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self.path.parent,
            delete=False,
        ) as tmp_file:
            tmp_file.write(serialized)
            temp_name = Path(tmp_file.name)
        temp_name.replace(self.path)
