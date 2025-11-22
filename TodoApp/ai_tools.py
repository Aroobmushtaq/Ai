# ai_tools.py
from TodoApp.db import todo_collection
from bson import ObjectId

# return dict / list to send back to client
async def add_todo_task(task: str):
    todo = {"task": task, "completed": False}
    result = await todo_collection.insert_one(todo)
    created = await todo_collection.find_one({"_id": result.inserted_id})
    return {"action": "add", "todo": {"id": str(created["_id"]), "task": created["task"], "completed": created["completed"]}}

async def complete_todo_by_id(todo_id: str):
    res = await todo_collection.update_one({"_id": ObjectId(todo_id)}, {"$set": {"completed": True}})
    if res.modified_count == 1:
        updated = await todo_collection.find_one({"_id": ObjectId(todo_id)})
        return {"action": "complete", "todo": {"id": str(updated["_id"]), "task": updated["task"], "completed": updated["completed"]}}
    return {"error": "Todo not found"}

async def delete_todo_by_id(todo_id: str):
    res = await todo_collection.delete_one({"_id": ObjectId(todo_id)})
    if res.deleted_count == 1:
        return {"action": "delete", "id": todo_id}
    return {"error": "Todo not found"}

async def get_all_todos():
    todos = []
    async for todo in todo_collection.find():
        todos.append({"id": str(todo["_id"]), "task": todo["task"], "completed": todo["completed"]})
    return {"action": "list", "todos": todos}
