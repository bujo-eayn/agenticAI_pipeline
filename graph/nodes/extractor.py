# graph/nodes/extractor.py
from tools.gpt_tool import extract_elements_with_gpt
from utils.logger import logger
from utils.debug_utils import save_gpt_data_json, create_structured_docx


def extractor_node(state):
    logger.info("Executing extractor_node with state keys: %s",
                list(state.keys()))

    # Get current status updates
    status_updates = state.get("status_updates", [])
    status_updates.append("🧠 Beginning extraction with GPT...")

    # Check if the state contains the required key
    # Added check for empty list
    if "file_path" not in state or not state["file_path"]:
        logger.error("State does not contain 'file_path' or it's empty.")
        raise ValueError(
            "State must contain 'file_path' key pointing to the PDF document.")

    # Extract the single file path string from the list
    file_path = state["file_path"][0]  # <-- MODIFIED LINE
    logger.info("Extracting elements from document at: %s", file_path)

    try:
        extracted = extract_elements_with_gpt(file_path)
        logger.info("Extraction completed successfully")

        # Save debug files
        save_gpt_data_json(extracted)
        create_structured_docx(extracted)
        logger.info("Debug files saved successfully.")

        # Update status
        status_updates.append("🧠 GPT extraction finished.")

        # Return updated state with gpt_data
        return {
            **state,  # Preserve existing state
            "gpt_data": extracted,
            "status_updates": status_updates
        }

    except Exception as e:
        logger.error("Error in GPT extraction: %s", e)
        status_updates.append("❌ GPT extraction failed.")
        return {
            **state,
            "gpt_data": {},  # Empty dict to indicate failure
            "status_updates": status_updates
        }
