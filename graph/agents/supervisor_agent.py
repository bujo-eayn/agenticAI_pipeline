# graph/agents/supervisor_agent.py

from langchain_openai import ChatOpenAI
from tools.smoldocling import smoldocling_tool
from tools.gemini import gemini_tool
from utils.prompts import SUPERVISOR_SYSTEM_PROMPT
from graph.state import PipelineState
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
import json

model = ChatOpenAI(model="gpt-4o", temperature=0)

# Bind tools to the model - this is crucial!
tools = [smoldocling_tool, gemini_tool]
model_with_tools = model.bind_tools(tools)

# Create a mapping of tool names to actual tools
tools_by_name = {tool.name: tool for tool in tools}


def call_supervisor_model(state: PipelineState, config: RunnableConfig = None):
    """Call the supervisor model with the current state."""

    print("Calling supervisor model...")

    # Get existing messages or create new ones
    messages = state.get("messages", [])

    # If no messages exist, create initial message from state
    if not messages:
        user_prompt = state.get("user_prompt", [""])
        file_content = state.get("file_content", [""])
        file_path = state.get("file_path", [""])

        # Convert to strings if they're lists
        user_prompt_str = user_prompt[0] if user_prompt and len(
            user_prompt) > 0 else ""
        file_content_str = file_content[0] if file_content and len(
            file_content) > 0 else ""
        file_path_str = file_path[0] if file_path and len(
            file_path) > 0 else ""

        # Create the input message
        if user_prompt_str or file_content_str:
            input_message = f"{user_prompt_str}\n\nFile content preview: {file_content_str[:1000]}..."
        elif user_prompt_str:
            input_message = user_prompt_str
        elif file_content_str:
            input_message = f"Please analyze this document: {file_content_str[:1000]}..."
        else:
            input_message = "Please help me with my request."

        # Add file path info for tools
        if file_path_str:
            input_message += f"\n\nFile path for processing: {file_path_str}"

        messages = [
            SystemMessage(content=SUPERVISOR_SYSTEM_PROMPT),
            HumanMessage(content=input_message)
        ]

    # Call the model with tools
    response = model_with_tools.invoke(messages, config)

    # Add the response to messages
    new_messages = messages + [response]

    # Update state
    state["messages"] = new_messages

    print(f"Model response: {response}")
    return state


def call_tools(state: PipelineState):
    """Execute tools based on the last message's tool calls."""

    print("Calling tools...")

    messages = state.get("messages", [])
    if not messages:
        return state

    last_message = messages[-1]

    # Check if there are tool calls
    if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
        return state

    outputs = []
    file_path = state.get("file_path", [""])[
        0] if state.get("file_path") else ""

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call_id = tool_call["id"]

        print(f"Executing tool: {tool_name} with args: {tool_args}")

        try:
            if tool_name in tools_by_name:
                # For smoldocling_tool, ensure it gets the file_path
                if tool_name == "smoldocling_tool" and "file_path" not in tool_args and file_path:
                    tool_args["file_path"] = file_path

                # Execute the tool
                tool_result = tools_by_name[tool_name].invoke(tool_args)

                # Create tool message
                outputs.append(
                    ToolMessage(
                        content=json.dumps(tool_result) if isinstance(
                            tool_result, dict) else str(tool_result),
                        name=tool_name,
                        tool_call_id=tool_call_id,
                    )
                )

                # Update state with tool results
                if tool_name == "smoldocling_tool" and isinstance(tool_result, dict):
                    state["smol_extracted"] = tool_result.get("data", {})
                elif tool_name == "gemini_tool" and isinstance(tool_result, dict):
                    state["gpt_data"] = tool_result.get("data", "")

            else:
                outputs.append(
                    ToolMessage(
                        content=f"Tool {tool_name} not found",
                        name=tool_name,
                        tool_call_id=tool_call_id,
                    )
                )
        except Exception as e:
            print(f"Error executing tool {tool_name}: {e}")
            outputs.append(
                ToolMessage(
                    content=f"Error executing {tool_name}: {str(e)}",
                    name=tool_name,
                    tool_call_id=tool_call_id,
                )
            )

    # Add tool outputs to messages
    if outputs:
        state["messages"] = messages + outputs

    print(f"Tool outputs: {outputs}")
    return state


def should_continue_supervisor(state: PipelineState):
    """Determine if we should continue with more tool calls or end."""

    messages = state.get("messages", [])
    if not messages:
        return "end"

    last_message = messages[-1]

    # If the last message has tool calls, continue to tools
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "continue"
    # Otherwise, we're done
    else:
        return "end"


def supervisor_executor(state: PipelineState) -> PipelineState:
    """Main supervisor function that handles the ReAct loop."""

    print("Starting Supervisor Agent with state:", state)

    try:
        # Initialize status updates
        status_updates = state.get("status_updates", [])
        status_updates.append("🤖 Supervisor agent started.")
        state["status_updates"] = status_updates

        # This is just a single step - the actual ReAct loop should be handled by the graph
        # For now, we'll just call the model once
        state = call_supervisor_model(state)

        # Extract final output
        messages = state.get("messages", [])
        if messages:
            final_message = messages[-1]
            if hasattr(final_message, 'content'):
                final_output = final_message.content
            else:
                final_output = str(final_message)
        else:
            final_output = "Supervisor completed"

        # Update status
        status_updates = state.get("status_updates", [])
        status_updates.append("✅ Supervisor agent completed successfully.")

        state.update({
            "final_output_text": final_output,
            "status_updates": status_updates
        })

        print("Supervisor Agent completed:", final_output)

    except Exception as e:
        print(f"Error in supervisor agent: {e}")
        status_updates = state.get("status_updates", [])
        status_updates.append(f"❌ Supervisor agent failed: {str(e)}")
        state.update({
            "status_updates": status_updates,
            "final_output_text": f"Error: {str(e)}"
        })

    return state
