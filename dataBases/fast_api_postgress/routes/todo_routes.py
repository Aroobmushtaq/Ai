from fastapi import APIRouter, Depends
from config.database import get_db
from sqlalchemy.orm import Session
from models.todo_model import Todo
from sqlalchemy.orm import Session
from validations.validation import TodoBase
todo_router = APIRouter()
# --- Create Todo ---
@todo_router.post("/todos", response_model=TodoBase)
def create_todo(todo: TodoBase, db: Session = Depends(get_db)):
    print("Creating todo:", todo)
    new_todo = Todo(title=todo.title, description=todo.description)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# --- Get all Todos ---
@todo_router.get("/todos", response_model=list[TodoBase])
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()
