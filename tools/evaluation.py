from langchain_core.tools import tool
from utils.evaluator import evaluate_extraction
from utils.logger import logger


@tool
def evaluate_tool(state: dict) -> dict:
    """Evaluate extraction quality between GPT and SmolDocling."""
    logger.info("🧪 Running Evaluation Tool")
    gpt_data = state.get("gpt_data", {})
    smol_data = state.get("smol_extracted", {})
    status_updates = state.get("status_updates", [])

    if not gpt_data or not smol_data:
        logger.error("Missing data for evaluation.")
        status_updates.append("❌ Evaluation skipped: missing data.")
        state["status_updates"] = status_updates
        return state

    result, score = evaluate_extraction(gpt_data, smol_data)

    formatted_score = f"{score:.4f}" if isinstance(
        score, (int, float)) else str(score)
    status_updates.append(
        f"✅ Evaluation score: {formatted_score} — {'Passed ✅' if result else 'Failed ❌'}"
    )

    state["evaluation_score"] = score
    state["evaluation_passed"] = result
    state["status_updates"] = status_updates

    return state
