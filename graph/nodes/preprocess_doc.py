# graph/nodes/preprocess_doc.py
import os
from utils.logger import log_node_execution, logger


def preprocess_doc_node(state):
    logger.info("Executing preprocess_doc_node with state: %s", state)
    file_path = state.get("file_path")
    if not file_path or not os.path.exists(file_path):
        logger.error("File path is missing or file does not exist: %s", file_path)
        raise FileNotFoundError("No file found in the state.")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        logger.info("File read successfully, length: %d", len(content))

    state["file_content"] = content
    log_node_execution("preprocess_doc_node", state)
    logger.info("Preprocessing completed, file content length: %d", len(content))
    logger.info("preprocess_doc_node completed with state: %s", state)
    return state
