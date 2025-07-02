from ollama import Client

client = Client()

def infer_intent(query: str) -> str:
    system_prompt = (
        "You are an intent classifier for a developer assistant.\n"
        "You must classify the user's query into one of the following structured intent labels:\n"
        "- github.pull_requests\n"
        "- github.issues\n"
        "- unknown\n"
        "Return ONLY the intent label. No explanation, no markdown, no extra text."
    )

    few_shot_prompt = f"""
Examples:
Q: what are the pull requests? → github.pull_requests  
Q: show the PRs please → github.pull_requests  
Q: are there any open issues? → github.issues  
Q: I need to know the issues in this repo → github.issues  
Q: tell me the status of this repo → unknown  
Q: how many commits were made this week? → unknown  

Now classify this query:
Q: {query}
Intent:
""".strip()

    response = client.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": few_shot_prompt}
        ]
    )

    raw = response["message"]["content"]
    if not isinstance(raw, str):
        return "unknown"

    cleaned = raw.strip().split("\n")[0].replace("-", "").replace("*", "").strip()

    # Optional fallback for edge-case tone or LLaMA miss
    if cleaned == "unknown":
        lowered = query.lower()
        if "issue" in lowered:
            return "github.issues"
        if "pr" in lowered or "pull" in lowered:
            return "github.pull_requests"

    return cleaned
