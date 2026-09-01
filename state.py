from typing import TypedDict, List

class Paper(TypedDict):
    title: str
    authors: List[str]
    abstract: str
    url: str
    published: str

class AgentState(TypedDict):
    topics: List[str]
    raw_papers: List[Paper]
    filtered_papers: List[Paper]
    summaries: List[dict]
    commentary: str
    digest: str

if __name__ == "__main__":
    #Test code
    state: AgentState = {
        "topics": ["AI Agents", "LLM reasoning"],
        "raw_papers":[],
        "filtered_papers":[],
        "summaries":[],
        "commentary":"",
        "digest":""
    }
    print(state)
    print("Keys",list(state.keys()))
    print("State.py end")
