# graph/nodes/entry.py

import os
from utils.logger import log_node_execution, logger

DUMMY_CONTEXT = "This is dummy context data to be used when the user provides only a prompt."


def entry_node(state):
    logger.info("Executing entry_node with state: %s", state)
    has_prompt = bool(state.get("user_prompt", "").strip())
    has_file = bool(state.get("file_path", "").strip())

    if not has_prompt and not has_file:
        raise ValueError("No prompt or document provided.")

    if has_prompt and not has_file:
        state["input_type"] = "prompt_only"
        state["dummy_context"] = DUMMY_CONTEXT
    elif has_file:
        state["input_type"] = "file_or_both"

        file_path = state.get("file_path")
        if not os.path.exists(file_path):
            logger.error(
                "File path is missing or file does not exist: %s", file_path)
            raise FileNotFoundError("No file found in the state.")

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            logger.info("File read successfully, length: %d", len(content))
        state["file_content"] = content

    log_node_execution("entry_node", state)
    logger.info("entry_node completed with state: %s", state)
    return state
