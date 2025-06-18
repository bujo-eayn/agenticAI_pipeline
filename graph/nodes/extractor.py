# graph/nodes/gpt_extract.py
from tools.gpt_tool import extract_elements_with_gpt, extract_from_doc
from utils.logger import logger


def extractor_node(state):
    logger.info("Executing extractor_node with state: %s", state)
    extracted = extract_from_doc(state["file_path"])
    state["gpt_extracted"] = extracted
    logger.info("Extraction completed, extracted data: %s", extracted)
    return state
# This node uses GPT to extract elements from the PDF document.
# It updates the state with the extracted elements.