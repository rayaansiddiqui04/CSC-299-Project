import os, sys, json
import requests

API_URL = "https://api.openai.com/v1/chat/completions"

def summarize(paragraph: str) -> str:
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json",
    }
    body = {
        "model": "gpt-5-mini",
        "messages": [
            {"role": "system", "content": "Summarize the user's task as a short, clear phrase (<= 10 words). Return ONLY the phrase."},
            {"role": "user", "content": paragraph.strip()}
        ]
    }
    r = requests.post(API_URL, headers=headers, data=json.dumps(body), timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text}")
    data = r.json()
    return (data["choices"][0]["message"].get("content") or "").strip()

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY is not set. Run: export OPENAI_API_KEY='YOUR_KEY_HERE'")
        sys.exit(1)

    descriptions = [
        """Develop a Python tool that analyzes large CSV files containing sales
        transactions, computes key statistics like total revenue and average
        order value, and exports the summary to a new file.""",
        """Design an AI-powered chatbot that assists students with homework
        questions, uses natural language understanding to detect question
        topics, and suggests follow-up resources or explanations."""
    ]

    lines = []
    for i, para in enumerate(descriptions, start=1):
        print(f"\n--- Original Task {i} ---")
        print(para.strip())
        try:
            summary = summarize(para)
        except Exception as e:
            summary = f"(error) {e}"
        print("\n--- Summary ---")
        print(summary)

        # also save to file
        lines.append(f"Task {i}:\n{para.strip()}\nSummary: {summary}\n")

    with open("summaries.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(lines) + "\n")
    print("\n📝 Results saved to summaries.txt")

if __name__ == "__main__":
    main()
