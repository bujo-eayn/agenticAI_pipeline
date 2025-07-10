# graph/graph_builder.py

from langgraph.graph import StateGraph
from graph.agents.supervisor_agent import supervisor_executor as supervisor_runnable
from graph.nodes.entry import entry_node  # keep this simple entry node
from langgraph.graph import END

from typing import Annotated, Optional, TypedDict
import operator


class PipelineState(TypedDict, total=False):
    file_path: list[str]
    file_content: Optional[list[str]]
    gpt_data: dict
    smol_extracted: dict
    evaluation_score: float
    evaluation_passed: bool
    evaluation_feedback: str
    retry_attempts: int
    final_doc: str
    final_output_text: str
    final_document_path: str
    user_prompt: Optional[list[str]]
    chat_history: Optional[list[str]]
    dummy_context: Optional[str]
    instructions: Optional[str]
    input_type: list[str]
    status_updates: Annotated[list[str], operator.add]


def build_graph():
    builder = StateGraph(PipelineState)

    builder.add_node("entry", entry_node)
    builder.add_node("supervisor", supervisor_runnable)

    builder.set_entry_point("entry")
    builder.add_edge("entry", "supervisor")

    builder.add_edge("supervisor", END)
    
    return builder.compile()
