from tasks3.core import add_task, list_tasks, mark_done, set_task, render_table, search_tasks, suggest_top3
from tasks3.storage import now_iso

print("now_iso:", now_iso())

# Add two tasks
t1 = add_task("Finish homework", priority=2, due="2025-11-15", tags="school,cs", note="DS homework")
t2 = add_task("Email TA",        priority=3, due="2025-11-10", tags="school",   note="Ask about office hours")

# List all
rows = list_tasks(sort="due")
print("\nLIST (sorted by due):")
print(render_table(rows))

# Update + mark done
set_task(t1["id"], priority=1, note="Start tonight")
mark_done(t2["id"])

# Verify updates
rows = list_tasks()
print("\nAFTER UPDATES:")
print(render_table(rows))

# Search
hits = search_tasks("email")
print("\nSEARCH 'email':", [h["title"] for h in hits])

# Suggestions
print("\nSUGGEST TOP3:", [r["title"] for r in suggest_top3()])
