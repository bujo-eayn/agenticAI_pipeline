# graph/nodes/retry_node.py
from tools.smoldocling_tool import call_smoldocling_with_feedback


def retry_node(state):
    feedback = state.get("evaluation_feedback", "")
    improved = call_smoldocling_with_feedback(state["pdf_path"], feedback)
    state["smol_extracted"] = improved
    return state
# This node retries the SmolDocling extraction with user feedback.
# It updates the state with the improved extraction results.