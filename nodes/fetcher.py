import arxiv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import AgentState, Paper
from config import load_config

def fetch_papers(state: AgentState) -> AgentState:
    config = load_config()
    topics = state["topics"]
    top_n = config["top_n"]

    raw_papers = []
    searchClient = arxiv.Client()
    seen = set()
    for topic in topics:
        search = arxiv.Search(
            query = topic,
            max_results = top_n,
            sort_by = arxiv.SortCriterion.SubmittedDate
        )

        for result in searchClient.results(search):
            if result.entry_id in seen:
                continue
            paper: Paper = {
                "title": result.title,
                "authors": [a.name for a in result.authors],
                "abstract": result.summary,
                "url": result.entry_id,
                "published": str(result.published.date())
            }
            seen.add(result.entry_id)
            raw_papers.append(paper)
    # seen = set()
    # unique_papers = []
    # for paper in raw_papers:
    #     if paper['url'] not in seen:
    #         unique_papers.append(paper)
    #         seen.add(paper['url'])

    state["raw_papers"] = raw_papers
    return state

if __name__ == "__main__":
    config = load_config()
    
    test_state: AgentState = {
        "topics": config["topics"],
        "raw_papers": [],
        "filtered_papers": [],
        "summaries": [],
        "commentary":"",
        "digest": ""
    }
    
    result = fetch_papers(test_state)
    
    print(f"Fetched {len(result['raw_papers'])} papers\n")
    for p in result["raw_papers"][:3]:
        print("Title:", p["title"])
        print("Authors:", p["authors"][:2])
        print("Published:", p["published"])
        print("URL:", p["url"])
        print("---")
    print("fetcher.py OK")