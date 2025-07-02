# graph/nodes/entry.py
import os
from utils.logger import logger

DUMMY_CONTEXT = "This is dummy context data to be used when the user provides only a prompt."


def entry_node(state):
    logger.info("Executing entry_node with state: %s", state)

    status_updates = state.get("status_updates", [])
    status_updates.append("🔁 Entry node activated.")

    user_prompt = state.get("user_prompt", [])
    has_prompt = bool(user_prompt and any(prompt.strip()
                      for prompt in user_prompt))
    file_path = state.get("file_path", [])
    has_file = bool(file_path and any(path.strip() for path in file_path))

    if not has_prompt and not has_file:
        status_updates.append("❌ No prompt or file provided.")
        state["status_updates"] = status_updates
        return state

    if has_prompt and not has_file:
        logger.info("✅ Prompt provided (no file).")
        status_updates.append("📝 Prompt detected, proceeding.")
        state.update({
            "input_type": ["prompt_only"],
            "dummy_context": DUMMY_CONTEXT,
            "status_updates": status_updates
        })
        return state

    if has_file:
        file_path_str = file_path[0]
        if not os.path.exists(file_path_str):
            logger.error("🚫 File path invalid: %s", file_path_str)
            status_updates.append("🚫 File missing.")
            state["status_updates"] = status_updates
            return state

        try:
            with open(file_path_str, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            logger.error("Error reading file: %s", e)
            status_updates.append("🚫 Error reading file.")
            state["status_updates"] = status_updates
            return state

        status_updates.append("📄 File uploaded and read successfully.")
        status_updates.append("✅ Entry node executed successfully.")
        state.update({
            "input_type": ["file_or_both"],
            "file_content": [content],
            "status_updates": status_updates
        })
        return state
