# graph/nodes/final_output.py
#To-do: Fix Final Conversation Output is always empty
from utils.doc_utils import create_final_doc
from utils.logger import log_info


def final_output_node(state):
    try:
        if "smol_extracted" in state and "pdf_path" in state:
            final_path = create_final_doc(
                state["smol_extracted"], state["pdf_path"])
            state["final_document_path"] = final_path
            log_info("Final document created from structured extraction.")
        else:
            # Prompt-only case: just convert GPT response into doc
            from docx import Document
            doc = Document()
            doc.add_paragraph(state.get("final_output_text", "No output found."))
            path = "outputs/final_conversation_output.docx"
            doc.save(path)
            state["final_document_path"] = path
            log_info("Final document created using GPT conversation response.")
    except Exception as e:
        from utils.logger import log_exception
        log_exception(e)
        raise e

    return state

# This node generates the final output document based on the available data.
# It checks if SmolDocling data is available and uses it; otherwise, it falls back to the GPT conversation response.