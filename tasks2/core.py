#!/usr/bin/env python3
import re, json
from typing import List, Dict, Any, Callable
from pathlib import Path
from storage import load_tasks, save_tasks, next_id, now_iso, parse_tags

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# -------- helpers --------
def _cmp_key(sort: str) -> Callable[[Dict[str, Any]], Any]:
    if sort == "due":
        return lambda t: (t.get("due") or "9999-12-31", t.get("priority", 3), t.get("id", 0))
    if sort == "updated":
        return lambda t: t.get("updated_at") or ""
    if sort == "created":
        return lambda t: t.get("created_at") or ""
    return lambda t: (t.get("priority", 3), t.get("due") or "9999-12-31", t.get("id", 0))

def _passes(t: Dict[str, Any], *, status=None, tags=None, project=None, before=None, after=None) -> bool:
    ok = True
    if status:
        ok &= (t.get("status") == status)
    if project:
        ok &= (t.get("project") == project)
    if tags:
        for tag in tags or []:
            if tag.lower() not in (t.get("tags") or []):
                return False
    if before:
        ok &= bool(t.get("due") and t["due"] <= before)
    if after:
        ok &= bool(t.get("due") and t["due"] >= after)
    return ok

# -------- CRUD --------
def add_task(title: str, priority: int = 3, *, due: str | None = None, tags: str | None = None,
             project: str | None = None, note: str | None = None, sub: str | None = None) -> Dict[str, Any]:
    tasks = load_tasks()
    if priority < 1 or priority > 5:
        raise SystemExit("priority must be 1..5")
    if due and not DATE_RE.match(due):
        raise SystemExit("--due must be YYYY-MM-DD")
    new = {
        "id": next_id(tasks),
        "title": title,
        "priority": priority,
        "status": "todo",
        "due": due,
        "tags": parse_tags(tags),
        "project": project,
        "note": note or "",
        "subtasks": [{"title": s.strip(), "done": False} for s in (sub or "").split("|") if s.strip()],
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    tasks.append(new)
    save_tasks(tasks)
    return new

def set_task(tid: int, **updates) -> Dict[str, Any]:
    tasks = load_tasks()
    t = next((x for x in tasks if x.get("id") == tid), None)
    if not t:
        raise SystemExit(f"Task {tid} not found")

    if "priority" in updates and updates["priority"] is not None:
        p = int(updates["priority"])
        if p < 1 or p > 5:
            raise SystemExit("priority must be 1..5")
        t["priority"] = p

    if "status" in updates and updates["status"] is not None:
        if updates["status"] not in {"todo","doing","done"}:
            raise SystemExit("status must be todo|doing|done")
        t["status"] = updates["status"]

    if "due" in updates and updates["due"] is not None:
        if updates["due"] and not DATE_RE.match(updates["due"]):
            raise SystemExit("--due must be YYYY-MM-DD")
        t["due"] = updates["due"]

    if "title" in updates and updates["title"] is not None:
        t["title"] = updates["title"]

    if "tags" in updates and updates["tags"] is not None:
        t["tags"] = parse_tags(updates["tags"]) if isinstance(updates["tags"], str) else (updates["tags"] or [])

    if "project" in updates and updates["project"] is not None:
        t["project"] = updates["project"]

    if "note" in updates and updates["note"] is not None:
        t["note"] = updates["note"]

    if "sub" in updates and updates["sub"] is not None:
        subs = [s.strip() for s in (updates["sub"] or "").split("|") if s.strip()]
        t["subtasks"] = [{"title": s, "done": False} for s in subs]

    t["updated_at"] = now_iso()
    save_tasks(tasks)
    return t

def mark_done(tid: int) -> Dict[str, Any]:
    return set_task(tid, status="done")

# -------- views --------
def list_tasks(*, status=None, tags=None, project=None, before=None, after=None, sort="priority") -> List[Dict[str, Any]]:
    tasks = load_tasks()
    rows = [t for t in tasks if _passes(t, status=status, tags=tags, project=project, before=before, after=after)]
    rows.sort(key=_cmp_key(sort))
    return rows

def render_table(rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return "(no tasks)"
    header = ["ID","p","status","due","project","title","[tags]"]
    lines = [f"{header[0]:>3}  {header[1]:<1}  {header[2]:<6}  {header[3]:<10}  {header[4]:<12}  {header[5]}  {header[6]}"]
    lines.append("-"*80)
    for t in rows:
        tags = ",".join(t.get("tags") or [])
        due = t.get("due") or ""
        lines.append(f"{t['id']:>3}  {t['priority']:<1}  {t['status']:<6}  {due:<10}  {(t.get('project') or ''):<12}  {t['title']}  [{tags}]")
    return "\n".join(lines)

def render_kanban(rows: List[Dict[str, Any]]) -> str:
    cols = {"todo": [], "doing": [], "done": []}
    for t in rows:
        cols.get(t.get("status","todo"), cols["todo"]).append(t)
    out = []
    for col in ("todo","doing","done"):
        out.append(col.upper() + ":")
        for t in cols[col]:
            due = t.get("due") or "—"
            out.append(f"  • #{t['id']} (p={t['priority']}, due={due}) {t['title']}")
        out.append("")
    return "\n".join(out).rstrip()

# -------- search & suggest --------
def search_tasks(q: str) -> List[Dict[str, Any]]:
    q = (q or "").lower()
    return [t for t in load_tasks() if q in t.get("title","").lower() or q in (t.get("note") or "").lower()]

def suggest_top3() -> List[Dict[str, Any]]:
    rows = [t for t in load_tasks() if t.get("status") != "done"]
    def score(t: Dict[str, Any]):
        due = t.get("due") or "9999-12-31"
        urgent_tag = any(x in (t.get("tags") or []) for x in ["urgent","school"])
        return (due, t.get("priority", 3), 0 if urgent_tag else 1)
    rows.sort(key=score)
    return rows[:3]

# -------- export --------
def export_json(path: str) -> None:
    Path(path).write_text(json.dumps(load_tasks(), indent=2), encoding="utf-8")

def export_md(path: str) -> None:
    tasks = list_tasks(sort="due")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Tasks Export\n\n")
        for t in tasks:
            box = "x" if t.get("status") == "done" else " "
            tags = f" (tags: {','.join(t.get('tags') or [])})" if t.get('tags') else ""
            due  = f", due {t['due']}" if t.get('due') else ""
            proj = f" [{t['project']}]" if t.get('project') else ""
            f.write(f"- [{box}] {t['title']}{proj} (p={t['priority']}{due}){tags}\n")