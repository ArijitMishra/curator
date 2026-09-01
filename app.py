import streamlit as st
import os
import json
from datetime import date
from config import load_config
from graph import build_graph

CACHE_FILE = "outputs/last_run.json"

def load_last_run():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return None

def save_last_run(topics, state):
    os.makedirs("outputs", exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump({
            "topics": topics,
            "raw_papers": state["raw_papers"],
            "summaries": state["summaries"],
            "commentary": state["commentary"],
            "date": str(date.today())
        }, f)

def run_pipeline(topics):
    initial_state = {
        "topics": topics,
        "raw_papers": [],
        "filtered_papers": [],
        "summaries": [],
        "commentary": "",
        "digest": ""
    }
    graph = build_graph()
    return graph.invoke(initial_state)

# -- UI --
st.set_page_config(layout="wide", page_title="Research Curator")
st.title("Research Curator")

config = load_config()

# init session state
if "summaries" not in st.session_state:
    st.session_state.summaries = []
if "commentary" not in st.session_state:
    st.session_state.commentary = ""
if "raw_papers" not in st.session_state:
    st.session_state.raw_papers = []
if "has_results" not in st.session_state:
    st.session_state.has_results = False

# topic input
topic_input = st.text_area(
    "Topics (One per line)",
    value="\n".join(config["topics"]),
    height=100
)
topics = [t.strip() for t in topic_input.strip().split("\n") if t.strip()]

run_button = st.button("Fetch Papers")

last_run = load_last_run()
same_topics = last_run and sorted(last_run["topics"]) == sorted(topics)

if run_button:
    if same_topics and last_run and last_run["date"] == str(date.today()):
        st.info("Same topics, loading from last run...")
        st.session_state.summaries = last_run["summaries"]
        st.session_state.commentary = last_run["commentary"]
        st.session_state.raw_papers = last_run.get("raw_papers", [])
    else:
        with st.spinner("Running pipeline... This might take some time."):
            results = run_pipeline(topics)
            save_last_run(topics, results)
            st.session_state.summaries = results["summaries"]
            st.session_state.commentary = results["commentary"]
            st.session_state.raw_papers = results["raw_papers"]
    st.session_state.has_results = True

# display
if st.session_state.has_results:
    show_all = st.toggle("Show all fetched papers", value=False)
    left, right = st.columns([1, 1])

    with left:
        st.subheader("Papers")
        if show_all:
            st.caption(f"Showing all {len(st.session_state.raw_papers)} fetched papers")
            for i, p in enumerate(st.session_state.raw_papers, 1):
                with st.expander(f"{i}. {p['title']}"):
                    st.markdown(f"**Authors:** {', '.join(p['authors'][:3])}")
                    st.markdown(f"**Published:** {p['published']}")
                    st.markdown(f"**URL:** [Link]({p['url']})")
                    st.markdown(f"**Abstract:** {p['abstract'][:300]}...")
        else:
            st.caption(f"Showing {len(st.session_state.summaries)} curated papers")
            for i, s in enumerate(st.session_state.summaries, 1):
                with st.expander(f"{i}. {s['title']}"):
                    st.markdown(f"**Authors:** {', '.join(s['authors'][:3])}")
                    st.markdown(f"**Published:** {s['published']}")
                    st.markdown(f"**URL:** [Link]({s['url']})")
                    st.markdown(f"**Summary:** {s['summary']}")

    with right:
        st.subheader("Commentary")
        st.markdown(st.session_state.commentary)

elif last_run:
    st.info(f"Last run: {last_run['date']} | Topics: {', '.join(last_run['topics'])}")
    st.caption("Press 'Fetch Papers' to refresh or update topics.")