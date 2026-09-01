import os
import sys
from datetime import date
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import AgentState

def deliver(state: AgentState) -> AgentState:
    digest = state["digest"]
    today = date.today().strftime("%d-%m-%Y")

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, f"digest_{today}.md")

    with open(filepath, "w") as f:
        f.write(digest)

    print(f"Digest saved to {output_dir}")
    return state

if __name__ == "__main__":
    test_state: AgentState = {
        "topics": ["AI agents", "LLM reasoning"],
        "raw_papers": [],
        "filtered_papers": [],
        "summaries": [],
        "digest": "# AI Research Digest\n\nThis is a test digest."
    }

    result = deliver(test_state)
    print("delivery.py OK")