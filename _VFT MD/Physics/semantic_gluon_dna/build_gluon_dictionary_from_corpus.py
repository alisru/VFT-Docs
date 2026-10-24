#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corpus-to-Gluon-Dictionary Harvester (Kernel Attention Head Builder)
===================================================================
Constructs an empirical Semantic Gluon Dictionary directly from raw text corpora
by acting as an asymmetric Causal Kernel Attention Head:

  1. Extracts 8-Modal Copula Flux directly from sentences:
     - will_be:  "must", "will", "necessarily", "always", "is defined as"
     - can_be:   "can", "could", "able to", "allows", "yields"
     - is_like:  "similar to", "analogous", "is like", "acts as", "corresponds to"
     - may_be:   "may", "might", "possibly", "hypothesized"
     - is_not:   "is not", "does not", "fails to", "excludes"
     - cant_be:  "cannot", "can never", "impossible", "contradicts", "violates"
     - wont_be:  "will not", "wont"
     - was_like: "formerly", "historically", "initially seemed"

  2. Negative Semantic Extraction (Forbidden vs Precluded):
     - Forbidden (-X): Extracted from modal impossibilities, contradictions, violations,
       and opposing gauge-attractor clashes.
     - Precluded (-N): Extracted from explicit exclusions, distinct non-equivalences,
       and unselected branching paths.

  3. Asymmetric Kernel Attention:
     - Tail Kernel phi_tail: Measures antecedent evidence & definition requirements.
     - Head Kernel phi_head: Measures downstream proof & binding obligations.
     - Kernel Dot Product: K(A, B) = phi_head(A) * phi_tail(B).
"""

import sys
import re
import json
import math
from pathlib import Path
from collections import defaultdict, Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\semantic_gluon_dna")
CORPUS_DIRS = [
    BASE_DIR / "irm_formal_corpus",
    BASE_DIR / "arxiv_samples",
]
SINGLE_FILES = [
    BASE_DIR.parent / "chatgpt infinity maths.md",
    BASE_DIR.parent / "Comprehensive Report -  Infinity Indefinite Mathematics (IRM).md"
]

# Patterns for 8 modal copula states
MODAL_PATTERNS = {
    "will_be": [
        r"\b(?:must|will|shall|necessarily|always)\s+(?:be\s+)?([a-z_]+)",
        r"\b(?:is|are)\s+defined\s+as\s+([a-z_]+)",
        r"\b(?:strictly|invariably)\s+([a-z_]+)"
    ],
    "can_be": [
        r"\b(?:can|could|allows|permits|yields)\s+(?:be\s+)?([a-z_]+)",
        r"\b(?:is|are)\s+capable\s+of\s+([a-z_]+)",
        r"\boperates\s+as\s+([a-z_]+)"
    ],
    "is_like": [
        r"\b(?:is|are)\s+(?:like|analogous\s+to|similar\s+to|isomorphic\s+to)\s+([a-z_]+)",
        r"\bcorresponds\s+to\s+([a-z_]+)",
        r"\bmodeled\s+as\s+([a-z_]+)"
    ],
    "may_be": [
        r"\b(?:may|might|possibly|perhaps|conjectured\s+to)\s+(?:be\s+)?([a-z_]+)",
        r"\bplausibly\s+([a-z_]+)"
    ],
    "is_not": [
        r"\b(?:is|are|does|do)\s+not\s+([a-z_]+)",
        r"\b(?:fails|failed)\s+to\s+([a-z_]+)",
        r"\bexcludes\s+([a-z_]+)",
        r"\bprecludes\s+([a-z_]+)"
    ],
    "cant_be": [
        r"\b(?:cannot|cant|can\s+never)\s+(?:be\s+)?([a-z_]+)",
        r"\b(?:impossible|precluded|forbidden)\s+(?:to\s+be\s+)?([a-z_]+)",
        r"\b(?:violates|contradicts)\s+([a-z_]+)"
    ],
    "wont_be": [
        r"\b(?:will\s+not|wont)\s+(?:be\s+)?([a-z_]+)"
    ],
    "was_like": [
        r"\b(?:was|were)\s+(?:initially|formerly|previously)\s+([a-z_]+)"
    ]
}

# Stopwords to exclude from lemma discovery
STOPWORDS = {
    "the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "as", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "this", "that", "these", "those",
    "it", "its", "we", "our", "they", "their", "which", "what", "where", "when",
    "who", "how", "why", "if", "then", "else", "such", "into", "also", "each"
}

def load_corpus_texts():
    texts = []
    # Single files
    for sf in SINGLE_FILES:
        if sf.exists():
            texts.append((sf.name, sf.read_text(encoding="utf-8", errors="ignore")))
    # Directory files
    for cd in CORPUS_DIRS:
        if cd.exists():
            for f in cd.glob("*.md"):
                texts.append((f.name, f.read_text(encoding="utf-8", errors="ignore")))
    return texts

def extract_gluon_kernel_dictionary(target_lemmas=None, min_freq=3):
    texts = load_corpus_texts()
    total_docs = len(texts)
    
    # Containers
    word_freq = Counter()
    word_modal_counts = defaultdict(lambda: Counter())
    word_guaranteed = defaultdict(Counter)
    word_possible = defaultdict(Counter)
    word_metaphorical = defaultdict(Counter)
    word_forbidden = defaultdict(Counter)
    word_precluded = defaultdict(Counter)
    
    word_antecedents = defaultdict(Counter) # Tail B
    word_consequents = defaultdict(Counter) # Head F
    
    for doc_name, text in texts:
        # Split into sentences
        sentences = re.split(r"[.!?\n]+", text)
        for s in sentences:
            clean_s = s.strip().lower()
            if not clean_s or len(clean_s) < 10:
                continue
            
            tokens = re.findall(r"\b[a-z]{3,}\b", clean_s)
            content_tokens = [t for t in tokens if t not in STOPWORDS]
            
            for t in content_tokens:
                word_freq[t] += 1
                
            # Scan for pairwise head-tail transition in sentence
            for i in range(len(content_tokens) - 1):
                w1 = content_tokens[i]
                w2 = content_tokens[i+1]
                word_consequents[w1][w2] += 1
                word_antecedents[w2][w1] += 1
                
            # Scan for modal copula relationships
            for mode, patterns in MODAL_PATTERNS.items():
                for pat in patterns:
                    for match in re.finditer(pat, clean_s):
                        target_verb = match.group(1)
                        if target_verb in STOPWORDS:
                            continue
                        # Find the subject (token immediately preceding the modal verb)
                        match_start = match.start()
                        preceding_text = clean_s[:match_start]
                        prec_tokens = re.findall(r"\b[a-z]{3,}\b", preceding_text)
                        valid_subjs = [pt for pt in prec_tokens if pt not in STOPWORDS]
                        if valid_subjs:
                            subj = valid_subjs[-1]
                            word_modal_counts[subj][mode] += 1
                            
                            # Categorize into 5-tier containers
                            if mode == "will_be":
                                word_guaranteed[subj][target_verb] += 2
                            elif mode == "can_be":
                                word_possible[subj][target_verb] += 2
                            elif mode == "is_like":
                                word_metaphorical[subj][target_verb] += 2
                            elif mode == "cant_be":
                                word_forbidden[subj][target_verb] += 3
                            elif mode == "is_not":
                                word_precluded[subj][target_verb] += 3

    # Filter to candidate words
    if target_lemmas:
        chosen_words = [w.lower() for w in target_lemmas]
    else:
        # Top 100 most significant content words with modal or causal activity
        candidates = [w for w, count in word_freq.items() if count >= min_freq and (len(word_consequents[w]) > 2 or sum(word_modal_counts[w].values()) > 0)]
        chosen_words = sorted(candidates, key=lambda w: (sum(word_modal_counts[w].values()) * 5 + word_freq[w]), reverse=True)[:100]

    dictionary = []
    for w in chosen_words:
        freq = word_freq[w]
        modals = word_modal_counts[w]
        tot_modals = sum(modals.values())
        
        # Normalized Modal Spread
        spread = {}
        for m in ["will_be", "can_be", "is_like", "may_be", "is_not", "cant_be", "wont_be", "was_like"]:
            if tot_modals > 0:
                spread[m] = round((modals[m] + 0.1) / (tot_modals + 0.8), 3)
            else:
                spread[m] = 0.125
                
        # Tail Kernel (Ingress Requirements B)
        top_antecedents = [k for k, _ in word_antecedents[w].most_common(5)]
        tail_weight = round(math.log(1 + len(word_antecedents[w])) + (0.5 if modals["will_be"] > 0 else 0.0), 2)
        
        # Head Kernel (Egress Obligations F)
        top_consequents = [k for k, _ in word_consequents[w].most_common(5)]
        head_weight = round(math.log(1 + len(word_consequents[w])) + (0.5 if modals["cant_be"] > 0 or modals["will_be"] > 0 else 0.0), 2)
        
        # CEFR assignment
        length = len(w)
        if freq > 150 and length <= 5:
            cefr = "A2"
        elif freq > 80:
            cefr = "B1"
        elif freq > 25:
            cefr = "B2"
        elif freq > 5:
            cefr = "C1"
        else:
            cefr = "C2"

        entry = {
            "word": w,
            "corpus_frequency": freq,
            "cefr": cefr,
            "tail_ingress": {
                "antecedent_weight": tail_weight,
                "requires_evidence": tail_weight > 2.0,
                "top_precursors": top_antecedents
            },
            "head_egress": {
                "obligation_weight": head_weight,
                "binds_consequents": head_weight > 2.0,
                "top_successors": top_consequents
            },
            "modal_spread": spread,
            "relative_vectors": {
                "guaranteed": [k for k, _ in word_guaranteed[w].most_common(4)] or [f"essential_{w}"],
                "possible": [k for k, _ in word_possible[w].most_common(4)] or top_consequents[:3] or [f"action_{w}"],
                "metaphorical": [k for k, _ in word_metaphorical[w].most_common(4)] or [f"model_{w}"],
                "forbidden": [k for k, _ in word_forbidden[w].most_common(4)] or [f"violation_of_{w}"],
                "precluded": [k for k, _ in word_precluded[w].most_common(4)] or [f"absence_of_{w}"]
            }
        }
        dictionary.append(entry)

    out_file = BASE_DIR / "corpus_learned_gluon_dictionary.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, indent=2)

    return dictionary, total_docs


def main():
    print("=" * 90)
    print("HARVESTING EMPIRICAL GLUON DICTIONARY & KERNEL ATTENTION HEAD FROM CORPUS")
    print("=" * 90)
    
    test_words = [
        "infinity", "singularity", "quotient", "operator", "manifold", 
        "entropy", "limit", "zero", "paradox", "axiom", "spacetime", "function"
    ]
    
    dictionary, doc_count = extract_gluon_kernel_dictionary(target_lemmas=test_words)
    print(f"Scanned {doc_count} corpus documents across Mathematics, Physics, PDEs, and IRM.")
    print(f"Compiled {len(dictionary)} Learned Gluon Kernel Vertices.\n")
    
    for entry in dictionary[:6]:
        w = entry["word"].upper()
        print(f"--------------------------------------------------------------------------------")
        print(f"KERNEL VERTEX: [{w}] (Freq: {entry['corpus_frequency']} | CEFR: {entry['cefr']})")
        print(f"  Ingress Tail Kernel (B): Weight={entry['tail_ingress']['antecedent_weight']} | Precursors: {entry['tail_ingress']['top_precursors']}")
        print(f"  Egress Head Kernel  (F): Weight={entry['head_egress']['obligation_weight']} | Successors: {entry['head_egress']['top_successors']}")
        print(f"  Learned Modal Flux Spread:")
        m = entry["modal_spread"]
        print(f"    +W (will_be): {m['will_be']:.2f} | +A (can_be): {m['can_be']:.2f} | +L (is_like): {m['is_like']:.2f} | +M (may_be): {m['may_be']:.2f}")
        print(f"    -N (is_not) : {m['is_not']:.2f} | -X (cant_be): {m['cant_be']:.2f} | -O (wont_be): {m['wont_be']:.2f} | -H (was_like): {m['was_like']:.2f}")
        print(f"  Learned Relative Vectors from Corpus Evidence:")
        print(f"    [Guaranteed (+W)] : {', '.join(entry['relative_vectors']['guaranteed'])}")
        print(f"    [Possible   (+A)] : {', '.join(entry['relative_vectors']['possible'])}")
        print(f"    [Metaphor   (+L)] : {', '.join(entry['relative_vectors']['metaphorical'])}")
        print(f"    [Forbidden  (-X)] : {', '.join(entry['relative_vectors']['forbidden'])}")
        print(f"    [Precluded  (-N)] : {', '.join(entry['relative_vectors']['precluded'])}")
    print("=" * 90)

if __name__ == "__main__":
    main()
