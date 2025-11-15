from __future__ import annotations

import argparse
import sys
from typing import Iterable, List, Sequence

from app import models
from app.models import (
    Task,
    TaskAlreadyCompletedError,
    TaskNotFoundError,
    ValidationError,
    create_task,
    filter_tasks,
    mark_task_complete,
    sort_tasks,
)
from storage import TaskStorage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tasker", description="JSON-backed command-line task manager"
    )
    parser.add_argument(
        "--data",
        dest="data_path",
        help="Path to task file (overrides TASK_FILE env var)",
    )
    parser.add_argument(
        "--color",
        action="store_true",
        help="Use ANSI colors in table output (default off)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes for complete/delete without writing",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument(
        "--priority",
        choices=[priority.value for priority in models.Priority],
        help="Task priority (default medium)",
    )
    add_parser.add_argument(
        "--due",
        help="Due date in YYYY-MM-DD format",
    )

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "--all",
        action="store_true",
        help="Show pending and completed tasks",
    )
    list_parser.add_argument(
        "--completed",
        action="store_true",
        help="Show only completed tasks",
    )
    list_parser.add_argument(
        "--pending",
        action="store_true",
        help="Show only pending tasks",
    )
    list_parser.add_argument(
        "--sort",
        choices=["priority", "due"],
        help="Sort tasks (default: creation time)",
    )

    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("task_id", type=int, help="ID to mark complete")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID to delete")
    delete_parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt (useful for scripts)",
    )
    return parser


def _status_char(task: Task) -> str:
    return "[x]" if task.completed else "[ ]"


def _colorize(value: str, color: str, use_color: bool) -> str:
    if not use_color:
        return value
    codes = {"green": "\033[32m", "red": "\033[31m", "reset": "\033[0m"}
    return f"{codes[color]}{value}{codes['reset']}"


def render_table(tasks: Sequence[Task], use_color: bool = False) -> str:
    headers = ["ID", "Status", "Priority", "Due", "Description"]
    rows: List[List[str]] = []
    for task in tasks:
        status = _status_char(task)
        if task.completed:
            status = _colorize(status, "green", use_color)
        else:
            status = _colorize(status, "red", use_color)
        rows.append(
            [
                str(task.id),
                status,
                task.priority.value,
                task.due.isoformat() if task.due else "-",
                task.description,
            ]
        )
    widths = [len(header) for header in headers]
    for row in rows:
        for idx, value in enumerate(row):
            widths[idx] = max(widths[idx], len(value))

    def format_row(row: Sequence[str]) -> str:
        padded = [
            value.ljust(widths[idx]) if idx != len(row) - 1 else value
            for idx, value in enumerate(row)
        ]
        return "  ".join(padded)

    output_lines = [format_row(headers)]
    output_lines.append(format_row(["-" * width for width in widths]))
    output_lines.extend(format_row(row) for row in rows)
    return "\n".join(output_lines)


def determine_view(args: argparse.Namespace) -> str:
    selected = [args.all, args.completed, args.pending]
    if sum(bool(flag) for flag in selected) > 1:
        raise ValidationError("Choose at most one of --all/--completed/--pending.")
    if args.completed:
        return "completed"
    if args.all:
        return "all"
    return "pending"


def handle_add(args: argparse.Namespace, storage: TaskStorage) -> None:
    tasks = storage.load_tasks()
    new_task = create_task(args.description, args.priority, args.due, tasks)
    tasks.append(new_task)
    storage.save_tasks(tasks)
    print(f"Added task {new_task.id}: {new_task.description}")


def handle_list(args: argparse.Namespace, storage: TaskStorage) -> None:
    tasks = storage.load_tasks()
    if not tasks:
        print("No tasks stored.")
        return
    view = determine_view(args)
    filtered = filter_tasks(tasks, view)
    if not filtered:
        print("No tasks found for the selected filter.")
        return
    ordered = sort_tasks(filtered, args.sort)
    print(render_table(ordered, use_color=args.color))


def handle_complete(args: argparse.Namespace, storage: TaskStorage) -> None:
    tasks = storage.load_tasks()
    task = models.find_task(tasks, args.task_id)
    mark_task_complete(task)
    if args.dry_run:
        print(f"[dry-run] Would complete task {task.id}: {task.description}")
        return
    storage.save_tasks(tasks)
    print(f"Completed task {task.id}.")


def handle_delete(args: argparse.Namespace, storage: TaskStorage) -> None:
    tasks = storage.load_tasks()
    task, updated = models.delete_task(tasks, args.task_id)
    if args.dry_run:
        print(f"[dry-run] Would delete task {task.id}: {task.description}")
        return
    if not args.force and sys.stdin.isatty():
        answer = input(f"Delete task {task.id} \"{task.description}\"? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Aborted.")
            return
    storage.save_tasks(updated)
    print(f"Deleted task {task.id}.")


def dispatch(args: argparse.Namespace, storage: TaskStorage) -> None:
    if args.command == "add":
        handle_add(args, storage)
    elif args.command == "list":
        handle_list(args, storage)
    elif args.command == "complete":
        handle_complete(args, storage)
    elif args.command == "delete":
        handle_delete(args, storage)
    else:
        raise ValidationError(f"Unknown command {args.command}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    storage = TaskStorage(args.data_path)
    try:
        dispatch(args, storage)
        return 0
    except (ValidationError, TaskNotFoundError, TaskAlreadyCompletedError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
