from langchain_core.tools import tool
from openai import OpenAI
from utils.logger import logger, log_exception
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a helpful assistant. Respond clearly and concisely using the provided context.
If context is insufficient, acknowledge limitations.
"""

CONTEXT_SNIPPETS = """
You are a smart assistant that helps users understand documents.
Your job is to respond to questions with accurate and relevant answers.
Context:
1. This system is designed for AI document intelligence.
2. It supports smoldocling for structure extraction and GPT for summarization.
3. Users may input prompts with or without documents.
"""


@tool
def conversation_tool(state: dict) -> dict:
    """Handle free-form prompt-only queries with GPT."""
    logger.info("💬 Running Conversation Tool")
    try:
        user_prompt = state.get("user_prompt", [""])[0]

        if not user_prompt:
            raise ValueError("No user prompt provided.")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{CONTEXT_SNIPPETS}\n\nUser Query: {user_prompt}"},
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        gpt_reply = response.choices[0].message.content.strip()
        state["gpt_data"] = {"conversation_response": gpt_reply}
        state["final_output_text"] = gpt_reply

    except Exception as e:
        log_exception(e)
        state["gpt_data"] = {"error": str(e)}
        state["final_doc"] = f"Error: {str(e)}"

    return state
