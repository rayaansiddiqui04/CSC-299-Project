# LifeDesk AI – Final Project

LifeDesk AI is a terminal-based **personal knowledge + task management system** with **AI agents** that help you prioritize tasks and study from your own notes.

It is written in **Python**, stores its state in a **JSON file**, and runs on **Windows, macOS, and Linux**.

---

## Features

### ✅ Personal Task Management
- Add tasks with **priority**, **due date**, **tags**, and optional notes
- List tasks (all, or filtered by status)
- Mark tasks as **done**
- Data stored in `data/lifedesk_state.json`

### ✅ Personal Knowledge Management (PKMS)
- Add notes with title, body, and tags
- List all notes
- Search notes by keyword in **title, body, or tags**

### ✅ Terminal-based Chat Interface with AI Agents
- `chat tasks` – Ask an AI agent to analyze your stored tasks and suggest the **top 3 tasks** to do next
- `chat notes` – Ask questions about your stored notes and get answers based on your own knowledge base

If the OpenAI client is not configured, the app still works and prints a helpful message instead of failing.

---

## Installation

You can use any virtual environment tool (e.g. `uv`, `venv`, or `pipenv`).

Example using plain `python` + `pip`:

```bash
cd "final project - Lifedesk AI"

python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

pip install -r requirements.txt