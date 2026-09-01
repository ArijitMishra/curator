import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import AgentState
from llm import generate


def summarize_papers(state: AgentState) -> AgentState:
    filtered_papers = state["filtered_papers"]
    summaries = []

    for paper in filtered_papers:
        prompt = f"""You are a research assistant. Summarize the following paper in 3-4 sentences for a technical audience.
                Title: {paper['title']}
                Abstract: {paper['abstract']}

                Write a concise summary highlighting the key contribution, method, and result.
                """
        
        summary = generate(prompt)
        summaries.append({
            "title": paper["title"],
            "authors": paper["authors"],
            "url": paper["url"],
            "published": paper["published"],
            "summary": summary
        })
        print(f"Summarized: {paper['title'][:60]}...")
    state["summaries"] = summaries
    return state

if __name__ == "__main__":
    from nodes.fetcher import fetch_papers
    from nodes.filter import filter_papers

    from config import load_config
    config = load_config()

    test_state: AgentState = {
        "topics": config["topics"],
        "raw_papers": [],
        "filtered_papers": [],
        "summaries": [],
        "digest": ""
    }

    print("Fetching papers...")
    test_state = fetch_papers(test_state)
    print(f"Fetched {len(test_state['raw_papers'])} papers")

    print("Filtering...")
    test_state = filter_papers(test_state)
    print(f"Filtered to {len(test_state['filtered_papers'])} papers")

    print("Summarizing...")
    result = summarize_papers(test_state)

    print(f"\nSummaries ({len(result['summaries'])}):")
    for s in result["summaries"]:
        print(f"\nTitle: {s['title']}")
        print(f"Summary: {s['summary']}")
        print("---")
    print("summarizer.py OK")