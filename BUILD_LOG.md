# Prism — Build Log

**tZERO hAIckathon | March 26–27, 2026 | Team Assisted Intelligence**

A running record of every decision, tool choice, failure, and lesson during the hackathon build.

---

## How to use this log

Add entries as you go. Timestamp everything. Log decisions (what and why), tools (what and why this one), failures (what broke, what we learned, what we changed), and milestones (what's working now). Don't reconstruct at the end — capture in real time.

---

## Pre-Build Planning (March 25, 2026)

**Decision: Product architecture**
Designed two-stage AI pipeline before writing any code. Stage 1: per-document extraction → cross-document synthesis. Stage 2: six parallel lens analyses cached in session state. Every architecture decision made in advance so the build window is pure execution.

**Decision: Tech stack**
Streamlit (known framework, 28 hours isn't time to learn React), Anthropic Claude API Sonnet 4.6 (strong structured reasoning, reliable JSON), pdfplumber (PDF text extraction), fpdf2 (PDF export). Four dependencies total.

**Decision: Security architecture**
Zero-retention by design — documents in memory only, never persisted to disk. API key in secrets.toml excluded from repo. BD lens confidentiality filter at prompt level. This isn't a limitation — it's the correct architecture for handling regulated securities documents.

**Decision: Six lenses**
Executive, Legal, Finance, BD, Token Ops, Investor. Based on the actual roles that sit at the table during a tokenized securities deal at tZERO. Each lens has a distinct professional role, priorities, and exclusions.

---

## Build Day — Thursday, March 26

### [~2:30 PM ET, March 26] — Build started
Dependencies installed: streamlit, anthropic, pdfplumber, fpdf2. Used `py -m pip install` (pip not on PATH directly — harmless). API key saved to .streamlit/secrets.toml (gitignored). Moving into sample doc generation.

### [TIMESTAMP] — Sample documents generated
**Method:** [how generated]
**Result:** [success/issues]

### [TIMESTAMP] — First successful extraction
**What worked:** [description]
**What failed first:** [description]
**Fix:** [what changed]
**Lesson:** [what was learned]

### [TIMESTAMP] — [Next milestone]
[Continue logging...]

---

## Build Day — Friday, March 27

### [TIMESTAMP] — [Entry]
[Continue logging...]

---

## AI Collaboration Log

Throughout the build, Claude (Anthropic's AI) served as the technical collaborator. This section documents how AI was used and what the human-AI split looked like.

**Human contributions:** Product vision, architecture decisions, UX design, domain expertise (due diligence, tokenized securities, tZERO's pipeline), demo scripting, all business/security/scalability reasoning.

**AI contributions:** Code implementation, prompt engineering iteration, error handling patterns, HTML/CSS for UI components, PDF generation scripts.

**Key AI interactions:**
- [Log specific prompts that worked well or poorly]
- [Log when AI suggestions were overridden and why]
- [Log failures and iterations]

---

## Failures & Lessons

| Failure | What happened | What we learned | What we changed |
|---------|--------------|-----------------|-----------------|
| [Description] | [Details] | [Lesson] | [Fix] |

---

## Final State

**Working features:** [list at submission time]
**Known issues:** [honest list of what doesn't work perfectly]
**If we had more time:** [what we'd add next]
