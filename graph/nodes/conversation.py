# graph/nodes/conversation.py

from dotenv import load_dotenv
from openai import OpenAI
from utils.logger import log_exception, log_info, logger
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

CONTEXT_SNIPPETS = """
You are a smart assistant that helps users understand documents.
Your job is to respond to questions with accurate and relevant answers.
Context:
1. This system is designed for AI document intelligence.
2. It supports smoldocling for structure extraction and GPT for summarization.
3. Users may input prompts with or without documents.
"""

SYSTEM_PROMPT = """
You are a helpful assistant. Respond clearly and concisely using the provided context.
If context is insufficient, acknowledge limitations.
"""


def conversation_node(state: dict) -> dict:
    logger.info("Executing conversation_node with state: %s", state)
    try:
        log_info("Running conversation node for prompt-only interaction.")
        user_prompt = state.get("user_prompt", "")

        if not user_prompt:
            raise ValueError("No user prompt provided.")
        logger.info("User prompt: %s", user_prompt)
        log_info("User prompt received, preparing to call GPT.")

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{CONTEXT_SNIPPETS}\n\nUser Query: {user_prompt}"},
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        gpt_reply = response.choices[0].message.content.strip()
        log_info("Conversation node received GPT response.")

        state["gpt_data"] = {"conversation_response": gpt_reply}
        print(f"GPT Response: {gpt_reply}")  # For debugging purposes
        state["final_output_text"] = gpt_reply  # 👈 Make output available to UI
        logger.info("Conversation node completed with state: %s", state)
        log_info("Conversation node execution completed successfully.")
        return state

    except Exception as e:
        log_exception(e)
        state["gpt_data"] = {"error": str(e)}
        state["final_doc"] = f"Error: {str(e)}"
        logger.error("Conversation node failed with state: %s", state)
        log_info("Conversation node execution failed.")
        return state
