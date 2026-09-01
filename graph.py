from langgraph.graph import StateGraph, END

from state import AgentState
from nodes.fetcher import fetch_papers
from nodes.filter import filter_papers
from nodes.summarizer import summarize_papers
from nodes.formatter import format_digest
from nodes.delivery import deliver
from nodes.commentary import generate_commentary
from config import load_config


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    #Add nodes
    graph.add_node("fetcher", fetch_papers)
    graph.add_node("filter", filter_papers)
    graph.add_node("summarizer", summarize_papers)
    graph.add_node("commentary", generate_commentary)
    graph.add_node("formatter", format_digest)
    graph.add_node("delivery", deliver)

    #Wire edges
    graph.set_entry_point("fetcher")
    graph.add_edge("fetcher","filter")
    graph.add_edge("filter","summarizer")
    graph.add_edge("summarizer","commentary")
    graph.add_edge("commentary","formatter")
    graph.add_edge("formatter","delivery")
    graph.add_edge("delivery",END)

    return graph.compile()

if __name__ == "__main__":
    config = load_config()

    initial_state: AgentState = {
        "topics": config["topics"],
        "raw_papers": [],
        "filtered_papers": [],
        "summaries": [],
        "commentary":"",
        "digest": ""
    }

    print("Building graph...")
    graph = build_graph()
    print(graph.get_graph().draw_mermaid())
    print("Running graph...")
    result = graph.invoke(initial_state)

    print(f"\nPipeline complete.")
    print(f"Raw papers fetched: {len(result['raw_papers'])}")
    print(f"Filtered papers: {len(result['filtered_papers'])}")
    print(f"Summaries: {len(result['summaries'])}")
    print(f"Digest preview:\n{result['digest'][:300]}")
    print("graph.py OK")