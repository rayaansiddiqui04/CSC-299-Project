# TaskTracker AI – Tasks 4  

### Overview  
**TaskTracker AI (Tasks 4)** adds AI-powered summarization to your CSC 299 project.  
This version uses the **OpenAI Chat Completions API** to take multiple paragraph-length task descriptions, summarize each one into a short phrase, and print the summaries in your terminal.  
It demonstrates looping over multiple API calls, managing environment variables, and integrating external APIs into a Python CLI project.

---

### 🚀 Features  
- Sends **paragraph-length descriptions** to the **OpenAI ChatGPT-5-mini** model  
- Prints **short, clear summaries** for each description  
- Processes **multiple descriptions independently** in a loop  
- Reads your **API key** securely from an environment variable or `.env` file  
- Organized modular code for clean testing and readability  

---

### ⚙️ Installation & Setup  
```bash
cd ~/Desktop/CSC-299-Project/tasks4
python3 --version    # should show Python 3.10+ or 3.11+
uv sync              # install dependencies (openai, dotenv, etc.)