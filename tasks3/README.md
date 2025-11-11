
### Overview  
**TaskTracker AI (Tasks 3)** continues the development of the TaskTracker CLI app for CSC 299 by turning it into a **Python package** with **automated testing** using `pytest` and environment management with `uv`.  
This version focuses on writing testable code, ensuring functionality through unit tests, and packaging the project so it can be executed with `uv run tasks3`.

---

### 🚀 Features  
- Fully packaged Python module runnable with `uv run tasks3`  
- Add, list, search, and mark tasks **done** using a JSON-based database  
- Includes **pytest** tests to verify key functionality  
- Organized **modular structure** for clean imports and testing  
- Rule-based AI logic suggests which task to do next (based on priority or due date)  
- Easy to extend for future features like reminders or analytics  

---

### ⚙️ Installation & Setup  
```bash
cd ~/Desktop/CSC-299-Project/tasks3
python3 --version    # should show Python 3.10+ or 3.11+
uv sync              # install dependencies (pytest, etc.)