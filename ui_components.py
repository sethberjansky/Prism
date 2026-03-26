import streamlit as st

def render_header():
    """Render the top header bar."""
    st.markdown("""
    <style>
    .prism-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .prism-title {
        color: #e0e0ff;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
    }
    .prism-sub {
        color: #8888aa;
        font-size: 0.85rem;
        margin: 0;
    }
    </style>
    <div class="prism-header">
        <div>
            <p class="prism-title">🔷 Prism</p>
            <p class="prism-sub">AI-powered data room intelligence for tokenized securities</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_doc_table(extractions):
    """Render a summary table of all extracted documents."""
    if not extractions:
        return
    
    st.subheader("Document Index")
    
    rows = []
    for doc in extractions:
        if "error" in doc and "document_type" not in doc:
            rows.append({
                "File": doc.get("filename", "unknown"),
                "Type": "Error",
                "Category": "—",
                "Confidentiality": "—",
                "Flags": doc.get("error", "Unknown error")
            })
        else:
            flags = doc.get("flags", [])
            flag_str = f"⚠️ {len(flags)}" if flags else "✓"
            rows.append({
                "File": doc.get("filename", "unknown"),
                "Type": doc.get("document_type", "—"),
                "Category": doc.get("category", "—"),
                "Confidentiality": doc.get("confidentiality", "—"),
                "Flags": flag_str
            })
    
    st.dataframe(rows, use_container_width=True, hide_index=True)


def render_flags_panel(extractions):
    """Render all document-level flags across the data room."""
    all_flags = []
    for doc in extractions:
        flags = doc.get("flags", [])
        for flag in flags:
            all_flags.append({"Document": doc.get("filename", "?"), "Flag": flag})
    
    if all_flags:
        st.subheader(f"Document Flags ({len(all_flags)})")
        for item in all_flags:
            st.markdown(f"**{item['Document']}** — {item['Flag']}")
    else:
        st.success("No document-level flags detected.")


def render_metric_row(deal_json):
    """Render the top-level deal metrics."""
    if not deal_json:
        return
    
    overview = deal_json.get("deal_overview", {})
    reg = deal_json.get("regulatory", {})
    token = deal_json.get("tokenization_parameters", {})
    offering = deal_json.get("offering_terms", {})
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Value", overview.get("total_value", "—"))
    with col2:
        st.metric("Framework", reg.get("framework", "—"))
    with col3:
        st.metric("Blockchain", token.get("blockchain", "—"))
    with col4:
        st.metric("Min Investment", offering.get("minimum_investment", "—"))