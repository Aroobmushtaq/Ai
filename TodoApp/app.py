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