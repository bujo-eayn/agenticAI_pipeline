# graph/nodes/preprocess_doc.py
import os
from utils.logger import log_node_execution


def preprocess_doc_node(state):
    file_path = state.get("file_path")
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError("No file found in the state.")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    state["file_content"] = content
    log_node_execution("preprocess_doc_node", state)
    return state
