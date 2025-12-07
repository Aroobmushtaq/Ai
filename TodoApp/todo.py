import os
import asyncio
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "todo_app")

if not GEMINI_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env")

# MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[DB_NAME]
todos_collection = db.todos

# Gemini client
client = AsyncOpenAI(
    api_key=GEMINI_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ----------------- Tools -----------------
@function_tool
def add_todo(item: str):
    todos_collection.insert_one({"item": item})
    return f"Added todo: {item}"

@function_tool
def show_todos():
    todos = list(todos_collection.find())
    if not todos:
        return "Todo list is empty."
    return "\n".join(f"{i+1}. {t['item']}" for i, t in enumerate(todos))

@function_tool
def delete_todo(index: int):
    todo = todos_collection.find().skip(index-1).limit(1)
    todos_collection.delete_one({"_id": todo["_id"]})
    return f"Deleted todo #{index}"

# ----------------- Agent -----------------
agent = Agent(
    name="TodoAgent",
    instructions="You are a todo agent. You can add, show, update, and delete todos.",
    model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    tools=[add_todo, show_todos, delete_todo]
)

# ----------------- CLI -----------------
async def main():
    print("=== Gemini Todo Agent ===")
    print("Type 'exit' to quit.")

    while True:
        query = input("Command: ")
        if query.lower() in ["exit", "quit"]:
            break
        result = await Runner.run(agent, query)
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
