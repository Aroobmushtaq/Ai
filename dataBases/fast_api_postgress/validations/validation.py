from pydantic import BaseModel,Field
from typing_extensions import Annotated
# --- Pydantic schema ---
class TodoBase(BaseModel):
    title: str
    description: str | None = None

    class Config:
        orm_mode = True
class UserCreate(BaseModel):
    name: Annotated[str, Field(min_length=3,max_length=50)]
    email: Annotated[str, Field(pattern=r'^\S+@\S+$')]
    password: Annotated[str, Field(min_length=6)]
class LoginUser(BaseModel):
    email: str
    password: str
