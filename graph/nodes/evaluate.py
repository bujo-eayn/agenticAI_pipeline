# graph/nodes/evaluate.py
from utils.evaluator import evaluate_extraction


def evaluate_node(state):
    gpt_data = state.get("gpt_extracted", {})
    smol_data = state.get("smol_extracted", {})
    result, score = evaluate_extraction(gpt_data, smol_data)
    state["evaluation_score"] = score
    state["evaluation_passed"] = result
    return state
# This node evaluates the extraction results from GPT and SmolDocling.
# It compares the extracted data and updates the state with the evaluation score and result.