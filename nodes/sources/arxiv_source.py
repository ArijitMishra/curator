import arxiv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from state import Paper

def fetch(topics: list[str], top_n: int) -> list[Paper]:
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
    return raw_papers


if __name__ == "__main__":
    results = fetch(["AI agents", "LLM reasoning"], top_n=5)
    print(f"Fetched {len(results)} papers from Arxiv")
    for p in results[:3]:
        print(f"- {p['title']}")
        print(f"  Authors: {p['authors'][:2]}")
        print(f"  URL: {p['url']}")
        print("---")
    print("arxiv.py OK")