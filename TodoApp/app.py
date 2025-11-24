from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from TodoApp.db import todo_collection
from bson import ObjectId

# import ai pieces
from TodoApp.ai_tools import add_todo_task, complete_todo_by_id, delete_todo_by_id, get_all_todos
from TodoApp.openai_client import parse_user_message_to_json

app = FastAPI()

class TodoItem(BaseModel):
    task: str
    completed: bool = False

# ... keep your existing helper and CRUD routes here (as you already have) ...


# NEW: AI endpoint
class AIRequest(BaseModel):
    message: str

@app.post("/ai")
async def ai_handle(req: AIRequest):
    """
    Receive user's natural text (req.message), ask OpenAI what to do (returns JSON),
    then call the corresponding ai_tools function and return the result.
    """
    parsed = await parse_user_message_to_json(req.message)
    action = parsed.get("action")
    params = parsed.get("params", {})

    # Normalize "LAST" directive handling
    if action in ("complete", "delete") and params.get("todo_id") == "LAST":
        # find most recent todo id
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
