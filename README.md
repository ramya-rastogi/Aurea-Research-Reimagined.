<div align="center">

# ✦ Aurea
### *Research, Reimagined.*

**A multi-agent AI research system that searches, scrapes, writes, and critiques — so you don't have to.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.x-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)](https://langchain.com)


</div>

---

## What is Aurea?

Aurea is a **multi-agent AI research pipeline** with a polished Streamlit UI. Give it any topic — from *fusion energy progress* to *CRISPR gene editing* — and four specialized AI agents collaborate in sequence to deliver a structured, critiqued research report in minutes.

No manual Googling. No copy-pasting from tabs. No blank-page paralysis. Just a topic in, a report out.

---

## How It Works

Aurea runs four agents in a fixed pipeline, each handing its output to the next:

```
Topic Input
    │
    ▼
┌─────────────────────────────────────────────────┐
│  01  Search Agent   — finds recent, reliable    │
│                        web sources for the topic│
├─────────────────────────────────────────────────┤
│  02  Reader Agent   — picks the best URL and    │
│                        scrapes it for depth     │
├─────────────────────────────────────────────────┤
│  03  Writer Chain   — synthesises all findings  │
│                        into a structured report │
├─────────────────────────────────────────────────┤
│  04  Critic Chain   — reviews the report and    │
│                        surfaces improvements    │
└─────────────────────────────────────────────────┘
    │
    ▼
Final Report + Critic Feedback
```

Each step updates **live** in the UI — you watch the pipeline light up as agents complete their work.

---

## Features

- **Live pipeline tracker** — four step-cards animate in real time: idle → running → done
- **Native Markdown report rendering** — headings, lists, and emphasis render properly, not as raw text
- **Critic feedback panel** — a second agent reviews the report and flags gaps or improvements
- **Raw data expanders** — inspect the search results and scraped content that fed the report
- **Two download formats** — the report as `.md`, or the full run output as `.txt`
- **Example topic chips** — one-click inspiration if you're not sure where to start
- **Dark, minimal UI** — Playfair Display + Inter + JetBrains Mono, space-navy palette with aurora-gold accents

---

## Project Structure

```
Aurea/
├── app.py            # Streamlit UI — the entry point
├── pipeline.py       # Orchestrates the full 4-step agent run
├── agents.py         # Builds each agent and chain (search, reader, writer, critic)
├── tools.py          # Tool definitions used by the agents
└── requirements.txt  # Python dependencies
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/ramya-rastogi/Aurea-Research-Reimagined..git
cd Aurea-Research-Reimagined.
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your API keys

Aurea uses an LLM provider (e.g. OpenAI) and a search tool. Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here      # or whichever search tool your agents.py uses
```

> Check `agents.py` and `tools.py` to confirm which keys your setup requires.

### 4. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage

1. Type a research topic into the input field (or click one of the example chips)
2. Hit **✦ Begin Research**
3. Watch the pipeline tracker — each agent card lights up as it runs
4. Read the final report and critic feedback when the run completes
5. Download the report as `.md` or the full output as `.txt`

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Agent orchestration | LangChain / LangGraph |
| Web search | Tavily (or configured search tool) |
| Web scraping | Reader agent via tool in `tools.py` |
| LLM backbone | OpenAI GPT (configurable in `agents.py`) |
| Fonts | Playfair Display, Inter, JetBrains Mono |

---

## Running Without the UI

The pipeline can also be run headlessly from the terminal:

```bash
python pipeline.py
```

You'll be prompted to enter a topic, and results will print to stdout.

---


**✦ Aurea — Research, Reimagined.**

</div>
