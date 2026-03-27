"""
cache_demo.py — Run the full Prism pipeline once and save output to demo_cache.json
Run this before the demo: py cache_demo.py
"""

import json
import os
import anthropic
from pdf_utils import extract_text_from_pdf
from prompts import (
    EXTRACTION_SYSTEM, get_extraction_prompt,
    SYNTHESIS_SYSTEM, get_synthesis_prompt,
    LENS_SYSTEM,
    get_executive_prompt, get_legal_prompt, get_finance_prompt,
    get_bd_prompt, get_token_ops_prompt, get_investor_prompt,
)

SAMPLE_DIR = "sample_docs"
OUTPUT_FILE = "demo_cache.json"

client = anthropic.Anthropic(api_key=open(".streamlit/secrets.toml").read().split('"')[1])

def call_claude(system, user_prompt, label):
    print(f"  Calling Claude: {label}...")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=system,
        messages=[{"role": "user", "content": user_prompt}]
    )
    raw = response.content[0].text
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {"raw": raw.strip()}

def main():
    print("=== Prism Demo Cache Generator ===\n")

    pdf_files = [f for f in os.listdir(SAMPLE_DIR) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} documents in {SAMPLE_DIR}/\n")

    # Stage 1a: Per-document extraction
    print("Stage 1a: Extracting documents...")
    extractions = []
    for filename in pdf_files:
        filepath = os.path.join(SAMPLE_DIR, filename)
        # pdf_utils expects a file-like object — open as binary
        with open(filepath, "rb") as f:
            text, err = extract_text_from_pdf(f)
        if err or not text:
            print(f"  ✗ {filename} (skipped: {err})")
            continue
        result = call_claude(EXTRACTION_SYSTEM, get_extraction_prompt(filename, text), filename)
        extractions.append(result)
        print(f"  ✓ {filename}")

    # Stage 1b: Synthesis
    print("\nStage 1b: Synthesizing...")
    docs_json = json.dumps(extractions, indent=2)
    deal_json = call_claude(SYNTHESIS_SYSTEM, get_synthesis_prompt(docs_json), "synthesis")
    print("  ✓ Synthesis complete")

    # Stage 2: Six lenses
    print("\nStage 2: Generating lenses...")
    lens_cache = {}
    deal_str = json.dumps(deal_json, indent=2)
    lens_prompts = {
        "Executive": get_executive_prompt,
        "Legal": get_legal_prompt,
        "Finance": get_finance_prompt,
        "BD": get_bd_prompt,
        "Token Ops": get_token_ops_prompt,
        "Investor": get_investor_prompt,
    }
    for lens_name, prompt_fn in lens_prompts.items():
        result = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=LENS_SYSTEM,
            messages=[{"role": "user", "content": prompt_fn(deal_str)}]
        ).content[0].text
        lens_cache[lens_name] = result
        print(f"  ✓ {lens_name}")

    # Save with matching session state key names
    cache = {
        "extractions": extractions,
        "deal_json": deal_json,
        "lens_cache": lens_cache,
    }
    with open(OUTPUT_FILE, "w") as f:
        json.dump(cache, f, indent=2)

    print(f"\n✓ Saved to {OUTPUT_FILE}")
    print("Load Demo Data button will now appear in the Prism sidebar.")

if __name__ == "__main__":
    main()