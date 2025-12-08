import os
import asyncio
from dotenv import load_dotenv
import motor.motor_asyncio
from groq import Groq
from bson import ObjectId

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "todo_app")

# ----------------------------
# Initialize GROQ client
# ----------------------------
client = Groq(api_key=GROQ_API_KEY)

# ----------------------------
# Initialize MongoDB client
# ----------------------------
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = mongo_client[DB_NAME]
todos_collection = db.todos

# ----------------------------
# MongoDB helper functions
# ----------------------------
async def add_todo(item: str) -> str:
    result = await todos_collection.insert_one({"item": item, "done": False})
    return f"Added todo: {item} (id: {str(result.inserted_id)})"

async def list_todos(filter_done=None) -> str:
    todos = await todos_collection.find().to_list(length=100)
    if filter_done is not None:
        todos = [t for t in todos if t.get("done", False) == filter_done]

    if not todos:
        return "No todos found."

    lines = []
    for t in todos:
        _id = str(t.get("_id", "<no-id>"))
        item = t.get("item", "<unknown>")
        done = t.get("done", False)
        lines.append(f"{_id}: {item} [{'Done' if done else 'Pending'}]")
    return "\n".join(lines)

async def delete_todo(todo_id: str) -> str:
    # Delete all todos
    if todo_id.lower() == "all":
        result = await todos_collection.delete_many({})
        return f"Deleted all todos ({result.deleted_count} items)."

    # Delete by ObjectId
    try:
        obj_id = ObjectId(todo_id)
    except Exception:
        return f"Invalid ID format: {todo_id}"

    result = await todos_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        return f"No todo found with id {todo_id}"
    return f"Deleted todo with id {todo_id}"

async def mark_done(todo_id: str) -> str:
    try:
        obj_id = ObjectId(todo_id)
    except Exception:
        return f"Invalid ID format: {todo_id}"

    result = await todos_collection.update_one({"_id": obj_id}, {"$set": {"done": True}})
    if result.matched_count == 0:
        return f"No todo found with id {todo_id}"
    return f"Marked todo {todo_id} as done"

# ----------------------------
# GROQ agent function
# ----------------------------
async def agent_decide(query: str) -> str:
    """
    Decide what to do with the user's input using GROQ model.
    """
    messages = [
        {"role": "system", "content": "You are a helpful todo assistant. Only respond with commands: add, list, delete, mark."},
        {"role": "user", "content": query}
    ]
    
    response = client.chat.completions.create(
        model="groq/compound-mini",
        messages=messages,
        max_tokens=150
    )
    
    return response.choices[0].message.content.strip()

# ----------------------------
# Main async loop
# ----------------------------
async def main():
    print("=== Todo Agent Started ===")
    print("Commands: add <item>, list, list completed, list pending, delete <id>, delete all, mark <id>")

    while True:
        query = input("Enter your command (or 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break

        # Ask the GROQ agent what action to perform
        decision = await agent_decide(query)
        print(f"Agent decided: {decision}")

        # Parse commands
        if decision.startswith("add "):
            item = decision[4:]
            result = await add_todo(item)

        elif decision.startswith("list"):
            parts = decision.split()
            if len(parts) == 1:
                result = await list_todos()
            elif len(parts) == 2 and parts[1] == "completed":
                result = await list_todos(filter_done=True)
            elif len(parts) == 2 and parts[1] == "pending":
                result = await list_todos(filter_done=False)
            else:
                result = f"Unknown list command: {decision}"

        elif decision.startswith("delete "):
            todo_id = decision[7:].strip().split()[0]  # take only first part as ID
            result = await delete_todo(todo_id)

        elif decision.startswith("mark "):
            todo_id = decision[5:].strip().split()[0]  # take only first part as ID
            result = await mark_done(todo_id)

        else:
            result = f"Unknown command: {decision}"

        print(result)
        print("-" * 40)

# ----------------------------
# Run the app
# ----------------------------
if __name__ == "__main__":
    asyncio.run(main())
