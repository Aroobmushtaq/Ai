from fastapi import FastAPI
from routes import todo_routes,user_routes
from models.todo_model import Base
from config.database import engine
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(todo_routes.todo_router, prefix="/todos", tags=["Todo"])
app.include_router(user_routes.user_router, prefix="/users", tags=["User"])
# Generate Migration Script
# uv run alembic revision --autogenerate -m "create todos table"
# Apply Migrations
# uv run alembic upgrade head