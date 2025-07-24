# graph/graph_builder.py

from langgraph.graph import StateGraph, END
from graph.agents.supervisor_agent import (
    call_supervisor_model,
    call_tools,
    should_continue_supervisor
)
from graph.nodes.entry import entry_node
from graph.state import PipelineState


def build_graph():
    builder = StateGraph(PipelineState)

    # Add the entry node
    builder.add_node("entry", entry_node)

    # Add supervisor nodes following ReAct pattern
    builder.add_node("supervisor", call_supervisor_model)
    builder.add_node("tools", call_tools)

    # Set entry point
    builder.set_entry_point("entry")

    # Entry flows to supervisor
    builder.add_edge("entry", "supervisor")

    # Add conditional edge from supervisor
    builder.add_conditional_edges(
        "supervisor",
        should_continue_supervisor,
        {
            "continue": "tools",  # If model wants to use tools
            "end": END,          # If model is done
        },
    )

    # After tools, go back to supervisor for next iteration
    builder.add_edge("tools", "supervisor")

    return builder.compile()
