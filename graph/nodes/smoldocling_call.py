# graph/nodes/smoldocling_call.py
from tools.smoldocling_tool import call_smoldocling
from utils.logger import logger


def smoldocling_node(state):
    logger.info("Executing smoldocling_node with state: %s", state)
    smol_result = call_smoldocling(state["file_path"])
    state["smol_extracted"] = smol_result
    logger.info(
        "SmolDocling extraction completed, extracted data: %s", smol_result)
    logger.info("smoldocling_node completed with state: %s", state)
    return state
# This node calls the SmolDocling tool to extract information from the PDF document.
# It updates the state with the extracted information.