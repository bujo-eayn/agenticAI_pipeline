# graph/graph_builder.py
from langgraph.graph import StateGraph
from graph.nodes.user_input import user_input_node
from graph.nodes.preprocess_doc import preprocess_doc_node
from graph.nodes.gpt_extract import gpt_extract_node
from graph.nodes.smoldocling_call import smoldocling_node
from graph.nodes.evaluate import evaluate_node
from graph.nodes.retry_node import retry_node
from graph.nodes.final_output import final_output_node
from graph.nodes.apply_prompt import apply_prompt_node

from typing import TypedDict


class PipelineState(TypedDict):
    file_path: str
    pdf_path: str
    gpt_data: dict
    smol_data: dict
    evaluation: dict
    evaluation_passed: bool
    evaluation_feedback: str
    retry_attempts: int
    final_doc: str
    user_prompt: str


def build_graph():
    builder = StateGraph(PipelineState)
    # builder.config(recursion_limit=5)  # Prevent infinite loop

    builder.add_node("user_input", user_input_node)
    builder.add_node("preprocess_doc", preprocess_doc_node)
    builder.add_node("gpt_extract", gpt_extract_node)
    builder.add_node("smoldocling", smoldocling_node)
    builder.add_node("evaluate", evaluate_node)
    builder.add_node("retry", retry_node)
    builder.add_node("final_output", final_output_node)
    builder.add_node("apply_prompt", apply_prompt_node)

    builder.set_entry_point("user_input")
    builder.add_edge("user_input", "preprocess_doc")
    builder.add_edge("preprocess_doc", "gpt_extract")
    builder.add_edge("gpt_extract", "smoldocling")
    builder.add_edge("smoldocling", "evaluate")

    builder.add_conditional_edges(
        "evaluate",
        lambda state: "retry" if not state.get(
            "evaluation_passed", False) else "final_output"
    )

    builder.add_edge("retry", "smoldocling")
    builder.add_edge("final_output", "apply_prompt")

    return builder.compile()
