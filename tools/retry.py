from langchain_core.tools import tool
from tools.smoldocling_tool import call_smoldocling_with_feedback
from utils.logger import logger

MAX_RETRIES = 3


@tool
def retry_tool(state: dict) -> dict:
    """Retry extraction using feedback until max retries."""
    logger.info("🔁 Running Retry Tool")
    file_paths = state.get("file_path", [])
    feedback = state.get("evaluation_feedback", "")
    retries = state.get("retry_attempts", 0)

    if retries >= MAX_RETRIES or not file_paths:
        logger.info("Max retries reached or missing file.")
        state["evaluation_passed"] = True
        state["evaluation_feedback"] = "Max retries reached. Proceeding with best effort."
        return state

    try:
        file_path = file_paths[0]
        improved = call_smoldocling_with_feedback(file_path, feedback)
        state["retry_attempts"] = retries + 1
        state["smol_extracted"] = improved
        logger.info("Retry successful, attempt %d", state["retry_attempts"])
    except Exception as e:
        logger.error("Retry failed: %s", e)

    return state
