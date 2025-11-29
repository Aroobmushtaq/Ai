import asyncio
from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# -----------------------------
# Database Setup
# -----------------------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

# Use TLS/SSL for Atlas, disable for local MongoDB
if "mongodb.net" in MONGO_URL:
    client = MongoClient(MONGO_URL, tls=True, tlsCAFile=certifi.where())
else:
    client = MongoClient(MONGO_URL, tls=False)

db = client["todo_db"]
todos_collection = db["todos"]

# -----------------------------
# FastAPI Setup
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Todo Functions
# -----------------------------
def add_todo(text: str):
    doc = {"text": text, "completed": False}
    todos_collection.insert_one(doc)
    return doc

def update_todo(old_text: str, new_text: str):
    result = todos_collection.find_one_and_update(
        {"text": old_text}, {"$set": {"text": new_text}}, return_document=True
    )
    return result

def delete_todo(text: str):
    result = todos_collection.delete_one({"text": text})
    if result.deleted_count == 0:
        return None
    return {"message": "Deleted"}

def get_all_todos():
    return list(todos_collection.find({}, {"_id": 0}))

# -----------------------------
# Terminal Agent Setup
# -----------------------------
pending_todos = {}  # {session_id: "todo_text"}

def safe_agent_response(tool_name, result):
    if result is None:
        return {"message": f"{tool_name} failed or todo not found."}
    return {"message": f"Tool executed: {tool_name}", "result": result}

async def chat_loop():
    session_id = "terminal_user"
    print("=== Todo Agent Started ===")
    print("Type 'exit' to quit\n")
    while True:
        message = input("You: ").strip()
        if message.lower() == "exit":
            print("Exiting agent...")
            break
        response = await agent(session_id, message)
        print("Agent:", response["message"])
        if "result" in response:
            print(response["result"])

async def agent(session_id: str, message: str):
    try:
        msg_lower = message.lower()

        # Confirm pending todo
        if session_id in pending_todos and msg_lower in ["yes", "y"]:
            todo_text = pending_todos[session_id]
            todo_doc = add_todo(todo_text)
            del pending_todos[session_id]
            return {"message": f'Todo added: "{todo_text}"', "todo": todo_doc}

        # Add todo
        if "add" in msg_lower:
            todo_text = message.split("add", 1)[1].strip()
            pending_todos[session_id] = todo_text
            return {"message": f'I understood: "{todo_text}". Should I add it to your todos? (yes/no)'}

        # Update todo
        if "update" in msg_lower or "change" in msg_lower:
            if " to " in message:
                old_text, new_text = message.split(" to ", 1)
                old_text = old_text.replace("update", "").replace("change", "").strip()
                result = update_todo(old_text, new_text.strip())
                return safe_agent_response("update_todo", result)
            else:
                return {"message": "Format for update: 'update <old_text> to <new_text>'"}

        # Delete todo
        if "delete" in msg_lower or "remove" in msg_lower:
            todo_text = message.split("delete", 1)[-1].split("remove", 1)[-1].strip()
            result = delete_todo(todo_text)
            return safe_agent_response("delete_todo", result)

        # Show all todos
        if "show" in msg_lower or "all todos" in msg_lower:
            result = get_all_todos()
            return safe_agent_response("get_all_todos", result)

        # Default
        return {"message": "Command not recognized. Use add/update/delete/show."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# FastAPI Endpoints
# -----------------------------
@app.get("/todos")
def api_get_todos():
    return get_all_todos()

@app.post("/todos")
def api_add_todo(text: str):
    return add_todo(text)

@app.put("/todos")
def api_update_todo(old_text: str, new_text: str):
    return update_todo(old_text, new_text)

@app.delete("/todos")
def api_delete_todo(text: str):
    return delete_todo(text)

# -----------------------------
# Run Terminal Agent
# -----------------------------
if __name__ == "__main__":
    asyncio.run(chat_loop())
