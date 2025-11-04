#!/usr/bin/env python3
import json, os
from datetime import datetime
from typing import List, Dict, Any

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")
ISO = "%Y-%m-%dT%H:%M:%S"

def now_iso() -> str:
    return datetime.now().strftime(ISO)

def _read_raw() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

def _write_raw(tasks: List[Dict[str, Any]]) -> None:
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)
    os.replace(tmp, DATA_FILE)

def parse_tags(s: str | None) -> list[str]:
    if not s:
        return []
    s = s.replace("|", ",")
    parts = [p.strip().lower() for p in s.split(",") if p.strip()]
    dedup, seen = [], set()
    for p in parts:
        if p not in seen:
            dedup.append(p); seen.add(p)
    return dedup

def normalize_task(t: Dict[str, Any]) -> Dict[str, Any]:
    t.setdefault("priority", 3)
    if "done" in t and "status" not in t:
        t["status"] = "done" if t["done"] else "todo"
        t.pop("done", None)
    t.setdefault("status", "todo")
    t.setdefault("due", None)
    t.setdefault("tags", [])
    t.setdefault("project", None)
    t.setdefault("note", "")
    t.setdefault("subtasks", [])
    t.setdefault("created_at", now_iso())
    t.setdefault("updated_at", now_iso())
    return t

def migrate_all(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_task(dict(t)) for t in tasks]

def load_tasks() -> List[Dict[str, Any]]:
    return migrate_all(_read_raw())

def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    _write_raw(tasks)

def next_id(tasks: List[Dict[str, Any]]) -> int:
    return (max((t.get("id", 0) for t in tasks), default=0) + 1)