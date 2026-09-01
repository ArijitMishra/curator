import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import requests
from datetime import date
from state import Paper


def fetch(topics: list[str], top_n: int) -> list[Paper]:
    papers = []
    seen = set()

    today = str(date.today())
    url = f"https://huggingface.co/api/daily_papers?date={today}&limit=50"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"HF Daily Papers API error: {response.status_code}")
        return []

    daily = response.json()

    topic_results = []
    for topic in topics:
        search_url = f"https://huggingface.co/api/papers/search?q={topic}&limit={top_n}"
        r = requests.get(search_url)
        if r.status_code == 200:
            topic_results.extend(r.json())

    all_results = daily + topic_results
    for item in all_results:
        paper_data = item.get("paper", item)  # daily papers nest under "paper"
        arxiv_id = paper_data.get("id", "")

        if not arxiv_id or arxiv_id in seen:
            continue

        seen.add(arxiv_id)

        authors = paper_data.get("authors", [])
        author_names = [a.get("name", "") for a in authors]

        paper: Paper = {
            "title": paper_data.get("title", ""),
            "authors": author_names,
            "abstract": paper_data.get("summary", ""),
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "published": paper_data.get("publishedAt", "")[:10]
        }
        papers.append(paper)

    return papers

if __name__ == "__main__":
    results = fetch(["AI agents", "LLM reasoning"], top_n=5)
    print(f"Fetched {len(results)} papers from HF")
    for p in results[:3]:
        print(f"- {p['title']}")
        print(f"  Authors: {p['authors'][:2]}")
        print(f"  URL: {p['url']}")
        print("---")
    print("hf_papers.py OK")