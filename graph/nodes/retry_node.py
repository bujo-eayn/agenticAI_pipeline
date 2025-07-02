# graph/nodes/retry_node.py
from tools.smoldocling_tool import call_smoldocling_with_feedback
from utils.logger import logger

MAX_RETRIES = 3  # You can also move this to a config file


def retry_node(state):
    logger.info("Executing retry_node with state: %s", state)
    current_retries = state.get("retry_attempts", 0)

    if current_retries >= MAX_RETRIES:
        state["evaluation_passed"] = True  # Force exit on max retry
        state["evaluation_feedback"] = "Max retries reached. Proceeding with best effort."
        return state

    feedback = state.get("evaluation_feedback", "")
    improved = call_smoldocling_with_feedback(state["file_path"], feedback)

    state["retry_attempts"] = current_retries + 1
    state["smol_extracted"] = improved  # Ensure correct key is used
    logger.info(
        "Retry attempt %d completed, updated state: %s",
        state["retry_attempts"],
        state,
    )
    return state

# This node handles the retry logic, calling the Smoldocling tool with feedback
# and updating the state accordingly. It checks the number of retries and exits