from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from TodoApp.db import todo_collection
from bson import ObjectId

app = FastAPI()

class TodoItem(BaseModel):
    task: str
    completed: bool = False

# Helper to convert MongoDB _id to string
def todo_helper(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "task": todo["task"],
        "completed": todo["completed"]
    }

@app.get("/todos")
async def get_todos():
    todos = []
    async for todo in todo_collection.find():
        todos.append(todo_helper(todo))
    return todos

@app.post("/todos")
async def add_todo(todo: TodoItem):
    new_todo = await todo_collection.insert_one(todo.dict())
    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return todo_helper(created_todo)

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: str, completed: bool):
    result = await todo_collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": {"completed": completed}}
    )

    if result.modified_count == 1:
        updated_todo = await todo_collection.find_one({"_id": ObjectId(todo_id)})
        return todo_helper(updated_todo)
    return {"error": "Todo not found"}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    result = await todo_collection.delete_one({"_id": ObjectId(todo_id)})

    if result.deleted_count == 1:
        return {"message": "Todo deleted successfully"}
    return {"error": "Todo not found"}
