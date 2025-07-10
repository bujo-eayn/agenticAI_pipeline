from langchain_core.tools import tool
from utils.logger import logger

@tool
def gemini_tool(state: dict) -> dict:
    """
    This tool extracts visual elements from files using Gemini 2.5pro.
    It receives the state attributes `file_path`, `status_updates`, and `instructions`.
    It returns the updated state with `gpt_data` containing the extracted elements.
    It should fail gracefully for any errors, logging them and updating `status_updates`.
    """
    logger.info("🔍 Running Gemini Tool")

    return state
