import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import AgentState
from config import load_config
from llm import generate

def filter_papers(state: AgentState) -> AgentState:
    config = load_config()
    raw_papers = state["raw_papers"]
    topics = state["topics"]
    top_n = config["top_n"]

    papers_text = "\n".join([
        f"[{i}] {p['title']}: {p['abstract'][:200]}"
        for i, p in enumerate(raw_papers)
    ])

    prompt = f"""You are a research curator. Return EXACTLY {top_n} indices of the most relevant papers.

Topics: {", ".join(topics)}

Papers:
{papers_text}

Rules:
- Return EXACTLY {top_n} numbers
- Comma-separated only
- No explanation, no text, just numbers
- Example format: 0,2,4,7,11

Your answer:"""

    response = generate(prompt)
    print("Raw LLM response:", response)
    # parse indices
    indices = [int(x.strip()) for x in response.strip().split(",") if x.strip().isdigit()]
    filtered = [raw_papers[i] for i in indices if i < len(raw_papers)]

    state["filtered_papers"] = filtered
    return state


if __name__ == "__main__":
    from nodes.fetcher import fetch_papers

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
    result = filter_papers(test_state)

    print(f"\nFiltered to {len(result['filtered_papers'])} papers:")
    for p in result["filtered_papers"]:
        print("-", p["title"])
    print("filter.py OK")