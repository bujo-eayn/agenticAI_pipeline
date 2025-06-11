# graph/nodes/gpt_extract.py
from tools.gpt_tool import extract_elements_with_gpt, extract_from_doc


def gpt_extract_node(state):
    extracted = extract_from_doc(state["pdf_path"])
    state["gpt_extracted"] = extracted
    return state
# This node uses GPT to extract elements from the PDF document.
# It updates the state with the extracted elements.