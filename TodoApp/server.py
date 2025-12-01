import asyncio
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# -----------------------------
# Database Setup (LOCAL ONLY)
# -----------------------------
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

# Always local connection (NO TLS)
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
    allow_credentials=True,
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
    return todos_collection.find_one_and_update(
        {"text": old_text},
        {"$set": {"text": new_text}},
        return_document=True
    )

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
pending_todos = {}

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

        try:
            response = await agent(session_id, message)
            print("Agent:", response)
        except Exception as e:
            print("Error:", str(e))
