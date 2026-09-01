import arxiv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import AgentState, Paper
from config import load_config
from nodes.sources.arxiv_source import fetch as fetch_arxiv
from nodes.sources.hf_papers import fetch as fetch_hf

def fetch_papers(state: AgentState) -> AgentState:
    config = load_config()
    topics = state["topics"]
    top_n = config["top_n"]

    raw_papers = []
    searchClient = arxiv.Client()
    seen = set()
    for paper in fetch_arxiv(topics, top_n) + fetch_hf(topics, top_n):
        if paper["url"] not in seen:
            seen.add(paper["url"])
            raw_papers.append(paper)

    state["raw_papers"] = raw_papers
    return state

if __name__ == "__main__":
    config = load_config()

    test_state: AgentState = {
        "topics": config["topics"],
        "raw_papers": [],
        "filtered_papers": [],
        "summaries": [],
        "commentary": "",
        "digest": ""
    }

    result = fetch_papers(test_state)
    print(f"Total papers fetched: {len(result['raw_papers'])}")
    for p in result["raw_papers"][:5]:
        print(f"- [{p['published']}] {p['title']}")
    print("fetcher.py OK")