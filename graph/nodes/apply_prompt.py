# graph/nodes/apply_prompt.py
from tools.gpt_tool import apply_user_prompt
from utils.logger import log_info, logger


def apply_prompt_node(state):
    logger.info("Executing apply_prompt_node with state keys: %s",
                list(state.keys()))

    status_updates = state.get("status_updates", [])
    user_prompt_list = state.get("user_prompt", [])

    # Check if there's any valid prompt text
    valid_prompts = [p for p in user_prompt_list if p.strip()]

    if not valid_prompts:
        logger.info(
            "No valid user prompt provided. Skipping apply_prompt_node.")
        status_updates.append(
            "⚠️ No prompt provided — skipping apply_prompt step.")
        state["status_updates"] = status_updates
        return state

    user_prompt = valid_prompts[0]  # Use the first valid one
    logger.info("Applying user prompt: %s", user_prompt)

    # Determine the source of extracted content
    if "smol_extracted" in state and state["smol_extracted"]:
        log_info("Applying prompt to SmolDocling extracted data.")
        extracted = state["smol_extracted"]
    else:
        log_info("Applying prompt to GPT fallback output.")
        extracted = state.get("gpt_data", {}).get(
            "conversation_response", "No context available.")

    logger.info("Extracted content being used: %s", str(extracted)[:200])

    # Apply the prompt to the extracted content
    try:
        output = apply_user_prompt(user_prompt, extracted)
        state["final_output_text"] = output
        status_updates.append(
            "✅ Prompt successfully applied to extracted content.")
        logger.info(
            "Prompt applied successfully. Final output: %s", output[:300])
    except Exception as e:
        from utils.logger import log_exception
        log_exception(e)
        logger.error("Error applying user prompt: %s", e)
        status_updates.append("❌ Failed to apply user prompt.")

    state["status_updates"] = status_updates
    return state
