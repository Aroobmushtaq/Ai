from fastapi import APIRouter, Depends
from config.database import get_db
from sqlalchemy.orm import Session
from models.todo_model import Todo
from sqlalchemy.orm import Session
from validations.validation import TodoBase
from utils.auth_utils import verify_token 
todo_router = APIRouter()
# --- Create Todo ---
@todo_router.post("/create" )
def create_todo(todo: TodoBase,user=Depends(verify_token) ,db: Session = Depends(get_db)):
    try:
        user_id = user.get("user_id")
        db_todo = Todo(title=todo.title, description=todo.description, user_id=user_id)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return {
            "data": db_todo,
            "message": "Todo created successfully",
            "status": "success"
        }
    except Exception as e:
        print('An exception occurred')
        print(e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }


# --- Get all Todos ---
@todo_router.get("/")
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

    
