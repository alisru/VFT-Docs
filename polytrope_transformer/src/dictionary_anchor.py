"""
Dictionary Anchor Module: Ingests the Invariant Bedrock Definitions
and the Scaled Semantic Gluon Dictionary (500 words, causal vectors,
guaranteed bindings, and forbidden clashing pairs).
"""

import os
import json
import torch
from typing import Dict, List, Optional, Tuple, Union
from coordinates import PolytropeCoordinate, ModalRay, QPlane, IntentVector

class DictionaryAnchorEngine:
    def __init__(self, gluon_dict_path: Optional[str] = None, aec_dict_path: Optional[str] = None):
        base = os.path.dirname(os.path.abspath(__file__))

        if gluon_dict_path is None:
            gluon_dict_path = os.path.abspath(
                os.path.join(base, "..", "..", "_VFT MD", "Physics", "semantic_gluon_dna", "agent_lexicon_kernel", "scaled_gluon_dictionary_v2.json")
            )
        if aec_dict_path is None:
            aec_dict_path = os.path.abspath(
                os.path.join(base, "..", "..", "Reality Classification v2", "aec_dictionary.json")
            )

        self.gluon_dict_path = gluon_dict_path
        self.aec_dict_path = aec_dict_path

        self.gluon_entries: Dict[str, Dict] = {}
        self.anchors: Dict[str, Dict] = {}

        self._load_gluon_dictionary()
        self._load_aec_dictionary()

    def _load_gluon_dictionary(self):
        if not os.path.exists(self.gluon_dict_path):
            print(f"[Warning] Scaled Gluon Dictionary not found at: {self.gluon_dict_path}")
            return

        with open(self.gluon_dict_path, "r", encoding="utf-8") as f:
            entries = json.load(f)

        for entry in entries:
            word = entry.get("word", "").lower().strip()
            if not word:
                continue
            
            # Map relations into fast-lookup maps
            rel_mags = entry.get("relative_vector_magnitudes", {})
            guaranteed = {item["target"].lower(): item for item in rel_mags.get("guaranteed", [])}
            possible = {item["target"].lower(): item for item in rel_mags.get("possible", [])}
            metaphorical = {item["target"].lower(): item for item in rel_mags.get("metaphorical", [])}
            forbidden = {item["target"].lower(): item for item in rel_mags.get("forbidden", [])}
            precluded = {item["target"].lower(): item for item in rel_mags.get("precluded", [])}

            self.gluon_entries[word] = {
                "word": word,
                "corpus_frequency": entry.get("corpus_frequency", 0),
                "cefr": entry.get("cefr", "B1"),
                "tail_ingress": entry.get("tail_ingress", {}),
                "head_egress": entry.get("head_egress", {}),
                "modal_spread": entry.get("modal_spread", {}),
                "kernel_vectors": entry.get("kernel_vectors", {}),
                "guaranteed": guaranteed,
                "possible": possible,
                "metaphorical": metaphorical,
                "forbidden": forbidden,
                "precluded": precluded
            }

        print(f"[DictionaryAnchorEngine] Loaded {len(self.gluon_entries)} scaled gluon entries with causal vector magnitudes.")

    def _load_aec_dictionary(self):
        if not os.path.exists(self.aec_dict_path):
            return

        with open(self.aec_dict_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        aec_forms = data.get("aec_forms", {})
        for form_key, form_val in aec_forms.items():
            words_info = form_val.get("descriptive_words", {})
            primary = words_info.get("primary_label", "").lower()
            if not primary:
                continue

            triad = form_val.get("invariant_triad", {})
            action = triad.get("action", [])
            strain = triad.get("strain", [])
            effect = triad.get("effect", [])
            process = form_val.get("definitive_process", "")

            q_planes = form_val.get("q_plane_instantiations", {})
            dominant_plane = QPlane.Q1_PHYSICAL
            for q_k in ["Q7", "Q6", "Q5", "Q4", "Q3", "Q2", "Q1"]:
                if q_k in q_planes and q_planes[q_k]:
                    try:
                        p_idx = int(q_k[1])
                        dominant_plane = QPlane(p_idx)
                        break
                    except Exception:
                        pass

            self.anchors[primary] = {
                "form_id": form_val.get("form_id", ""),
                "primary_label": primary,
                "aliases": [a.lower() for a in words_info.get("aliases", [])],
                "action": action,
                "strain": strain,
                "effect": effect,
                "definitive_process": process,
                "dominant_plane": dominant_plane
            }

    def get_gluon_entry(self, word: str) -> Optional[Dict]:
        return self.gluon_entries.get(word.lower().strip())

    def get_causal_relation(self, from_word: str, to_word: str) -> Dict[str, Union[str, float]]:
        """
        Determines the directed 5' -> 3' causal relationship from from_word to to_word.
        Returns:
            relation_type: 'guaranteed' | 'possible' | 'metaphorical' | 'forbidden' | 'precluded' | 'neutral'
            coupling_score: float (positive for constructive bonds, negative for clashes)
            closing_token: str
        """
        w_from = from_word.lower().strip()
        w_to = to_word.lower().strip()

        entry = self.get_gluon_entry(w_from)
        if not entry:
            return {"relation": "neutral", "score": 0.0, "closing_token": ""}

        # 1. Guaranteed deductive link
        if w_to in entry["guaranteed"]:
            info = entry["guaranteed"][w_to]
            score = float(info.get("coupling_g", 0.5)) + float(info.get("deductive_weight", 0.5))
            return {"relation": "guaranteed", "score": score, "closing_token": info.get("closing_token", "proves")}

        # 2. Forbidden semantic clash (string snap / contradiction)
        if w_to in entry["forbidden"]:
            info = entry["forbidden"][w_to]
            clash = float(info.get("clash_score", 1.0))
            return {"relation": "forbidden", "score": -2.5 * clash, "closing_token": info.get("closing_token", "invalidates")}

        # 3. Precluded boundary partition
        if w_to in entry["precluded"]:
            info = entry["precluded"][w_to]
            excl = float(info.get("exclusion_confidence", 1.0))
            return {"relation": "precluded", "score": -1.5 * excl, "closing_token": info.get("closing_token", "excludes")}

        # 4. Possible probabilistic link
        if w_to in entry["possible"]:
            info = entry["possible"][w_to]
            score = float(info.get("npmi", 0.3))
            return {"relation": "possible", "score": 0.5 * score, "closing_token": info.get("closing_token", "branches_to")}

        # 5. Metaphorical lyrical resonance
        if w_to in entry["metaphorical"]:
            info = entry["metaphorical"][w_to]
            score = float(info.get("structural_similarity", 0.5))
            return {"relation": "metaphorical", "score": 0.3 * score, "closing_token": info.get("closing_token", "resonates_with")}

        return {"relation": "neutral", "score": 0.0, "closing_token": ""}

    def build_pairwise_causal_target(self, words: List[str]) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Builds the Ground Truth Causal Coupling Matrix for a sequence of words.
        Returns:
            target_flux_matrix: [N, N] target attention/gluon affinity (positive for bonds, negative for clashes)
            ingress_demands:    [N] continuous evidence requirements
            egress_supplies:    [N] continuous deductive proof supply
        """
        N = len(words)
        target_matrix = torch.zeros(N, N, dtype=torch.float32)
        ingress_demands = torch.zeros(N, dtype=torch.float32)
        egress_supplies = torch.zeros(N, dtype=torch.float32)

        for i, w_i in enumerate(words):
            e_i = self.get_gluon_entry(w_i)
            if e_i:
                ing = e_i.get("tail_ingress", {})
                ingress_demands[i] = float(ing.get("antecedent_weight", 0.0))
                egr = e_i.get("head_egress", {})
                egress_supplies[i] = float(egr.get("obligation_weight", 0.0))

            for j, w_j in enumerate(words):
                if i == j:
                    target_matrix[i, j] = 1.0 # Self-identity
                else:
                    rel = self.get_causal_relation(w_j, w_i) # j -> i directed flow
                    target_matrix[i, j] = rel["score"]

        return target_matrix, ingress_demands, egress_supplies
