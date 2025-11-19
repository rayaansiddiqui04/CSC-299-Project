import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
STATE_FILE = DATA_DIR / "lifedesk_state.json"

def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_state() -> Dict[str, Any]:
    _ensure_data_dir()
    if not STATE_FILE.exists():
        return {
            "tasks": [],
            "notes": [],
            "next_task_id": 1,
            "next_note_id": 1,
        }
    with STATE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state: Dict[str, Any]) -> None:
    _ensure_data_dir()
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)