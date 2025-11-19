from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"  

client = AsyncIOMotorClient(MONGO_URL)
db = client.todo_db    
todo_collection = db.todos
