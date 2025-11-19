import argparse
from typing import List

from . import tasks, notes, agents


def _print_task(t) -> None:
    print(
        f"[{t['id']}] {t['title']}  "
        f"(status={t['status']}, priority={t['priority']}, "
        f"due={t.get('due_date')}, tags={','.join(t.get('tags', []))})"
    )
    if t.get("notes"):
        print(f"    notes: {t['notes']}")


def _print_note(n) -> None:
    print(f"[{n['id']}] {n['title']}  (tags={','.join(n.get('tags', []))})")
    for line in n["body"].splitlines():
        print(f"    {line}")


def handle_tasks(args: argparse.Namespace) -> None:
    if args.action == "add":
        tag_list: List[str] = args.tags.split(",") if args.tags else []
        t = tasks.add_task(
            title=args.title,
            priority=args.priority,
            due_date=args.due,
            tags=tag_list,
            notes=args.notes,
        )
        print("Created task:")
        _print_task(t)

    elif args.action == "list":
        for t in tasks.list_tasks(status=args.status):
            _print_task(t)

    elif args.action == "done":
        t = tasks.complete_task(args.id)
        if t:
            print("Marked as done:")
            _print_task(t)
        else:
            print(f"No task found with id {args.id}")


def handle_notes(args: argparse.Namespace) -> None:
    if args.action == "add":
        tag_list: List[str] = args.tags.split(",") if args.tags else []
        n = notes.add_note(
            title=args.title,
            body=args.body,
            tags=tag_list,
        )
        print("Created note:")
        _print_note(n)

    elif args.action == "list":
        for n in notes.list_notes():
            _print_note(n)

    elif args.action == "search":
        for n in notes.search_notes(args.keyword):
            _print_note(n)


def handle_chat(args: argparse.Namespace) -> None:
    if args.mode == "tasks":
        print(agents.agent_suggest_next_tasks())
    elif args.mode == "notes":
        answer = agents.agent_answer_question_about_notes(args.question)
        print(answer)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lifedesk",
        description="LifeDesk AI – terminal knowledge + task manager with AI help.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- tasks ----
    p_tasks = subparsers.add_parser("tasks", help="Manage tasks")
    tasks_sub = p_tasks.add_subparsers(dest="action", required=True)

    p_add = tasks_sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title")
    p_add.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    p_add.add_argument("--due", help="Due date as YYYY-MM-DD")
    p_add.add_argument("--tags", help="Comma-separated list of tags")
    p_add.add_argument("--notes", help="Extra notes for this task", default="")
    p_add.set_defaults(func=handle_tasks)

    p_list = tasks_sub.add_parser("list", help="List tasks")
    p_list.add_argument("--status", choices=["todo", "done"], help="Filter by status")
    p_list.set_defaults(func=handle_tasks)

    p_done = tasks_sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("id", type=int)
    p_done.set_defaults(func=handle_tasks)

    # ---- notes ----
    p_notes = subparsers.add_parser("notes", help="Manage knowledge notes")
    notes_sub = p_notes.add_subparsers(dest="action", required=True)

    p_n_add = notes_sub.add_parser("add", help="Add a new note")
    p_n_add.add_argument("title")
    p_n_add.add_argument("body")
    p_n_add.add_argument("--tags", help="Comma-separated list of tags")
    p_n_add.set_defaults(func=handle_notes)

    p_n_list = notes_sub.add_parser("list", help="List notes")
    p_n_list.set_defaults(func=handle_notes)

    p_n_search = notes_sub.add_parser("search", help="Search notes")
    p_n_search.add_argument("keyword")
    p_n_search.set_defaults(func=handle_notes)

    # ---- chat ----
    p_chat = subparsers.add_parser("chat", help="Talk to AI agents")
    p_chat.add_argument(
        "mode",
        choices=["tasks", "notes"],
    )
    p_chat.add_argument(
        "--question",
        help="(Required for 'chat notes') Question about your notes",
    )
    p_chat.set_defaults(func=handle_chat)

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "chat" and args.mode == "notes" and not args.question:
        parser.error("When using 'chat notes', you must pass --question.")

    args.func(args)


if __name__ == "__main__":
    main()