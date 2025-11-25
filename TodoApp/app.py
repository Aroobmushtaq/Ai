# TodoApp/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from TodoApp.db import todo_collection
from bson import ObjectId

# AI tools
from TodoApp.ai_tools import add_todo_task, complete_todo_by_id, delete_todo_by_id, get_all_todos
from TodoApp.openai_client import parse_user_message_to_json  # <-- use Gemini

app = FastAPI()

# Standard Todo model
class TodoItem(BaseModel):
    task: str
    completed: bool = False

# -----------------------
# CRUD routes (your existing ones)
# -----------------------

@app.get("/todos")
async def get_todos():
    todos = []
    async for todo in todo_collection.find():
        todos.append({
            "id": str(todo["_id"]),
            "task": todo["task"],
            "completed": todo["completed"]
        })
    return todos

@app.post("/todos")
async def add_todo(todo: TodoItem):
    new_todo = await todo_collection.insert_one(todo.dict())
    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return {
        "id": str(created_todo["_id"]),
        "task": created_todo["task"],
        "completed": created_todo["completed"]
    }

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, completed: bool):
    result = await todo_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": {"completed": completed}})
    if result.modified_count == 1:
        updated_todo = await todo_collection.find_one({"_id": ObjectId(todo_id)})
        return {
            "id": str(updated_todo["_id"]),
            "task": updated_todo["task"],
            "completed": updated_todo["completed"]
        }
    return {"error": "Todo not found"}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    result = await todo_collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 1:
        return {"message": "Todo deleted successfully"}
    return {"error": "Todo not found"}

# -----------------------
# AI endpoint
# -----------------------
class AIRequest(BaseModel):
    message: str

@app.post("/ai")
async def ai_handle(req: AIRequest):
    """
    Receive user's natural text (req.message), ask Gemini AI what to do (returns JSON),
    then call the corresponding ai_tools function and return the result.
    """
    parsed = await parse_user_message_to_json(req.message)
    action = parsed.get("action")
    params = parsed.get("params", {})

    # Normalize "LAST" directive handling
    if action in ("complete", "delete") and params.get("todo_id") == "LAST":
        last = await todo_collection.find().sort([("_id", -1)]).to_list(length=1)
        if not last:
            return {"error": "No todos found"}
        params["todo_id"] = str(last[0]["_id"])

    if action == "add":
        task = params.get("task") or req.message
        return await add_todo_task(task)
    elif action == "complete":
        todo_id = params.get("todo_id")
        if not todo_id:
            return {"error": "todo_id required for complete action"}
        return await complete_todo_by_id(todo_id)
    elif action == "delete":
        todo_id = params.get("todo_id")
        if not todo_id:
            return {"error": "todo_id required for delete action"}
        return await delete_todo_by_id(todo_id)
    elif action == "list":
        return await get_all_todos()
    else:
        return {"error": "unknown action, showing todos", "result": await get_all_todos()}
