# utils/logger.py
import logging


def setup_logger():
    logger = logging.getLogger("AgenticPipeline")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

# Create a logger instance
logger = setup_logger()

def log_info(message):
    """Log an informational message."""
    logger.info(message)

def log_error(message):
    """Log an error message."""
    logger.error(message)

def log_debug(message):
    """Log a debug message."""
    logger.debug(message)

def log_warning(message):
    """Log a warning message."""
    logger.warning(message)

def log_critical(message):
    """Log a critical message."""
    logger.critical(message)

def log_exception(exc):
    """Log an exception with traceback."""
    logger.exception("An exception occurred: %s", exc)

def log_state(state):   
    """Log the current state of the pipeline."""
    logger.debug("Current state: %s", state)

def log_node_execution(node_name, state):
    """Log the execution of a node with its state."""
    logger.info("Executing node: %s", node_name)
    log_state(state)
    logger.info("Node %s executed successfully.", node_name)

def log_pipeline_start():
    """Log the start of the pipeline execution."""
    logger.info("Pipeline execution started.")

def log_pipeline_end():
    """Log the end of the pipeline execution."""
    logger.info("Pipeline execution completed.")

def log_pipeline_error(exc):
    """Log an error that occurred during pipeline execution."""
    logger.error("Pipeline execution failed: %s", exc)
    log_exception(exc)
    logger.info("Pipeline execution terminated due to an error.")

def log_pipeline_summary(state):
    """Log a summary of the pipeline execution."""
    logger.info("Pipeline Summary:")
    logger.info("Final Document Path: %s", state.get("final_document_path", "Not available"))
    logger.info("SmolDocling Extraction: %s", state.get("smol_extracted", "Not available"))
    logger.info("GPT Extraction: %s", state.get("gpt_extracted", "Not available"))
    logger.info("Evaluation Feedback: %s", state.get("evaluation_feedback", "Not available"))

def log_evaluation_results(state):
    """Log the evaluation results of the extraction."""
    score = state.get("evaluation_score", "Not available")
    passed = state.get("evaluation_passed", "Not available")
    logger.info("Evaluation Results:")
    logger.info("Score: %s", score)
    logger.info("Passed: %s", passed)
    if not passed:
        logger.warning("The extraction did not pass the evaluation.")
    else:
        logger.info("The extraction passed the evaluation successfully.")

# Example usage of the logger
if __name__ == "__main__":
    log_pipeline_start()
    try:
        # Simulate pipeline execution
        state = {"pdf_path": "example.pdf", "smol_extracted": {}, "gpt_extracted": {}}
        log_node_execution("smoldocling_node", state)
        log_node_execution("final_output_node", state)
        log_node_execution("evaluate_node", state)
        log_evaluation_results(state)
        log_pipeline_summary(state)
    except Exception as e:
        log_pipeline_error(e)
    finally:
        log_pipeline_end()

# This module provides logging functionality for the Agentic AI Document Intelligence pipeline.
# It includes functions to log various events, states, and errors during the pipeline execution.