import json
from datetime import datetime
from typing import List, Dict, Any

from .tasks import list_tasks
from .notes import list_notes

# Optional OpenAI support (only used if configured)
try:
    from openai import OpenAI
    _client = OpenAI()
except Exception:
    _client = None


# ---------------------------
# Local (no-OpenAI) heuristics
# ---------------------------

def _priority_weight(priority: str) -> int:
    priority = (priority or "").lower()
    if priority == "high":
        return 3
    if priority == "low":
        return 1
    return 2  # medium or anything else


def _score_task(task: Dict[str, Any]) -> float:
    """
    Compute a simple score for a task:
    - higher for higher priority
    - higher if due soon or overdue
    """
    base = _priority_weight(task.get("priority"))
    due_str = task.get("due_date")
    bonus = 0.0

    if due_str:
        try:
            due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
            today = datetime.today().date()
            days_diff = (due_date - today).days
            # Overdue → big bonus
            if days_diff < 0:
                bonus += 10
            else:
                # Due sooner → higher score, but capped
                bonus += max(0, 30 - days_diff) / 5.0
        except Exception:
            # If date is malformed, ignore date bonus
            pass

    return base * 10 + bonus


def _local_suggest_next_tasks() -> str:
    """
    Local, rule-based suggestion:
    - consider only todo tasks
    - rank by priority and due date
    """
    tasks_list: List[Dict[str, Any]] = list_tasks()
    todo_tasks = [t for t in tasks_list if t.get("status") == "todo"]

    if not todo_tasks:
        return "You have no TODO tasks. Everything is either done or empty."

    ranked = sorted(todo_tasks, key=_score_task, reverse=True)
    top = ranked[:3]

    lines = []
    lines.append("Here are the top tasks to do next (local heuristic, no OpenAI):")
    for t in top:
        reason_bits = []
        prio = (t.get("priority") or "medium").lower()
        reason_bits.append(f"priority={prio}")
        if t.get("due_date"):
            reason_bits.append(f"due={t['due_date']}")
        if t.get("tags"):
            reason_bits.append(f"tags={','.join(t['tags'])}")

        reason = "; ".join(reason_bits)
        lines.append(f"- [#{t['id']}] {t['title']}  ({reason})")

    return "\n".join(lines)


def _local_answer_question_about_notes(question: str) -> str:
    """
    Very simple local Q&A:
    - look for notes that share words with the question
    - return the best matches with their content
    """
    notes_list: List[Dict[str, Any]] = list_notes()
    if not notes_list:
        return "You have no notes yet. Add some notes first."

    q = question.lower()
    # crude tokenization
    q_words = [w for w in q.replace("?", " ").replace(",", " ").split() if len(w) > 2]

    def score_note(n: Dict[str, Any]) -> int:
        text = (n.get("title", "") + " " + n.get("body", " ")).lower()
        tags = " ".join(n.get("tags", [])).lower()
        text_all = text + " " + tags
        return sum(text_all.count(w) for w in q_words)

    scored = [(score_note(n), n) for n in notes_list]
    scored = [pair for pair in scored if pair[0] > 0]

    if not scored:
        return (
            "I looked through your notes but could not find anything that clearly "
            "matches your question. Try adding more detailed notes or using different keywords."
        )

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [n for _, n in scored[:3]]

    lines = []
    lines.append("Here are some notes that seem most relevant to your question:")
    lines.append(f'Question: "{question}"')
    lines.append("")

    for n in top:
        lines.append(f"- [{n['id']}] {n['title']} (tags={','.join(n.get('tags', []))})")
        preview = n["body"].strip().splitlines()[0]
        if len(preview) > 120:
            preview = preview[:117] + "..."
        lines.append(f"    {preview}")
        lines.append("")

    return "\n".join(lines).rstrip()


# ---------------------------
# Optional OpenAI wrapper
# ---------------------------

def _call_openai(system_prompt: str, user_prompt: str) -> str:
    """
    Helper to call the OpenAI Chat Completions API.
    If OpenAI is not available, fall back to local behavior.
    """
    if _client is None:
        # Should never be used directly now; callers decide what to do.
        return (
            "OpenAI client not configured. "
            "Install the 'openai' library and set OPENAI_API_KEY "
            "to enable cloud-based AI features."
        )

    response = _client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content.strip()


# ---------------------------
# Public agent APIs
# ---------------------------

def agent_suggest_next_tasks() -> str:
    """
    Top-level API for suggesting next tasks.
    - If OpenAI is configured, use it.
    - Otherwise, use local heuristic.
    """
    tasks_list: List[Dict[str, Any]] = list_tasks()
    if not tasks_list:
        return "You have no tasks yet. Start by adding a few tasks first."

    # If no OpenAI client, use local heuristic
    if _client is None:
        return _local_suggest_next_tasks()

    tasks_json = json.dumps(tasks_list, indent=2)

    system_prompt = "You are a helpful assistant that prioritizes a student's tasks."
    user_prompt = (
        "Here is my current task list as JSON. "
        "Suggest the top 3 tasks I should do next and explain why, "
        "using bullet points.\n\n"
        f"{tasks_json}"
    )

    return _call_openai(system_prompt, user_prompt)


def agent_answer_question_about_notes(question: str) -> str:
    """
    Top-level API for answering questions about notes.
    - If OpenAI is configured, ask the model.
    - Otherwise, use a local keyword-based search.
    """
    notes_list: List[Dict[str, Any]] = list_notes()
    if not notes_list:
        return "You have no notes yet. Add some notes so I can answer questions about them."

    if _client is None:
        return _local_answer_question_about_notes(question)

    notes_json = json.dumps(notes_list, indent=2)

    system_prompt = (
        "You are a study assistant. Use ONLY the user's notes to answer their question. "
        "If the notes do not contain enough information, say that you are unsure."
    )
    user_prompt = (
        f"Here are my notes as JSON:\n{notes_json}\n\n"
        f"My question is: {question}"
    )

    return _call_openai(system_prompt, user_prompt)