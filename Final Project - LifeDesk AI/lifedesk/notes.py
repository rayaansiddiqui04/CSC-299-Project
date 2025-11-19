from typing import List, Dict, Any, Optional
from .storage import load_state, save_state


def add_note(
    title: str,
    body: str,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Create a new note, save it, and return it."""
    state = load_state()
    note_id = state.get("next_note_id", 1)

    note = {
        "id": note_id,
        "title": title,
        "body": body,
        "tags": tags or [],
    }

    state["notes"].append(note)
    state["next_note_id"] = note_id + 1
    save_state(state)
    return note


def list_notes() -> List[Dict[str, Any]]:
    """Return all notes."""
    state = load_state()
    return state.get("notes", [])


def search_notes(keyword: str) -> List[Dict[str, Any]]:
    """
    Return notes where the keyword appears in title, body, or tags.
    """
    keyword_lower = keyword.lower()
    return [
        n for n in list_notes()
        if keyword_lower in n["title"].lower()
        or keyword_lower in n["body"].lower()
        or any(keyword_lower in tag.lower() for tag in n.get("tags", []))
    ]