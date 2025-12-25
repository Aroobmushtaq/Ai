from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()