LifeDesk AI - CSC 299 Final Project

This is what I have been working on all semester, I have decided to call my project LifeDesk AI, becasue it is extremely helpful both in life, and in school. 

"LifeDesk AI" is the final and compelete version of my quarter-long project for CSC 299. This project was designed for mutiple reasons, and made to incorporate many aspects. I integrated mutiple software components to create a personal knowledge system as well as a task managent system. Thus the name "LifeDesk AI"

The final version of my project includes a Personal Knowledge Management System or PKMS, a Task Manager with all tasks I need to due. The task manager also includes add ons such as priority, date, and status. It includes a terminal-based chat interface to edit different sections, and AI-powered agents to provide the user with suggestions and answers. Everything we have built is implemented in Python and stores using JSON files and works across all major platforms such as macOS, Windows, and Linux.

This summary will go into all the details about my process and everything I did to get to the final result

1. Planning
I first started off this project by trying to understand what the requirements were. This is the first time I heard of many of the words and software we used in this project. For example I have never used Git, GitHub, VS Code, and more before. On the other hand trying to understand what a PKMS is, task manager, terminal chatbot, and all the other things required.

So first I used ChatGPT to break down everything for me inclduing designing a PKMS, building a task amanager, adding a terminal chatbot interface, integrating AI agents, JSON storage and making these ideas into an actaul plan and structure.

ChatGPT helped me genrate this following structure for the Final Project

`lifedesk/` package with submodules:
`tasks.py` – task management logic
`notes.py` – Personal Knowledge Managment System (PKMS) logic
`storage.py` – persistence layer
`cli.py` – command-line interface
`agents.py` – intelligent task & notes agents
`data/lifedesk_state.json` – central storage file
This helped me make a blueprint of what is what, and helping creating structure

I relied alot on ChatGPT again to design me the interface of the modules before I actually asking it to write code.
I asked it questions such as:
 What functions should the PKMS have?
 How should tasks be structured in JSON?
What should the CLI commands look like?
How do I implement AI  without an API key?
This helped me a lot and gave me a blueprint and prevenetd trouble down the line

2.
Prototypes
The earlier course assignemnt such as Tasks 1-5 were very helpful, and gave me building blocks for the final project. Each prototype  intourduced a new concept, and expanded my knowledge to give me the best practice for my final project.

Task 1
Task 1 help me intourduce the core workflow of this Python command lien tool that reads and writes to JSOn files, leaning things such as

a single CLI script (cli.py)

a JSON file for persistence

a minimal add / list workflow

So even though this task was very small, it taught me a core fundamental that I would resuse in almost every prototype
Reading JSON -> Modify Python Dict -> Save JSON back

Task 2
Tasks 2 is when we got a little more advances and used the command line into use, here we created things such as
Introduced multiple Python modules (cli.py, core.py, storage.py)
Added filtering logic
Added more structured task dictionaries
Improved JSON handling
Followed a modular project structure
This was a big jump from Tasks 1, and this prototype directly inspireed my storage and tasks file in my final project

Tasks 3
This task was all about testing, pytest, and making sure everything is correct.

It intourduced many vital things such as how important testing is.
How long this took me made me learn how testing and open a huge door, and reveal problems earlier that occured.
Things I learned from doing this prototype include 
How to write basic smoke tests
How to validate JSON output formats
How broken architecture becomes obvious once you start testing
How to formalize expected behaviors

When building my final project I made sure to make each fucntion seperatly then test it to make sure everything is working. The files storage, notes, and tasks in my LifeDesk AI was heavily influenced by this protoype

Task 4
This task was all about AI, and how to integrate it in my workflow

I experimented with TONS of things in this prototype including
A summarization CLI
Using the OpenAI API (gpt-4.1-mini)
Token limits
Error handling
Local fallbacks when API keys are missing

This taught me the MOST out of any other prototype. I was having so many issues, and problem that I learned countless important things. I didnt even know what an OpenAI API was before this, but my knowledge has been expanded.

This prototype taught me things such as
How to call the OpenAI API reliably
How to structure prompts and system messages
How to gracefully degrade when AI is unavailable
How to handle exceptions such as missing API keys
How to add AI generated outputs to command line

This prototype would be the backbone for my agents.py in my final project, however in my final project I added a feature in case the user would not like to use an API key

Task 5
This was the final protoype for my final project and was directly involved with Task Manager Spec-Kit
In this this task I created things such as 
formal specifications
structured planning documents
acceptance criteria
a clearer architectural vision
early tests and behaviors
But it taught me the most important things for my final project, and ultimatly shaped my final projects structure
how to plan software before coding it
how to describe modules and interfaces
how to write a project with clear responsibilities

3.
AI-Coding assistants + tools
The primary model I used throughout this whole project for design and most of coding was GPT-5.1 by OPEN AI,
I used it for the large sum of takss such as
The primary model used throughout development was **ChatGPT using GPT-5.1**. I used it for:

Architectural planning  
Writing entire modules (tasks, notes, storage, CLI, agents)  
Debugging errors and stack traces  
Designing CLI semantics  
Explaining Python concepts when needed  
Helping resolve git merge conflicts  

GPT-5.1 (Codex) was my right hand man throughout this whole project

When relating to Prototype 4, and also in my fianl project I included optional support and feature for OpenAI's API

I used gpt-4.1 mini usign the openai client,
however this only works when a user has an API key that works. This key was used for
task prioritization  
note-based question answering  
However I also do have an option for non API key in my final project which it is defaulted on just to put no pressure on user using this tool.

Claude Code
I also used a bit of Claude Code in the beginning to write me early drafts and modules
It was very helpful to me early on in this project

GitHub Copilot
Copilot imbedded into VS code was also very vital for me. 
This helped me with countless things such as 
completing loops and conditionals  
filling function parameters  
redicting return structures  
auto-generating repetitive code
So Copilot was helpful at small suggestions, but sometimes would give wrong suggestions so I made sure to keep an eye on everything

Back to ChatGPT for specifcation and planning as I said before I engaged in conversation with module 5 and 5.1 extensively for
odule breakdowns  
JSON schemes 
interface design  
flowcharts and logic

Their was alot of debugging the idea that you can just copy and paste and everything will work is wrong. You have to do a lot of debugging, and hold the code assistants hand. I repeatedly asked GPT 5.1 about my errors and issues, and most times it explained errors clearly and gave correct soltions. However in many instances I would have to hold its hand until the end becasue it kept giving wrong directiosn

Testing
I did a tremendous amount of testing for this project and prototype. If their is a bug it is much easier if theirs 1 file than 5, so throughout developemnt I extensively ran commands such as 

Throughout development, I tested the final system constantly by running commands like:

tasks add`  
notes add`  
tasks done`  
tasks list`  
notes search`  
chat tasks`  
chat notes`  

I made sure to veryify:

Data saving correctly in JSON   
Filters working  
Agents working with or without API key  
The chat interface responding logically 

Whenever something failed I would iterate it to Copilot & GPT 5.1 until issue was resolved

What worked well?
1. AI assisted planning

As I mentioned before using GPT-5.1, CoPilot, and Claude code for extensive planning and design was extremely successfully

Details such as 
ChatGPT helped design the folder layout (lifedesk/, storage.py, agents.py, etc.)
Claude Code was excellent at rewriting early drafts to be more modular and clearer
Copilot offered smart autocomplete for repetitive CLI boilerplate
AI discussion let me think aloud through the system design before writing code

Using Mutiple AI approach kept everything clean and structured

2. Modular Design & JSON

Designing everything as four different models or files made everything work flawlessly (tasks.py, notes.py, agents.py, storage.py) 

It gave me so many benefits such as
Debugging became way easier
Each module was testable (inspired by Task 3)
JSON storage kept everything portable across macOS, Windows, and Linux

So this was very helpful and gave me a smooth approach, and since I am reusing JSON from earlier protoypes everything worked to the tea

3. Optional AI worked amazing

What I mean
Why it worked:
If OPENAI_API_KEY is missing → system switches to offline “heuristic mode”
No network dependency
Still demonstrates “AI integration” for the final project requirement
Grading will work even if your professor doesn’t set an API key

So the idea you can use API if you want, made this tool more reliable and user friendly. If user chooses to use API he can, but their is an offline option also

What did not work?
1. GitHub Merge conflicts

When I was pushing the final project I was having issues with merge conflicts, and so many issues with Github I have never seen
Problems included:
conflict markers (<<<<<<< HEAD)
Tasks 2 content merged into the Final Project README
pushing blocked
Git history divergence
This was very confusing, and made me manually solve these conflicts and learn Git

2. Over complicating AI in the beginning

My first version of the agents module was way too complicated, for some reason I tried to include
hierarchical sub-agents
chain-of-thought prompts
embedding search
dynamic model switching
I do not know what I was thinking, and it did not work at all

I threw this whole file away, and completely restarted and made everything simple. Only included things I need such as

Task prioritization
Notes answering
Optional OpenAI support

3. Virual Enviroment
I was having extreme troubles with Python imports and Virtual enviroments working correctly.
I kept running into the same issues such as
	Running the CLI showed:
ModuleNotFoundError: No module named 'lifedesk'
I forgot to activate .venv many times, so dependencies didn’t load
I had a folder name with spaces (“Final Project - LifeDesk AI”), which confused Python’s import resolution
__init__.py was missing at one point, so the package wasn’t recognized
running from the wrong directory caused Python to import from the wrong path

All of these errors were very annoying, and I had to make sure my virtual enviroment was activated

But once I resolved these it was a huge weight off my shoulders, and the whole system was working amazing

Conclusion
In conclusion this was a very fun project and I feel like I came out of it learning so much. It really showed me how powerful AI is and how it can be a real programming partner. I am glad I took this course, and will continue to expand my knowledge in this space and keep up with new AI capabilities.