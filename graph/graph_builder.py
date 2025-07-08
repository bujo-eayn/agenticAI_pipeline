# graph/graph_builder.py

import operator
from typing import Annotated, Optional, TypedDict
from langgraph.graph import StateGraph

from graph.nodes.apply_prompt import apply_prompt_node
from graph.nodes.conversation import conversation_node
from graph.nodes.entry import entry_node
from graph.nodes.evaluate import evaluate_node
from graph.nodes.extractor import extractor_node
from graph.nodes.final_output import final_output_node
from graph.nodes.retry_node import retry_node
from graph.nodes.smoldocling_call import smoldocling_node
from utils.logger import logger


MAX_RETRIES = 3


class PipelineState(TypedDict, total=False):
    file_path: list[str]
    file_content: list[str]
    gpt_data: dict
    smol_extracted: dict
    evaluation_score: float
    evaluation_passed: bool
    evaluation_feedback: str
    retry_attempts: int
    final_doc: str
    final_output_text: str
    final_document_path: str
    user_prompt: list[str]
    dummy_context: Optional[str]
    input_type: list[str]
    status_updates: Annotated[list[str], operator.add]


def build_graph():
    logger.info("Building the sequential LangGraph workflow.")
    builder = StateGraph(PipelineState)

    # Set up nodes
    builder.add_node("entry", entry_node)
    builder.add_node("conversation", conversation_node)
    builder.add_node("smoldocling", smoldocling_node)
    builder.add_node("extractor", extractor_node)
    builder.add_node("evaluate", evaluate_node)
    builder.add_node("retry", retry_node)
    builder.add_node("apply_prompt", apply_prompt_node)
    builder.add_node("final_output", final_output_node)

    # Entry point — no other node should ever route back here
    builder.set_entry_point("entry")

    # Branch after entry
    builder.add_conditional_edges(
        "entry",
        lambda state: "conversation"
        if state.get("input_type") == ["prompt_only"]
        else "smoldocling"
    )

    builder.add_edge("conversation", "final_output")
    builder.add_edge("smoldocling", "extractor")
    builder.add_edge("extractor", "evaluate")

    # Evaluate branch
    def eval_branch(state):
        if not state.get("evaluation_passed", False):
            if state.get("retry_attempts", 0) >= MAX_RETRIES:
                return "final_output"
            else:
                return "retry"
        elif state.get("user_prompt") and any(p.strip() for p in state["user_prompt"]):
            return "apply_prompt"
        else:
            return "final_output"

    builder.add_conditional_edges("evaluate", eval_branch)

    builder.add_edge("retry", "extractor")
    builder.add_edge("apply_prompt", "final_output")

    logger.info("Graph definition completed.")
    return builder.compile()
