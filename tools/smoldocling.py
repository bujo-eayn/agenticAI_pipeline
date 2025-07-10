from langchain_core.tools import tool
from tools.smoldocling_tool import call_smoldocling
from utils.logger import logger


@tool
def smoldocling_tool(state: dict) -> dict:
    """Extract structured information from PDF using SmolDocling."""
    logger.info("🪶 Running SmolDocling Tool")
    file_paths = state.get("file_path", [])
    status_updates = state.get("status_updates", [])

    if not file_paths:
        logger.error("No file path provided.")
        status_updates.append("❌ SmolDocling failed: missing file.")
        state["status_updates"] = status_updates
        return state

    try:
        file_path = file_paths[0]
        smol_result = call_smoldocling(file_path)
        state["smol_extracted"] = smol_result
        status_updates.append("✅ SmolDocling extraction complete.")
    except Exception as e:
        logger.error("SmolDocling error: %s", e)
        state["smol_extracted"] = {}
        status_updates.append("❌ SmolDocling extraction failed.")

    state["status_updates"] = status_updates
    return state
