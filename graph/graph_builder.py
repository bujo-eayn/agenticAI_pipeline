# graph/graph_builder.py
from langgraph.graph import StateGraph
from graph.nodes.entry import entry_node
from graph.nodes.extractor import extractor_node
from graph.nodes.smoldocling_call import smoldocling_node
from graph.nodes.evaluate import evaluate_node
from graph.nodes.retry_node import retry_node
from graph.nodes.final_output import final_output_node
from graph.nodes.apply_prompt import apply_prompt_node
from graph.nodes.conversation import conversation_node

from typing import TypedDict, Optional

from utils.logger import logger


class PipelineState(TypedDict, total=False):
    file_path: str
    file_content: str
    gpt_data: dict
    smol_data: dict
    smol_extracted: str
    evaluation: dict
    evaluation_passed: bool
    evaluation_feedback: str
    retry_attempts: int
    final_doc: str
    final_output_text: str
    final_document_path: str
    user_prompt: str
    dummy_context: Optional[str]
    input_type: str


def build_graph():
    logger.info("Inside build_graph function, starting to build the state graph.")
    builder = StateGraph(PipelineState)

    builder.add_node("entry", entry_node)
    builder.add_node("extractor", extractor_node)
    builder.add_node("smoldocling", smoldocling_node)
    builder.add_node("evaluate", evaluate_node)
    builder.add_node("retry", retry_node)
    builder.add_node("conversation", conversation_node)
    builder.add_node("final_output", final_output_node)
    builder.add_node("apply_prompt", apply_prompt_node)

    builder.set_entry_point("entry")

    builder.add_conditional_edges(
        "entry",
        lambda state: (
            "extractor" if state.get(
                "input_type") == "file_or_both" else "conversation"
        )
    )

    builder.add_edge("extractor", "smoldocling")
    builder.add_edge("smoldocling", "evaluate")

    builder.add_conditional_edges(
        "evaluate",
        lambda state: "retry" if not state.get(
            "evaluation_passed", False) else "apply_prompt"
    )

    builder.add_edge("retry", "smoldocling")
    builder.add_edge("apply_prompt", "final_output")
    builder.add_edge("conversation", "final_output")
    logger.info("Graph built successfully, compiling the graph.")

    return builder.compile()
