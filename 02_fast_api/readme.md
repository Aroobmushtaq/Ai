
# 1. Creating a Route
Routes define the paths or endpoints for the API.
```bash
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

```
#  FastAPI Parameters 

# 2. Path Parameters
- Path parameters are used to capture values from the URL path itself.

```bash
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

# 3. Query Parameters
Query parameters are values sent in the URL after the ? symbol.

```bash
@app.get("/search")
def search_items(q: str = None, limit: int = 10):
    return {"query": q, "limit": limit}
```
# 4. Organizing Routes with APIRouter

For larger projects, FastAPI offers APIRouter to modularize your routes and keep things clean.

```bash
from fastapi import APIRouter

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

```
