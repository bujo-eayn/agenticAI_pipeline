from langchain_core.tools import tool
from tools.gpt_tool import apply_user_prompt
from utils.logger import logger, log_exception


@tool
def apply_prompt_tool(state: dict) -> dict:
    """Apply user prompt to extracted content."""
    logger.info("📣 Running Prompt Applier Tool")
    user_prompt_list = state.get("user_prompt", [])
    status_updates = state.get("status_updates", [])

    valid_prompts = [p for p in user_prompt_list if p.strip()]
    if not valid_prompts:
        status_updates.append("⚠️ No prompt to apply.")
        state["status_updates"] = status_updates
        return state

    prompt = valid_prompts[0]
    content = state.get("smol_extracted") or state.get(
        "gpt_data", {}).get("conversation_response", "")

    try:
        output = apply_user_prompt(prompt, content)
        state["final_output_text"] = output
        status_updates.append("✅ Prompt applied.")
    except Exception as e:
        log_exception(e)
        status_updates.append("❌ Failed to apply prompt.")

    state["status_updates"] = status_updates
    return state
