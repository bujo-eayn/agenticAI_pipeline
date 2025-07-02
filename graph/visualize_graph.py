# graph/visualize_graph.py

from graph.graph_builder import build_graph


def visualize():
    graph = build_graph()
    print(graph.get_graph().print_ascii())
    graph.get_graph().draw_png("pipeline_graph.png")
    print("✅ Graph visual saved to pipeline_graph.png")


if __name__ == "__main__":
    visualize()
