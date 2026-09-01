from graph import build_graph
from config import load_config

def run_pipeline():
    config = load_config()
    initial_state = {
        "topics": config["topics"],
        "raw_papers": [],
        "filtered_papers": [],
        "summaries": [],
        "digest": ""
    }

    print(f"Running pipeline...")
    graph = build_graph()
    graph.invoke(initial_state)
    print("Pipeline complete")

if __name__ == "__main__":
    run_pipeline()
