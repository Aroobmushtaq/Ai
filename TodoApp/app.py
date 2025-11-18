from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory storage
todos: List[dict] = []

class TodoItem(BaseModel):
    id: int
    task: str
    completed: bool = False

@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos")
def add_todo(todo: TodoItem):
    todos.append(todo.dict())
    return {"message": "Todo added successfully"}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, completed: bool):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["completed"] = completed
            return {"message": "Todo updated successfully"}
    return {"error": "Todo not found"}  

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return {"message": "Todo deleted successfully"}
    return {"error": "Todo not found"}
