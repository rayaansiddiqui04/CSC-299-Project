# tasks1 — Minimal JSON Task CLI (CSC 299 / TaskTracker AI Phase 1)

Prototype command-line task tracker that stores tasks in a JSON file.  
This is the foundation for **TaskTracker AI**, a Python-based productivity app that will later include
AI-assisted task recommendations and scheduling logic.

---

## 📁 Files

- `cli.py` — the single-file Python CLI  
- `tasks.json` — created automatically next to `cli.py` after your first command  
- `.gitignore` — ignores virtualenvs, `__pycache__`, and the data file  

---

## 🚀 Quick Start

Run these commands inside the `tasks1` directory:

```bash
cd tasks1
python3 cli.py add "Finish homework" -p 2
python3 cli.py add "Email TA about office hours"
python3 cli.py list                 # show todo by default
python3 cli.py list --done          # show completed tasks
python3 cli.py list --todo          # show only incomplete tasks
python3 cli.py search home          # search tasks by keyword
python3 cli.py done 1               # mark task #1 done
python3 cli.py list                 # confirm it’s marked complete