📘 LifeDesk AI – Final Project (CSC 299)

LifeDesk AI is a cross-platform Python application that integrates:
	•	A Personal Knowledge Management System (PKMS)
	•	A Personal Task Management System
	•	A Terminal-Based Chat Interface for interacting with your stored knowledge and tasks
	•	AI Agents that analyze your tasks or notes and provide intelligent suggestions or answers
	•	A persistent JSON-based data store that works on macOS, Linux, and Windows

This project was planned, developed, and tested using AI coding assistants, demonstrating modern AI-assisted software engineering workflows.

⸻

⭐ Features

📄 Personal Knowledge Management System (PKMS)
	•	Add, list, and search notes
	•	Tag notes (e.g., “philosophy”, “exam”, “cs”)
	•	Store structured knowledge in JSON
	•	AI Note Agent answers questions using your notes

📝 Task Management System
	•	Add tasks with priority, due dates, tags, and notes
	•	Mark tasks as done
	•	Filter tasks by status (todo, done)
	•	View full task metadata
	•	AI Task Agent recommends the top tasks to focus on next

💬 Terminal Chat Interface
	•	Interact with AI agents from the CLI
	•	Ask questions about your notes
	•	Request task prioritization
	•	Works offline (local heuristic mode)
	•	Works online if an OpenAI API key is provided

🤖 AI Agents

Two intelligent agents included:

✔ Task Suggestion Agent
Analyzes:
	•	Priority
	•	Due date
	•	Tags
	•	Status

…and recommends the next tasks to complete.

✔ Notes Question-Answering Agent
Searches your notes and returns the most relevant entries, optionally using OpenAI if available.

💾 JSON Storage

All data is stored inside:
data/lifedesk_state.json

This includes:
	•	tasks
	•	notes
	•	incremental IDs


🗂 Project Structure
lifedesk/
    cli.py        ← command-line interface
    storage.py    ← JSON persistence layer
    tasks.py      ← task manager logic
    notes.py      ← PKMS logic
    agents.py     ← AI agents
data/
    lifedesk_state.json
requirements.txt
README.md
🏗 Installation
1. Create a virtual environment
python3 -m venv .venv
2. Activate it

 macOS / Linux:
 source .venv/bin/activate

 Windows:
 .venv\Scripts\Activate.ps1
 3. Install dependencies
 pip install -r requirements.txt

🚀 Usage

Check available commands
python3 -m lifedesk.cli --help
📝 Notes (PKMS)

Add a note
python3 -m lifedesk.cli notes add "Plato Book 10" "Soul immortal..." --tags philosophy,exam

List notes
python3 -m lifedesk.cli notes list

Search notes
python3 -m lifedesk.cli notes search exam

📌 Tasks

Add a task
python3 -m lifedesk.cli tasks add "Study for CSC 300" --priority high --due 2025-11-25 --tags school,exam --notes "Heaps and PQ"

List tasks
python3 -m lifedesk.cli tasks list

Mark done
python3 -m lifedesk.cli tasks done 1

Filter
python3 -m lifedesk.cli tasks list --status todo
python3 -m lifedesk.cli tasks list --status done

🤖 AI Chat Interface

Task recommendations
python3 -m lifedesk.cli chat tasks

Notes Q&A
python3 -m lifedesk.cli chat notes --question "What should I study for Plato?"

Heaps example
python3 -m lifedesk.cli chat notes --question "Explain heaps to me"

🌐 Optional: OpenAI Integration

Install library:
pip install openai


Set API key:
export OPENAI_API_KEY="your_key_here"

If no key is provided:
	•	AI runs in local mode
	•	No errors
	•	No internet required

🧠 AI Coding Assistant Usage

LifeDesk AI was created through an iterative workflow using AI to:
	•	Plan architecture
	•	Generate module code
	•	Debug errors
	•	Design CLI commands
	•	Implement agents
	•	Test features
	•	Verify requirements


🛠 Future Improvements
	•	SQLite or Neo4J backend
	•	Natural-language task creation
	•	More advanced reasoning agents
	•	Reminders and notifications
	•	Web or TUI interface


🏁 Conclusion

LifeDesk AI fully satisfies the CSC-299 Final Project requirements:

✔ PKMS
✔ Task Manager
✔ Chat Interface
✔ AI Agents
✔ JSON State Persistence
✔ Python + Portable
✔ Developed with AI Coding Assistants




















