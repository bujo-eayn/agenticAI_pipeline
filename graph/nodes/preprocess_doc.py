# graph/nodes/preprocess_doc.py
import os
from utils.doc_utils import convert_to_pdf


def preprocess_doc_node(state):
    file_path = state["file_path"]
    pdf_path = convert_to_pdf(file_path)
    state["pdf_path"] = pdf_path
    return state
# This node processes the document by converting it to PDF format.
# It updates the state with the path to the converted PDF file.