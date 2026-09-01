import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from state import AgentState
from llm import generate

def generate_commentary(state: AgentState) -> AgentState:
    summaries = state["summaries"]
    topics = state["topics"]

    summaries_text = "\n".join([
        f"- {s['title']}: {s['summary']}"
        for s in summaries
    ])

    prompt = f"""You are an expert AI research analyst. Based on the following recent papers, provide a high-level commentary (5-7 sentences) covering:
- Key trends you observe
- Most exciting or surprising work
- What directions the field seems to be moving

Topics being tracked: {", ".join(topics)}

Recent papers:
{summaries_text}

Write your commentary:"""
    commentary = generate(prompt, model_type="commentary")
    state["commentary"] = commentary
    return state

if __name__ == "__main__":
    test_state: AgentState = {
        "topics": ["AI agents", "LLM reasoning"],
        "raw_papers": [],
        "filtered_papers": [],
        "summaries": [
            {
                "title": "Advances in LLM Reasoning",
                "authors": ["Author One"],
                "url": "https://arxiv.org/abs/0000.00000",
                "published": "2026-08-31",
                "summary": "This paper proposes a new reasoning framework for LLMs."
            }
        ],
        "commentary":"",
        "digest": ""
    }

    result = generate_commentary(test_state)
    print("Commentary:", result["commentary"])
    print("commentary.py OK")