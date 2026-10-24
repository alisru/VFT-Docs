#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chatlog-to-Document Extractor & Distiller (Chat-to-Doc Exon Purifier)
====================================================================
Transforms raw conversational chat logs (e.g. ChatGPT, Claude, Gemini exports)
into publication-grade, self-contained formal treatises and whitepapers.

Key Transformations:
  1. Dialogue Intron Stripping:
     - Excises user prompt instructions ("add the whole...", "give me a continuation", "can you show me").
     - Excises AI conversational pleasantries ("Nice — here's...", "Yes — we can...", "Done. I've compiled...").
     - Excises conversational meta-scaffolding ("You've hit on something real", "Let me structure this").
  2. Voice Normalization (Conversational -> Objective Expository):
     - Converts second-person / first-person chat framing:
       "your unified fractal number model" -> "the unified fractal number model"
       "what you're describing" -> "the framework"
       "I give a few concrete circuit patterns" -> "Concrete circuit patterns include"
  3. Content-Bearing Exon Preservation:
     - Preserves all mathematical definitions, theorems, axioms, formulas, tables, and circuit schematics.
  4. Thematic Section Sequencing:
     - Automatically structures extracted content into structured chapters:
       I. Foundational Definitions & Axioms
       II. The INDEF Object & Infinitesimal Arithmetic
       III. Operational Generative Calculus & Continuous Resolution
       IV. Analog & Neuromorphic Hardware Implementation
       V. Hyperreal, Non-Standard & Model-Theoretic Formalization
"""

import sys
import re
from pathlib import Path
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\semantic_gluon_dna")
CHAT_PATH = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\chatgpt infinity maths.md")

# Strict patterns indicating pure conversational dialogue or prompt introns
CHAT_PROMPT_PATTERNS = [
    r"^(?:add the whole|can you|could you|please explain|show me|give me|what if|continue|tell me|rewrite|i want a complete|what about|how about|how do we|how can we)\b",
    r"^(?:Chat history|##### You said|###### ChatGPT said|Was this response better\?|Level [0-9]:)",
    r"\[\[Skip to content\]",
    r"^(?:Done\.|Nice —|Yes —|Excellent\.|Sure,|Here is|In this response|You’ve hit on|You're effectively|Let me unpack|That reads like you)\b"
]

# Patterns for conversational hedging inside a block that can be surgically trimmed
HEADING_CLEANERS = [
    (r"^(?:Nice — here’s a clear[^.]+?\.\s*)", ""),
    (r"^(?:Yes — we can absolutely[^.]+?\.\s*)", ""),
    (r"^(?:Yes — we can\.[^.]+?\.\s*)", ""),
    (r"^(?:Excellent\. I’ll prepare[^.]+?\.\s*)", ""),
    (r"^(?:You’ve hit on something very real here\.[^.]+?\.\s*)", ""),
    (r"^(?:Done\. I’ve compiled[^.]+?\.\s*)", ""),
    (r"^(?:That reads like you’re trying to formalise a recursive definition[^:]*?:\s*)", "A recursive definition can be formalized as follows:\n\n"),
    (r"^(?:That reads like you're trying to formalise a recursive definition[^:]*?:\s*)", "A recursive definition can be formalized as follows:\n\n"),
    (r"^(?:If you really want a function expression, you could define:\s*)", "The function expression can be defined as:\n\n"),
    (r"\byour unified\b", "the unified"),
    (r"\byour \[Variable", "the [Variable"),
    (r"\byour framework\b", "the framework"),
    (r"\byour model\b", "the model"),
    (r"\byour system\b", "the system"),
    (r"\byou’re describing\b", "described herein"),
    (r"\byou're describing\b", "described herein"),
    (r"\bI give a few\b", "Presented below are"),
    (r"\bI’ll give you\b", "Below are")
]

THEMATIC_CHAPTERS = [
    {
        "id": "ch1_foundations",
        "title": "I. Foundational Principles & Relative Infinities",
        "keywords": ["relative infinities", "framing operator", "uncountably infinite", "definitive 0", "100%", "container", "definition of number"]
    },
    {
        "id": "ch2_indef_object",
        "title": "II. The INDEF Object, Shells & Infinitesimal Arithmetic",
        "keywords": ["indef", "x = [x] + x_chi", "infinitesimal", "chi-tensor", "propagation operator", "carry", "base-b", "stabilization", "heartbeat"]
    },
    {
        "id": "ch3_calculus_time",
        "title": "III. Operational Generative Calculus, Planck Time & Dynamic Collapse",
        "keywords": ["t[0,1]", "heartbeat of reality", "algebraic transformation", "collapse", "implicative state", "definitive state", "instantaneous resolution", "pi as the geometric"]
    },
    {
        "id": "ch4_hardware",
        "title": "IV. Analog, Voltage-Based & Neuromorphic Hardware Implementation",
        "keywords": ["fractalnode", "voltage", "capacitor", "csum", "circuit", "charge sharing", "analog multiplier", "neuromorphic", "memristive", "spice", "pcb"]
    },
    {
        "id": "ch5_hyperreal_formalism",
        "title": "V. Hyperreal, Non-Standard & Model-Theoretic Foundations",
        "keywords": ["ultrapower", "ultrafilter", "nonstandard", "hahn field", "non-archimedean", "transfer principle", "series", "laurent", "formal proof"]
    }
]

def is_pure_dialogue_intron(text: str) -> bool:
    t = text.strip()
    if len(t) < 15:
        return True
    # Explicit user prompts to the AI assistant
    if re.search(r"^(?:can you|could you|please|show me|give me|what about|add the whole|rewrite|turn this into|how would we|how can we|what if we|is this|why is this|does this)\b", t, re.I):
        return True
    if re.search(r"\b(?:can you turn this into|give me a continuation prompt|i want a complete verbose document)\b", t, re.I):
        return True
    # Short question lines without math
    if t.endswith("?") and len(t.split()) < 20 and not re.search(r"(=|<=|>=|\\frac|\$\$|X\s*=|\\chi|\\pi|\\lim)", t):
        return True
    # AI conversational pleasantries and agreements
    if re.search(r"^(?:You’re right to|You are right to|You’re correct|You are correct|You’re spot on|Good question|Great question|You hit on)\b", t, re.I):
        return True
    # AI questions and dialogue closures back to the user
    if re.search(r"\b(?:do you want me to|would you like me to|let me know if you want|should i rewrite|shall i|if you'd like me to|how would you like to proceed)\b", t, re.I):
        return True
    # Dangling fragments starting with lowercase conjunctions or copula
    if re.match(r"^(?:is|are|was|were|and|or|but|so|with|that)\s", t) and len(t.split()) < 20:
        return True
    for pat in CHAT_PROMPT_PATTERNS:
        if re.search(pat, t, re.I):
            if len(t) < 300 and not re.search(r"(=|<=|>=|\\frac|\$\$|X\s*=|Capacitor|Node|Definition|Theorem)", t):
                return True
    return False

def clean_dialogue_artifacts(text: str) -> str:
    t = text.strip()
    for pat, repl in HEADING_CLEANERS:
        t = re.sub(pat, repl, t, flags=re.I)
    # Windows-1252 & Pandoc repairs
    t = t.replace("(I., I^)", r"$(\upsilon, \psi)$").replace("(I.,I^)", r"$(\upsilon, \psi)$")
    t = t.replace("x_I", r"$x_\chi$").replace('I"H', r"$\Delta H$").replace("+'", r"\to").replace("+->", r"\to")
    t = re.sub(r"\bEpoch[A-Za-z0-9]*\b", "Epoché", t)
    t = re.sub(r"\bTechn[A-Za-z0-9]*\b", "Technē", t)
    return t.strip()

def distill_chatlog_to_document(chatlog_path: Path, output_doc_path: Path):
    if not chatlog_path.exists():
        print(f"Error: {chatlog_path} does not exist.")
        return

    raw_text = chatlog_path.read_text(encoding="utf-8", errors="ignore")
    raw_blocks = [b.strip() for b in re.split(r"\n\s*\n", raw_text) if b.strip()]
    total_blocks = len(raw_blocks)

    pure_exons = []
    culled_introns = 0

    for b in raw_blocks:
        if is_pure_dialogue_intron(b):
            culled_introns += 1
            continue

        cleaned = clean_dialogue_artifacts(b)
        if len(cleaned) < 20 or (cleaned.lower().startswith("and said") and len(cleaned.split()) < 25):
            culled_introns += 1
            continue

        pure_exons.append(cleaned)

    # De-duplicate identical or near-identical statements within chapters
    chapter_buckets = defaultdict(list)
    for exon in pure_exons:
        exon_lower = exon.lower()
        best_ch = THEMATIC_CHAPTERS[0]["id"]
        best_score = -1.0
        for ch in THEMATIC_CHAPTERS:
            score = sum(2.0 for kw in ch["keywords"] if kw.lower() in exon_lower)
            if score > best_score:
                best_score = score
                best_ch = ch["id"]
        chapter_buckets[best_ch].append(exon)

    # Assemble formal document
    doc_lines = [
        "# Infinity Indefinite Mathematics (IRM): Formal Technical Monograph",
        "## Derived from Ancestral Exploratory Research Dialogue via Automated Exon Distillation",
        f"**Source Chat Log Ingested**: `{chatlog_path.name}` ({total_blocks} raw dialogue blocks)",
        f"**Pure Formal Exons Distilled**: {len(pure_exons)} | **Conversational Introns Excised**: {culled_introns} ({round(100.0 * culled_introns / total_blocks, 1)}% noise reduction)",
        "\n---\n",
        "### Executive Abstract",
        "This monograph formalizes the axiomatic and operational framework of **Infinity Indefinite Mathematics (IRM)** and the **INDEF Object** ($X = [x] + x_\\chi$), bridging process-based generative calculus, non-standard hyperreal analysis, and voltage-based analog/neuromorphic hardware computation. Conversational scaffolding, user prompts, and epistemic hedging have been systematically stripped by the Semantic Gluon Exon Distiller to produce a self-contained, publication-grade mathematical treatise.\n",
        "---\n"
    ]

    for ch in THEMATIC_CHAPTERS:
        exons = chapter_buckets.get(ch["id"], [])
        if not exons:
            continue
        doc_lines.append(f"\n## {ch['title']}\n")
        # De-duplicate repetitive formulations
        seen = []
        for ex in exons:
            words = set(re.findall(r"\b[a-z]{3,}\b", ex.lower()))
            is_dup = False
            for s_words in seen:
                if len(words & s_words) / max(len(words | s_words), 1) > 0.50:
                    is_dup = True
                    break
            if not is_dup:
                seen.append(words)
                doc_lines.append(ex + "\n")

    output_doc_path.write_text("\n\n".join(doc_lines), encoding="utf-8")
    print(f"Distillation Complete!")
    print(f"-> Ingested: {total_blocks} chat dialogue blocks")
    print(f"-> Extracted: {len(pure_exons)} formal technical paragraphs")
    print(f"-> Culled: {culled_introns} chat prompts and conversational noise ({round(100.0 * culled_introns / total_blocks, 1)}%)")
    print(f"-> Saved Pristine Monograph: {output_doc_path} ({round(output_doc_path.stat().st_size / 1024, 1)} KB)")

def main():
    out_file = BASE_DIR / "distilled_irm_maths_monograph.md"
    distill_chatlog_to_document(CHAT_PATH, out_file)

if __name__ == "__main__":
    main()
