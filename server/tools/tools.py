# ============================================================
# TOOL FUNCTIONS
# The LLM cannot run these - YOU run them, then hand results back
# ============================================================
from tools.environ import *

class ToolFunctions:
    def __init__(self):
        pass

    def web_search(self, query:str, max_results:int=4):
        # Search the web using DuckDuckGo (free, no API key)
        # Returns: formatted string of search results with titles and summaries
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return f"No results found for: {query}"
            lines = []
            for i, r in enumerate(results, 1):
                lines.append(f"Result {i}: {r['title']}")
                lines.append(f"URL: {r['href']}")
                lines.append(f"Summary: {r['body']}")
                lines.append("")
            return "\n".join(lines)
        except Exception as e:
            return f"Search error: {e}"
        

    def wikipedia_search(self, topic:str, sentences:int=5):
        # Get Wikipedia summary for a topic
        # Returns: summary text or disambiguation/error message
        try:
            summary = wikipedia.summary(topic, sentences=sentences, auto_suggest=True)
            return f"Wikipedia - {topic}:\n{summary}"
        except wikipedia.DisambiguationError as e:
            return f"Ambiguous topic. Try: {', '.join(e.options[:5])}"
        except wikipedia.PageError:
            return f"No Wikipedia page for: {topic}"
        except Exception as e:
            return f"Wikipedia error: {e}"
        

    def calculate(self, expression:str):
        # Evaluate a math expression safely
        # expression example: "(347 - 363) / 363 * 100" for percentage change
        # Security: eval with empty globals prevents code injection
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return f"{expression} = {result}"
        except Exception as e:
            return f"Calculation error: {e}"
        


    def get_order_status(self, order_id:str):
        # Mock order database lookup (production would query a real DB)
        mock_orders = {
            "12345": {"status": "In Transit",  "item": "Laptop Stand",
                    "estimated_delivery": "May 16, 2026", "carrier": "FedEx"},
            "98765": {"status": "Delivered",   "item": "Wireless Keyboard",
                    "delivered_on": "May 10, 2026"},
            "11111": {"status": "Processing",  "item": "USB-C Hub",
                    "estimated_ship": "May 15, 2026"},
        }
        clean_id = order_id.replace("#", "").strip()
        if clean_id in mock_orders:
            order = mock_orders[clean_id]
            details = "\n".join([f"  {k}: {v}" for k, v in order.items()])
            return f"Order #{clean_id}:\n{details}"
        return f"Order #{clean_id} not found. Verify the order number."


    def search_faq(self, question:str):
        # Search support FAQ by keyword matching
        # Production version would use semantic vector search
        faqs = {
            "return":   "Return Policy: 30 days from delivery. Original packaging required. 5-day refund process.",
            "refund":   "Refunds process within 5 business days after item is received. Email confirmation sent.",
            "shipping": "Standard: 3-5 days. Express (1-2 days) available at checkout.",
            "warranty": "1-year manufacturer warranty on all electronics. Extended plans available.",
            "cancel":   "Cancel within 2 hours of placing order if not yet shipped.",
            "damage":   "Damaged item? Contact us within 48 hours with photos for immediate replacement.",
        }
        for keyword, answer in faqs.items():
            if keyword in question.lower():
                return f"FAQ: {answer}"
        return "No FAQ match found. Escalating to human agent (response within 2 hours)."


    print("Tool functions ready:")
    for name in ["web_search", "wikipedia_search", "calculate", "get_order_status", "search_faq"]:
        print(f"  - {name}")




