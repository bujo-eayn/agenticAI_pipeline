# graph/nodes/apply_prompt.py
from tools.gpt_tool import apply_user_prompt


def apply_prompt_node(state):
    output = apply_user_prompt(state["user_prompt"], state["smol_extracted"])
    state["final_output"] = output
    return state
# This node applies a user-defined prompt to the extracted data from SmolDocling.
# It updates the state with the final output after applying the prompt.