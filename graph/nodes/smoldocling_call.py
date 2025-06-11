# graph/nodes/smoldocling_call.py
from tools.smoldocling_tool import call_smoldocling


def smoldocling_node(state):
    smol_result = call_smoldocling(state["pdf_path"])
    state["smol_extracted"] = smol_result
    return state
# This node calls the SmolDocling tool to extract information from the PDF document.
# It updates the state with the extracted information.