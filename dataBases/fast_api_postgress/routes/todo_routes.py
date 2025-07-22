from fastapi import APIRouter, Depends
from config.database import get_db
from sqlalchemy.orm import Session
from models.todo_model import Todo
from sqlalchemy.orm import Session
from validations.validation import TodoBase
from utils.auth_utils import verify_token 
todo_router = APIRouter()
# --- Create Todo ---
@todo_router.post("/create", response_model=TodoBase )
def create_todo(todo: TodoBase,user=Depends(verify_token) ,db: Session = Depends(get_db)):
    user_id = user.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    print("Creating todo:", todo)
    new_todo = Todo(title=todo.title, description=todo.description,user_id=user_id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

# --- Get all Todos ---
@todo_router.get("/todos", response_model=list[TodoBase] )
def get_todos(user=Depends(verify_token) ,db: Session = Depends(get_db)):
    try:
        todos=db.query(Todo).all()
        return{
    "data": todos,
    "message": "Todos retrieved successfully",
    "status": "success",
    }
    except Exception as e:
        print("Error retrieving todos:", e)
        return{
        "data": [],
        "message": "Failed to retrieve todos",  
        "status": "error",
    }    

    
