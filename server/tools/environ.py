from openai import OpenAI
import os
import json
from dotenv import load_dotenv
load_dotenv()


# Search libraries
# from duckduckgo_search import DDGS
from ddgs import DDGS
import wikipedia
wikipedia.set_lang("en")

# Display libraries - makes the ReAct trace much more readable
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
console = Console()

class Base:

    def __init__(self,):
        # Load GROQ API key safely from environment variables
        self.QROQ_API_KEY = os.environ.get("QROQ_API_KEY")

        # Use OpenAI SDK but point it to Groq's free servers!
        self.client = OpenAI(
            api_key=self.QROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

        # Use Llama 3 (Free, blazing fast, and great at function calling)
        self.MODEL = "llama-3.3-70b-versatile"
       

base = Base()
print("Setup complete")
print(f"  API key: {'loaded' if base.QROQ_API_KEY else 'MISSING - check .env file'}")
print(f"  Model: {base.MODEL}")