# openai_client.py
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment or .env")

client = OpenAI(api_key=OPENAI_KEY)

PROMPT_INSTRUCTIONS = """
You are a helper that maps a user's natural-language todo request into a single JSON object with two keys:
- "action": one of ["add", "complete", "delete", "list"]
- "params": an object with parameters for that action.

Rules:
1. For adding a todo return: {"action":"add", "params":{"task":"<the task text>"}}
2. For completing or deleting a todo prefer an id if the user supplies one; if the user says "last" or "most recent", return {"action":"complete"/"delete","params":{"todo_id":"LAST"}}.
3. For listing todos return {"action":"list","params":{}}.
4. Always output valid JSON only (no extra commentary). If unsure, return {"action":"list","params":{}}.

Now convert the following user message to JSON.

User message:
"""

async def parse_user_message_to_json(user_message: str):
    prompt = PROMPT_INSTRUCTIONS + user_message
    # call Chat Completion endpoint
    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # change model if you need another
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.0
    )
    # safest: get text and parse JSON
    text = resp.choices[0].message["content"]
    # Try to find JSON substring and parse it
    try:
        # if model returns raw JSON, this works
        obj = json.loads(text)
        return obj
    except Exception:
        # fallback: try to extract first {...} block
        import re
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    # final fallback
    return {"action": "list", "params": {}}
