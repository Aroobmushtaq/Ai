from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"  # or your Atlas URL

client = AsyncIOMotorClient(MONGO_URL)
db = client.todo_db       # database
todo_collection = db.todos  # collection
