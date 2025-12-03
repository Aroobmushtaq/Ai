# agents/agent.py
class Agent:
    def __init__(self, name, instructions, tools=None):
        self.name = name
        self.instructions = instructions
        self.tools = tools or []

    def as_tool(self, tool_name, tool_description):
        return {
            "name": tool_name,
            "description": tool_description,
            "run": lambda *args, **kwargs: f"Tool {tool_name} called",
        }

    # Add this decorator if you want @agent.tool syntax
    def tool(self, func):
        """Register a function as a tool"""
        self.tools.append(func)
        return func
