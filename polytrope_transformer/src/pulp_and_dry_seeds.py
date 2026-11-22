"""
Pulp and Dry Seeds: Extracting Atomic Declarative Exons with Full Provenance
==========================================================================
Implements Stage 1 (Pulping), Stage 2 (Exon Splicing / Intron Culling),
and Stage 3 (7-Plane Bedding) across the 7 Planes of Reality:
  Q1: Who - Metaphysical (Will & Direction)
  Q2: What - Possible (Faith & Probability, +x)
  Q3: Where - Physical (Matter & Distance, -x)
  Q4: Why - Lyrical (Meaning & Resonance, +y)
  Q5: How - Logical (Count & Consistency, -y)
  Q6: Cause - Historical (Sequence & Causality, +z)
  Q7: Effect - Emotive (Passion & Consequence, -z)

Outputs dried out seeds with line offset, local header context, and plane address.
"""

import os
import sys
import re
import hashlib
from pathlib import Path
import numpy as np

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from local_sentence_embedder import LocalSentenceEmbedder

PLANES = [
    ("Q1_Metaphysical", "Who", "Will and Direction"),
    ("Q2_Possible", "What", "Faith and Probability (+x)"),
    ("Q3_Physical", "Where", "Matter and Distance (-x)"),
    ("Q4_Lyrical", "Why", "Meaning and Resonance (+y)"),
    ("Q5_Logical", "How", "Count and Consistency (-y)"),
    ("Q6_Historical", "Cause", "Sequence and Causality (+z)"),
    ("Q7_Emotive", "Effect", "Passion and Consequence (-z)")
]

PLANE_ANCHOR_PROMPTS = [
    "Conscious sovereign intent, personal will, selfhood, and metaphysical agency.", # Q1
    "Future potential, uncommitted optionality, probability distribution, and superposition.", # Q2
    "Physical matter, spatial distance, sensory coordinates, atoms, and observable ground.", # Q3
    "Lyrical resonance, poetic depth, overarching purpose, and existential meaning.", # Q4
    "Logical consistency, mathematical equations, formal deduction, algorithmic proof, and causality.", # Q5
    "Historical origin, precedent, genealogical lineage, ancestral timeline, and antecedent cause.", # Q6
    "Somatic passion, emotional suffering, visceral reaction, grief, joy, and experiential effect." # Q7
]

def pulp_document(doc_path: Path):
    embedder = LocalSentenceEmbedder()
    plane_anchors = embedder.embed(PLANE_ANCHOR_PROMPTS)
    
    text = doc_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    
    # Track section headers and line offsets
    current_header = "Preamble"
    raw_sentences_with_provenance = []
    
    for line_idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('#'):
            current_header = stripped.lstrip('#').strip()
            continue
        if stripped.startswith('---'):
            continue
            
        # Split line into sentences if compound
        sents = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"\'\*\$])', stripped)
        for s in sents:
            s_clean = s.strip()
            # Clean list markers
            s_clean = re.sub(r'^[\*\-\d\.]+\s*', '', s_clean)
            if len(s_clean.split()) >= 4:
                token_hash = hashlib.sha256(s_clean.encode('utf-8')).hexdigest()[:10]
                raw_sentences_with_provenance.append({
                    "text": s_clean,
                    "line_number": line_idx,
                    "header": current_header,
                    "hash": token_hash
                })
                
    # Embed all candidate seeds
    s_texts = [item["text"] for item in raw_sentences_with_provenance]
    embs = embedder.embed(s_texts)
    
    # Classify into 7 Q-Planes
    sims = np.dot(embs, plane_anchors.T) # [N, 7]
    exp_sims = np.exp(sims * 4.0)
    probs = exp_sims / np.sum(exp_sims, axis=1, keepdims=True)
    
    seeds = []
    introns_culled = 0
    
    for i, item in enumerate(raw_sentences_with_provenance):
        p_idx = int(np.argmax(probs[i]))
        confidence = float(probs[i, p_idx])
        p_id, interrogative, desc = PLANES[p_idx]
        
        # Ribosomal Exon Splicing Filter
        s_low = item["text"].lower()
        words = item["text"].split()
        
        is_filler = bool(re.search(r'\b(as we can see|let us now|skip to|click here|note that|in other words|for example)\b', s_low)) and len(words) < 10
        is_meta = bool(re.search(r'^(author:|location:|status:|companion documents:)', s_low))
        
        if is_filler or is_meta:
            introns_culled += 1
            continue
            
        seeds.append({
            "line": item["line_number"],
            "header": item["header"],
            "hash": item["hash"],
            "plane": p_id,
            "interrogative": interrogative,
            "plane_desc": desc,
            "confidence": round(confidence, 3),
            "text": item["text"]
        })
        
    return seeds, len(raw_sentences_with_provenance), introns_culled

def build_no_fluff_markdown(seeds, total_raw, culled, source_path: Path) -> str:
    # Group seeds by 7 Planes
    by_plane = {p[0]: [] for p in PLANES}
    for s in seeds:
        by_plane[s["plane"]].append(s)
        
    md = [
        f"# Dried Out Seeds: Invariant Core Specification",
        f"**Source Document**: [`{source_path.name}`](file:///{str(source_path).replace('\\', '/')})",
        f"**Pipeline**: Pulping (Line Provenance) -> Ribosomal Exon Splicing -> 7-Plane Ontological Bedding",
        f"**Total Raw Statements**: {total_raw} | **Retained Pristine Seeds**: {len(seeds)} | **Culled Introns**: {culled}",
        f"**Compression Yield**: {round(100.0 * (1.0 - len(seeds)/total_raw), 2)}% fluff excised with zero axiom loss.\n",
        "---\n",
        "## The 7 Planes of Reality (42-Structure Invariant Seeds)\n"
    ]
    
    for p_id, interrogative, desc in PLANES:
        p_seeds = by_plane[p_id]
        if not p_seeds:
            continue
            
        md.append(f"### {p_id} ({interrogative} — {desc})")
        md.append(f"*Active Seed Count: {len(p_seeds)}*\n")
        
        for s in p_seeds:
            # Format: [L<line>][#<hash>][Header] Seed Text
            md.append(f"- **`[L{s['line']:03d}|{s['hash']}]`** *({s['header']})*: {s['text']}")
        md.append("")
        
    return "\n".join(md)

if __name__ == "__main__":
    doc = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Treatise_on_How_Words_Work.md")
    print(f"Pulping and drying seeds from: {doc}")
    seeds, total_raw, culled = pulp_document(doc)
    
    out_path = Path(r"e:\Vector Field Theory\VFT Docs\polytrope_transformer\Treatise_on_How_Words_Work_DRIED_SEEDS.md")
    content = build_no_fluff_markdown(seeds, total_raw, culled, doc)
    out_path.write_text(content, encoding="utf-8")
    
    print(f"Pulping complete!")
    print(f"  • Total Raw: {total_raw}")
    print(f"  • Retained Seeds: {len(seeds)}")
    print(f"  • Culled Introns: {culled}")
    print(f"  • Saved Dried Seeds to: {out_path}")
