from fastapi import FastAPI
from pydantic import BaseModel
from routes import todo_routes,user_routes
app = FastAPI()

# --- Pydantic schema ---
class TodoBase(BaseModel):
    title: str
    description: str | None = None

    class Config:
        orm_mode = True

app.include_router(todo_routes.todo_router, prefix="/todos", tags=["Todo"])
app.include_router(user_routes.user_router, prefix="/users", tags=["User"])
# Generate Migration Script
# uv run alembic revision --autogenerate -m "create todos table"
# Apply Migrations
# uv run alembic upgrade head