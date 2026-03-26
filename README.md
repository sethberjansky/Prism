# ◆ Prism

### Intelligent data room for tokenized securities

> One upload. Six perspectives. Built for how tZERO actually works.

---

## What Prism does

Every tokenized securities deal starts the same way — someone dumps a pile of PDFs into a folder and calls it a data room. Subscription agreements, cap tables, PPMs, compliance filings, board resolutions — critical documents that six different teams all need to review, each looking for completely different things.

The attorney is hunting for compliance gaps. The CFO is checking the numbers. The partnerships lead needs something they can share with a counterparty. The executive needs a go/no-go in two minutes. The token ops team needs to know if they can start configuring smart contracts. The investor needs to understand what they're buying.

Today, every one of those people reads the same messy documents and builds their own summary by hand. **Prism does it in seconds.**

Upload your deal documents. Prism reads every one, classifies them, extracts key terms, and cross-references the entire set — flagging inconsistencies, missing documents, and compliance gaps automatically. Then it generates six role-specific views of the same data:

| Lens | Built for | What they see |
|------|-----------|---------------|
| **Executive** | CEO, decision-makers | One-page deal brief with go/no-go recommendation and top risks |
| **Legal** | Securities attorneys | Regulatory review, missing docs checklist, compliance blockers |
| **Finance** | CFO, investment committee | Valuation, cap table, financials, and numerical inconsistencies |
| **BD** | Partnerships, external parties | Clean, partner-safe overview — all confidential information stripped |
| **Token Ops** | Tokenization team | Smart contract parameters, ATS readiness, implementation blockers |
| **Investor** | Prospective investors | Offering terms, risk factors, returns, eligibility requirements |

**Switching between lenses is instant.** The analysis happens once on upload. Every view is pre-computed and cached. Click a tab, get a completely different perspective on the same deal.

---

## Why this matters for tZERO

Every deal that flows through tZERO's tokenization pipeline — from issuer onboarding through ATS listing — requires exactly this kind of multi-stakeholder document review. Prism sits upstream of tokenization, turning document chaos into structured, role-specific intelligence.

The **Token Ops lens** speaks tZERO's internal language: it references tZERO Securities, tZERO Transfer Services, and tZERO Digital Asset Securities as separate entities. It checks ATS listing readiness, SPBD custody status, smart contract whitelist configuration, and VerifyInvestor.com/On-ChainPass integration. This isn't a generic data room tool with a tZERO label. It's built around how tZERO actually operates.

---

## What it catches

Prism doesn't just organize files — it thinks across documents. In our demo data room (a fictional Series A tokenization), Prism automatically identifies:

- **Cross-document inconsistencies** — The cap table says $2.1M committed; the subscription agreement says $1.8M. A $300K discrepancy that could mean unpapered commitments.
- **Entity name mismatches** — The operating agreement says "NovaTech Inc." but every other document and the Certificate of Formation confirm it's "NovaTech LLC." A template error that could affect enforceability.
- **Missing compliance documents** — No accredited investor verification letters in the data room. For a Reg D 506(c) offering, self-certification isn't enough — third-party verification is required.
- **ATS readiness gaps** — The tokenization spec references VerifyInvestor.com for KYC/AML, but no actual screening documentation is present. Can't list on the ATS without it.

Each finding is surfaced differently depending on the lens. The Executive sees "cap table discrepancy — reconcile before closing." The Legal lens calls it a potential securities violation. The Finance lens calculates the valuation impact. The BD lens doesn't mention it at all — it's an internal issue. **Same fact. Six different framings. That's the product.**

---

## Security

Prism handles the most sensitive documents in a deal — PPMs, subscription agreements, cap tables, investor information — flowing through an SEC and FINRA-regulated company's infrastructure. Security isn't a feature. It's the foundation.

**What we built:**

- **Zero document retention.** PDFs are processed in memory. Nothing is written to disk. No database. When your session ends, everything is gone. For a due diligence tool, persistent document storage is a liability, not a feature.
- **Credential isolation.** API keys live in `.streamlit/secrets.toml`, excluded from version control. Zero credentials anywhere in the codebase.
- **BD confidentiality filter.** The BD lens automatically strips internal risk flags, investor names, side letter terms, and compliance gaps before generating output. You can share the BD export externally without reviewing it for leaks — the filter is built into the AI layer.
- **Closed prompt surface.** Users upload files. No free-text input is passed to the AI model. This eliminates prompt injection as an attack vector.

**What we designed for production:**

- Role-based access control — Legal sees the Legal lens, BD sees BD only, executives see everything
- On-premise deployment within tZERO's compliance perimeter — no document data leaving the infrastructure
- Encryption at rest (AES-256) and in transit (TLS 1.3)
- Full audit trail — who uploaded what, who viewed which lens, who exported — for FINRA/SEC compliance
- Configurable document retention with automated deletion

---

## How it's built

```
Upload PDFs
     │
     ▼
┌─────────────────────────────────────────┐
│  Stage 1a: Per-document extraction      │
│  One AI call per PDF → structured JSON  │
│  (type, summary, key terms, flags)      │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Stage 1b: Cross-document synthesis     │
│  Deal summary, inconsistencies,         │
│  missing docs, completeness score       │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Stage 2: Six lens analyses             │
│  All pre-computed and cached            │
│  Lens switching = instant, no API call  │
└─────────────────────────────────────────┘
```

| Component | Tool | Why |
|-----------|------|-----|
| Web interface | [Streamlit](https://streamlit.io/) | Rapid prototyping, built-in file upload, session state |
| Document analysis | [Anthropic Claude API](https://docs.anthropic.com/) (Sonnet 4.6) | Strong structured reasoning, reliable JSON, fast |
| PDF extraction | [pdfplumber](https://github.com/jsvine/pdfplumber) | Clean text extraction from PDF documents |
| Report export | [fpdf2](https://github.com/py-pdf/fpdf2) | Generates branded PDF reports per lens |

### File structure

```
prism/
├── app.py                  # Main application — four UI states
├── prompts.py              # All 8 Claude prompts (extraction, synthesis, 6 lenses)
├── pdf_utils.py            # PDF text extraction with error handling
├── ui_components.py        # Custom HTML/CSS renderers for cards, stats, lenses
├── export.py               # PDF report generation with Prism branding
├── requirements.txt        # Python dependencies
├── sample_docs/            # Demo deal documents (NovaTech Series A)
└── .streamlit/
    ├── config.toml         # Theme configuration
    └── secrets.toml        # API key (excluded from repo)
```

---

## Run locally

**Prerequisites:** Python 3.9+

```bash
git clone https://github.com/[your-username]/prism.git
cd prism
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

Run:
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Team

**Team Assisted Intelligence**

Seth B — Product vision, architecture, UX design, domain expertise

Built with Claude as a genuine AI collaborator. The product concept, the six-lens architecture, the security decisions, and the tZERO-specific domain knowledge are human. The implementation is a real human-AI collaboration.

---

*◆ Prism — tZERO hAIckathon 2026*
