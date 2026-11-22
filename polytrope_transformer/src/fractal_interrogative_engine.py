"""
Fractal Interrogative Engine: Recursive Syntactic Dependency Slot Parser
=======================================================================
Implements the 7x7x7 structure across the 42-Structure and the 7 Planes of Reality:
  Q1: Who - Metaphysical (Will & Direction, The Driver / 7th Angle Axis)
  Q2: What - Possible (Faith & Probability, Lateral Axis +x)
  Q3: Where - Physical (Matter & Distance, Lateral Axis -x)
  Q4: Why - Lyrical (Meaning & Resonance, Longitudinal Axis +y)
  Q5: How - Logical (Count & Consistency, Longitudinal Axis -y)
  Q6: Cause - Historical (Sequence & Causality, Vertical Axis +z)
  Q7: Effect - Emotive (Passion & Consequence, Vertical Axis -z)

On Q layer: interrogative Q
On q layer: interrogative q of Q
On c layer: interrogative c of q of Q

Features:
- Deterministic extraction via spaCy dependency trees.
- Temporal vs Spatial preposition disambiguation (Dates/Times -> Q6 Historical, Locations -> Q3 Physical).
- Copula identity handling ("A is B" -> Q2 What / Potential).
- Recursive re-entrant dispatching on clause spans down to Depth 2 (q) and Depth 3 (c).
- Preserves sentence-level Gluon Bond pointers and line-number provenance.
"""

import os
import sys
import re
import json
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import spacy

nlp = spacy.load("en_core_web_sm")

PLANE_MAP = {
    1: ("Q1", "Who", "Metaphysical Plane (Will and Direction)"),
    2: ("Q2", "What", "Possible Plane (Faith and Probability, +x)"),
    3: ("Q3", "Where", "Physical Plane (Matter and Distance, -x)"),
    4: ("Q4", "Why", "Lyrical Plane (Meaning and Resonance, +y)"),
    5: ("Q5", "How", "Logical Plane (Count and Consistency, -y)"),
    6: ("Q6", "Cause", "Historical Plane (Sequence and Causality, +z)"),
    7: ("Q7", "Effect", "Emotive Plane (Passion and Consequence, -z)")
}

SUB_PREFIX = {1: "Q", 2: "q", 3: "c"}

@dataclass
class CoordinateSeedNode:
    address: str
    depth: int
    facet_id: int
    facet_name: str
    text: str
    sub_frames: Dict[str, "CoordinateSeedNode"] = field(default_factory=dict)

class FractalInterrogativeEngine:
    def __init__(self, max_depth: int = 2):
        self.max_depth = max_depth

    def parse_span_into_slots(self, text_span: str, parent_address: str = "", current_depth: int = 1) -> Dict[str, CoordinateSeedNode]:
        clean_span = text_span.strip()
        if not clean_span:
            return {}

        doc = nlp(clean_span)
        if not len(doc):
            return {}

        slots: Dict[int, str] = {i: "" for i in range(1, 8)}

        # 1. Locate local focal root verb/copula
        roots = [tok for tok in doc if tok.head == tok]
        root = roots[0] if roots else doc[0]

        # 2. Extract Q1 (Who: Subject agent / sovereign will)
        subjects = [w for w in root.lefts if w.dep_ in ("nsubj", "nsubjpass", "csubj")]
        if subjects:
            slots[1] = " ".join([t.text for t in subjects[0].subtree if not t.is_punct])
        elif current_depth > 1 and doc[0].pos_ in ("NOUN", "PROPN", "PRON"):
            # If drilling down into a noun phrase, lead noun is the sub-actor (q1)
            slots[1] = doc[0].text

        # 3. Extract Q2 (What: Action verb + direct nominal object / copula predicate)
        objects = [w for w in root.rights if w.dep_ in ("dobj", "attr", "acomp", "oprd")]
        if objects:
            slots[2] = f"{root.text} " + " ".join([t.text for t in objects[0].subtree if not t.is_punct])
        elif root.pos_ in ("VERB", "AUX"):
            slots[2] = root.text

        # 4. Scan syntactic dependents for spatial, purposive, operational, temporal, and causal planes
        for child in root.children:
            child_text = " ".join([t.text for t in child.subtree if not t.is_punct])
            child_lower = child.text.lower()

            # Prepositional attachments
            if child.dep_ == "prep":
                # Check for temporal vs spatial distinction using child entity and tokens
                has_date_ent = any(t.ent_type_ in ("DATE", "TIME") for t in child.subtree)
                is_temporal_word = any(w in child_text.lower() for w in ("year", "century", "time", "beginning", "history", "ancient", "past", "moment", "era"))
                
                if has_date_ent or is_temporal_word or child_lower in ("before", "after", "during", "since", "until"):
                    # Q6: Cause / Historical timeline
                    slots[6] = child_text
                elif child_lower in ("in", "at", "on", "across", "inside", "within", "throughout", "under", "over"):
                    # Q3: Where / Bounded physical space
                    slots[3] = child_text
                elif child_lower in ("by", "via", "through", "using", "with", "without"):
                    # Q5: How / Logical mechanism
                    slots[5] = child_text
                elif child_lower in ("for", "toward", "towards") and not slots[4]:
                    # Q4: Why / Purposive direction
                    slots[4] = child_text

            # Adverbial clauses
            elif child.dep_ == "advcl":
                first_tokens = [t.text.lower() for t in list(child.subtree)[:2]]
                
                # Check for infinitive purpose (to do something -> Q4 Why)
                if any(w.tag_ == "TO" for w in child.lefts) or child_text.lower().startswith("to "):
                    slots[4] = child_text
                # Check for causal conditions (when, if, because, since -> Q6 Cause)
                elif any(m in first_tokens for m in ("if", "when", "whenever", "because", "since", "due", "once")):
                    slots[6] = child_text
                # Check for consequent participles (resulting in, causing -> Q7 Effect)
                elif any(m in first_tokens for m in ("resulting", "leading", "thereby", "causing", "yielding")):
                    slots[7] = child_text
                elif not slots[5]:
                    slots[5] = child_text

            # Adverbial modifiers
            elif child.dep_ == "advmod":
                if child_lower.endswith("ly") and not slots[5]:
                    # Manner adverb -> Q5 How
                    slots[5] = child.text
                elif child_lower in ("then", "previously", "originally", "historically") and not slots[6]:
                    slots[6] = child.text

        # Fallback regex for effect clauses if grammatical attachment was detached
        if not slots[7]:
            effect_match = re.search(r"(?:,\s*|\s+)(?:resulting in|leading to|thereby|causing|yielding)\s+([^.]+)", clean_span, re.IGNORECASE)
            if effect_match:
                slots[7] = effect_match.group(0).lstrip(", ").strip()

        # Build coordinate tree nodes and execute recursive re-entrant parsing
        prefix = SUB_PREFIX.get(current_depth, "c")
        frame_nodes = {}

        for facet_id, content in slots.items():
            if not content.strip():
                continue

            tag_prefix, facet_name, facet_plane_desc = PLANE_MAP[facet_id]
            curr_tag = f"{prefix}{facet_id}"
            address_tag = f"{parent_address}.{curr_tag}" if parent_address else curr_tag

            node = CoordinateSeedNode(
                address=address_tag,
                depth=current_depth,
                facet_id=facet_id,
                facet_name=facet_name,
                text=content.strip()
            )

            # RECURSIVE DISPATCH RULE:
            # If current depth < max_depth and the extracted span contains multiple words (a compound clause),
            # drill down into its own internal interrogative sub-engine!
            words = node.text.split()
            if current_depth < self.max_depth and len(words) >= 4:
                # Do not re-enter if span is identical to parent span (prevent cycles)
                if node.text != clean_span:
                    sub_results = self.parse_span_into_slots(
                        text_span=node.text,
                        parent_address=address_tag,
                        current_depth=current_depth + 1
                    )
                    node.sub_frames = sub_results

            frame_nodes[curr_tag] = node

        return frame_nodes

    def serialize_node(self, node: CoordinateSeedNode) -> Dict[str, Any]:
        data = {
            "address": node.address,
            "depth": node.depth,
            "facet": node.facet_name,
            "text": node.text,
            "sub_frames": {}
        }
        for sub_k, sub_node in node.sub_frames.items():
            data["sub_frames"][sub_k] = self.serialize_node(sub_node)
        return data

    def parse_document(self, doc_path: Path) -> List[Dict[str, Any]]:
        text = doc_path.read_text(encoding="utf-8")
        lines = text.splitlines()

        current_header = "Preamble"
        sentences_to_process = []

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
                    token_hash = hashlib.sha256(clean_s.encode('utf-8')).hexdigest()[:8]
                    sentences_to_process.append({
                        "line": line_num,
                        "header": current_header,
                        "text": clean_s,
                        "hash": token_hash
                    })

        processed_sentences = []
        for idx, item in enumerate(sentences_to_process):
            tree_slots = self.parse_span_into_slots(item["text"], parent_address="", current_depth=1)
            serialized_slots = {k: self.serialize_node(v) for k, v in tree_slots.items()}
            
            processed_sentences.append({
                "sentence_index": idx,
                "line": item["line"],
                "header": item["header"],
                "hash": item["hash"],
                "raw_sentence": item["text"],
                "slots": serialized_slots
            })

        return processed_sentences

def flatten_coordinate_seeds(parsed_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Flattens the recursive slot tree into a list of exact dot-notation coordinate seeds."""
    flat_seeds = []

    def walk_slots(slots_dict: Dict[str, Any], sent_meta: Dict[str, Any]):
        for slot_key, slot_val in slots_dict.items():
            flat_seeds.append({
                "address": slot_val["address"],
                "depth": slot_val["depth"],
                "facet": slot_val["facet"],
                "text": slot_val["text"],
                "sentence_index": sent_meta["sentence_index"],
                "line": sent_meta["line"],
                "header": sent_meta["header"],
                "hash": sent_meta["hash"]
            })
            if slot_val.get("sub_frames"):
                walk_slots(slot_val["sub_frames"], sent_meta)

    for item in parsed_docs:
        walk_slots(item["slots"], item)

    return flat_seeds

def format_markdown_seed_catalogue(flat_seeds: List[Dict[str, Any]], doc_name: str) -> str:
    md = [
        f"# Fractal Interrogative Coordinate Catalogue: Exact Invariant Seeds",
        f"**Source Document**: `{doc_name}`",
        f"**Architecture**: 7x7x7 Recursive Dependency Slot Parser (spaCy + Event Physics)",
        f"**Total Atomic Coordinate Seeds**: {len(flat_seeds)}\n",
        "---\n",
        "## The 7 Planes of Reality (42-Structure Invariant Coordinates)\n"
    ]

    # Group by top-level Q plane
    by_macro = {f"Q{i}": [] for i in range(1, 8)}
    for s in flat_seeds:
        macro_prefix = s["address"].split('.')[0]
        if macro_prefix in by_macro:
            by_macro[macro_prefix].append(s)

    for i in range(1, 8):
        q_tag = f"Q{i}"
        _, name, plane_desc = PLANE_MAP[i]
        macro_seeds = by_macro.get(q_tag, [])
        if not macro_seeds:
            continue

        md.append(f"### {q_tag} — {name} ({plane_desc})")
        md.append(f"*Active Seed Coordinates: {len(macro_seeds)}*\n")

        for seed in macro_seeds:
            depth_marker = "●" if seed["depth"] == 1 else "  └─►"
            md.append(f"- {depth_marker} **`[{seed['address']}]`** *(L{seed['line']:03d}|{seed['header']})*: {seed['text']}")
        md.append("")

    return "\n".join(md)

if __name__ == "__main__":
    doc_path = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Treatise_on_How_Words_Work.md")
    print(f"[FractalInterrogativeEngine] Parsing document: {doc_path}...")
    
    engine = FractalInterrogativeEngine(max_depth=2)
    parsed = engine.parse_document(doc_path)
    flat = flatten_coordinate_seeds(parsed)
    
    out_json = Path(r"e:\Vector Field Theory\VFT Docs\polytrope_transformer\Treatise_on_How_Words_Work_FRACTAL_COORDINATES.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2)
        
    out_md = Path(r"e:\Vector Field Theory\VFT Docs\polytrope_transformer\Treatise_on_How_Words_Work_FRACTAL_COORDINATES.md")
    md_content = format_markdown_seed_catalogue(flat, doc_path.name)
    out_md.write_text(md_content, encoding="utf-8")
    
    print(f"\nParsing Complete!")
    print(f"  • Sentences Processed: {len(parsed)}")
    print(f"  • Total Coordinate Seeds Extracted: {len(flat)}")
    print(f"  • JSON Tree Saved: {out_json}")
    print(f"  • Markdown Catalogue Saved: {out_md}")
