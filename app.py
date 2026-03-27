import streamlit as st
import json
import os
import anthropic
from pdf_utils import extract_text_from_pdf
from prompts import (
    EXTRACTION_SYSTEM, get_extraction_prompt,
    SYNTHESIS_SYSTEM, get_synthesis_prompt,
    LENS_SYSTEM,
    get_executive_prompt, get_legal_prompt, get_finance_prompt,
    get_bd_prompt, get_token_ops_prompt, get_investor_prompt
)
from ui_components import (
    inject_global_css,
    render_header,
    render_stats_bar,
    render_flags_section,
    render_deal_overview,
    render_lens_header,
    render_lens_content,
    render_empty_state,
    render_sidebar_header,
    render_sidebar_lens_buttons,
    TEAL
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prism — Data Room Intelligence",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject global CSS (runs once per session)
inject_global_css()

# ── Init session state ────────────────────────────────────────────────────────
if "extractions" not in st.session_state:
    st.session_state.extractions = []
if "deal_json" not in st.session_state:
    st.session_state.deal_json = None
if "lens_cache" not in st.session_state:
    st.session_state.lens_cache = {}
if "active_lens" not in st.session_state:
    st.session_state.active_lens = None

# ── Claude client ─────────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def call_claude(system, user_prompt):
    """Single Claude call. Returns text string or raises."""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=system,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return response.content[0].text

def run_extraction(uploaded_files):
    """Stage 1a: Extract structured data from each PDF."""
    extractions = []
    progress = st.progress(0)
    status = st.empty()

    for i, f in enumerate(uploaded_files):
        status.markdown(f"""
        <div style="font-size:13px;color:#6B6B68;padding:6px 0;">
            Extracting <strong style="color:#1A1A18;">{f.name}</strong>
            <span style="color:#9CA3A0;"> · {i+1} of {len(uploaded_files)}</span>
        </div>
        """, unsafe_allow_html=True)

        text, err = extract_text_from_pdf(f)
        if err:
            extractions.append({"filename": f.name, "error": err})
        else:
            try:
                raw = call_claude(EXTRACTION_SYSTEM, get_extraction_prompt(f.name, text))
                data = json.loads(raw)
                extractions.append(data)
            except Exception as e:
                extractions.append({"filename": f.name, "error": str(e)})
        progress.progress((i + 1) / len(uploaded_files))

    progress.empty()
    status.empty()
    return extractions

def run_synthesis(extractions):
    """Stage 1b: Cross-document synthesis."""
    docs_json = json.dumps(extractions, indent=2)
    raw = call_claude(SYNTHESIS_SYSTEM, get_synthesis_prompt(docs_json))
    return json.loads(raw)

def run_lens(lens_name, deal_json):
    """Stage 2: Generate one lens view. Cached in session state."""
    if lens_name in st.session_state.lens_cache:
        return st.session_state.lens_cache[lens_name]

    deal_str = json.dumps(deal_json, indent=2)
    prompt_fn = {
        "Executive": get_executive_prompt,
        "Legal": get_legal_prompt,
        "Finance": get_finance_prompt,
        "BD": get_bd_prompt,
        "Token Ops": get_token_ops_prompt,
        "Investor": get_investor_prompt,
    }[lens_name]

    result = call_claude(LENS_SYSTEM, prompt_fn(deal_str))
    st.session_state.lens_cache[lens_name] = result
    return result

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    render_sidebar_header()

    uploaded_files = st.file_uploader(
        "Upload deal documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload PDFs from your data room. Supports up to 20 documents.",
        label_visibility="collapsed"
    )

    st.markdown("""
    <div style="font-size:12px;color:#9CA3A0;margin-bottom:8px;">
        Upload deal documents (PDF)
    </div>
    """, unsafe_allow_html=True)

    if uploaded_files:
        st.markdown(f"""
        <div style="font-size:12px;color:#6B6B68;margin-bottom:10px;">
            {len(uploaded_files)} document{'s' if len(uploaded_files) != 1 else ''} loaded
        </div>
        """, unsafe_allow_html=True)

        if st.button("Analyze Data Room", type="primary", use_container_width=True):
            st.session_state.extractions = []
            st.session_state.deal_json = None
            st.session_state.lens_cache = {}
            st.session_state.active_lens = None

            with st.spinner("Running extraction pipeline..."):
                extractions = run_extraction(uploaded_files)
                st.session_state.extractions = extractions

            with st.spinner("Synthesizing deal intelligence..."):
                try:
                    deal_json = run_synthesis(extractions)
                    st.session_state.deal_json = deal_json
                    st.success("Analysis complete.")
                except Exception as e:
                    st.error(f"Synthesis failed: {e}")

    # Lens navigation — only shown when analysis is complete
    if st.session_state.deal_json:
        st.markdown('<hr style="border-color:#E5E4E0;margin:1rem 0;">', unsafe_allow_html=True)
        new_lens = render_sidebar_lens_buttons(
            st.session_state.deal_json,
            st.session_state.active_lens,
            st.session_state.lens_cache
        )
        if new_lens != st.session_state.active_lens:
            st.session_state.active_lens = new_lens
            st.rerun()

    # ── Load Demo Data ─────────────────────────────────────────────────────────
    demo_cache_path = "demo_cache.json"
    if os.path.exists(demo_cache_path):
        st.markdown('<hr style="border-color:#E5E4E0;margin:1rem 0;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:11px;color:#9CA3A0;font-weight:500;
                    text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;">
            Demo
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚡ Load Demo Data", use_container_width=True,
                     help="Load pre-computed NovaTech analysis — no API call"):
            with open(demo_cache_path, "r") as f:
                cache = json.load(f)
            st.session_state.extractions = cache.get("extractions", [])
            st.session_state.deal_json = cache.get("deal_json", {})
            st.session_state.lens_cache = cache.get("lens_cache", {})
            st.session_state.active_lens = None
            st.rerun()

# ── Main area ─────────────────────────────────────────────────────────────────

# Determine deal name for header
deal_name = None
if st.session_state.deal_json:
    overview = st.session_state.deal_json.get("deal_overview", {})
    deal_name = overview.get("deal_name")
doc_count = len(st.session_state.extractions) if st.session_state.extractions else None

render_header(deal_name=deal_name, doc_count=doc_count)

# ── State: Empty ──────────────────────────────────────────────────────────────
if st.session_state.deal_json is None:
    render_empty_state()

# ── State: Data Room (analysis done, no lens selected) ────────────────────────
elif st.session_state.active_lens is None:
    deal = st.session_state.deal_json

    render_deal_overview(deal)
    render_stats_bar(deal)
    render_flags_section(deal)

    st.markdown(f"""
    <div style="margin-top:1.5rem;padding:12px 16px;background:#FAFAF9;
                border:1px solid #E5E4E0;border-radius:6px;text-align:center;">
        <span style="font-size:12px;color:#9CA3A0;">
            Select a lens from the sidebar to generate a role-specific view
        </span>
    </div>
    """, unsafe_allow_html=True)

# ── State: Lens View ──────────────────────────────────────────────────────────
elif st.session_state.active_lens:
    lens = st.session_state.active_lens
    deal = st.session_state.deal_json
    overview = deal.get("deal_overview", {}) if deal else {}

    render_lens_header(
        lens_name=lens,
        deal_name=overview.get("deal_name")
    )

    # Back to data room link
    col_back, col_export = st.columns([1, 5])
    with col_back:
        if st.button("← Data Room", key="back_btn"):
            st.session_state.active_lens = None
            st.rerun()
    with col_export:
        st.markdown(
            '<div style="font-size:11px;color:#9CA3A0;padding-top:8px;">PDF export available in v2</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div style="margin-bottom:0.75rem;"></div>', unsafe_allow_html=True)

    # Generate or retrieve from cache
    if lens not in st.session_state.lens_cache:
        with st.spinner(f"Generating {lens} analysis..."):
            try:
                result = run_lens(lens, st.session_state.deal_json)
            except Exception as e:
                st.error(f"Lens generation failed: {e}")
                result = None
    else:
        result = st.session_state.lens_cache[lens]

    if result:
        render_lens_content(lens, result)