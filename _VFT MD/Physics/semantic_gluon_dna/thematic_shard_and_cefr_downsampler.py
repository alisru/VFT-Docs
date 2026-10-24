#!/usr/bin/env python3
"""
Thematic Sharding and CEFR Readability Down-Sampling Engine (v1.0.0)
===================================================================
1. Thematic Sharding: Ingests multiple overlapping documents on a subject,
   identifies distinct semantic basins, de-duplicates overlapping blocks,
   and exports targeted, modular micro-monographs.
2. CEFR Down-Sampling: Translates dense C1/C2 academic compounds and pseudo-
   intellectual jargon into grounded B1/B2 English, splitting convoluted sentences
   while strictly preserving mathematical formulas, proofs, and definitions.
"""

import os
import re
import sys
import json
import math
from pathlib import Path
from collections import Counter, defaultdict

# Ensure UTF-8 output on Windows CP1252 consoles
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ---------------------------------------------------------------------------
# C1/C2 Academic Jargon -> Grounded B1/B2 Pub-Test Translation Lexicon
# ---------------------------------------------------------------------------
CEFR_SIMPLIFICATION_MAP = {
    # Latinate / Academic Compounds -> Clear Direct Verbs/Nouns
    r"\bepistemological\b": "knowledge-based",
    r"\bepistemology\b": "theory of knowledge",
    r"\bontological\b": "fundamental reality",
    r"\bontology\b": "nature of reality",
    r"\bhermeneutic\b": "interpretation",
    r"\bhermeneutics\b": "rules of interpretation",
    r"\bteleological\b": "purpose-driven",
    r"\bteleology\b": "purpose or ultimate goal",
    r"\binstantiation\b": "concrete example",
    r"\binstantiations\b": "concrete examples",
    r"\binstantiate\b": "make concrete",
    r"\bphenomenological\b": "direct experiential",
    r"\bphenomenology\b": "study of direct experience",
    r"\bpresupposition\b": "assumption",
    r"\bpresuppositions\b": "assumptions",
    r"\butilize\b": "use",
    r"\butilized\b": "used",
    r"\butilizing\b": "using",
    r"\butilization\b": "use",
    r"\bfacilitate\b": "help",
    r"\bfacilitates\b": "helps",
    r"\bfacilitated\b": "helped",
    r"\belucidate\b": "explain",
    r"\belucidates\b": "explains",
    r"\belucidated\b": "explained",
    r"\bdemarcation\b": "boundary",
    r"\bdemarcations\b": "boundaries",
    r"\bprognosticate\b": "predict",
    r"\bprognostication\b": "prediction",
    r"\bdelineate\b": "outline",
    r"\bdelineated\b": "outlined",
    r"\bdelineates\b": "outlines",
    r"\bconcomitant\b": "accompanying",
    r"\bconcomitantly\b": "along with this",
    r"\bjuxtapose\b": "compare side by side",
    r"\bjuxtaposition\b": "side-by-side comparison",
    r"\bparadigm\b": "model",
    r"\bparadigms\b": "models",
    r"\bparadigmatic\b": "typical",
    r"\bquiescent\b": "dormant",
    r"\brecalcitrant\b": "stubborn",
    r"\bbifurcation\b": "split",
    r"\bbifurcations\b": "splits",
    r"\bmanifestation\b": "visible form",
    r"\bmanifestations\b": "visible forms",
    r"\bmanifest\b": "show",
    r"\bmanifests\b": "shows",
    r"\bmanifested\b": "shown",
    r"\bco-occurrence\b": "happening together",
    r"\bco-occur\b": "happen together",
    r"\bco-occurring\b": "happening together",
    r"\bhomology\b": "shared structural ancestry",
    r"\bhomologies\b": "shared structural patterns",
    r"\bcommensurate\b": "proportionate",
    r"\bincommensurate\b": "mismatched",
    r"\bpercipient\b": "observer",
    r"\bpostulate\b": "claim",
    r"\bpostulates\b": "claims",
    r"\bpostulated\b": "claimed",
    r"\bsubstantiate\b": "back up with evidence",
    r"\bsubstantiates\b": "backs up with evidence",
    r"\bsubstantiated\b": "backed up with evidence",
    r"\bsubstantiation\b": "proof or backing",
    r"\bcircumlocution\b": "beating around the bush",
    r"\bveridical\b": "truthful",
    r"\bcontingency\b": "dependence on circumstances",
    r"\binterlocutor\b": "speaking partner",
    r"\binterlocutors\b": "speaking partners",
    r"\bimperative\b": "necessary action",
    r"\bpropensity\b": "tendency",
    r"\bpropensities\b": "tendencies",
    r"\bcongruence\b": "agreement",
    r"\bcongruent\b": "matching",
    r"\bincongruent\b": "mismatched",
    r"\bincongruity\b": "mismatch",
    r"\bpreponderance\b": "majority",
    r"\bprobity\b": "honesty",
    r"\bhegemony\b": "dominant control",
    r"\bhegemonic\b": "dominating",
    r"\bdichotomy\b": "two-way split",
    r"\bdichotomies\b": "two-way splits",
    r"\bdichotomous\b": "split in two",
    r"\bmultifaceted\b": "complex",
    r"\bunderscore\b": "highlight",
    r"\bunderscores\b": "highlights",
    r"\bunderscored\b": "highlighted",
    r"\btestament to\b": "proof of",
    r"\bfoster\b": "encourage",
    r"\bfosters\b": "encourages",
    r"\bfostered\b": "encouraged",
    r"\bdelve into\b": "look closely into",
    r"\btapestry of\b": "network of",
}

# Dialogue & AI pleasantry filters
CHAT_STRIP_PATTERNS = [
    r"^here is (an|the) overview of.*?:",
    r"^let'?s dive into.*?:",
    r"^as (we|you) discussed.*?,",
    r"^in summary,?",
    r"^in conclusion,?",
    r"^to summarize,?",
    r"^certainly!?\s*",
    r"^sure!?\s*",
    r"^of course!?\s*",
    r"^(what|as) you're proposing is",
    r"^what follows is",
]

def clean_chat_framing(text: str) -> str:
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()
        if any(re.match(pat, lower) for pat in CHAT_STRIP_PATTERNS):
            continue
        cleaned.append(line)
    return "\n".join(cleaned)

def compute_readability_metrics(text: str) -> dict:
    words = re.findall(r"\b[A-Za-z]+\b", text)
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 3]
    
    num_words = max(len(words), 1)
    num_sentences = max(len(sentences), 1)
    
    # Syllable approximation
    syllables = 0
    for w in words:
        w_lower = w.lower()
        count = len(re.findall(r"[aeiouy]+", w_lower))
        if w_lower.endswith("e") and not w_lower.endswith("le") and count > 1:
            count -= 1
        syllables += max(count, 1)
        
    avg_sentence_len = num_words / num_sentences
    avg_syllables_per_word = syllables / num_words
    
    # Flesch Reading Ease
    fre = 206.835 - (1.015 * avg_sentence_len) - (84.6 * avg_syllables_per_word)
    # Flesch-Kincaid Grade Level
    fkgl = (0.39 * avg_sentence_len) + (11.8 * avg_syllables_per_word) - 15.59
    
    # Estimate CEFR level based on FKGL & Jargon density
    c1_c2_count = 0
    for pat in CEFR_SIMPLIFICATION_MAP.keys():
        c1_c2_count += len(re.findall(pat, text, flags=re.IGNORECASE))
        
    c1_c2_density = (c1_c2_count / num_words) * 100
    
    if fkgl >= 14 or c1_c2_density > 2.5:
        cefr = "C2 (Scholastic / Research)"
    elif fkgl >= 11 or c1_c2_density > 1.2:
        cefr = "C1 (Advanced Academic)"
    elif fkgl >= 8.5:
        cefr = "B2 (General Professional)"
    elif fkgl >= 6.0:
        cefr = "B1 (Intermediate / Pub-Test)"
    else:
        cefr = "A2 (Basic)"
        
    return {
        "word_count": num_words,
        "sentence_count": num_sentences,
        "avg_sentence_length": round(avg_sentence_len, 2),
        "flesch_reading_ease": round(fre, 2),
        "flesch_kincaid_grade": round(fkgl, 2),
        "c1_c2_jargon_density_pct": round(c1_c2_density, 2),
        "estimated_cefr": cefr
    }

def downsample_cefr_text(text: str, target_level: str = "B1") -> str:
    """
    Downsamples academic C1/C2 jargon to grounded B1/B2 English.
    Preserves all LaTeX math $...$ and code blocks ```...``` untouched.
    """
    # 1. Protect code blocks and math
    placeholders = []
    def save_protected(match):
        idx = len(placeholders)
        placeholders.append(match.group(0))
        return f"__PROTECTED_BLOCK_{idx}__"
    
    # Protect fenced code
    text = re.sub(r"```[\s\S]*?```", save_protected, text)
    # Protect inline code
    text = re.sub(r"`[^`\n]+`", save_protected, text)
    # Protect display math
    text = re.sub(r"\$\$[\s\S]*?\$\$", save_protected, text)
    # Protect inline math
    text = re.sub(r"\$[^\$\n]+\$", save_protected, text)
    
    # 2. Apply Vocabulary Simplification Map
    for pat, replacement in CEFR_SIMPLIFICATION_MAP.items():
        def replace_with_case(m):
            orig = m.group(0)
            if orig.isupper():
                return replacement.upper()
            elif orig[0].isupper():
                return replacement.capitalize()
            return replacement
        text = re.sub(pat, replace_with_case, text, flags=re.IGNORECASE)
        
    # 3. Split over-long sentences if target is B1
    if target_level.upper() in ["B1", "B2"]:
        # Split sentences with multiple semicolons or excessive conjunctions
        lines = text.split("\n")
        new_lines = []
        for line in lines:
            if line.startswith("#") or line.strip().startswith("-") or line.strip().startswith("*") or line.strip().startswith(">"):
                new_lines.append(line)
                continue
            # Split semicolons into periods
            line = re.sub(r";\s+([A-Za-z])", r". \1", line)
            new_lines.append(line)
        text = "\n".join(new_lines)

    # 4. Restore protected blocks
    for idx, orig in enumerate(placeholders):
        text = text.replace(f"__PROTECTED_BLOCK_{idx}__", orig)
        
    return text

def parse_markdown_blocks(filepath: Path) -> list:
    """Parses markdown into logical section blocks preserving headers."""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    content = clean_chat_framing(content)
    raw_blocks = re.split(r"\n(?=#{1,4}\s)", content)
    
    parsed = []
    for i, rb in enumerate(raw_blocks):
        rb_strip = rb.strip()
        if not rb_strip:
            continue
        header_match = re.match(r"^(#{1,4})\s+(.+)$", rb_strip, flags=re.MULTILINE)
        header = header_match.group(2) if header_match else f"Section_{i}"
        
        words = re.findall(r"\b[A-Za-z]{3,}\b", rb_strip.lower())
        parsed.append({
            "source_file": filepath.name,
            "index": i,
            "header": header,
            "text": rb_strip,
            "word_count": len(words),
            "words": set(words)
        })
    return parsed

def determine_thematic_basins(all_blocks: list) -> dict:
    """
    Groups blocks into distinct thematic basins using semantic keyword distributions.
    """
    basin_keywords = {
        "moral_geometry_and_axes": {"morality", "will", "axis", "upsilon", "psi", "coordinates", "justice", "extraction", "tyranny", "altruism"},
        "the_archetypal_crucible": {"crucible", "archetype", "character", "adversity", "refinement", "virtue", "soul", "temptation", "trials"},
        "epistemic_translation_and_invariants": {"actualism", "translation", "invariant", "epistemic", "context", "action", "effect", "plane", "hermeneutic"},
        "cognitive_neuroscience_and_stress": {"stress", "strain", "brain", "neuroscience", "friction", "cognitive", "entropy", "capacity", "tensor"},
        "sociological_hegemony_and_institutions": {"hegemony", "psochic", "institution", "power", "control", "society", "propaganda", "consensus", "media"}
    }
    
    basins = defaultdict(list)
    for block in all_blocks:
        best_basin = "general_foundations"
        max_overlap = 0
        for b_name, b_keys in basin_keywords.items():
            overlap = len(block["words"] & b_keys)
            if overlap > max_overlap:
                max_overlap = overlap
                best_basin = b_name
        basins[best_basin].append(block)
        
    return basins

def de_duplicate_basin_blocks(blocks: list, sim_threshold: float = 0.55) -> list:
    """
    Deduplicates overlapping blocks within a basin, keeping the most informative/complete block.
    """
    retained = []
    for cand in blocks:
        is_dup = False
        cand_words = cand["words"]
        if not cand_words:
            continue
        for idx, exist in enumerate(retained):
            exist_words = exist["words"]
            inter = len(cand_words & exist_words)
            union = len(cand_words | exist_words)
            jaccard = inter / union if union > 0 else 0
            if jaccard >= sim_threshold:
                is_dup = True
                # Keep the longer, more substantiated block
                if cand["word_count"] > exist["word_count"]:
                    retained[idx] = cand
                break
        if not is_dup:
            retained.append(cand)
    return retained

def run_thematic_sharder(input_files: list, output_dir: Path, target_cefr: str = "B1"):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_blocks = []
    for f in input_files:
        p = Path(f)
        if p.exists():
            all_blocks.extend(parse_markdown_blocks(p))
            
    print(f"[*] Ingested {len(all_blocks)} blocks across {len(input_files)} source files.")
    
    basins = determine_thematic_basins(all_blocks)
    shards_generated = []
    
    for basin_name, b_blocks in basins.items():
        if not b_blocks:
            continue
        print(f"\n[+] Processing Basin: {basin_name} ({len(b_blocks)} input blocks)")
        retained = de_duplicate_basin_blocks(b_blocks)
        culling_pct = round(((len(b_blocks) - len(retained)) / len(b_blocks)) * 100, 2)
        print(f"    - De-duplicated {len(b_blocks)} -> {len(retained)} blocks ({culling_pct}% redundancy removed)")
        
        # Assemble shard content
        title = basin_name.replace("_", " ").title()
        shard_md = [f"# {title}\n", f"> **Target Readability**: CEFR {target_cefr} | De-duplicated Exons: {len(retained)}\n"]
        
        for blk in retained:
            clean_text = blk["text"]
            if target_cefr in ["B1", "B2"]:
                clean_text = downsample_cefr_text(clean_text, target_level=target_cefr)
            shard_md.append(clean_text)
            shard_md.append("\n---\n")
            
        final_content = "\n".join(shard_md)
        out_file = output_dir / f"shard_{basin_name}_{target_cefr.lower()}.md"
        out_file.write_text(final_content, encoding="utf-8")
        
        # Compute metrics
        metrics = compute_readability_metrics(final_content)
        shards_generated.append({
            "shard_name": basin_name,
            "filename": out_file.name,
            "path": str(out_file),
            "input_blocks": len(b_blocks),
            "retained_blocks": len(retained),
            "redundancy_culling_pct": culling_pct,
            "metrics": metrics
        })
        print(f"    - Output: {out_file.name}")
        print(f"    - Reading Ease: {metrics['flesch_reading_ease']} | Grade: {metrics['flesch_kincaid_grade']} | CEFR: {metrics['estimated_cefr']}")

    # Save summary ledger
    ledger_path = output_dir / "sharding_and_cefr_summary.json"
    ledger_path.write_text(json.dumps(shards_generated, indent=2), encoding="utf-8")
    print(f"\n[✓] Sharding complete! Summary saved to {ledger_path.name}")
    return shards_generated

if __name__ == "__main__":
    test_files = [
        r"e:\Vector Field Theory\VFT Docs\_VFT MD\IO\Actualism and the Psochic Hegemony.md",
        r"e:\Vector Field Theory\VFT Docs\_VFT MD\IO\Academic Perspectives on the Psochic Hegemony.md",
        r"e:\Vector Field Theory\VFT Docs\_VFT MD\IO\Actualism; The Crucible of the Archetypal Good Person.md"
    ]
    out_dir = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\semantic_gluon_dna\thematic_shards")
    run_thematic_sharder(test_files, out_dir, target_cefr="B1")
