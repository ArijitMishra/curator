# Research Curator

An AI-powered research paper curator built with LangGraph. Give it any topic, and it fetches, filters, summarizes, and delivers a curated digest of the latest papers — with a high-level commentary on trends.

---

## What it does

1. **Fetches** papers from Arxiv and HuggingFace Daily Papers
2. **Filters** the most relevant papers using an LLM
3. **Summarizes** each paper
4. **Generates commentary** on trends and key findings across all fetched papers
5. **Delivers** a markdown digest saved to file
6. **Displays** everything in a Streamlit web UI

---

## Project Structure

```
research-curator/
├── app.py                  # Streamlit UI
├── graph.py                # LangGraph pipeline wiring
├── llm.py                  # Model loading (runs on local GPU)
├── state.py                # Shared state schema
├── config.py               # Loads .env and topics.yaml
├── main.py                 # Run pipeline manually
├── topics.yaml             # Your topics and settings
├── nodes/
│   ├── fetcher.py          # Orchestrates all paper sources
│   ├── filter.py           # LLM-based relevance filtering
│   ├── summarizer.py       # LLM-based summarization
│   ├── commentary.py       # LLM trend analysis
│   ├── formatter.py        # Builds markdown digest
│   ├── delivery.py         # Saves digest to file
│   └── sources/
│       ├── arxiv_source.py # Arxiv paper fetcher
│       └── hf_papers.py    # HuggingFace Daily Papers fetcher
└── outputs/                # Generated digests saved here
```

---

## Pipeline

```
Arxiv + HF Papers
       ↓
    Fetcher  (deduplicates across sources)
       ↓
    Filter   (LLM picks most relevant, gemma-3-1b-it)
       ↓
   Summarizer (LLM summarizes each paper, gemma-3-1b-it)
       ↓
  Commentary  (LLM trend analysis across all papers, Qwen2.5-3B-Instruct)
       ↓
   Formatter  (builds markdown digest)
       ↓
   Delivery   (saves to outputs/)
```

---

## Requirements

- Python 3.10+
- NVIDIA GPU with 8GB+ VRAM (runs models locally)
- CUDA installed
- HuggingFace account + API token (for model downloads)

---

## Setup

**1. Clone and create virtual environment**
```bash
git clone https://github.com/yourusername/research-curator.git
cd research-curator
python3 -m venv venv
source venv/bin/activate
```

**2. Install dependencies**
```bash
pip install langgraph langchain langchain-core langchain-huggingface
pip install transformers torch accelerate
pip install arxiv requests pyyaml python-dotenv
pip install streamlit apscheduler
```

**3. Set up environment**
```bash
cp .env.example .env
# edit .env and add your HuggingFace token
```

`.env`:
```
HUGGINGFACEHUB_API_TOKEN=hf_xxxxxxxxxxxx
```

**4. Accept model licenses on HuggingFace**

Both models require accepting terms before first use:
- [google/gemma-3-1b-it](https://huggingface.co/google/gemma-3-1b-it)
- [Qwen/Qwen2.5-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct)

Then login:
```bash
huggingface-cli login
```

**5. Configure topics**

Edit `topics.yaml`:
```yaml
topics:
  - "machine learning"
  - "computer vision"
  - "robotics"
top_n: 5
schedule: "08:00"
delivery: "file"
```

---

## Usage

**Run via UI:**
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

**Run pipeline directly:**
```bash
python main.py
```

Output saved to `outputs/digest_YYYY-MM-DD.md`

---

## UI Features

- Enter any topics in the text box
- Click **Fetch Papers** to run the full pipeline
- Toggle **Show all fetched papers** to see everything fetched before filtering
- Curated papers shown with title, authors, published date, link, and summary
- Commentary panel shows trend analysis across all papers
- Results cached — same topics on same day loads instantly without re-running

---

## Models

| Model | Used for | VRAM |
|---|---|---|
| `google/gemma-3-1b-it` | Filter + Summarize | ~2GB |
| `Qwen/Qwen2.5-3B-Instruct` | Commentary | ~6GB |

Models load and unload sequentially to fit within 8GB VRAM. First run downloads models (~5GB total).

---

## Extending

The fetcher is modular — add new sources by creating a file in `nodes/sources/` with a `fetch(topics, top_n) -> list[Paper]` function and importing it in `nodes/fetcher.py`.

Topics are fully interchangeable — works for any research domain, not just AI.