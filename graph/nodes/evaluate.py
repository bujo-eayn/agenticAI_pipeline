# graph/nodes/evaluate.py
from utils.logger import logger
from utils.evaluator import evaluate_extraction


def evaluate_node(state):
    logger.info("Executing evaluate_node with state keys: %s",
                list(state.keys()))

    if "gpt_data" not in state:
        logger.error("Missing gpt_data from extractor node")
        raise ValueError("gpt_data not found in state")

    if "smol_extracted" not in state:
        logger.error("Missing smol_extracted from smoldocling node")
        raise ValueError("smol_extracted not found in state")

    status_updates = state.get("status_updates", [])
    status_updates.append("🧪 Evaluating extraction results...")

    gpt_data = state["gpt_data"]
    smol_data = state["smol_extracted"]

    result, score = evaluate_extraction(gpt_data, smol_data)

    logger.info("Evaluation completed. Result: %s | Score: %s", result, score)

    # Format score dictionary for logging
    if isinstance(score, dict):
        formatted_score = ", ".join(f"{k}: {v:.4f}" for k, v in score.items())
    else:
        formatted_score = f"{score:.4f}"

    status_updates.append(
        f"✅ Evaluation score → {formatted_score} — {'Passed ✅' if result else 'Failed ❌'}"
    )

    updated_state = {
        **state,
        "evaluation_score": score,
        "evaluation_passed": result,
        "status_updates": status_updates
    }

    # logger.info("Updated state after evaluation: %s", updated_state)
    return updated_state
