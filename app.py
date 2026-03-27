import streamlit as st
import json
import os
import anthropic
import concurrent.futures
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

st.set_page_config(
    page_title="Prism — Data Room Intelligence",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_global_css()

if "extractions" not in st.session_state:
    st.session_state.extractions = []
if "deal_json" not in st.session_state:
    st.session_state.deal_json = None
if "lens_cache" not in st.session_state:
    st.session_state.lens_cache = {}
if "active_lens" not in st.session_state:
    st.session_state.active_lens = None

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

LENS_PROMPT_FNS = {
    "Executive": get_executive_prompt,
    "Legal": get_legal_prompt,
    "Finance": get_finance_prompt,
    "BD": get_bd_prompt,
    "Token Ops": get_token_ops_prompt,
    "Investor": get_investor_prompt,
}

def call_claude(system, user_prompt, temperature=1):
    import time
    for attempt in range(4):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                temperature=temperature,
                system=system,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.content[0].text
        except Exception as e:
            if ("529" in str(e) or "overloaded" in str(e).lower()) and attempt < 3:
                wait = (attempt + 1) * 8
                time.sleep(wait)
                continue
            raise e

def extract_one(args):
    i, f, name, text, err = args
    if err:
        return i, {"filename": name, "error": err}
    try:
        raw = call_claude(EXTRACTION_SYSTEM, get_extraction_prompt(name, text))
        data = json.loads(raw)
        return i, data
    except Exception as e:
        return i, {"filename": name, "error": str(e)}

def run_extraction(uploaded_files):
    results = [None] * len(uploaded_files)
    progress = st.progress(0)
    status = st.empty()
    status.markdown(
        f'<div style="font-size:13px;color:#6B6B68;padding:6px 0;">Extracting <strong style="color:#1A1A18;">{len(uploaded_files)} documents</strong> in parallel...</div>',
        unsafe_allow_html=True
    )
    args_list = []
    for i, f in enumerate(uploaded_files):
        text, err = extract_text_from_pdf(f)
        args_list.append((i, f, f.name, text, err))
    completed = [0]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(extract_one, args): args[0] for args in args_list}
        for future in concurrent.futures.as_completed(futures):
            i, result = future.result()
            results[i] = result
            completed[0] += 1
            progress.progress(completed[0] / len(uploaded_files))
    progress.empty()
    status.empty()
    return results

def run_synthesis(extractions):
    import time
    docs_json = json.dumps(extractions, indent=2)
    for attempt in range(3):
        try:
            raw = call_claude(SYNTHESIS_SYSTEM, get_synthesis_prompt(docs_json), temperature=0)
            return json.loads(raw)
        except Exception as e:
            if "529" in str(e) or "overloaded" in str(e).lower():
                if attempt < 2:
                    time.sleep(5)
                    continue
            raise e
    raise Exception("Synthesis failed after 3 attempts — API overloaded. Try again in 30 seconds.")

def generate_one_lens(args):
    lens_name, deal_str = args
    try:
        result = call_claude(LENS_SYSTEM, LENS_PROMPT_FNS[lens_name](deal_str), temperature=0)
        return lens_name, result
    except Exception as e:
        return lens_name, None

def run_all_lenses(deal_json):
    deal_str = json.dumps(deal_json, indent=2)
    args_list = [(lens_name, deal_str) for lens_name in LENS_PROMPT_FNS.keys()]
    lens_cache = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(generate_one_lens, args): args[0] for args in args_list}
        for future in concurrent.futures.as_completed(futures):
            lens_name, result = future.result()
            if result:
                lens_cache[lens_name] = result
    return lens_cache

def run_lens(lens_name, deal_json):
    if lens_name in st.session_state.lens_cache:
        return st.session_state.lens_cache[lens_name]
    deal_str = json.dumps(deal_json, indent=2)
    result = call_claude(LENS_SYSTEM, LENS_PROMPT_FNS[lens_name](deal_str), temperature=0)
    st.session_state.lens_cache[lens_name] = result
    return result

with st.sidebar:
    render_sidebar_header()

    uploaded_files = st.file_uploader(
        "Upload deal documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload PDFs from your data room. Supports up to 20 documents.",
        label_visibility="collapsed"
    )

    st.markdown('<div style="font-size:12px;color:#9CA3A0;margin-bottom:4px;">Upload deal documents (PDF)</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#C4C3BF;margin-bottom:8px;">One deal per session</div>', unsafe_allow_html=True)

    if uploaded_files:
        st.markdown(f'<div style="font-size:12px;color:#6B6B68;margin-bottom:10px;">{len(uploaded_files)} document{"s" if len(uploaded_files) != 1 else ""} loaded</div>', unsafe_allow_html=True)

        if st.button("Analyze Data Room", type="primary", use_container_width=True):
            st.session_state.extractions = []
            st.session_state.deal_json = None
            st.session_state.lens_cache = {}
            st.session_state.active_lens = None

            with st.spinner("Extracting documents..."):
                extractions = run_extraction(uploaded_files)
                st.session_state.extractions = extractions

            with st.spinner("Synthesizing deal intelligence..."):
                try:
                    deal_json = run_synthesis(extractions)
                    st.session_state.deal_json = deal_json
                except Exception as e:
                    st.error(f"Synthesis failed: {e}")
                    st.stop()

            with st.spinner("Generating all lens views..."):
                lens_cache = run_all_lenses(st.session_state.deal_json)
                st.session_state.lens_cache = lens_cache

            st.success("Analysis complete. All lenses ready.")

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

    demo_cache_path = "demo_cache.json"
    if os.path.exists(demo_cache_path):
        st.markdown('<hr style="border-color:#E5E4E0;margin:1rem 0;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:11px;color:#9CA3A0;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;">Demo</div>', unsafe_allow_html=True)
        if st.button("⚡ Load Demo Data", use_container_width=True,
                     help="Load pre-computed NovaTech analysis — no API call"):
            with open(demo_cache_path, "r") as f:
                cache = json.load(f)
            st.session_state.extractions = cache.get("extractions", [])
            st.session_state.deal_json = cache.get("deal_json", {})
            st.session_state.lens_cache = cache.get("lens_cache", {})
            st.session_state.active_lens = None
            st.rerun()

deal_name = None
if st.session_state.deal_json:
    overview = st.session_state.deal_json.get("deal_overview", {})
    deal_name = overview.get("deal_name")
doc_count = len(st.session_state.extractions) if st.session_state.extractions else None

render_header(deal_name=deal_name, doc_count=doc_count)

if st.session_state.deal_json is None:
    render_empty_state()

elif st.session_state.active_lens is None:
    deal = st.session_state.deal_json
    render_deal_overview(deal)
    render_stats_bar(deal)
    render_flags_section(deal)
    st.markdown('<div style="margin-top:1.5rem;padding:12px 16px;background:#FAFAF9;border:1px solid #E5E4E0;border-radius:6px;text-align:center;"><span style="font-size:12px;color:#9CA3A0;">Select a lens from the sidebar to generate a role-specific view</span></div>', unsafe_allow_html=True)

elif st.session_state.active_lens:
    lens = st.session_state.active_lens
    deal = st.session_state.deal_json
    overview = deal.get("deal_overview", {}) if deal else {}

    render_lens_header(lens_name=lens, deal_name=overview.get("deal_name"))

    if lens not in st.session_state.lens_cache:
        with st.spinner(f"Generating {lens} analysis..."):
            try:
                result = run_lens(lens, st.session_state.deal_json)
            except Exception as e:
                st.error(f"Lens generation failed: {e}")
                result = None
    else:
        result = st.session_state.lens_cache[lens]

    col_back, col_export = st.columns([1, 5])
    with col_back:
        if st.button("← Data Room", key="back_btn"):
            st.session_state.active_lens = None
            st.rerun()
    with col_export:
        if result:
            st.download_button(
                label=f"↓ Download {lens} report",
                data=result,
                file_name=f"prism_{lens.lower().replace(' ', '_')}_report.md",
                mime="text/markdown",
                key=f"download_{lens}"
            )

    st.markdown('<div style="margin-bottom:0.75rem;"></div>', unsafe_allow_html=True)

    if result:
        render_lens_content(lens, result)