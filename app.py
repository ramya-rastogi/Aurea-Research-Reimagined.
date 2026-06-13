import streamlit as st
import sys
import time
from io import StringIO

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Aurea — Research, Reimagined",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0B0F1A !important;
    color: #F0EDE8;
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background-color: #0B0F1A;
}

[data-testid="stHeader"] {
    background-color: #0B0F1A !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

/* ── Hero ── */
.hero-wrapper {
    text-align: center;
    padding: 3.5rem 0 2rem;
}

.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #E8C97A;
    margin-bottom: 1rem;
    opacity: 0.85;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.6rem, 6vw, 4rem);
    font-weight: 700;
    color: #F0EDE8;
    line-height: 1.1;
    margin: 0 0 0.35rem;
    letter-spacing: -0.02em;
}

.hero-title span {
    color: #E8C97A;
    font-style: italic;
}

.hero-tagline {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1.05rem;
    color: #8A8FAA;
    margin: 0;
    letter-spacing: 0.01em;
}

.hero-rule {
    width: 48px;
    height: 1.5px;
    background: linear-gradient(90deg, #E8C97A, transparent);
    margin: 1.6rem auto 0;
}

/* ── Input area ── */
.input-section {
    max-width: 640px;
    margin: 2.5rem auto 0;
}

.input-label {
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6A6F85;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.5rem;
}

/* Streamlit text_input override */
[data-testid="stTextInput"] input {
    background-color: #131929 !important;
    border: 1px solid #252D45 !important;
    border-radius: 6px !important;
    color: #F0EDE8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}

[data-testid="stTextInput"] input:focus {
    border-color: #E8C97A !important;
    box-shadow: 0 0 0 3px rgba(232,201,122,0.08) !important;
    outline: none !important;
}

[data-testid="stTextInput"] label {
    color: #6A6F85 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
}

/* ── Button ── */
[data-testid="stButton"] button {
    width: 100%;
    background: linear-gradient(135deg, #E8C97A 0%, #C9A84C 100%) !important;
    color: #0B0F1A !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em !important;
    padding: 0.7rem 2rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.1s !important;
    margin-top: 0.5rem !important;
}

[data-testid="stButton"] button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

[data-testid="stButton"] button:active {
    transform: translateY(0) !important;
}

/* ── Pipeline tracker ── */
.pipeline-wrapper {
    max-width: 640px;
    margin: 3rem auto 0;
}

.pipeline-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4A5AE8;
    margin-bottom: 1.2rem;
}

.step-card {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem 1.2rem;
    border-radius: 8px;
    margin-bottom: 0.6rem;
    border: 1px solid transparent;
    transition: all 0.3s ease;
    background: #0D1220;
}

.step-card.idle {
    border-color: #1C2338;
    opacity: 0.45;
}

.step-card.active {
    border-color: #4A5AE8;
    background: #0F1628;
    opacity: 1;
    box-shadow: 0 0 20px rgba(74,90,232,0.12);
}

.step-card.done {
    border-color: #2A3828;
    background: #0D1A12;
    opacity: 1;
}

.step-icon {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    margin-top: 0.1rem;
}

.step-icon.idle   { background: #161D30; color: #3A4055; }
.step-icon.active { background: #1A1F3A; color: #4A5AE8; }
.step-icon.done   { background: #162415; color: #4CAF72; }

.step-body { flex: 1; }

.step-name {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.88rem;
    color: #C8C5C0;
    margin-bottom: 0.15rem;
}

.step-name.active { color: #F0EDE8; }
.step-name.done   { color: #8FBF96; }

.step-desc {
    font-size: 0.75rem;
    color: #4A5060;
    font-family: 'Inter', sans-serif;
}

.step-desc.active { color: #6870A0; }
.step-desc.done   { color: #4A6A50; }

.spinner {
    display: inline-block;
    width: 10px;
    height: 10px;
    border: 1.5px solid #4A5AE8;
    border-top-color: transparent;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    margin-right: 6px;
    vertical-align: middle;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* ── Result panels ── */
.result-section {
    max-width: 640px;
    margin: 2.5rem auto 0;
}

.result-panel {
    background: #0D1220;
    border: 1px solid #1C2338;
    border-radius: 10px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1.2rem;
}

.result-panel-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
}

.result-panel-icon {
    font-size: 1rem;
}

.result-panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #E8C97A;
}

.result-panel-body {
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    line-height: 1.75;
    color: #B8B5B0;
    white-space: pre-wrap;
    word-break: break-word;
}

/* Scrollable boxes for raw content */
.scrollable {
    max-height: 240px;
    overflow-y: auto;
    padding-right: 0.3rem;
}

.scrollable::-webkit-scrollbar { width: 4px; }
.scrollable::-webkit-scrollbar-track { background: #0B0F1A; }
.scrollable::-webkit-scrollbar-thumb { background: #252D45; border-radius: 2px; }

/* ── Divider ── */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #E8C97A44, transparent);
    margin: 2.5rem 0;
}

/* ── Error box ── */
.error-box {
    background: #1A0D0D;
    border: 1px solid #4A1515;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    color: #C87A7A;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
    max-width: 640px;
    margin: 1.5rem auto 0;
}

/* ── Footer ── */
.aurea-footer {
    text-align: center;
    padding: 3rem 0 2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    color: #2A2F42;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <p class="hero-eyebrow">✦ Multi-Agent Intelligence ✦</p>
    <h1 class="hero-title">Au<span>rea</span></h1>
    <p class="hero-tagline">Research, Reimagined.</p>
    <div class="hero-rule"></div>
</div>
""", unsafe_allow_html=True)


# ── Input ──────────────────────────────────────────────────────────────────────
col_pad1, col_main, col_pad2 = st.columns([0.08, 0.84, 0.08])
with col_main:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. The future of nuclear fusion energy",
        label_visibility="visible",
    )
    run_btn = st.button("✦  Begin Research", use_container_width=True)


# ── Pipeline step definitions ──────────────────────────────────────────────────
STEPS = [
    {
        "icon": "⌕",
        "name": "Search Agent",
        "desc": "Scours the web for recent, reliable sources",
        "key": "search",
    },
    {
        "icon": "⛏",
        "name": "Reader Agent",
        "desc": "Scrapes & extracts content from top URLs",
        "key": "reader",
    },
    {
        "icon": "✍",
        "name": "Writer Chain",
        "desc": "Synthesises findings into a structured report",
        "key": "writer",
    },
    {
        "icon": "◈",
        "name": "Critic Chain",
        "desc": "Reviews the report and surfaces improvements",
        "key": "critic",
    },
]


def render_pipeline(active_key: str | None, done_keys: list[str]):
    """Render the 4-step pipeline tracker."""
    html = '<div class="pipeline-wrapper">'
    html += '<p class="pipeline-header">— Live pipeline —</p>'
    for step in STEPS:
        k = step["key"]
        if k in done_keys:
            state_cls = "done"
            icon_char = "✓"
        elif k == active_key:
            state_cls = "active"
            icon_char = step["icon"]
        else:
            state_cls = "idle"
            icon_char = step["icon"]

        spinner_html = '<span class="spinner"></span>' if state_cls == "active" else ""

        html += f"""
        <div class="step-card {state_cls}">
            <div class="step-icon {state_cls}">{icon_char}</div>
            <div class="step-body">
                <div class="step-name {state_cls}">{spinner_html}{step['name']}</div>
                <div class="step-desc {state_cls}">{step['desc']}</div>
            </div>
        </div>"""
    html += "</div>"
    return html


def render_result_panel(icon: str, title: str, body: str, scrollable: bool = False):
    scroll_cls = "scrollable" if scrollable else ""
    return f"""
    <div class="result-panel">
        <div class="result-panel-header">
            <span class="result-panel-icon">{icon}</span>
            <span class="result-panel-title">{title}</span>
        </div>
        <div class="result-panel-body {scroll_cls}">{body}</div>
    </div>
    """


# ── Session state ──────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "error" not in st.session_state:
    st.session_state.error = None


# ── Run pipeline ───────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.markdown(
            '<div class="error-box">⚠ Please enter a research topic before starting.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.session_state.results = None
        st.session_state.error = None

        # Import here so the app still loads even if deps are missing
        try:
            from pipeline import run_research_pipeline  # noqa: E402
        except ImportError as e:
            st.session_state.error = f"Import error: {e}"
            st.rerun()

        # ── Animated pipeline execution ──
        col_pad1, col_run, col_pad2 = st.columns([0.08, 0.84, 0.08])
        with col_run:
            pipeline_placeholder = st.empty()
            results_placeholder = st.empty()

        done_keys: list[str] = []
        step_results: dict = {}

        def show_step(active_key):
            pipeline_placeholder.markdown(
                render_pipeline(active_key, done_keys), unsafe_allow_html=True
            )

        # We monkey-patch the pipeline to intercept step-by-step results
        # by running it step by step using the same logic from pipeline.py
        try:
            from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

            state = {}

            # ── Step 1: Search ──
            show_step("search")
            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state["search_results"] = search_result["messages"][-1].content
            done_keys.append("search")
            step_results["search"] = state["search_results"]

            # ── Step 2: Reader ──
            show_step("reader")
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scraped_content"] = reader_result["messages"][-1].content
            done_keys.append("reader")
            step_results["reader"] = state["scraped_content"]

            # ── Step 3: Writer ──
            show_step("writer")
            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined,
            })
            done_keys.append("writer")
            step_results["writer"] = state["report"]

            # ── Step 4: Critic ──
            show_step("critic")
            state["feedback"] = critic_chain.invoke({"report": state["report"]})
            done_keys.append("critic")
            step_results["critic"] = state["feedback"]

            # All done — no active step
            show_step(None)
            st.session_state.results = step_results

        except Exception as exc:
            st.session_state.error = str(exc)
            show_step(None)

        st.rerun()


# ── Show persisted results ─────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(
        f'<div class="error-box">⚠ {st.session_state.error}</div>',
        unsafe_allow_html=True,
    )

if st.session_state.results:
    r = st.session_state.results

    col_pad1, col_res, col_pad2 = st.columns([0.08, 0.84, 0.08])
    with col_res:
        # Show completed pipeline
        st.markdown(
            render_pipeline(None, ["search", "reader", "writer", "critic"]),
            unsafe_allow_html=True,
        )

        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="result-section">', unsafe_allow_html=True)

        # Final report (hero panel)
        import html as _html
        report_text = r.get("writer", "")
        st.markdown(
            render_result_panel("✍", "Final Report", _html.escape(report_text)),
            unsafe_allow_html=True,
        )

        # Critic feedback
        feedback_text = r.get("critic", "")
        st.markdown(
            render_result_panel("◈", "Critic Feedback", _html.escape(feedback_text)),
            unsafe_allow_html=True,
        )

        # Collapsible raw data
        with st.expander("View raw search & scrape data"):
            st.markdown(
                render_result_panel(
                    "⌕", "Search Agent Output",
                    _html.escape(r.get("search", "")),
                    scrollable=True,
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                render_result_panel(
                    "⛏", "Reader Agent Output",
                    _html.escape(r.get("reader", "")),
                    scrollable=True,
                ),
                unsafe_allow_html=True,
            )

        # Download button
        full_output = (
            f"AUREA RESEARCH REPORT\nTopic: {topic}\n"
            f"{'='*60}\n\n"
            f"REPORT\n{report_text}\n\n"
            f"CRITIC FEEDBACK\n{feedback_text}\n\n"
            f"SEARCH RESULTS\n{r.get('search','')}\n\n"
            f"SCRAPED CONTENT\n{r.get('reader','')}\n"
        )
        st.download_button(
            label="⬇  Download full research output",
            data=full_output,
            file_name=f"aurea_{topic[:40].replace(' ','_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="aurea-footer">Aurea · Multi-Agent Research System · Powered by LangGraph</div>',
    unsafe_allow_html=True,
)