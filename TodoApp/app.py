from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# In-memory storage for simplicity
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
@app.put("/todo/{todo_id}")
def update_todo(todo_id:id,completed:bool):
    for todo in todos:
        if todo["id"]==todo_id:
           todo["completed"]=completed
           return{"message":"Todo Update Successfully"}
        return{"error":"todo not found"}



