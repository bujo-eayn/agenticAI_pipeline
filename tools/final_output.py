from langchain_core.tools import tool
from utils.doc_utils import create_final_doc
from utils.logger import logger, log_info, log_exception
from docx import Document


@tool
def final_output_tool(state: dict) -> dict:
    """Generate final DOCX from extracted content or conversation."""
    logger.info("📦 Running Final Output Tool")

    try:
        if "smol_extracted" in state and "file_path" in state:
            state["final_output_text"] = state.get(
                "smol_extracted", "No Output found.")
            final_path = create_final_doc(
                state["smol_extracted"], state["file_path"])
            state["final_doc"] = final_path
            log_info("✅ Final document created from SmolDocling extraction.")
        else:
            doc = Document()
            doc.add_paragraph(
                state.get("final_output_text", "No Output found."))
            path = "outputs/final_conversation_output.docx"
            doc.save(path)
            state["final_doc"] = path
            log_info("✅ Final document created from conversation response.")

    except Exception as e:
        log_exception(e)
        logger.error("Error during final output: %s", e)

    return state
