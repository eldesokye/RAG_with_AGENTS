import json
import time
from tools.environ import base, console, Panel
from tools.tools import ToolFunctions
from modules.query_handlers import query_chain



class ReActAgent:
    def __init__(self):
        pass

    def react_agent_costs(self,
        system_prompt,
        user_message,
        tools_schema,
        tool_functions,
        max_iterations=10,
        agent_name="Agent",
        verbose=True
    ):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ]

        if verbose:
            console.print(Panel(
                f"[bold cyan]{agent_name}[/bold cyan] starting\n[dim]{user_message[:100]}[/dim]",
                title="[bold blue]ReAct Loop[/bold blue]", border_style="blue"
            ))

        for iteration in range(max_iterations):

            # STEP 1: Ask the LLM what to do next — with retry on BadRequestError
            response = None
            for attempt in range(3):   # up to 3 retries
                try:
                    response = base.client.chat.completions.create(
                        model=base.MODEL,
                        messages=messages,
                        tools=tools_schema,
                        tool_choice="auto",
                        temperature=0.1
                    )
                    break   # success — exit retry loop
                except Exception as e:
                    error_str = str(e)
                    if "400" in error_str or "tool_use_failed" in error_str:
                        if verbose:
                            console.print(f"[bold red]Retry {attempt+1}/3 — bad tool call generated, retrying...[/bold red]")
                        time.sleep(1.5 * (attempt + 1))   # 1.5s, 3s, 4.5s
                    else:
                        raise   # not a retryable error — re-raise immediately

        if response is None:
            print("Failed after 3 attempts.")
        else:
            print("RAW API RESPONSE:")
            print()

            finish = response.choices[0].finish_reason
            print(f"finish_reason: '{finish}'")
            print(f"  In run_react_agent: the 'if response_message.tool_calls:' check uses this")
            print()

            msg = response.choices[0].message

            if finish == "tool_calls":
                print(f"Tool calls requested: {len(msg.tool_calls)}")
                print()
                for i, tc in enumerate(msg.tool_calls):
                    print(f"Tool call #{i+1}:")
                    print(f"  tc.id                 : {tc.id}")
                    print(f"  (must appear in tool result message to link them)")
                    print(f"  tc.function.name      : {tc.function.name}")
                    print(f"  tc.function.arguments : {tc.function.arguments}")
                    print(f"  (this is a JSON STRING - use json.loads() to parse it)")
                    args = json.loads(tc.function.arguments)
                    print(f"  json.loads(arguments) : {args}")
                    print(f"  (now it is a Python dict: {tc.function.name}(**{args}))")
                    print()
                print("What run_react_agent does next:")
                print("  1. Calls: tool_functions[func_name](**func_args)")
                print("  2. Gets the result string back")
                print("  3. Adds both the tool call request AND the result to messages")
                print("  4. Makes another API call - model reads result and decides next step")
            else:
                print("Model answered directly:")
                # print(msg.content[:300])

            print()
            u = response.usage
            print(f"Tokens used: {u.prompt_tokens} input + {u.completion_tokens} output = {u.total_tokens} total")
            cost = u.prompt_tokens * 0.0000025 + u.completion_tokens * 0.0000100
            print(f"Estimated cost: ${cost:.6f}")

            return {
                "response_message": response.choices[0].message,
                "finish_reason": response.choices[0].finish_reason,
                "tokens": {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens,
                },
                "estimated_cost": cost          }   
        

# chat_agent = ReActAgent()

# chat_agent.react_agent_costs(
#     system_prompt="You are a helpful assistant that tries to answer the user's question. You have access to tools, and will use them if it seems helpful. If you use a tool, you will get the result back and can use that to help answer the question.",
#     user_message="What is the current weather in New York, and how does it compare to the weather in San Francisco?",
#     tools_schema=[



