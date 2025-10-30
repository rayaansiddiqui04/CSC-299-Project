#!/usr/bin/env python3
"""
Minimal JSON Task CLI (single file)

Stores tasks in a JSON file next to this script (tasks.json).
Commands:
  add "TITLE" [-p PRIORITY]        Add a new task
  list [--done | --todo]           List tasks (default: todo)
  search "QUERY"                   Search tasks by title substring
  done ID                          Mark a task as done by ID

Examples:
  python3 cli.py add "Finish homework" -p 2
  python3 cli.py list
  python3 cli.py search home
  python3 cli.py done 1
"""

from __future__ import annotations
import argparse
import json
import os
from typing import List, Dict, Any

# --- Always save/load tasks.json next to this file (not CWD) ---
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(HERE, "tasks.json")


def load_tasks() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Corrupt file: back it up and start fresh
        backup = DATA_FILE + ".bak"
        try:
            os.replace(DATA_FILE, backup)
            print(f"[!] tasks.json was corrupt. Backed up to {os.path.basename(backup)} and started fresh.")
        except OSError:
            print("[!] tasks.json was corrupt and could not be backed up. Starting fresh.")
        return []


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    os.replace(tmp, DATA_FILE)


def next_id(tasks: List[Dict[str, Any]]) -> int:
    return (max((t.get("id", 0) for t in tasks), default=0) + 1) if tasks else 1


def cmd_add(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "title": args.title.strip(),
        "priority": args.priority,
        "done": False,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added #{task['id']}: {task['title']} (p={task['priority']})")


def format_task(t: Dict[str, Any]) -> str:
    box = "✔" if t.get("done") else "·"
    return f"{t['id']:>3} {box}  [p{t.get('priority', 3)}] {t['title']}"


def cmd_list(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    if not tasks:
        print("(no tasks yet)")
        return

    view = tasks
    if args.todo:
        view = [t for t in tasks if not t.get("done")]
    elif args.done:
        view = [t for t in tasks if t.get("done")]

    for t in view:
        print(format_task(t))


def cmd_search(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    q = args.query.lower()
    matches = [t for t in tasks if q in t["title"].lower()]
    if not matches:
        print("(no matches)")
        return
    for t in matches:
        print(format_task(t))


def cmd_done(args: argparse.Namespace) -> None:
    tasks = load_tasks()
    for t in tasks:
        if t.get("id") == args.id:
            t["done"] = True
            save_tasks(tasks)
            print(f"Marked #{args.id} done.")
            return
    print(f"Task #{args.id} not found.")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="JSON Task CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    addp = sub.add_parser("add", help="add a new task")
    addp.add_argument("title", help='task title in quotes')
    addp.add_argument("-p", "--priority", type=int, default=3, help="1 (high) .. 5 (low), default 3")
    addp.set_defaults(func=cmd_add)

    listp = sub.add_parser("list", help="list tasks")
    g = listp.add_mutually_exclusive_group()
    g.add_argument("--done", action="store_true", help="show only completed tasks")
    g.add_argument("--todo", action="store_true", help="show only incomplete tasks (default)")
    listp.set_defaults(func=cmd_list, todo=True)

    searchp = sub.add_parser("search", help="search tasks")
    searchp.add_argument("query", help="substring to look for (case-insensitive)")
    searchp.set_defaults(func=cmd_search)

    donep = sub.add_parser("done", help="mark task done by ID")
    donep.add_argument("id", type=int)
    donep.set_defaults(func=cmd_done)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()