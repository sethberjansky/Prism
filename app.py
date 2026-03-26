import streamlit as st
import json
import anthropic
from pdf_utils import extract_text_from_pdf
from prompts import (
    EXTRACTION_SYSTEM, get_extraction_prompt,
    SYNTHESIS_SYSTEM, get_synthesis_prompt,
    LENS_SYSTEM,
    get_executive_prompt, get_legal_prompt, get_finance_prompt,
    get_bd_prompt, get_token_ops_prompt, get_investor_prompt
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prism — Data Room Intelligence",
    page_icon="🔷",
    layout="wide"
)

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
        status.text(f"Extracting: {f.name} ({i+1}/{len(uploaded_files)})")
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

# ── UI ────────────────────────────────────────────────────────────────────────
st.title("🔷 Prism")
st.caption("AI-powered data room intelligence for tokenized securities")

# Sidebar — upload
with st.sidebar:
    st.header("Data Room")
    uploaded_files = st.file_uploader(
        "Upload deal documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload PDFs from your data room. Prism supports up to 20 documents."
    )
    
    if uploaded_files:
        st.caption(f"{len(uploaded_files)} document(s) loaded")
        
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
                    st.success("Analysis complete. Select a lens below.")
                except Exception as e:
                    st.error(f"Synthesis failed: {e}")
    
    if st.session_state.deal_json:
        st.divider()
        st.subheader("Lens Views")
        lenses = ["Executive", "Legal", "Finance", "BD", "Token Ops", "Investor"]
        for lens in lenses:
            cached = "✓ " if lens in st.session_state.lens_cache else ""
            if st.button(f"{cached}{lens}", use_container_width=True):
                st.session_state.active_lens = lens

# Main area
if st.session_state.deal_json is None and not uploaded_files:
    # Empty state
    st.markdown("### Upload your data room documents to get started")
    st.markdown("""
    Prism analyzes your deal documents and generates role-specific intelligence across six lenses:
    
    | Lens | What it covers |
    |------|---------------|
    | **Executive** | Deal snapshot, key numbers, recommendation, risks |
    | **Legal** | Regulatory framework, missing docs, compliance gaps |
    | **Finance** | Valuation, cap table, projections, financial flags |
    | **BD** | Partner-facing brief (no internal flags) |
    | **Token Ops** | Blockchain config, KYC/AML readiness, blockers |
    | **Investor** | Terms, risks, returns, eligibility |
    """)

elif st.session_state.deal_json and st.session_state.active_lens is None:
    # Analysis done, no lens selected yet
    deal = st.session_state.deal_json
    overview = deal.get("deal_overview", {})
    
    st.subheader(f"Deal: {overview.get('deal_name', 'Unknown Deal')}")
    st.caption(overview.get("deal_description", ""))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Value", overview.get("total_value", "—"))
    with col2:
        reg = deal.get("regulatory", {})
        st.metric("Framework", reg.get("framework", "—"))
    with col3:
        token = deal.get("tokenization_parameters", {})
        st.metric("Blockchain", token.get("blockchain", "—"))
    
    # Cross-document flags
    cross = deal.get("cross_document_analysis", {})
    inconsistencies = cross.get("inconsistencies", [])
    missing = cross.get("missing_documents", [])
    gaps = cross.get("compliance_gaps", [])
    
    if inconsistencies or missing or gaps:
        st.divider()
        st.subheader("⚠️ Cross-Document Flags")
        
        if inconsistencies:
            with st.expander(f"Inconsistencies ({len(inconsistencies)})", expanded=True):
                for item in inconsistencies:
                    st.markdown(f"- {item}")
        
        if missing:
            with st.expander(f"Missing Documents ({len(missing)})", expanded=True):
                for item in missing:
                    st.markdown(f"- {item}")
        
        if gaps:
            with st.expander(f"Compliance Gaps ({len(gaps)})", expanded=False):
                for item in gaps:
                    st.markdown(f"- {item}")
    
    st.divider()
    st.caption("Select a lens from the sidebar to generate a role-specific view.")

elif st.session_state.active_lens:
    # Lens view
    lens = st.session_state.active_lens

    col_title, col_export = st.columns([4, 1])
    with col_title:
        st.subheader(f"{lens} View")
    with col_export:
        pass  # PDF export — post-hackathon polish
    
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
        st.markdown(result)