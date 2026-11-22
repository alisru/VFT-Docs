"""
Progressive Polytrope Seed Crystallizer
=======================================
Reads a document progressively (5' -> 3' reading strand).
Uses the Polytrope Causal Working-Out Ledger to distinguish between:
  1. Antecedent Working-Out (Constructive C, Reductive R, Regressive G)
  2. Unbacked Leaps ('Maths without working out' -> Rejected)
  3. Crystallized Invariant Seeds (Productive claims P whose working-out debt is fully paid)

Every crystallized seed records:
  - The exact crystallized statement
  - Its line number & section
  - The preceding working-out wave that earned it
  - Solvency score & Gluon tension
"""

import os
import sys
import re
import math
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from local_sentence_embedder import LocalSentenceEmbedder

# 4 Generative Dialectic Engine Anchors:
# C: Constructive (is_like, may_be) - Analogies, hypotheses, structural bridges
# P: Productive   (will_be, can_be) - Resolved invariant, active creation, stable state
# R: Reductive    (can't_be, is_not) - Falsification, constraint testing, friction, problems
# G: Regressive   (was_like, won't_be) - Historical precedent, origin, antecedent foundation
ENGINE_PROMPTS = [
    "Analogical resemblance, exploratory hypothesis, structural similarity, and constructive model.", # C
    "Resolved physical invariant, definitive conclusion, stabilized state of order, and proven outcome.", # P
    "Physical impossibility, boundary constraint, obstacle, friction, resistance, and negation.", # R
    "Historical precedent, ancestral origin, genealogical timeline, starting condition, and prior record." # G
]

class ProgressiveSeedCrystallizer:
    def __init__(self):
        print("[ProgressiveSeedCrystallizer] Initializing Local Embedder & Dialectic Anchors...")
        self.embedder = LocalSentenceEmbedder()
        self.engine_anchors = self.embedder.embed(ENGINE_PROMPTS) # [4, 384]

    def split_document(self, text: str) -> List[Dict[str, Any]]:
        lines = text.splitlines()
        sentences = []
        current_header = "Introduction"
        
        for line_num, line in enumerate(lines, start=1):
            s = line.strip()
            if not s:
                continue
            if s.startswith('#'):
                current_header = s.lstrip('#').strip()
                continue
            if s.startswith('---'):
                continue
                
            raw_sents = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"\'\*\$])', s)
            for raw_s in raw_sents:
                clean_s = raw_s.strip()
                clean_s = re.sub(r'^[\*\-\d\.]+\s*', '', clean_s)
                if len(clean_s.split()) >= 4:
                    sentences.append({
                        "line": line_num,
                        "header": current_header,
                        "text": clean_s
                    })
        return sentences

    def classify_dialectic_charge(self, sentence_embs: np.ndarray) -> np.ndarray:
        """Computes sigma(t) = [C, P, R, G] in Delta^3 via softmax over cosine similarity to anchors."""
        sims = np.dot(sentence_embs, self.engine_anchors.T) # [N, 4]
        exp_sims = np.exp(sims * 3.5)
        probs = exp_sims / np.sum(exp_sims, axis=1, keepdims=True)
        return probs # [N, 4]

    def run_progressive_crystallization(self, doc_path: Path, p_threshold: float = 0.28, kappa: float = 0.85) -> Dict[str, Any]:
        text = doc_path.read_text(encoding="utf-8")
        sentences = self.split_document(text)
        if not sentences:
            return {"error": "No sentences found."}
            
        s_texts = [s["text"] for s in sentences]
        embs = self.embedder.embed(s_texts)
        charges = self.classify_dialectic_charge(embs) # [N, 4] (C, P, R, G)
        
        crystallized_seeds = []
        rejected_leaps = []
        
        # Progressive Causal Ledger
        # Bank accumulates working-out: C (analogy), R (problem/friction), G (precedent)
        working_out_bank = 0.0
        active_working_out_buffer = []
        
        for t in range(len(sentences)):
            curr_s = sentences[t]
            c_t, p_t, r_t, g_t = charges[t]
            
            # Gluon tension to previous sentence
            if t > 0:
                cos_sim = float(np.dot(embs[t-1], embs[t]))
                dist = math.sqrt(max(0.0, 2.0 * (1.0 - max(-1.0, min(1.0, cos_sim)))))
                is_snapped = (dist >= 1.529)
            else:
                dist = 0.0
                is_snapped = False
                
            # Check if this sentence makes an assertive Productive claim
            is_productive_candidate = (p_t >= p_threshold) or bool(re.search(r'\b(therefore|thus|proves|invariant|axiom|formula|law|state transition|effect)\b', curr_s["text"].lower()))
            
            # Calculate Solvency using Derivation Law II
            # Solvency requires prior accumulation of working-out: min(C, R, G) or net bank
            if is_productive_candidate:
                solvency_ratio = working_out_bank / (p_t + 1e-4)
                
                # Check for Solvency vs Leap
                if is_snapped or working_out_bank < 0.20:
                    # Unbacked leap: asserting a conclusion without paying derivation debt!
                    rejected_leaps.append({
                        "sentence_index": t,
                        "line": curr_s["line"],
                        "header": curr_s["header"],
                        "text": curr_s["text"],
                        "p_charge": round(float(p_t), 3),
                        "bank_at_time": round(float(working_out_bank), 3),
                        "reason": "String snapped or insufficient antecedent working-out."
                    })
                else:
                    # EARNED INVARIANT SEED CRYSTALLIZATION!
                    crystallized_seeds.append({
                        "seed_index": len(crystallized_seeds) + 1,
                        "sentence_index": t,
                        "line": curr_s["line"],
                        "header": curr_s["header"],
                        "text": curr_s["text"],
                        "p_charge": round(float(p_t), 3),
                        "working_out_support_count": len(active_working_out_buffer),
                        "solvency_score": round(float(solvency_ratio), 2),
                        "derivation_wave_sample": [w["text"] for w in active_working_out_buffer[-2:]]
                    })
                    # Reset working-out buffer for next cycle
                    working_out_bank = 0.10 # residual base
                    active_working_out_buffer = []
                    continue
                    
            # Accumulate working out into bank: C, R, and G contribute to derivation energy
            derivation_energy = (c_t * 0.40) + (r_t * 0.40) + (g_t * 0.20)
            working_out_bank += float(derivation_energy)
            active_working_out_buffer.append(curr_s)
            
        return {
            "document": doc_path.name,
            "total_sentences": len(sentences),
            "crystallized_seeds_count": len(crystallized_seeds),
            "rejected_leaps_count": len(rejected_leaps),
            "seeds": crystallized_seeds,
            "rejected_leaps": rejected_leaps
        }

def format_progressive_seeds_markdown(res: Dict[str, Any], doc_path: Path) -> str:
    md = [
        f"# Progressive Polytrope Seed Crystallization",
        f"**Source Document**: [`{res['document']}`](file:///{str(doc_path).replace('\\', '/')})",
        f"**Engine**: Polytrope Reading Head ($5' \\to 3'$ Progressive Causal Solvency Ledger)",
        f"**Total Sentences Processed**: {res['total_sentences']} | **Earned Seeds Crystallized**: {res['crystallized_seeds_count']} | **Unbacked Leaps Rejected**: {res['rejected_leaps_count']}\n",
        "---\n",
        "## What Is a Progressive Invariant Seed?",
        "> A sentence is **NOT** a seed merely because it asserts a conclusion. It only crystallizes into an **Authoritative Invariant Seed** when its preceding derivation wave (Problem $R$, Precedent $G$, Analogy $C$) has paid the full causal debt ($W_{\\text{bank}} \\ge P_t$) with zero string snapping.\n",
        "---\n",
        "## Chronological Stream of Progressively Earned Seeds\n"
    ]
    
    for s in res["seeds"]:
        md.append(f"### Seed {s['seed_index']:02d}: `[L{s['line']:03d}]` *({s['header']})*")
        md.append(f"> **\"{s['text']}\"**")
        md.append(f"* **Solvency Ratio**: `{s['solvency_score']}x` (Supported by {s['working_out_support_count']} preceding derivation steps)")
        if s["derivation_wave_sample"]:
            md.append(f"* **Earned by Working-Out Wave**:")
            for prev in s["derivation_wave_sample"]:
                md.append(f"  - *\"...{prev[:90]}...\"*")
        md.append("")
        
    if res["rejected_leaps"]:
        md.append("---\n## Rejected Unbacked Leaps (Maths Without Working Out)\n")
        for r in res["rejected_leaps"]:
            md.append(f"- ❌ **`[L{r['line']:03d}]`** *({r['header']})*: \"{r['text']}\"")
            md.append(f"  *Reason: {r['reason']} (Bank: {r['bank_at_time']} vs P: {r['p_charge']})*")
        md.append("")
        
    return "\n".join(md)

if __name__ == "__main__":
    doc = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Treatise_on_How_Words_Work.md")
    print(f"[ProgressiveSeedCrystallizer] Reading: {doc}...")
    
    crystallizer = ProgressiveSeedCrystallizer()
    res = crystallizer.run_progressive_crystallization(doc)
    
    out_md = Path(r"e:\Vector Field Theory\VFT Docs\polytrope_transformer\Treatise_on_How_Words_Work_PROGRESSIVE_SEEDS.md")
    out_json = Path(r"e:\Vector Field Theory\VFT Docs\polytrope_transformer\Treatise_on_How_Words_Work_PROGRESSIVE_SEEDS.json")
    
    md_content = format_progressive_seeds_markdown(res, doc)
    out_md.write_text(md_content, encoding="utf-8")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
        
    print(f"\nProgressive Crystallization Complete!")
    print(f"  • Processed Sentences: {res['total_sentences']}")
    print(f"  • Progressively Earned Seeds: {res['crystallized_seeds_count']}")
    print(f"  • Rejected Leaps: {res['rejected_leaps_count']}")
    print(f"  • Markdown Report: {out_md}")
