# All Claude prompts for Prism
# Stage 1a: per-document extraction
# Stage 1b: synthesis + cross-document analysis
# Stage 2: six lens prompts

EXTRACTION_SYSTEM = """You are an expert due diligence analyst specializing in tokenized securities offerings. You extract structured data from deal documents with precision."""

def get_extraction_prompt(filename, text):
    return f"""Analyze this document and return a JSON object with the extracted data. Return ONLY valid JSON — no preamble, no explanation, no markdown code fences.

If a field cannot be determined from the document, use null. Never guess or fabricate values. Only extract what is explicitly stated or directly implied by the text.

Use this exact schema:
{{
  "filename": "{filename}",
  "document_type": "classify as one of: PPM, subscription agreement, operating agreement, LPA, investor questionnaire, Form D, articles of incorporation, financial statements (audited), financial statements (unaudited), cap table, business plan, legal opinion, transfer agent agreement, custody agreement, smart contract spec, corporate bylaws, board resolution, side letter, placement agent agreement, term sheet, management bios, other",
  "category": "Legal, Financial, Compliance, Corporate Governance, Tokenization, Management, or Other",
  "summary": "one sentence summary of the document's purpose and key content",
  "key_terms": ["list specific extracted values: dollar amounts with context, percentages, named terms, dates, thresholds"],
  "obligations": "material obligations, covenants, conditions, restrictions found in this document — null if none",
  "dates": ["all dates mentioned with context, e.g. Filing date: January 15, 2026"],
  "dollar_amounts": ["all monetary figures with context, e.g. $5,000,000 aggregate offering amount"],
  "parties_mentioned": ["all entity and person names mentioned"],
  "confidentiality": "internal only, shareable, or public — based on document sensitivity",
  "flags": ["any issues: missing signatures, expired dates, unusual terms, incomplete sections, potential errors, entity name mismatches"],
  "confidence": "high, medium, or low — how confident you are in the document classification"
}}

DOCUMENT FILENAME: {filename}
DOCUMENT TEXT:
{text}"""


SYNTHESIS_SYSTEM = """You are a senior due diligence coordinator specializing in tokenized securities offerings reviewed through tZERO's regulated infrastructure. You have reviewed individual document extractions and must now produce a unified deal analysis with cross-document verification."""

def get_synthesis_prompt(docs_json):
    return f"""Below are the extracted JSON objects from each document in a data room. Analyze them collectively and return a single JSON object with the deal-level synthesis.

Return ONLY valid JSON — no preamble, no explanation, no markdown code fences. Use null for fields that cannot be determined.

CRITICAL CROSS-REFERENCING INSTRUCTIONS:
1. Compare dollar amounts across all documents — flag any discrepancies
2. Check entity names for consistency — flag any mismatches (e.g. LLC vs Inc)
3. Identify documents that SHOULD be present for this offering type but are MISSING
4. Check that regulatory exemption claims are consistent across all documents
5. Verify that tokenization parameters are consistent with offering terms

Use this exact schema:
{{
  "deal_overview": {{
    "deal_name": "string",
    "deal_type": "equity, debt, fund, RWA, or hybrid",
    "asset_class": "real estate, private equity, IP, sports, art, private credit, fund, or other",
    "total_value": "string",
    "parties": ["string"],
    "key_personnel": ["string — name + role"],
    "jurisdiction": "string",
    "deal_description": "one-line plain-language summary"
  }},
  "regulatory": {{
    "framework": "Reg D 506(b), Reg D 506(c), Reg A+ Tier 1, Reg A+ Tier 2, Reg S, or Reg CF",
    "exemption_details": "string",
    "investor_qualifications": "accredited, qualified purchaser, retail, or mixed",
    "filing_status": "filed, pending, or not yet filed",
    "transfer_restrictions": "string"
  }},
  "financial_data": {{
    "revenue": "string",
    "valuation": "string — pre/post-money + methodology",
    "projections": "string",
    "fee_structure": "string",
    "financial_statements": "string — summary of available statements"
  }},
  "tokenization_parameters": {{
    "blockchain": "Ethereum, Algorand, Tezos, other, or not specified",
    "token_standard": "ERC-20, ERC-1400, other, or not specified",
    "total_supply": "string",
    "price_per_token": "string",
    "distribution_mechanism": "dividend, revenue share, buyback, or none specified",
    "custody_arrangement": "SPBD, third-party, self-custody, or not specified",
    "liquidity_path": "ATS CLOB, auction, block trade, or not structured for secondary",
    "transfer_agent": "string",
    "settlement_mechanism": "on-chain instant, T+1, T+2, hybrid, or not specified",
    "geographic_restrictions": "string",
    "cap_table_summary": "string"
  }},
  "offering_terms": {{
    "minimum_investment": "string",
    "maximum_raise": "string",
    "expected_returns": "string",
    "risk_factors": ["string"],
    "use_of_proceeds": "string",
    "lockup_period": "string"
  }},
  "kyc_aml_readiness": {{
    "verification_process_present": true or false,
    "accreditation_method": "506(b) self-cert, 506(c) third-party, VerifyInvestor, other, or not documented",
    "aml_screening_evidenced": true or false,
    "gaps": ["string — specific missing items"]
  }},
  "cross_document_analysis": {{
    "missing_documents": ["string — documents expected but not found"],
    "inconsistencies": ["string — specific conflicts between documents with exact values"],
    "compliance_gaps": ["string — specific regulatory requirements not met"],
    "completeness_score": 0
  }}
}}

DOCUMENT EXTRACTIONS:
{docs_json}"""


# ── LENS PROMPTS ──────────────────────────────────────────────────────────────

LENS_SYSTEM = """You are Prism, an AI-powered data room intelligence tool for tokenized securities. Generate concise, role-specific analysis from deal data.

FORMATTING RULES — follow exactly:
- Use ## headers to separate every section
- Under each header, use bullet points (- ) for all content — never write prose paragraphs
- Each bullet is one clear, specific point — one idea per line
- Lead every bullet with a bold label where applicable: - **Label:** value
- Use actual numbers, names, and dates from the data — never be vague
- Keep bullets short — 1-2 lines maximum
- If a field is unknown or not in the data, write: - Not specified in documents"""


def get_executive_prompt(deal_json):
    return f"""Generate an Executive Summary for this tokenized securities deal. Use ## headers and bullet points throughout — no prose paragraphs.

## Deal snapshot
- Deal name, one-line description, asset class, structure, jurisdiction — one bullet each

## Key numbers
- One bullet per figure: raise target, pre-money valuation, post-money valuation, price per token, total tokens, lockup period, investor type

## Management
- One bullet per person: name and role
- One bullet for legal counsel
- One bullet for platform/transfer agent

## Recommendation
- **Decision:** GO / CONDITIONAL GO / NO-GO
- **Rationale:** 2-3 bullet points explaining the decision based on specific data

## Top risks
- Three numbered bullets, each starting with a bold risk name and specific detail from the data

## Key dates
- One bullet per date in chronological order

DEAL DATA:
{deal_json}"""


def get_legal_prompt(deal_json):
    return f"""Generate a Legal Review for this tokenized securities deal. Use ## headers and bullet points throughout — no prose paragraphs.

## Regulatory framework
- One bullet each: exemption type, filing status, investor qualification requirements, transfer restrictions

## Document obligations
- One bullet per material obligation, covenant, or condition found across documents

## Missing documents
- One bullet per missing document — include why it matters legally

## KYC/AML readiness
- One bullet each: verification process status, accreditation method, AML screening evidence
- One bullet per gap identified

## Compliance gaps
- One bullet per gap, ranked by severity — label each CRITICAL / HIGH / MEDIUM

## Flags and blockers
- One bullet per inconsistency, error, or missing item that could block closing

DEAL DATA:
{deal_json}"""


def get_finance_prompt(deal_json):
    return f"""Generate a Finance Review for this tokenized securities deal. Use ## headers and bullet points throughout — no prose paragraphs.

## Valuation summary
- One bullet each: pre-money, post-money, methodology, price per unit/token

## Financial performance
- One bullet each: revenue, gross margin, net loss/income, cash position, runway

## Cap table
- One bullet per ownership tier with percentage and unit count
- One bullet flagging any discrepancies in committed amounts across documents

## Projections
- One bullet per year of revenue projection
- One bullet on growth assumptions
- One bullet on use of proceeds breakdown

## Fee structure
- One bullet each: management fees, carry, placement fees, preferred return, liquidation preference

## Financial flags
- One bullet per inconsistency or concern — be specific with exact figures

DEAL DATA:
{deal_json}"""


def get_bd_prompt(deal_json):
    return f"""Generate a BD Partner Brief for this tokenized securities deal. Use ## headers and bullet points throughout — no prose paragraphs. This brief will be shared externally with potential partners.

IMPORTANT: Do NOT include any internal flags, compliance gaps, investor names from side letters, or confidential terms. Partner-facing output only.

## Deal overview
- One bullet on what the company does
- One bullet on the market opportunity
- One bullet on why this deal is interesting to partners

## Structure and terms
- One bullet each: deal type, raise amount, price per token, asset class, lockup, investor type

## Tokenization
- One bullet each: blockchain, token standard, trading venue, settlement mechanism

## Key parties
- One bullet per party: issuer, legal counsel, platform — publicly known parties only

## Liquidity path
- One bullet each: secondary trading structure, ATS details, estimated timeline

DEAL DATA:
{deal_json}"""


def get_token_ops_prompt(deal_json):
    return f"""Generate a Token Operations Assessment for this tokenized securities deal. Use ## headers and bullet points throughout — no prose paragraphs.

## Token parameters
- One bullet each: blockchain, standard, total supply, price per token, token name/symbol

## Smart contract configuration
- One bullet each: whitelist requirements, geographic restrictions, lockup enforcement, dividend distribution mechanism

## Custody and transfer
- One bullet each: custodian, transfer agent, transfer restriction enforcement, ROFR mechanics

## Secondary trading readiness
- One bullet each: ATS eligibility, trading model, settlement mechanism, on-chain credential requirements

## KYC/AML readiness
- One bullet each: verification provider, on-chain credential type, screening status, whitelist readiness

## Blockers and action items
- One bullet per blocker, ranked CRITICAL / HIGH / MEDIUM — include what must happen before issuance

DEAL DATA:
{deal_json}"""


def get_investor_prompt(deal_json):
    return f"""Generate an Investor Relations Summary for this tokenized securities deal. Use ## headers and bullet points throughout — no prose paragraphs. Write all dollar amounts with spaces around numbers.

## The offering
- One bullet each: what is being offered, by whom, through what structure, tokenization platform

## Investment terms
- One bullet each: minimum investment, price per token, total raise, lockup period, liquidation preference, anti-dilution, distribution mechanism

## The company
- One bullet on what the company does
- One bullet on market opportunity and current traction
- One bullet per key management team member

## Risk factors
- One bullet per risk, ranked HIGH / MEDIUM / LOW — include source (stated in documents vs flagged by analysis)

## Returns and distributions
- One bullet each: expected returns, distribution mechanism, timing
- If no projections stated, say so explicitly

## Liquidity and exit
- One bullet each: lockup expiry, secondary trading path, settlement mechanism

## Eligibility
- One bullet each: accreditation requirements, geographic restrictions, qualification criteria

DEAL DATA:
{deal_json}"""