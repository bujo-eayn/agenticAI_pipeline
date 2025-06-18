# graph/nodes/apply_prompt.py
from tools.gpt_tool import apply_user_prompt
from utils.logger import log_info, logger


def apply_prompt_node(state):
    logger.info("Executing apply_prompt_node with state: %s", state)
    user_prompt = state.get("user_prompt", "")

    if "smol_extracted" in state:
        log_info("Apply prompt using smol_extracted.")
        extracted = state["smol_extracted"]
        logger.info(
            "Using SmolDocling extracted data: %s", extracted)
        logger.info(
            "State is: %s", state)
    else:
        log_info("Apply prompt using GPT conversation output.")
        extracted = state.get("gpt_data", {}).get(
            "conversation_response", "No context available.")
        logger.info(
            "Using GPT conversation response: %s", extracted)
        logger.info(
            "State is: %s", state)

    output = apply_user_prompt(user_prompt, extracted)
    state["final_output_text"] = output
    logger.info("Prompt applied, final output text: %s", output)
    logger.info("apply_prompt_node completed with state: %s", state)
    return state

# This node applies the user prompt to the extracted data or GPT response.
# It checks if smol data is available and uses it; otherwise, it falls back to the GPT response.