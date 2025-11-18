# TaskTracker AI – Tasks 2

### Overview
**TaskTracker AI (Tasks 2)** is a command-line task manager built in Python for CSC 299.  
It stores tasks in a JSON file and supports adding, listing, searching, marking done, and exporting tasks — all from your terminal.  
This version expands on *Tasks 1* with filters, subtasks, tags, projects, due-dates, and a smart “suggest” command.

---

### 🚀 Features
- Add tasks with **priority**, **due date**, **tags**, and **project**
- Update or mark tasks **done**
- Filter tasks by **status**, **tags**, or **due date**
- **Search** titles and notes
- **Suggest** top 3 next tasks based on urgency
- Display tasks in **table** or **kanban** view
- **Export** tasks to `.json` or `.md`
- Data automatically saved in `tasks.json`

---

### ⚙️ Installation & Setup
```bash
cd ~/Desktop/CSC-299-Project/tasks2
python3 --version   # should show Python 3.10+
[ -f tasks.json ] || echo "[]" > tasks.json
