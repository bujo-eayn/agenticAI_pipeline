# graph/nodes/smoldocling_call.py
from tools.smoldocling_tool import call_smoldocling
from utils.logger import logger


def smoldocling_node(state):
    logger.info("Executing smoldocling_node with state keys: %s",
                list(state.keys()))

    status_updates = state.get("status_updates", [])
    status_updates.append("🪶 Starting SmolDocling extraction...")

    file_paths = state.get("file_path", [])
    if not file_paths:
        logger.error("❌ 'file_path' is missing or empty in state.")
        status_updates.append("❌ Missing file for SmolDocling.")
        state["status_updates"] = status_updates
        return state

    try:
        file_path = file_paths[0]
        smol_result = call_smoldocling(file_path)
        logger.info("✅ SmolDocling extraction completed successfully.")

        status_updates.append("🪶 SmolDocling extraction finished.")
        state["smol_extracted"] = smol_result
        state["status_updates"] = status_updates
        return state

    except Exception as e:
        logger.error("❌ Error in SmolDocling extraction: %s", e)
        status_updates.append("❌ SmolDocling extraction failed.")
        state["smol_extracted"] = {}
        state["status_updates"] = status_updates
        return state
