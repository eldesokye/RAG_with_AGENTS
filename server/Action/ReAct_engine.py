import json
import time
from tools.environ import base, console, Panel
from tools.tools import ToolFunctions
from modules.query_handlers import query_chain



class ReActAgent:
    def __init__(self):
        pass

    def run_react_agent(self,
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
                return "Error: model failed to generate a valid tool call after 3 attempts."

            response_message = response.choices[0].message
            finish_reason = response.choices[0].finish_reason
            print(f"finish_reason: '{finish_reason}'")

            # STEP 2: Did the model request a tool?
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)

                    if verbose:
                        console.print(
                            f"\n[bold yellow]Step {iteration+1}[/bold yellow] | "
                            f"[bold magenta]ACTION[/bold magenta]: "
                            f"[cyan]{func_name}[/cyan]({func_args})"
                        )

                    # STEP 3: Execute the tool
                    if func_name in tool_functions:
                        result = tool_functions[func_name](**func_args)
                    else:
                        result = f"Error: unknown tool '{func_name}'"

                    if verbose:
                        preview = str(result)[:200] + "..." if len(str(result)) > 200 else str(result)
                        console.print(f"[bold green]OBSERVATION[/bold green]: [dim]{preview}[/dim]")

                    # STEP 4: Add tool call + result to history
                    messages.append(response_message)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })

            else:
                # STEP 5: No tool call = final answer
                final = response_message.content
                if verbose:
                    n_tools = sum(1 for m in messages
                                if (m.get("role") if isinstance(m, dict) else m.role) == "tool")
                    console.print(Panel(
                        final,
                        title=f"[bold green]FINAL ANSWER ({iteration+1} steps, {n_tools} tool calls)[/bold green]",
                        border_style="green"
                    ))
                return final

        return "Max iterations reached."


    print("ReAct engine ready")