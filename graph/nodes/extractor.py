# graph/nodes/extractor.py
from tools.gpt_tool import extract_elements_with_gpt
from utils.logger import logger
from utils.debug_utils import save_gpt_data_json, create_structured_docx


def extractor_node(state):
    logger.info("Executing extractor_node with state: %s", state)
    # Check if the state contains the required key
    if "file_path" not in state:
        logger.error("State does not contain 'file_path'.")
        raise ValueError("State must contain 'file_path' key pointing to the PDF document.")
    
    # Extract elements from the document using the provided file path
    logger.info("Extracting elements from document at: %s", state["file_path"])
    extracted = extract_elements_with_gpt(state["file_path"])

    # Return the extracted elements
    state["gpt_data"] = extracted
    logger.info("Extraction completed, extracted data: %s", extracted)
    logger.info("Completion State: %s", state)

    # Save debug files
    gpt_data = extracted
    save_gpt_data_json(gpt_data)
    create_structured_docx(gpt_data)
    logger.info("Debug files saved successfully.")
    return state

# This node uses GPT to extract elements from the PDF document.
# It updates the state with the extracted elements.

# This node is designed to be used in a workflow where the state contains
# a "file_path" key pointing to the PDF document to be processed.
# The extracted elements are stored in the "gpt_data" key of the state.
# The logger is used to log the execution and results of the extraction.
# The extract_elements_with_gpt function is assumed to handle the actual extraction logic.
# The logger is used to log the execution and results of the extraction.

