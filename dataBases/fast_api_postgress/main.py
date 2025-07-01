from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models.todo_model import Todo  # Assuming your model is in models.py
from config.database import get_db  # Assuming your DB setup is in database.py
from pydantic import BaseModel

app = FastAPI()

# --- Pydantic schema ---
class TodoBase(BaseModel):
    title: str
    description: str | None = None

    class Config:
        orm_mode = True

# --- Create Todo ---
@app.post("/todos", response_model=TodoBase)
def create_todo(todo: TodoBase, db: Session = Depends(get_db)):
    print("Creating todo:", todo)
    new_todo = Todo(title=todo.title, description=todo.description)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# --- Get all Todos ---
@app.get("/todos", response_model=list[TodoBase])
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

# Generate Migration Script
# uv run alembic revision --autogenerate -m "create todos table"
# Apply Migrations
# uv run alembic upgrade head