#!/usr/bin/env python3
import argparse, sys
from tasks3.core import (
    add_task, set_task, mark_done,
    list_tasks, render_table, render_kanban,
    search_tasks, suggest_top3,
    export_json, export_md,
)

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tasks3", description="tasks3 CLI")
    sub = p.add_subparsers(dest="cmd")
    # If user runs with no subcommand, print help instead of erroring
    p.set_defaults(func=lambda _args: p.print_help())

    a = sub.add_parser("add", help="add a new task")
    a.add_argument("title")
    a.add_argument("-p", "--priority", type=int, default=3)
    a.add_argument("--due")
    a.add_argument("--tags")
    a.add_argument("--project")
    a.add_argument("--note")
    a.add_argument("--sub", help='Subtasks separated by "|"')
    a.set_defaults(func=lambda args: _print_added(
        add_task(**{k: v for k, v in vars(args).items() if k not in {"cmd", "func"}})
    ))

    l = sub.add_parser("list", help="list tasks with filters")
    l.add_argument("--status", choices=["todo", "doing", "done"])
    l.add_argument("--tag", action="append")
    l.add_argument("--project")
    l.add_argument("--before")
    l.add_argument("--after")
    l.add_argument("--sort", choices=["priority", "due", "updated", "created"], default="priority")
    l.add_argument("--kanban", action="store_true")
    def _list(args):
        rows = list_tasks(
            status=args.status,
            tags=args.tag,
            project=args.project,
            before=args.before,
            after=args.after,
            sort=args.sort
        )
        print(render_kanban(rows) if args.kanban else render_table(rows))
    l.set_defaults(func=_list)

    s = sub.add_parser("set", help="update fields of a task")
    s.add_argument("id", type=int)
    s.add_argument("--title")
    s.add_argument("--priority", type=int)
    s.add_argument("--status", choices=["todo", "doing", "done"])
    s.add_argument("--due")
    s.add_argument("--tags")
    s.add_argument("--project")
    s.add_argument("--note")
    s.add_argument("--sub", help='Reset subtasks with "|" list')
    s.set_defaults(func=lambda args: _print_updated(
        set_task(args.id, **{k: v for k, v in vars(args).items() if k not in {"id", "cmd", "func"}})
    ))

    d = sub.add_parser("done", help="mark a task done")
    d.add_argument("id", type=int)
    d.set_defaults(func=lambda args: _print_updated(mark_done(args.id)))

    f = sub.add_parser("search", help="search title or note")
    f.add_argument("query")
    f.set_defaults(func=lambda args: _print_search(search_tasks(args.query)))

    g = sub.add_parser("suggest", help="show Top 3 suggestions")
    def _suggest(_):
        picks = suggest_top3()
        if not picks:
            print("No suggestions."); return
        print("Top 3 suggestions:")
        for t in picks:
            print(f"- #{t['id']}  {t['title']}  (p={t['priority']}, due={t.get('due') or '—'}, tags={','.join(t.get('tags') or [])})")
    g.set_defaults(func=_suggest)

    e = sub.add_parser("export", help="export tasks to .json or .md")
    e.add_argument("path")
    def _export(args):
        if args.path.endswith(".json"):
            export_json(args.path)
        elif args.path.endswith(".md"):
            export_md(args.path)
        else:
            print("Export path must end with .json or .md"); sys.exit(1)
        print(f"Exported → {args.path}")
    e.set_defaults(func=_export)

    return p

def _print_added(t):
    print(f"Added #{t['id']}: {t['title']} (p={t['priority']})")

def _print_updated(t):
    print(f"Updated #{t['id']}: {t['title']} (status={t['status']}, p={t['priority']})")

def _print_search(rows):
    if not rows:
        print("(no matches)"); return
    for t in rows:
        print(f"{t['id']:>3}  {t['title']}")

def main():
    args = build_parser().parse_args()
    args.func(args)

if __name__ == "__main__":
    main()