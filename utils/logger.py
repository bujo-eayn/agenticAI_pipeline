# utils/logger.py
import logging
import os

LOG_FILE_PATH = "pipeline_debug.log"


def setup_logger(debug_mode=False):
    logger = logging.getLogger("AgenticPipeline")
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    # Console handler (used for Streamlit print redirection)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler with UTF-8 encoding to support emojis
    file_handler = logging.FileHandler(
        LOG_FILE_PATH, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger



# Global logger instance
logger = setup_logger()


def log_info(message): logger.info(message)
def log_error(message): logger.error(message)
def log_debug(message): logger.debug(message)
def log_warning(message): logger.warning(message)
def log_critical(message): logger.critical(message)


def log_exception(exc):
    logger.exception("Exception occurred: ", exc_info=exc)


def log_state(state):
    logger.debug("Pipeline State: %s", state)


def log_node_execution(node_name, state):
    logger.info(f"🟦 Executing Node: {node_name}")
    log_state(state)


def log_pipeline_start(): logger.info("🚀 Pipeline execution started.")
def log_pipeline_end(): logger.info("✅ Pipeline execution completed.")


def log_pipeline_error(exc):
    logger.error("❌ Pipeline execution failed: %s", exc)
    log_exception(exc)
    logger.info("Terminating pipeline due to error.")


def log_pipeline_summary(state):
    logger.info("📊 Pipeline Summary:")
    logger.info("Final Document Path: %s",
                state.get("final_doc", "N/A"))
    smol_data = state.get("smol_data", {})
    logger.info("SmolDocling Output: %s", smol_data)
    logger.info("GPT Output: %s", state.get("gpt_data", "N/A"))
    logger.info("Evaluation Feedback: %s",
                state.get("evaluation_feedback", "N/A"))


def log_evaluation_results(state):
    score = state.get("evaluation_score", "N/A")
    passed = state.get("evaluation_passed", "N/A")
    logger.info("📈 Evaluation Results:")
    logger.info("Score: %s", score)
    logger.info("Passed: %s", passed)
    if not passed:
        logger.warning("⚠️ Extraction did not meet the threshold.")
    else:
        logger.info("✅ Extraction passed successfully.")

# This logger setup allows you to capture detailed logs of the pipeline execution,
# including node execution, state changes, and evaluation results.