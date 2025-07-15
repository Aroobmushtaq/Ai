from sqlalchemy import Column, Integer, String
from config.database import Base  

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  
    email = Column(String, nullable=False, unique=True)  
    password = Column(String, nullable=True)

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
