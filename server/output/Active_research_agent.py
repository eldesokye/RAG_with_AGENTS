# ============================================================
# RUN THE RESEARCH AGENT
# Change TOPIC to any subject you want to research
# ============================================================

from datetime import time
import re
# ============================================================
# MEMORY: adding session history to the support agent
# ============================================================
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from Action.research_Agent import research_Agent
from tools.prompt import prompts
from Action.ReAct_engine import ReActAgent
from tools.tools import ToolFunctions
from tools.environ import base, console, Panel
from output.costs_failures import ReActAgent as Costs_ReActAgent

class Active_research_agent:
    def __init__(self,message=""):
        self.ReAct = ReActAgent()
        self.Costs_ReAct = Costs_ReActAgent()
        self.research_agent= research_Agent()
        self.message = message
        self.session_histories = {}   # For memory of past interactions in the support agent
    def research(self,user_id="default"):
        TOPIC = self.message

        # Other topics to try:
        # TOPIC = "LangGraph AI agent framework 2026"
        # TOPIC = "AWS Bedrock Agents capabilities"
# Retrieve or create history for this user
        if user_id not in self.session_histories:
            self.session_histories[user_id] = []   # new user - empty history

        # Get this user's conversation history so far
        history = self.session_histories[user_id]

        # Add the new user message to history
        history.append({"role": "user", "content": f"<user_input>{TOPIC}</user_input>"})

        # Build a full prompt that includes the conversation history
        history_text = ""
        if len(history) > 1:
            # Format past turns so the agent understands the context
            past = history[:-1]  # everything except the current message
            history_text = "\n\nPREVIOUS CONVERSATION THIS SESSION:\n"
            for turn in past[-6:]:  # last 6 turns max (keep context window small)
                role = "Customer" if turn["role"] == "user" else "You (Layla)"
                history_text += f"{role}: {turn['content'][:200]}\n"

        # Combine history + current message into one user message
        full_message = history_text + "\n\nCURRENT MESSAGE: " + f"<user_input>{TOPIC}</user_input>"

        RESEARCH_TOOLS, RESEARCH_FUNCTIONS = self.research_agent.get_research_tools()
        result = self.ReAct.run_react_agent(
            system_prompt=prompts.RESEARCH_SYSTEM,
            user_message=f"Please research this topic and write a comprehensive report: {full_message}",
            tools_schema=RESEARCH_TOOLS,
            tool_functions=RESEARCH_FUNCTIONS,
            max_iterations=12,
            agent_name="Research Agent",
            verbose=True
        )
        return result
    


    def handle_customer_with_memory(self, user_id="default"):
        message = self.message
        # Retrieve or create history for this user
        if user_id not in self.session_histories:
            self.session_histories[user_id] = []   # new user - empty history

        # Get this user's conversation history so far
        history = self.session_histories[user_id]

        # Add the new user message to history
        history.append({"role": "user", "content": f"<user_input>{message}</user_input>"})

        # Build a full prompt that includes the conversation history
        history_text = ""
        if len(history) > 1:
            # Format past turns so the agent understands the context
            past = history[:-1]  # everything except the current message
            history_text = "\n\nPREVIOUS CONVERSATION THIS SESSION:\n"
            for turn in past[-6:]:  # last 6 turns max (keep context window small)
                role = "Customer" if turn["role"] == "user" else "You (Layla)"
                history_text += f"{role}: {turn['content'][:200]}\n"

        # Combine history + current message into one user message
        full_message = history_text + "\n\nCURRENT MESSAGE: " + f"<user_input>{message}</user_input>"

        SUPPORT_TOOLS, SUPPORT_FUNCTIONS = self.research_agent.get_support_tools()
        result = self.ReAct.run_react_agent(
            system_prompt=prompts.SUPPORT_SYSTEM,
            user_message=full_message,
            tools_schema=SUPPORT_TOOLS,
            tool_functions=SUPPORT_FUNCTIONS,
            max_iterations=3,
            agent_name=f"Support Agent (Layla) [session: {user_id}]",
            verbose=True
        ) 
        return result
    

    def costs_failures(self,user_id="default"):
        TOPIC = self.message
         # Retrieve or create history for this user
        RESEARCH_TOOLS, RESEARCH_FUNCTIONS = self.research_agent.get_research_tools()
        result = self.Costs_ReAct.react_agent_costs(
            system_prompt=prompts.RESEARCH_SYSTEM,
            user_message=f"Please research this topic and write a comprehensive report: <user_input>{TOPIC}</user_input>",
            tools_schema=RESEARCH_TOOLS,
            tool_functions=RESEARCH_FUNCTIONS,
            max_iterations=12,
            agent_name="Research Agent",
            verbose=True
        )
        return result
    

if __name__ == "__main__":
    research = Active_research_agent("Hi, I need help with order number 12345. Where is it?")
    print("TURN 1: Customer asks about their order")
    print("-" * 50)
    # فتح صندوق العزل للمحاولة الأولى
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    final_report = research.costs_failures( user_id="ahmed_session_1")
    # time.sleep(1)
    print(final_report)
    print("\n[bold green]Final Research Report:[/bold green]\n")