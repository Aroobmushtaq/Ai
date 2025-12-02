import asyncio
from pymongo import MongoClient
import os
import re
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# DATABASE (LOCAL)
# -----------------------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = MongoClient(MONGO_URL, tls=False)

db = client["todo_db"]
todos = db["todos"]

# -----------------------------
# TODO FUNCTIONS
# -----------------------------
def add_todo(text):
    doc = {"text": text, "completed": False}
    todos.insert_one(doc)
    return doc

def complete_todo(text):
    return todos.find_one_and_update(
        {"text": text},
        {"$set": {"completed": True}},
        return_document=True
    )

def update_todo(old, new):
    return todos.find_one_and_update(
        {"text": old},
        {"$set": {"text": new}},
        return_document=True
    )

def delete_todo(text):
    return todos.delete_one({"text": text}).deleted_count > 0

def get_all_todos():
    return list(todos.find({}, {"_id": 0}))


# -----------------------------
# NLP INTENT DETECTION
# -----------------------------
def detect_intent(message):
    msg = message.lower().strip()

    # ---------------- ADD ----------------
    if re.search(r"\b(add|create|insert|put|note|remember)\b", msg):
        text = re.sub(r"(please|add|create|insert|put|note|remember)", "", msg).strip()
        return "add", text

    # ---------------- COMPLETE ----------------
    if re.search(r"(done|finish|completed|complete|i am done)", msg):
        match = re.search(r"(done with|finish|completed|complete)(.*)", msg)
        if match:
            task = match.group(2).strip()
            return "complete", task

    # ---------------- UPDATE ----------------
    if "update" in msg or "change" in msg or "rename" in msg:
        m = re.search(r"(update|change|rename) (.+?) to (.+)", msg)
        if m:
            return "update", (m.group(2).strip(), m.group(3).strip())

    # ---------------- DELETE ----------------
    if re.search(r"(delete|remove|clear|erase)", msg):
        text = re.sub(r"(delete|remove|clear|erase)", "", msg).strip()
        return "delete", text

    # ---------------- SHOW ----------------
    if re.search(r"(show|list|display|all todos|full list)", msg):
        return "show", None

    return "unknown", None


# -----------------------------
# AGENT
# -----------------------------
async def agent(msg: str):
    intent, data = detect_intent(msg)

    if intent == "add":
        doc = add_todo(data)
        return f"✔ Added: **{doc['text']}**"

    if intent == "complete":
        updated = complete_todo(data)
        if updated:
            return f"✔ Marked completed: **{data}**"
        return f"⚠ Task not found: **{data}**"

    if intent == "update":
        old, new = data
        updated = update_todo(old, new)
        if updated:
            return f"✔ Updated: **{old} → {new}**"
        return f"⚠ Task not found: **{old}**"

    if intent == "delete":
        ok = delete_todo(data)
        if ok:
            return f"🗑 Deleted: **{data}**"
        return f"⚠ Task not found: **{data}**"

    if intent == "show":
        items = get_all_todos()
        if not items:
            return "📭 No todos found."

        return "\n".join([f"- {t['text']} (completed: {t['completed']})" for t in items])

    return "🤖 Sorry, I didn’t understand. Try: add / update / delete / complete / show."


# -----------------------------
# TERMINAL LOOP
# -----------------------------
async def chat_loop():
    print("=== Todo Agent Started ===")
    print("I understand natural language!")
    print()

    while True:
        msg = input("You: ").strip()
        if msg.lower() == "exit":
            print("Goodbye!")
            break

        response = await agent(msg)
        print("Agent:", response)


if __name__ == "__main__":
    asyncio.run(chat_loop())
