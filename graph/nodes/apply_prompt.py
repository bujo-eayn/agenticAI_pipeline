# graph/nodes/apply_prompt.py
from tools.gpt_tool import apply_user_prompt
from utils.logger import log_info


def apply_prompt_node(state):
    user_prompt = state.get("user_prompt", "")

    if "smol_extracted" in state:
        log_info("Apply prompt using smol_extracted.")
        extracted = state["smol_extracted"]
    else:
        log_info("Apply prompt using GPT conversation output.")
        extracted = state.get("gpt_data", {}).get(
            "conversation_response", "No context available.")

    output = apply_user_prompt(user_prompt, extracted)
    state["final_output_text"] = output
    return state

# This node applies the user prompt to the extracted data or GPT response.
# It checks if smol data is available and uses it; otherwise, it falls back to the GPT response.