# Tool definitions (JSON Schema)
# The LLM reads the "description" to know WHEN to use each tool
# The "parameters" define WHAT arguments to provide
from tools.environ import *
from tools.tools import ToolFunctions
from Action.ReAct_engine import ReActAgent

class research_Agent:
    def __init__(self):
        self.tool_functions = ToolFunctions()
    def get_research_tools(self):
        RESEARCH_TOOLS = [
            {
                "type": "function",
                "function": {
                    "name": "web_search",
                    "description": "Search the web for current info, news, statistics. Use for recent events.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query":       {"type": "string",  "description": "Search query"},
                            "max_results": {"type": "integer", "description": "Number of results (default 4)"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "wikipedia_search",
                    "description": "Get Wikipedia summary for background, history, definitions. Not for recent news.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic":     {"type": "string",  "description": "Topic to look up"},
                            "sentences": {"type": "integer", "description": "Sentences to return (default 5)"}
                        },
                        "required": ["topic"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": (
                        "Evaluate a math expression: percentages, growth rates, totals. "
                        "Always pass a single Python-evaluable string as 'expression'. "
                        "Example: calculate(expression='(1400 - 1200) / 1200 * 100') "
                        "Never pass separate named arguments like old_value or new_value."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "A Python math expression as a string, e.g. '(1400 - 1200) / 1200 * 100'"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            }
        ]
        # tool_functions = ToolFunctions()

        # RESEARCH_FUNCTIONS: maps tool name -> Python function
        # When LLM says "call web_search", the engine does:
        # RESEARCH_FUNCTIONS["web_search"](query="...") -> runs web_search() above
        RESEARCH_FUNCTIONS = {
            "web_search": self.tool_functions.web_search,
            "wikipedia_search": self.tool_functions.wikipedia_search,
            "calculate": self.tool_functions.calculate,
        }

        return RESEARCH_TOOLS, RESEARCH_FUNCTIONS
    
    def get_support_tools(self):
        SUPPORT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Look up order by ID. Use when customer mentions an order number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "Order number with or without #"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_faq",
            "description": "Search FAQ for policy. Use for returns, refunds, shipping, warranty.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Question or topic to search"}
                },
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate refund amounts or price differences.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression"}
                },
                "required": ["expression"]
            }
        }
    }
]

        # SUPPORT_FUNCTIONS: maps tool name (string) -> actual Python function
        # The ReAct engine uses this dict to find and call the right function
        # when the LLM says: "I want to call get_order_status"
        # The engine does: tool_functions["get_order_status"](**args)
        SUPPORT_FUNCTIONS = {
            "get_order_status": self.tool_functions.get_order_status,
            "search_faq": self.tool_functions.search_faq,
            "calculate": self.tool_functions.calculate,
} 
        return SUPPORT_TOOLS, SUPPORT_FUNCTIONS
        


# research_Agent = research_Agent()
# RESEARCH_TOOLS, RESEARCH_FUNCTIONS = research_Agent.get_research_tools()
# print("Research tools defined:", [t["function"]["name"] for t in RESEARCH_TOOLS])

# SUPPORT_TOOLS, SUPPORT_FUNCTIONS = research_Agent.get_support_tools()
# print("Support tools defined:", [t["function"]["name"] for t in SUPPORT_TOOLS])