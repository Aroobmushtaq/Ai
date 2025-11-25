# TodoApp/gemini_client.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT_INSTRUCTIONS = """
You are a helper that converts user's natural text todo request into JSON:
- "action": one of ["add", "complete", "delete", "list"]
- "params": action parameters

Rules:
1. Add: {"action":"add", "params":{"task":"<task>"}}
2. Complete/Delete: use "todo_id" or "LAST" if most recent
3. List: {"action":"list","params":{}}
4. Only return valid JSON
"""

async def parse_user_message_to_json(user_message: str):
    prompt = PROMPT_INSTRUCTIONS + "\nUser message: " + user_message

    resp = genai.chat.create(
        model="models/Chat-Bison-001",
        messages=[{"author": "user", "content": prompt}],
        temperature=0
    )

    text = resp.last  # Gemini text output
    try:
        return json.loads(text)
    except:
        return {"action": "list", "params": {}}
