"""
Prism — UI Components
Custom HTML/CSS renderers injected via st.markdown(unsafe_allow_html=True)
"""

import re
import streamlit as st

TEAL = "#1D9E75"
TEAL_LIGHT = "#E1F5EE"
TEAL_DARK = "#085041"


def inject_global_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display: none; }

    .stApp { background: #F5F5F2; }

    .main .block-container { padding: 1.5rem 2rem 3rem 2rem; max-width: 1200px; }

    [data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E5E4E0; }
    [data-testid="stSidebar"] > div { padding: 1.5rem 1rem; }

    .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500;
        border-radius: 6px;
        border: 1px solid #E5E4E0;
        background: #FFFFFF;
        color: #1A1A18;
        font-size: 13px;
        padding: 0.4rem 0.8rem;
        transition: all 0.15s ease;
    }
    .stButton > button:hover { border-color: #1D9E75; color: #085041; background: #E1F5EE; }
    .stButton > button[kind="primary"] { background: #1D9E75; color: #FFFFFF; border-color: #1D9E75; }
    .stButton > button[kind="primary"]:hover { background: #178A65; border-color: #178A65; }

    [data-testid="stFileUploader"] { border: 1.5px dashed #D1D0CC; border-radius: 8px; background: #FAFAF9; padding: 0.5rem; }

    .streamlit-expanderHeader { font-family: 'DM Sans', sans-serif !important; font-weight: 500; font-size: 13px; color: #1A1A18; background: #FFFFFF; border: 1px solid #E5E4E0; border-radius: 6px; }

    .stSpinner > div { border-top-color: #1D9E75 !important; }
    .stProgress > div > div { background: #1D9E75; }

    hr { border-color: #E5E4E0; margin: 1rem 0; }
    .stMarkdown p { margin-bottom: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)


def _sanitize_lens_output(text):
    """Fix common formatting issues in Claude's lens output."""
    # Strip backtick code spans — `text` → text (numbers showing as green monospace)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Escape dollar signs to prevent Streamlit LaTeX math rendering ($5M → \$5M)
    text = text.replace('$', r'\$')
    # Strip bold markers (**text**) — replace with just the text
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # Strip italic markers (*text*) — replace with just the text
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    # Remove any remaining stray asterisks
    text = re.sub(r'\*+', '', text)
    # Add space between number and letter running together
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    # Add space between letter/punctuation and number
    text = re.sub(r'([a-zA-Z,\.])(\d)', r'\1 \2', text)
    # Fix em dash missing spaces
    text = re.sub(r'(\S)—(\S)', r'\1 — \2', text)
    return text


def render_header(deal_name=None, doc_count=None):
    subtitle = ""
    if deal_name and doc_count:
        subtitle = f'<span style="color:#6B6B68;font-size:13px;font-weight:400;margin-left:12px;padding-left:12px;border-left:1px solid #E5E4E0;">{deal_name} &middot; {doc_count} documents</span>'
    elif deal_name:
        subtitle = f'<span style="color:#6B6B68;font-size:13px;font-weight:400;margin-left:12px;padding-left:12px;border-left:1px solid #E5E4E0;">{deal_name}</span>'
    st.markdown(f'<div style="display:flex;align-items:center;justify-content:space-between;padding:0 0 1.25rem 0;border-bottom:1px solid #E5E4E0;margin-bottom:1.5rem;"><div style="display:flex;align-items:center;"><span style="font-size:20px;font-weight:600;color:#1A1A18;letter-spacing:-0.5px;"><span style="color:{TEAL};">&#9670;</span> Prism</span>{subtitle}</div><span style="font-size:11px;color:#9CA3A0;">AI Data Room Intelligence</span></div>', unsafe_allow_html=True)


def render_stats_bar(deal_json):
    overview = deal_json.get("deal_overview", {})
    regulatory = deal_json.get("regulatory", {})
    tokenization = deal_json.get("tokenization_parameters", {})
    cross = deal_json.get("cross_document_analysis", {})

    total_value = overview.get("total_value", "—")
    framework = regulatory.get("framework", "—")
    blockchain = tokenization.get("blockchain", "—")

    flag_count = len(cross.get("inconsistencies", [])) + len(cross.get("missing_documents", [])) + len(cross.get("compliance_gaps", []))
    flag_color = "#DC2626" if flag_count > 0 else "#16A34A"
    flag_display = f"{flag_count} flag{'s' if flag_count != 1 else ''}"

    st.markdown(f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:1.5rem;">{_stat_card("Total Value", total_value, "#1A1A18")}{_stat_card("Framework", framework, "#1A1A18")}{_stat_card("Blockchain", blockchain, "#1A1A18")}{_stat_card("Flags", flag_display, flag_color)}</div>', unsafe_allow_html=True)
    return flag_count


def _stat_card(label, value, value_color):
    return f'<div style="background:#FFFFFF;border:1px solid #E5E4E0;border-radius:8px;padding:14px 16px;"><div style="font-size:11px;color:#9CA3A0;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;">{label}</div><div style="font-size:18px;font-weight:600;color:{value_color};letter-spacing:-0.3px;line-height:1.2;">{value}</div></div>'


def render_flags_section(deal_json):
    cross = deal_json.get("cross_document_analysis", {})
    inconsistencies = cross.get("inconsistencies", [])
    missing = cross.get("missing_documents", [])
    gaps = cross.get("compliance_gaps", [])

    if not inconsistencies and not missing and not gaps:
        st.markdown('<div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;padding:12px 16px;margin-bottom:1.5rem;display:flex;align-items:center;gap:8px;"><span style="color:#16A34A;font-size:15px;">&#10003;</span><span style="font-size:13px;color:#14532D;font-weight:500;">No cross-document flags detected</span></div>', unsafe_allow_html=True)
        return

    total = len(inconsistencies) + len(missing) + len(gaps)
    st.markdown(f'<div style="background:#FFF8F8;border:1px solid #FECACA;border-radius:8px;padding:14px 16px;margin-bottom:1rem;"><div style="display:flex;align-items:center;gap:8px;"><span style="background:#DC2626;color:#FFFFFF;font-size:11px;font-weight:600;padding:2px 8px;border-radius:4px;">FLAGS &nbsp;{total}</span><span style="font-size:13px;color:#7F1D1D;font-weight:500;">Cross-document analysis detected issues requiring attention</span></div></div>', unsafe_allow_html=True)

    if inconsistencies:
        with st.expander(f"⚠ Inconsistencies ({len(inconsistencies)})", expanded=True):
            for item in inconsistencies:
                st.markdown(f'<div style="display:flex;gap:8px;padding:8px 0;border-bottom:1px solid #F3F4F6;"><span style="color:#D97706;flex-shrink:0;">&#9670;</span><span style="font-size:13px;color:#1A1A18;line-height:1.5;">{item}</span></div>', unsafe_allow_html=True)

    if missing:
        with st.expander(f"✕ Missing Documents ({len(missing)})", expanded=True):
            for item in missing:
                st.markdown(f'<div style="display:flex;gap:8px;padding:8px 0;border-bottom:1px solid #F3F4F6;"><span style="color:#DC2626;flex-shrink:0;">&#9670;</span><span style="font-size:13px;color:#1A1A18;line-height:1.5;">{item}</span></div>', unsafe_allow_html=True)

    if gaps:
        with st.expander(f"◉ Compliance Gaps ({len(gaps)})", expanded=False):
            for item in gaps:
                st.markdown(f'<div style="display:flex;gap:8px;padding:8px 0;border-bottom:1px solid #F3F4F6;"><span style="color:#2563EB;flex-shrink:0;">&#9670;</span><span style="font-size:13px;color:#1A1A18;line-height:1.5;">{item}</span></div>', unsafe_allow_html=True)


def render_deal_overview(deal_json):
    overview = deal_json.get("deal_overview", {})
    deal_name = overview.get("deal_name", "Untitled Deal")
    description = overview.get("deal_description", "")
    deal_type = overview.get("deal_type", "")
    asset_class = overview.get("asset_class", "")
    jurisdiction = overview.get("jurisdiction", "")
    parties = overview.get("parties", [])

    tags_html = ""
    for tag in [deal_type, asset_class, jurisdiction]:
        if tag and tag not in ["—", "unknown", ""]:
            tags_html += f'<span style="background:#F5F5F2;border:1px solid #E5E4E0;border-radius:4px;padding:2px 8px;font-size:11px;color:#6B6B68;font-weight:500;">{tag}</span> '

    parties_html = ""
    if parties:
        parties_str = " · ".join(parties[:4])
        if len(parties) > 4:
            parties_str += f" +{len(parties)-4} more"
        parties_html = f'<div style="font-size:12px;color:#9CA3A0;margin-top:4px;">{parties_str}</div>'

    desc_html = f'<p style="font-size:13px;color:#6B6B68;margin:0 0 8px 0;line-height:1.5;">{description}</p>' if description else ""
    st.markdown(f'<div style="margin-bottom:1.5rem;"><div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px;"><div><h2 style="font-size:22px;font-weight:600;color:#1A1A18;letter-spacing:-0.5px;margin:0 0 4px 0;line-height:1.2;">{deal_name}</h2>{desc_html}{parties_html}</div><div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end;flex-shrink:0;">{tags_html}</div></div></div>', unsafe_allow_html=True)


def render_lens_header(lens_name, deal_name=None):
    lens_descriptions = {
        "Executive": "Decision brief &middot; Go/no-go recommendation with key risks and timeline",
        "Legal": "Regulatory review &middot; Compliance status, missing documents, severity-ranked gaps",
        "Finance": "Financial analysis &middot; Valuation, cap table, projections, and financial flags",
        "BD": "Partner brief &middot; External-safe deal overview (confidential items excluded)",
        "Token Ops": "Tokenization readiness &middot; Smart contract parameters, ATS status, blockers by priority",
        "Investor": "Investor summary &middot; Offering terms, risk factors, eligibility, and return profile",
    }
    description = lens_descriptions.get(lens_name, "")
    deal_label = f" &middot; {deal_name}" if deal_name else ""
    st.markdown(f'<div style="background:#FFFFFF;border:1px solid #E5E4E0;border-radius:8px;padding:16px 20px;margin-bottom:1.25rem;"><div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;"><span style="background:{TEAL};color:#FFFFFF;font-size:11px;font-weight:600;padding:3px 10px;border-radius:4px;text-transform:uppercase;letter-spacing:0.05em;">{lens_name}</span><span style="font-size:13px;color:#1A1A18;font-weight:500;">{deal_label}</span></div><div style="font-size:12px;color:#9CA3A0;">{description}</div></div>', unsafe_allow_html=True)


def render_lens_content(lens_name, content):
    if lens_name == "BD":
        st.markdown(f'<div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:6px;padding:10px 14px;margin-bottom:1rem;display:flex;align-items:center;gap:8px;"><span style="color:#D97706;">&#9670;</span><span style="font-size:12px;color:#78350F;font-weight:500;">Confidentiality filter active &mdash; internal flags, investor names, and compliance gaps excluded from this view</span></div>', unsafe_allow_html=True)

    st.markdown("""
    <style>
    .lens-content { background:#FFFFFF; border:1px solid #E5E4E0; border-radius:8px; padding:24px 32px; }
    .lens-content h1, .lens-content h2, .lens-content h3 { letter-spacing:-0.3px; margin-top:1.75rem; margin-bottom:0.5rem; padding-bottom:0.4rem; border-bottom:1px solid #F0EFEB; }
    .lens-content h1:first-child, .lens-content h2:first-child, .lens-content h3:first-child { margin-top:0; }
    .lens-content p { line-height:1.75; margin-bottom:0.85rem; color:#2A2A28; max-width:72ch; }
    .lens-content ul, .lens-content ol { margin-bottom:1rem; padding-left:1.4rem; }
    .lens-content li { line-height:1.65; margin-bottom:0.35rem; color:#2A2A28; }
    .lens-content strong { color:#1A1A18; font-weight:600; }
    .lens-content code { background:#F5F5F2; border:1px solid #E5E4E0; border-radius:3px; padding:1px 5px; font-size:0.88em; color:#1A1A18; }
    .lens-content hr { border-color:#F0EFEB; margin:1.5rem 0; }
    .lens-content blockquote { border-left:3px solid #1D9E75; margin:1rem 0; padding:0.5rem 0 0.5rem 1rem; background:#F9FDFB; border-radius:0 4px 4px 0; }
    .lens-content table { width:100%; border-collapse:collapse; margin-bottom:1rem; font-size:13px; }
    .lens-content th { background:#F5F5F2; border:1px solid #E5E4E0; padding:8px 12px; text-align:left; font-weight:600; color:#1A1A18; }
    .lens-content td { border:1px solid #E5E4E0; padding:8px 12px; color:#2A2A28; vertical-align:top; }
    .lens-content tr:nth-child(even) td { background:#FAFAF9; }
    </style>
    <div class="lens-content">
    """, unsafe_allow_html=True)

    st.markdown(_sanitize_lens_output(content))
    st.markdown('</div>', unsafe_allow_html=True)


def render_empty_state():
    cards = "".join([
        _lens_preview_card("Executive", "Go/no-go brief"),
        _lens_preview_card("Legal", "Compliance review"),
        _lens_preview_card("Finance", "Valuation analysis"),
        _lens_preview_card("BD", "Partner-safe brief"),
        _lens_preview_card("Token Ops", "Tokenization readiness"),
        _lens_preview_card("Investor", "Offering summary"),
    ])
    st.markdown(f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:5rem 2rem;text-align:center;"><div style="font-size:72px;margin-bottom:2rem;opacity:0.12;color:{TEAL};">&#9670;</div><h3 style="font-size:28px;font-weight:600;color:#1A1A18;letter-spacing:-0.5px;margin:0 0 12px 0;">Upload your data room</h3><p style="font-size:16px;color:#6B6B68;margin:0 0 2.5rem 0;max-width:480px;line-height:1.7;">Drop your deal documents in the sidebar. Prism classifies, extracts, and translates them across six role-specific views.</p><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:780px;width:100%;">{cards}</div></div>', unsafe_allow_html=True)


def _lens_preview_card(name, description):
    return f'<div style="background:#FFFFFF;border:1px solid #E5E4E0;border-radius:10px;padding:18px 20px;text-align:left;"><div style="font-size:14px;font-weight:600;color:#1A1A18;margin-bottom:4px;">{name}</div><div style="font-size:12px;color:#9CA3A0;">{description}</div></div>'


def render_processing_state(message="Analyzing documents..."):
    st.markdown(f'<div style="display:flex;align-items:center;gap:10px;padding:12px 16px;background:#FFFFFF;border:1px solid #E5E4E0;border-radius:8px;margin-bottom:1rem;"><div style="width:8px;height:8px;border-radius:50%;background:{TEAL};"></div><span style="font-size:13px;color:#1A1A18;font-weight:500;">{message}</span></div>', unsafe_allow_html=True)


def render_sidebar_header():
    st.markdown(f'<div style="margin-bottom:1rem;"><div style="font-size:18px;font-weight:600;color:#1A1A18;letter-spacing:-0.3px;margin-bottom:4px;"><span style="color:{TEAL};">&#9670;</span> Prism</div><div style="font-size:11px;color:#9CA3A0;">Data Room Intelligence</div></div><hr style="border-color:#E5E4E0;margin:0 0 1rem 0;">', unsafe_allow_html=True)


def render_sidebar_lens_buttons(deal_json, active_lens, lens_cache):
    lenses = ["Executive", "Legal", "Finance", "BD", "Token Ops", "Investor"]
    st.markdown('<div style="font-size:11px;color:#9CA3A0;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;">Lens Views</div>', unsafe_allow_html=True)

    selected = active_lens
    for lens in lenses:
        is_active = lens == active_lens
        is_cached = lens in lens_cache

        if is_active:
            st.markdown(f'<div style="background:{TEAL_LIGHT};border:1px solid {TEAL};border-radius:6px;padding:8px 12px;margin-bottom:4px;display:flex;justify-content:space-between;align-items:center;"><span style="font-size:13px;font-weight:600;color:{TEAL_DARK};">{lens}</span><span style="font-size:10px;color:{TEAL};font-weight:500;">ACTIVE</span></div>', unsafe_allow_html=True)
        else:
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(lens, key=f"sidebar_lens_{lens}", use_container_width=True):
                    selected = lens
            with col2:
                if is_cached:
                    st.markdown(f'<div style="color:{TEAL};font-size:14px;padding-top:6px;text-align:center;">&#10003;</div>', unsafe_allow_html=True)

    return selected