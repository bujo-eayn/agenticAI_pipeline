from langchain_core.tools import tool
from tools.gpt_tool import extract_elements_with_gpt
from utils.logger import logger
from utils.debug_utils import save_gpt_data_json, create_structured_docx


@tool
def extractor_tool(state: dict) -> dict:
    """Extract elements from document using GPT."""
    logger.info("🧠 Running GPT Extractor Tool")
    file_paths = state.get("file_path", [])
    status_updates = state.get("status_updates", [])

    if not file_paths:
        status_updates.append("❌ GPT extractor failed: no file path.")
        state["status_updates"] = status_updates
        return state

    file_path = file_paths[0]

    try:
        result = extract_elements_with_gpt(file_path)
        save_gpt_data_json(result)
        create_structured_docx(result)
        status_updates.append("✅ GPT extraction complete.")
        state["gpt_data"] = result
    except Exception as e:
        logger.error("GPT extractor error: %s", e)
        status_updates.append("❌ GPT extraction error.")

    state["status_updates"] = status_updates
    return state
