from fastapi import FastAPI
from fastapi import APIRouter
app=FastAPI()
@app.get("/")
def get_hello_world():
    return{
        "hello":"world"
    }
# Path Parameters 
@app.get("/item/{item_id}")
def get_item(item_id:int):
    return {"item":item_id}

# Query Parameter 
@app.get("/items/")
def get_item(id:int,q=str):
    return{"id":id,"q":q}

# Grouping Routes with Routers

router = APIRouter()

@router.get("/users")
def get_users():
    return [{"user_id": 1, "name": "John"}]

@router.post("/users")
def create_user(user: dict):
    return {
        "message": "User created",
        "user": user
    }
app.include_router(router, prefix="/api")