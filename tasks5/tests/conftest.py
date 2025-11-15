from __future__ import annotations

from pathlib import Path
from typing import Callable, Sequence

import pytest

from cli import main
from storage import TaskStorage


@pytest.fixture
def task_file(tmp_path: Path) -> Path:
    return tmp_path / "tasks.json"


@pytest.fixture
def storage(task_file: Path) -> TaskStorage:
    return TaskStorage(task_file)


@pytest.fixture
def cli_runner(task_file: Path) -> Callable[[Sequence[str]], int]:
    def run_cli(args: Sequence[str]) -> int:
        argv = ["--data", str(task_file), *args]
        return main(argv)

    return run_cli
