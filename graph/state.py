# graph/state.py

from langgraph.graph.message import add_messages
from typing import Annotated, Optional, TypedDict
from langchain_core.messages import BaseMessage


class PipelineState(TypedDict, total=False):
    # File handling
    file_path: list[str]
    file_content: Optional[list[str]]

    # Processing results
    gpt_data: dict
    smol_extracted: dict
    evaluation_score: float
    evaluation_passed: bool
    evaluation_feedback: str
    retry_attempts: int
    final_doc: str
    final_output_text: str
    final_document_path: str

    # User interaction
    user_prompt: Optional[list[str]]
    chat_history: Optional[list[BaseMessage]]
    dummy_context: Optional[str]
    instructions: Optional[str]
    input_type: list[str]

    # Status tracking
    # Remove the Annotated wrapper to avoid conflicts
    status_updates: list[str]

    # Agent communication (for LangGraph compatibility)
    messages: Optional[list[BaseMessage]]
