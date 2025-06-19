# graph/nodes/final_output.py
#To-do: Fix Final Conversation Output is always empty
from utils.doc_utils import create_final_doc
from utils.logger import log_info, logger


def final_output_node(state):
    logger.info("Executing final_output_node with state: %s", state)
    try:
        if "smol_extracted" in state and "pdf_path" in state:
            final_path = create_final_doc(
                state["smol_extracted"], state["pdf_path"])
            state["final_document_path"] = final_path
            log_info("Final document created from structured extraction.")
            logger.info(
                "Final document created from SmolDocling extraction: %s", final_path)
            logger.info("Final output node completed with state: %s", state)
        else:
            # Prompt-only case: just convert GPT response into doc
            from docx import Document
            doc = Document()
            doc.add_paragraph(
                state.get("final_output_text", "No output found."))
            path = "outputs/final_conversation_output2.docx"
            doc.save(path)
            state["final_document_path"] = path
            log_info("Final document created using GPT conversation response.")
            logger.info("Final output node completed with state: %s", state)
    except Exception as e:
        from utils.logger import log_exception
        log_exception(e)
        logger.error("Error during final output node execution: %s", e)
        logger.error("State at error: %s", state)
        raise e
    
    logger.info("Final output node execution completed with state: %s", state)
    log_info("Final output node execution completed.")
    return state

# This node generates the final output document based on the available data.
# It checks if SmolDocling data is available and uses it; otherwise, it falls back to the GPT conversation response.