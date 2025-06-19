# graph/nodes/entry.py
from utils.logger import log_node_execution, logger

DUMMY_CONTEXT = "This is dummy context data to be used when the user provides only a prompt."


def entry_node(state):
    logger.info("Executing entry_node with state: %s", state)
    has_prompt = bool(state.get("user_prompt", "").strip())
    has_file = bool(state.get("file_path", "").strip())

    if not has_prompt and not has_file:
        raise ValueError("No prompt or document provided.")

    if has_prompt and not has_file:
        # Prompt only
        state["input_type"] = "prompt_only"
        state["dummy_context"] = DUMMY_CONTEXT
    elif has_file:
        # Document only or document + prompt
        state["input_type"] = "file_or_both"

    log_node_execution("entry_node", state)
    logger.info("entry_node completed with state: %s", state)
    
    return state
