# Prism — Build Log

**tZERO hAIckathon | March 26–27, 2026 | Team Assisted Intelligence**

A running record of every decision, tool choice, failure, and lesson during the hackathon build. The CTO specifically asked for this — process and thinking matter as much as execution.

---

## How to use this log

Add entries as you go. Timestamp everything. Log decisions (what and why), tools (what and why this one), failures (what broke, what we learned, what we changed), and milestones (what's working now). Don't reconstruct at the end — capture in real time.

---

## Pre-Build Planning — March 25, 2026 (evening before kick-off)

No code was written on March 25. This section documents the planning and decision-making done the night before the build window opened — architecture, schema design, product decisions, and the build specification document. All implementation happened on March 26–27.

**Decision: Product architecture**
Designed two-stage AI pipeline before writing any code. Stage 1a: per-document extraction (one Claude call per PDF). Stage 1b: cross-document synthesis (one Claude call, all extractions as input). Stage 2: six parallel lens analyses, cached in session state after first generation. Every architecture decision made in advance so the build window is pure execution.

**Decision: Tech stack**
Streamlit (known framework, 28 hours isn't time to learn React), Anthropic Claude API claude-sonnet-4-20250514 (reliable JSON output, fast enough for real-time use), pdfplumber (PDF text extraction), fpdf2 (PDF export). Four dependencies total. Minimal surface area reduces failure modes.

**Decision: Security architecture**
Zero-retention by design — documents in memory only, never persisted to disk or logged. API key isolated in `.streamlit/secrets.toml`, excluded from version control via `.gitignore`. BD lens confidentiality filter at prompt level — internal flags and investor names stripped before generating partner-facing output. Security isn't a feature added at the end; it's the foundation of the architecture.

**Decision: Six lenses**
Executive, Legal, Finance, BD, Token Ops, Investor. Derived from the actual roles that sit at the table during a tokenized securities deal at tZERO. Each lens has a distinct professional audience, distinct priorities, and explicit exclusions. The BD lens is the clearest example: it explicitly excludes internal compliance flags that would be appropriate for Legal but inappropriate to share with external partners.

**Decision: JSON schema**
Designed complete 60+ field schema before writing prompts. The schema is the contract between Stage 1 and everything downstream. Getting it right in advance prevents mid-build refactoring. Key sections: deal_overview, regulatory, financial_data, tokenization_parameters, offering_terms, kyc_aml_readiness, documents[], cross_document_analysis.

**Decision: Sample documents**
Designed 15 NovaTech sample PDFs with 4 deliberately planted errors to demonstrate Prism's cross-document intelligence:
1. Entity name mismatch — operating_agreement_v3.pdf says "NovaTech Inc." vs. "NovaTech LLC" everywhere else
2. Subscription amount discrepancy — $2.1M in cap table vs. $1.8M in subscription agreement vs. $750K in Form D
3. Form D investor count — reports 1 investor, cap table shows multiple subscribers
4. Missing executed signatures — referenced in subscription agreement but not present in data room

Two structural gaps always present: missing accredited investor verification letters (required for 506(c)) and missing AML/KYC documentation (referenced in tokenization spec, absent from data room).

**Output of March 25 planning:**
- 1,047-line build specification document covering every architecture, design, product, and demo decision
- File structure defined (no code written — only empty placeholder files with docstring comments to establish the scaffold)
- Sample document content specifications written out in full

---

## Build Day — Thursday, March 26

### ~11:00 AM ET — Kick-off call

Attended tZERO hAIckathon kick-off. Key takeaways:
- **Judges:** Ganesh (CTO, process/scalability focus), Chris Russell (security focus), Julie (marketing/use case focus)
- **Presentation:** 10-minute live demo at 4:45 PM CT Friday
- **Submission:** 2:00 PM CT Friday
- **Rules:** Security hardening required (Snyk recommended), function over style, graceful failure (Goal + Technique + Pivot), BUILD_LOG.md required, code must be available for review
- **Five judging pillars:** Functionality, Stability, Security, Scalability, Ingenuity

### ~11:30 AM ET — Environment setup and build begins

**Tools installed (one at a time per Windows/PowerShell constraints):**
- `pip install streamlit`
- `pip install anthropic`
- `pip install pdfplumber`
- `pip install fpdf2`

Note: pip PATH warning appeared during install — resolved by using `py -m` prefix. No functional impact.

**Files created:**
- `.streamlit/secrets.toml` — API key stored here, excluded from git
- `.gitignore` — secrets.toml, __pycache__, .env confirmed excluded

### ~12:00 PM ET — Sample documents generated

Generated all 15 NovaTech sample PDFs using fpdf2 via `generate_samples.py`. All documents created programmatically to ensure consistent data with controlled errors. Verified all 4 planted errors present in correct documents before proceeding.

**Milestone: Environment ready, sample docs exist.**

### ~12:30–2:00 PM ET — Foundation: pdf_utils.py

Built `pdf_utils.py` — pdfplumber text extraction with graceful error handling. Key decisions:
- Truncate extracted text at 3,000 characters per document for hackathon (controls token usage, synthesis call stays manageable)
- Return `(text, error)` tuple — caller decides how to handle failure rather than raising
- Unreadable PDFs (scanned/image-based) skip silently with warning, don't crash the pipeline

### ~2:00–4:00 PM ET — Prompt engineering: prompts.py

Built all 8 prompts in `prompts.py`. Most significant engineering work of the build.

**Stage 1a (extraction prompt):**
Critical instruction: "Return ONLY valid JSON — no preamble, no explanation, no markdown code fences." Without this Claude occasionally wraps output in ```json blocks, which breaks JSON parsing downstream. Added defensive parsing in app.py to strip fences if present regardless.

**Stage 1b (synthesis prompt):**
Added explicit cross-referencing instructions — compare dollar amounts, check entity name consistency, identify missing documents. Without explicit instructions Claude synthesizes but doesn't aggressively cross-reference. The "CRITICAL CROSS-REFERENCING INSTRUCTIONS" block is what enables catching the planted errors.

**Stage 2 (lens prompts):**
Initial version used a minimal LENS_SYSTEM with no formatting rules. Output was readable prose but dense. Updated LENS_SYSTEM to include explicit formatting rules: ## headers for every section, bullet points for all content (no prose paragraphs), bold labels, one idea per line, actual numbers and names from data. Each individual lens prompt updated to specify "one bullet per X."

**Failure:** First synthesis test returned inconsistent JSON — some fields missing, others renamed. Root cause: prompt schema had ambiguous field names. Fix: made schema explicit with typed values for every field ("equity | debt | fund | RWA | hybrid" rather than "string").

**Lesson:** Defensive JSON parsing is not optional. Built strip-fence + json.loads() with retry from the first call.

### ~4:00–4:30 PM ET — Full pipeline: app.py

Built `app.py` — the orchestration layer connecting all components. Four-state architecture: upload → processing → data room → lens view. Session state manages all data so lens switching doesn't re-call Claude.

### ~4:30 PM ET — Pipeline confirmed end-to-end

Full 15-document NovaTech run completed successfully:
- All 15 PDFs extracted
- Synthesis completed — deal overview, regulatory framework, tokenization parameters all populated
- All 4 planted errors caught in cross_document_analysis
- All 6 lenses generating correctly

**Milestone: Full pipeline working.**

### ~5:00 PM ET — Investor prompt fix

First full run revealed Investor lens returning malformed output. Root cause: ambiguous dollar amount formatting instruction. Fixed by rewriting investor prompt with explicit "Write all dollar amounts with spaces around numbers" and restructuring sections.

### ~5:15 PM ET — First GitHub push

Pushed to GitHub. Commit: "Initial working build — pipeline end-to-end, all lenses generating."

**Decision: PDF export disabled**
`fpdf2` encoding bug on special characters (em dashes, smart quotes, dollar signs) caused export to crash. Non-critical for judging. Disabled export button. Replaced with markdown download button (see Demo Day entry).

### ~7:00 PM ET — Security scan

**Tool:** Snyk (snyk.io web dashboard — npm not installed on machine, web import used instead)
**Method:** Connected GitHub repo, Snyk imported requirements.txt
**Result:** 0 issues, 0 vulnerable paths across all dependencies (streamlit, anthropic, pdfplumber, fpdf2)

Snyk scan report available at snyk.io/org/sethberjansky/projects.

### ~7:15 PM ET — Demo cache built

Built `cache_demo.py` — standalone script that runs the full pipeline once against all 15 sample docs and saves output to `demo_cache.json`. Added "Load Demo Data" button to sidebar — appears only if `demo_cache.json` exists, loads pre-computed analysis instantly with no API call.

**Why:** Demo insurance policy. If API times out during the live 10-minute demo, one button click restores the full pre-computed NovaTech analysis.

First cache run hit a 529 overloaded error on the final lens. Transient API issue — re-ran immediately, completed successfully. Informed the decision to add exponential backoff retry logic to `call_claude`.

### ~8:00 PM–11:00 PM ET — UI polish session

Built complete `ui_components.py` — custom HTML/CSS rendering layer injected via `st.markdown(unsafe_allow_html=True)`.

**Design decisions:**
- DM Sans (Google Fonts) — clean, modern
- Teal (#1D9E75) used in exactly three places: logo mark, active lens state, cache checkmark indicators
- Near-achromatic base (#F5F5F2 background, #FFFFFF cards)
- Semantic colors: red for flags, amber for warnings, green for clear/success
- 72ch max-width on paragraph text — prevents line stretch on wide viewports

**Failures encountered and fixed:**

*Multi-line HTML strings rendering as raw text*
Cause: Blank lines inside multi-line HTML strings trigger Streamlit's markdown parser to fall back to code block rendering. Fix: Collapsed all multi-line HTML strings to single lines.

*Nested f-string syntax error*
Cause: Conditional expression inside f-string using escaped quotes. Fix: Extracted conditional to a variable before the markdown call.

*Sidebar toggle hidden after UI changes*
Cause: `header { visibility: hidden; }` in global CSS was hiding the Streamlit header bar, which is where the sidebar toggle button lives. Fix: Removed `header` from the hidden elements entirely.

*Completeness stat showing "—"*
Cause: `completeness_score` absent from synthesis JSON output in practice. Replaced with live flag count — always available and semantically stronger.

**Second GitHub push at ~11:00 PM ET.**

---

## Demo Day — Friday, March 27

### ~9:00 AM ET — Export button added (markdown download)

Added `st.download_button` to each lens view. Users can download any lens output as a `.md` file named after the lens. Functional export, zero encoding risk.

### ~9:30 AM ET — Parallel extraction implemented

Replaced sequential per-document extraction with `ThreadPoolExecutor(max_workers=5)`. Five documents extract simultaneously. Extraction time for 15 documents dropped from ~60 seconds to ~20-25 seconds. PDF text is read on the main thread before handing to workers (Streamlit file objects are not thread-safe).

### ~10:00 AM ET — Text sanitization fixes

*Dollar signs rendering as LaTeX math*
Cause: Streamlit's markdown parser treats `$...$` as LaTeX math mode. Fix: Added `text.replace('$', r'\$')` in `_sanitize_lens_output()`.

*Green monospace text on numbers*
Cause: Claude occasionally wrapped numbers in backtick code spans. Fix: Regex to strip backtick spans before rendering.

*Bold/italic markers rendering inconsistently*
Cause: `**bold**` and `*italic*` markers adding noise since CSS handles visual hierarchy. Fix: Regex to strip these markers before rendering.

### ~10:30 AM ET — Parallel lens pre-generation

**Problem:** Lens switching was 15-20 seconds per click — each click made a fresh API call.

**Fix:** Added `LENS_PROMPT_FNS` dict, `generate_one_lens()` function, and `run_all_lenses()` with `ThreadPoolExecutor(max_workers=6)`. After synthesis completes, all 6 lens prompts fire simultaneously. Third spinner — "Generating all lens views..." — appears after synthesis. Once complete, all lenses are pre-cached and switching is instant.

**Result:** Lens switching is now instant after initial analysis. Total pipeline time ~90-120 seconds upfront for 15 documents.

Also reduced `max_tokens` from 2000 to 1500 — lens prompts use ~800-1000 tokens in practice, reducing the ceiling shaves time off the parallel round.

### ~11:00 AM ET — temperature=0 for output consistency

**Problem:** Flag count varied slightly between runs due to model temperature variance. "Missing documents" and "compliance gaps" in particular shifted since they are synthesis judgments rather than hard-coded facts.

**Fix:** Added `temperature` parameter to `call_claude()`. Set `temperature=0` on synthesis and all lens calls. Extraction calls left at default (1) — per-document extraction is deterministic enough from structured documents.

**Result:** Flag count now consistent across runs. Confirmed 12 flags on every run: 2 inconsistencies, 7 missing documents, 3 compliance gaps. All 4 planted errors surface consistently.

### ~11:15 AM ET — "One deal per session" UI hint

Identified edge case: uploading documents from two companies in one session would confuse synthesis. Added one-liner under upload area: "One deal per session." Multi-deal portfolio analysis is v2.

### ~11:30 AM ET — Demo cache regenerated

Regenerated `demo_cache.json` to reflect updated LENS_SYSTEM formatting rules, `temperature=0`, and current sanitization logic. Previous cache was built before these changes.

### Final GitHub push — before submission

Committed all final changes: parallel extraction, parallel lenses, text sanitization, temperature=0, markdown export, "one deal per session" hint, BUILD_LOG final.

---

## AI Collaboration Log

Throughout the build, Claude (Anthropic's AI) served as the technical collaborator. This documents the human-AI split.

**Human contributions:** Product vision, architecture decisions, UX design principles, domain expertise (due diligence, tokenized securities, tZERO's pipeline), demo scripting, all business/security/scalability reasoning, error identification during testing, prompt iteration based on observed output quality, all judgment calls on what to build vs. defer.

**AI contributions:** Code implementation across all five Python files, prompt engineering iteration, error handling patterns, HTML/CSS for UI components, PDF generation scripts, regex sanitization logic, parallel threading implementation, retry logic with exponential backoff.

**Key AI interactions:**
- Extraction prompt iterated 3 times — "Return ONLY valid JSON" and schema specificity were the key variables
- UI rendering required 4 iterations to resolve Streamlit HTML/markdown parsing conflicts
- Dollar sign LaTeX bug: identified visually, root cause traced to Streamlit markdown parser, fix applied
- Parallel lens architecture implemented but missed in one file version during a paste — caught by testing and corrected morning of demo day
- temperature=0: observed flag count variance, identified root cause, applied targeted fix

---

## Failures & Lessons

| Failure | What happened | What we learned | What we changed |
|---------|--------------|-----------------|-----------------|
| Inconsistent extraction JSON | Claude added preamble and ```json fences | Always include "Return ONLY valid JSON" in prompt | Added to all extraction/synthesis prompts |
| PDF export crash | fpdf2 encoding error on special characters | Special chars need sanitization before PDF generation | Replaced with markdown download button |
| Sidebar toggle disappeared | CSS `header { visibility: hidden }` hid toggle button | Streamlit's sidebar toggle lives in the header element | Removed header from hidden elements |
| Completeness score showing "—" | Field path wrong in synthesis JSON output | Rely on always-available fields for UI stats | Replaced with flag count |
| Dollar signs as LaTeX | Streamlit parses `$...$` as math mode | Escape dollar signs before markdown rendering | Added `replace('$', r'\$')` in sanitizer |
| Backtick numbers green monospace | Claude used backtick code spans on numbers | Strip backticks before rendering | Added regex to sanitize function |
| Lens switching slow (15-20s) | Parallel lens generation missing from deployed file | Verify features are in the correct deployed file after paste | Added run_all_lenses with ThreadPoolExecutor |
| API 529 overloaded | Transient Anthropic API overload mid-pipeline | Retry logic with backoff is essential | Added 4-attempt retry with exponential backoff |
| Inconsistent flag counts | Model temperature variance affecting synthesis judgments | temperature=0 dramatically improves output consistency | Applied temperature=0 to synthesis and all lens calls |

---

## Final State at Submission

**Working features:**
- PDF upload (single or multiple documents, one deal per session)
- Parallel document extraction (5 concurrent workers, ~20-25 seconds for 15 docs)
- Cross-document synthesis with entity name, dollar amount, and consistency checks
- All 4 planted NovaTech errors caught on every run — confirmed consistent at temperature=0
- All 6 lens views pre-generated in parallel after synthesis (instant switching)
- Markdown download button per lens
- Load Demo Data emergency backup (pre-computed JSON, zero API calls)
- Clean Snyk scan (0 issues, 0 vulnerable paths)
- Zero-retention architecture (no disk writes, no logging of document content)
- BD lens confidentiality filter (prompt-level exclusion of internal flags)

**Known limitations:**
- Single deal per session (multi-deal portfolio analysis is v2)
- Branded PDF export disabled due to fpdf2 encoding bug on special characters
- Analysis time ~90-120 seconds for 15 documents on live run
- temperature=0 dramatically improves but does not mathematically guarantee identical output across runs

**If we had more time:**
- Async/parallel synthesis using Anthropic Batch API
- Branded PDF export with fpdf2 (special character sanitization fix)
- RBAC — Legal sees Legal, BD sees BD, exec sees all
- Redis for session state (enables horizontal scaling)
- Feedback loop: user corrections that improve extraction accuracy over time
- tZERO API integration: Token Ops lens pre-populates configuration rather than just assessing readiness

---

## Scalability Notes (for Ganesh)

**Current architecture:** Parallel per-document extraction (5 workers) → single synthesis call → 6 parallel lens calls. Streamlit manages session state in memory.

**10 users:** Works as-is. Each session is independent.

**10,000 users:** Add a task queue (Celery + Redis) in front of the pipeline. Move session state from Streamlit memory to Redis. API rate limits are the primary bottleneck, not application architecture.

**10 million users:** Anthropic Batch API for synthesis and lens generation (cost drops ~50%, async). Kubernetes for horizontal scaling. The pipeline architecture doesn't change — only where it runs and how it's queued.

**Multi-chain:** Schema has a `blockchain` field that's chain-agnostic. Demo uses Ethereum ERC-1400, but extraction and lens logic reads whatever's in the documents. Token Ops lens would surface different smart contract standards for Algorand or Tezos — architecture is identical.