# graph/nodes/final_output.py
from utils.doc_utils import create_final_doc


def final_output_node(state):
    final_path = create_final_doc(state["smol_extracted"], state["pdf_path"])
    state["final_document_path"] = final_path
    return state
# This node creates the final document from the extracted information.
# It updates the state with the path to the final document.