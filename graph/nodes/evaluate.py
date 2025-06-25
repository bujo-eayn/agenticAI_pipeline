# graph/nodes/evaluate.py
from utils.logger import logger
from utils.evaluator import evaluate_extraction


def evaluate_node(state):
    logger.info("Executing evaluate_node with state: %s", state)
    gpt_data = state.get("gpt_data", {})
    logger.info("GPT extracted data: %s", gpt_data)
    smol_data = state.get("smol_extracted", {})
    logger.info("SmolDocling extracted data: %s", smol_data)
    result, score = evaluate_extraction(gpt_data, smol_data)
    state["evaluation_score"] = score
    state["evaluation_passed"] = result
    logger.info(
        "Evaluation completed with score: %s, result: %s", score, result)
    return state
# This node evaluates the extraction results from GPT and SmolDocling.
# It compares the extracted data and updates the state with the evaluation score and result.