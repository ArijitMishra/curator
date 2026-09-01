import os
import sys
from datetime import date
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import AgentState

def format_digest(state:AgentState) -> AgentState:
    summaries = state["summaries"]
    today = date.today().strftime("%B %d, %Y")

    lines = []
    lines.append(f"# AI Research Digest- {today}\n")
    lines.append(f"**Topics:** {','.join(state["topics"])}\n")
    lines.append(f"**Papers curated:** {len(summaries)}\n")
    lines.append("---\n")

    for i,s in enumerate(summaries,1):
        lines.append(f"## {i}. {s['title']}")
        lines.append(f"**Authors:** {', '.join(s['authors'][:3])}")
        lines.append(f"**Published:** {s['published']}")
        lines.append(f"**URL:** {s['url']}")
        lines.append(f"\n{s['summary']}\n")
        lines.append("## Commentary\n")
        lines.append(state["commentary"])
        lines.append("---\n")

    state["digest"] = "\n".join(lines)
    return state

if __name__ == "__main__":
    # test with dummy data
    test_state: AgentState = {
        "topics": ["AI agents", "LLM reasoning"],
        "raw_papers": [],
        "filtered_papers": [],
        "summaries": [
            {
                "title": "Dummy Paper Title",
                "authors": ["Author One", "Author Two"],
                "url": "https://arxiv.org/abs/0000.00000",
                "published": "2026-08-31",
                "summary": "This is a dummy summary of the paper."
            }
        ],
        "commentary":"",
        "digest": ""
    }

    result = format_digest(test_state)
    print(result["digest"])
    print("formatter.py OK")