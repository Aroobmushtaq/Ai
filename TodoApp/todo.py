import os
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from openai import AsyncOpenAI

# ------------------------------
# Load environment
# ------------------------------
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "todo_app")

if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in .env")

# ------------------------------
# MongoDB setup
# ------------------------------
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[DB_NAME]
todos_collection = db.todos

# ------------------------------
# OpenAI client
# ------------------------------
client = AsyncOpenAI(api_key=OPENAI_KEY)

# ------------------------------
# Todo functions
# ------------------------------
async def add_todo(item: str):
    await todos_collection.insert_one({"item": item})
    return f"Added todo: {item}"

async def show_todos():
    todos = await todos_collection.find().to_list(length=100)
    if not todos:
        return "Your todo list is empty."
    return "\n".join(f"{i+1}. {t['item']}" for i, t in enumerate(todos))

async def ask_openai(prompt: str):
    """Ask OpenAI for simple instructions"""
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content

# ------------------------------
# CLI Loop
# ------------------------------
async def main():
    print("=== Todo App with OpenAI ===")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nEnter your command: ")
        if query.lower() in ["exit", "quit"]:
            break

        # Basic commands
        if query.lower().startswith("add "):
            item = query[4:]
            result = await add_todo(item)
        elif query.lower() in ["show", "list"]:
            result = await show_todos()
        else:
            # Use OpenAI to help interpret commands
            result = await ask_openai(f"Interpret this command for a todo app: {query}")

        print(f"\n{result}")

if __name__ == "__main__":
    asyncio.run(main())
