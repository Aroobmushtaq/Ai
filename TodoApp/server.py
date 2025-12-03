# import asyncio
# from pymongo import MongoClient
# import re
# import os

# # -----------------------------
# # Simple Agent Framework
# # -----------------------------
# class Agent:
#     def __init__(self, name, instructions, tools=None):
#         self.name = name
#         self.instructions = instructions
#         self.tools = tools or {}

#     def as_tool(self, tool_name, tool_description):
#         def tool_call(**kwargs):
#             return self.handle(kwargs)
#         tool_call.__name__ = tool_name
#         tool_call.description = tool_description
#         return tool_call

#     def handle(self, params):
#         raise NotImplementedError()


# # -----------------------------
# # DATABASE (LOCAL)
# # -----------------------------
# MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
# client = MongoClient(MONGO_URL, tls=False)
# db = client["todo_db"]
# todos = db["todos"]


# # -----------------------------
# # TOOL AGENT — contains real tools
# # -----------------------------
# class TodoToolAgent(Agent):
#     def handle(self, params):
#         """This agent receives structured calls like:
#         { action: "add", text: "milk" }
#         """

#         action = params.get("action")
#         text = params.get("text")
#         new_text = params.get("new_text")

#         # ADD
#         if action == "add":
#             todos.insert_one({"text": text, "completed": False})
#             return f"Added todo: {text}"

#         # DELETE
#         if action == "delete":
#             deleted = todos.delete_one({"text": text})
#             return "Deleted." if deleted.deleted_count else "Todo not found."

#         # COMPLETE
#         if action == "complete":
#             res = todos.find_one_and_update(
#                 {"text": text},
#                 {"$set": {"completed": True}},
#                 return_document=True
#             )
#             return "Marked as completed." if res else "Todo not found."

#         # UPDATE TEXT
#         if action == "update":
#             res = todos.find_one_and_update(
#                 {"text": text},
#                 {"$set": {"text": new_text}},
#                 return_document=True
#             )
#             return "Updated." if res else "Todo not found."

#         # SHOW
#         if action == "show":
#             items = list(todos.find({}, {"_id": 0}))
#             if not items:
#                 return "Your todo list is empty."
#             return "\n".join([f"- {i['text']} (done: {i['completed']})" for i in items])

#         return "Unknown tool action"
        

# todo_tool_agent = TodoToolAgent(
#     name="Todo Tool Agent",
#     instructions="This agent performs real todo operations.",
# )


# # -----------------------------
# # MAIN AGENT — reads natural language and calls tools
# # -----------------------------
# class MainTodoAgent(Agent):
#     async def handle(self, user_message):

#         msg = user_message.lower().strip()

#         # ---------------- DETECT ADD ----------------
#         if re.search(r"\b(add|create|remember|note|put)\b", msg):
#             task = re.sub(r"(please|add|create|remember|note|put)", "", msg).strip()
#             return todo_tool_agent.handle({"action": "add", "text": task})

#         # ---------------- DETECT COMPLETE ----------------
#         if re.search(r"(done|completed|finish)", msg):
#             task = re.sub(r"(i am|i'm|done|completed|finish|with)", "", msg).strip()
#             return todo_tool_agent.handle({"action": "complete", "text": task})

#         # ---------------- DETECT UPDATE ----------------
#         m = re.search(r"(update|change) (.+?) to (.+)", msg)
#         if m:
#             return todo_tool_agent.handle({
#                 "action": "update",
#                 "text": m.group(2).strip(),
#                 "new_text": m.group(3).strip()
#             })

#         # ---------------- DETECT DELETE ----------------
#         if re.search(r"(delete|remove|clear|erase)", msg):
#             task = re.sub(r"(delete|remove|clear|erase)", "", msg).strip()
#             return todo_tool_agent.handle({"action": "delete", "text": task})

#         # ---------------- DETECT SHOW ----------------
#         if re.search(r"(show|list|all)", msg):
#             return todo_tool_agent.handle({"action": "show"})

#         # Fallback
#         return (
#             "I can help with todos. Examples:\n"
#             "• add buy milk\n"
#             "• delete milk\n"
#             "• update milk to eggs\n"
#             "• I'm done with milk\n"
#             "• show my list"
#         )


# main_agent = MainTodoAgent(
#     name="Todo Main Agent",
#     instructions=(
#         "You understand natural language. "
#         "Your job is to understand user's meaning and call the todo tools."
#     ),
#     tools={
#         "todo_tools": todo_tool_agent.as_tool(
#             tool_name="todo_tools",
#             tool_description="Real todo operations"
#         )
#     }
# )


# # -----------------------------
# # TERMINAL LOOP
# # -----------------------------
# async def chat_loop():
#     print("=== Todo Agent Started ===")
#     while True:
#         user = input("You: ").strip()
#         if user == "exit":
#             break

#         response = await main_agent.handle(user)
#         print("Agent:", response)


# if __name__ == "__main__":
#     asyncio.run(chat_loop())
# server.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import google.generativeai as genai
import json

# --- Load environment variables ---
load_dotenv()
GEN_API_KEY = os.getenv("GEN_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

if not GEN_API_KEY:
    raise RuntimeError("GEN_API_KEY not set in environment or .env")

# --- Configure Gemini AI ---
genai.configure(api_key=GEN_API_KEY)

# --- MongoDB setup ---
client = MongoClient(MONGO_URI)
db = client["todo_db"]
todos_collection = db["todos"]

# --- Agent Tools ---
class Agent:
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions
        self.tools = {}

    def tool(self, name):
        """Decorator to register a function as a tool"""
        def decorator(func):
            self.tools[name] = func
            return func
        return decorator

todo_agent = Agent(
    name="Todo Agent",
    instructions="Manage todos in MongoDB. Add, delete, update, list tasks."
)

# --- CRUD tools ---
@todo_agent.tool("add")
def add_todo(task: str):
    todos_collection.insert_one({"task": task, "done": False})
    return f"Todo '{task}' added."

@todo_agent.tool("delete")
def delete_todo(task: str):
    result = todos_collection.delete_one({"task": task})
    if result.deleted_count > 0:
        return f"Todo '{task}' deleted."
    return f"Todo '{task}' not found."

@todo_agent.tool("update")
def update_todo(old_task: str, new_task: str):
    result = todos_collection.update_one({"task": old_task}, {"$set": {"task": new_task}})
    if result.modified_count > 0:
        return f"Todo '{old_task}' updated to '{new_task}'."
    return f"Todo '{old_task}' not found."

@todo_agent.tool("list")
def list_todos():
    todos = list(todos_collection.find({}, {"_id": 0}))
    if not todos:
        return "No todos found."
    lines = []
    for t in todos:
        task = t.get("task", "unknown task")
        done = t.get("done", False)
        lines.append(f"- {task} (done: {done})")
    return "\n".join(lines)

# --- Gemini AI parser ---
def parse_user_input(user_input: str):
    """
    Send user input to Gemini AI to determine the action.
    Returns a dict: {"action": "add/delete/update/list", "task": ..., "old_task": ..., "new_task": ...}
    """
    try:
        response = genai.chat.create(
            model="chat-bison-001",
            messages=[
                {"author": "user", "content": f"""
You are a Todo agent. Convert the user's input into a JSON object with:
- action: one of ["add", "delete", "update", "list"]
- task: string (for add/delete)
- old_task and new_task: strings for update

User input: "{user_input}"

Only respond with JSON.
"""}
            ],
        )
        content = response.last.content[0].text
        return json.loads(content)
    except Exception as e:
        print("Error parsing input:", e)
        # Default to list todos if parsing fails
        return {"action": "list"}

# --- Main interactive loop ---
if __name__ == "__main__":
    print("=== Todo Agent Started ===")
    print("You can type anything to manage todos. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        parsed = parse_user_input(user_input)
        action = parsed.get("action")
        task = parsed.get("task", "")
        old_task = parsed.get("old_task", "")
        new_task = parsed.get("new_task", "")

        if action in todo_agent.tools:
            if action == "add":
                print(todo_agent.tools[action](task))
            elif action == "delete":
                print(todo_agent.tools[action](task))
            elif action == "update":
                print(todo_agent.tools[action](old_task, new_task))
            elif action == "list":
                print(todo_agent.tools[action]())
        else:
            print("I didn't understand that command.")
