"""
Fractal Polytrope Sovereign LLM: Continuous Geodesic Trajectory Tracking
& Hansard Dialogue Turn Causal Extraction.
Cycle 6 R&D Milestone. Self-contained module with zero external dependencies.
"""

import json
import os
import re
import time
import numpy as np
import pathlib

# ============================================================================
# 1. EPISTEMIC AUDIT ENGINE
# ============================================================================

class EpistemicAuditEngine:
    @staticmethod
    def audit(text, coords, q_planes):
        text_lower = text.lower()
        u, p, z = float(coords[0]), float(coords[1]), float(coords[2])
        q = q_planes.copy().astype(np.float64)
        violations = []

        # Tense / Horizon Audit
        future_patterns = [r"\bwill\b", r"\bshall\b", r"\bplans to\b", r"\baims to\b", r"\bdeliver\b"]
        has_future = any(re.search(pat, text_lower) for pat in future_patterns)
        if has_future:
            if u <= 0.05 or p <= 0.05:
                violations.append("MODAL_COLLAPSE: Promissory future assertion erroneously mapped to Regressive [was like]")
                u = max(u, 0.45)
                p = max(p, 0.55)
            if z <= 0.0:
                z = max(z, 0.25)

        # Sovereignty / Governance -> Q1 (Who)
        if any(w in text_lower for w in ["government", "labor", "albanese", "parliament", "state", "national"]):
            q[0] += 0.6
        # Economic -> Q5 (How)
        if any(w in text_lower for w in ["economic", "growth", "economy", "budget"]):
            q[4] += 0.6
        # Purpose -> Q4 (Why)
        if any(w in text_lower for w in ["support", "working families", "families"]):
            q[3] += 0.4

        q = q / np.sum(q)
        return {
            "audited_coords": np.array([u, p, z], dtype=np.float64),
            "audited_q": q,
            "violations_detected": violations,
            "audit_passed": len(violations) == 0
        }

# ============================================================================
# 2. TOKENIZER & NEURAL ARCHITECTURE
# ============================================================================

class ScaledTokenizer:
    def __init__(self, vocab_size=500):
        self.vocab_size = vocab_size
        self.word2idx = {"<PAD>": 0, "<UNK>": 1, "<BOS>": 2, "<EOS>": 3}
        self.idx2word = {0: "<PAD>", 1: "<UNK>", 2: "<BOS>", 3: "<EOS>"}
        
    def fit(self, texts):
        word_counts = {}
        for text in texts:
            words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            for w in words:
                word_counts[w] = word_counts.get(w, 0) + 1
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        for w, _ in sorted_words[:self.vocab_size - len(self.word2idx)]:
            if w not in self.word2idx:
                idx = len(self.word2idx)
                self.word2idx[w] = idx
                self.idx2word[idx] = w

    def encode(self, text, max_len=24):
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        tokens = [self.word2idx.get(w, 1) for w in words[:max_len]]
        if len(tokens) < max_len:
            tokens = tokens + [0] * (max_len - len(tokens))
        return np.array(tokens, dtype=np.int32)

class ScaledPolytropeTransformer:
    def __init__(self, vocab_size=500, d_model=64, d_hidden=128, seq_len=24):
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.d_hidden = d_hidden
        self.seq_len = seq_len
        
        np.random.seed(42)
        self.embedding = np.random.randn(vocab_size, d_model) * 0.08
        self.W_q = np.random.randn(d_model, d_model) * 0.08
        self.W_k = np.random.randn(d_model, d_model) * 0.08
        self.W_v = np.random.randn(d_model, d_model) * 0.08
        
        self.W_ff1 = np.random.randn(d_model, d_hidden) * 0.08
        self.b_ff1 = np.zeros(d_hidden)
        self.W_ff2 = np.random.randn(d_hidden, d_model) * 0.08
        self.b_ff2 = np.zeros(d_model)
        
        self.W_geo = np.random.randn(d_model, 3) * 0.08
        self.b_geo = np.zeros(3)
        self.W_qplane = np.random.randn(d_model, 7) * 0.08
        self.b_qplane = np.zeros(7)

    def softmax(self, x, axis=-1):
        e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
        return e_x / np.sum(e_x, axis=axis, keepdims=True)

    def forward(self, token_ids):
        B, L = token_ids.shape
        self.E = self.embedding[token_ids]
        
        Q = self.E @ self.W_q
        K = self.E @ self.W_k
        V = self.E @ self.W_v
        
        scores = (Q @ K.transpose(0, 2, 1)) / np.sqrt(self.d_model)
        attn = self.softmax(scores, axis=-1)
        ctx = attn @ V
        
        post_attn = self.E + ctx
        H_ff = np.tanh(post_attn @ self.W_ff1 + self.b_ff1)
        ff_out = H_ff @ self.W_ff2 + self.b_ff2
        H_out = post_attn + ff_out
        
        pooled = np.mean(H_out, axis=1)
        pred_coords = 2.0 * np.tanh(pooled @ self.W_geo + self.b_geo)
        pred_q = self.softmax(pooled @ self.W_qplane + self.b_qplane, axis=-1)
        return pred_coords, pred_q

# ============================================================================
# 3. CONTINUOUS GEODESIC TRAJECTORY TRACKER
# ============================================================================

class GeodesicTrajectoryTracker:
    @staticmethod
    def trace_sentence(sentence, tokenizer, model):
        words = re.findall(r'\b[a-zA-Z]+\b', sentence)
        trajectory = []
        
        for i in range(1, len(words) + 1):
            sub_text = " ".join(words[:i])
            toks = tokenizer.encode(sub_text, max_len=24)[None, :]
            pred_c, pred_q = model.forward(toks)
            
            audit = EpistemicAuditEngine.audit(sub_text, pred_c[0], pred_q[0])
            coords = audit["audited_coords"]
            q_dist = audit["audited_q"]
            
            trajectory.append({
                "step": i,
                "token": words[i - 1],
                "sub_text": sub_text,
                "coords": [round(float(v), 4) for v in coords],
                "q_planes": [round(float(v), 4) for v in q_dist],
                "dominant_plane": int(np.argmax(q_dist) + 1)
            })
            
        coord_matrix = np.array([pt["coords"] for pt in trajectory])
        if len(coord_matrix) > 1:
            step_deltas = np.diff(coord_matrix, axis=0)
            step_lengths = np.linalg.norm(step_deltas, axis=1)
            total_arc_length = float(np.sum(step_lengths))
            mean_momentum = float(np.mean(step_lengths))
            curvature_strain = float(np.std(step_lengths))
        else:
            total_arc_length, mean_momentum, curvature_strain = 0.0, 0.0, 0.0
            
        return {
            "sentence": sentence,
            "trajectory_points": trajectory,
            "metrics": {
                "total_arc_length": round(total_arc_length, 4),
                "mean_momentum": round(mean_momentum, 4),
                "curvature_strain": round(curvature_strain, 4)
            }
        }

# ============================================================================
# 4. HANSARD MULTI-TURN EXTRACTION
# ============================================================================

def extract_hansard_dialogues(hansard_path, limit=10):
    dialogues = []
    if not os.path.exists(hansard_path):
        return dialogues
    with open(hansard_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            try:
                item = json.loads(line)
                text = item.get("text", "")
                debate = item.get("debate_title", "Parliamentary Debate")
                date = item.get("date", "")
                sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', text) if len(s.strip()) > 20]
                if len(sentences) >= 2:
                    dialogues.append({
                        "debate": debate,
                        "date": date,
                        "premise_turn": sentences[0],
                        "response_turn": sentences[1]
                    })
            except: continue
            if len(dialogues) >= limit: break
    return dialogues

# ============================================================================
# 5. EXECUTION & LOGGING
# ============================================================================

def run_cycle_6_experiment():
    print("=" * 70)
    print("HOURLY R&D EXECUTION: CYCLE 6 (GEODESIC TRAJECTORY TRACKING)")
    print("=" * 70)
    
    test_statement = "The national government will deliver economic growth and support working families"
    
    tokenizer = ScaledTokenizer(vocab_size=300)
    tokenizer.fit([test_statement, "parliamentary debate australia economic policy"])
    model = ScaledPolytropeTransformer(vocab_size=len(tokenizer.word2idx)+10, d_model=64, d_hidden=128, seq_len=24)
    
    trace_res = GeodesicTrajectoryTracker.trace_sentence(test_statement, tokenizer, model)
    
    print(f"Statement: \"{test_statement}\"")
    print(f"Total Geodesic Arc Length: {trace_res['metrics']['total_arc_length']}")
    print(f"Mean Thought Momentum:    {trace_res['metrics']['mean_momentum']}")
    print(f"Curvature Strain (σ):     {trace_res['metrics']['curvature_strain']}")
    
    print("\nContinuous Manifold Trajectory Steps:")
    plane_names = ["Q1:Metaphysical", "Q2:Possible", "Q3:Physical", "Q4:Lyrical", "Q5:Logical", "Q6:Historical", "Q7:Emotive"]
    for pt in trace_res["trajectory_points"]:
        p_name = plane_names[pt["dominant_plane"] - 1]
        print(f"  Step {pt['step']:2d} [Token: {pt['token']:10s}] -> Coords: {pt['coords']} | Substrate: {p_name}")
        
    hansard_path = "downloads/albanese_statements_1999.jsonl"
    hansard_pairs = extract_hansard_dialogues(hansard_path, limit=5)
    print(f"\nExtracted {len(hansard_pairs)} Multi-Turn Hansard Causal Debate Exchanges:")
    for i, ex in enumerate(hansard_pairs):
        print(f"  [{i+1}] Debate: \"{ex['debate']}\"")
        print(f"      Premise (Cause -z):  \"{ex['premise_turn'][:60]}...\"")
        print(f"      Response (Yield +z): \"{ex['response_turn'][:60]}...\"")
        
    out_file = "/working_dir/c_424c86baff31945d/artifacts/file_generation/ttl=63d/output/geodesic_trajectory_metrics.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "cycle": 6,
            "experiment": "Continuous Manifold Geodesic Tracking & Hansard Multi-Turn Causal Extraction",
            "test_statement": test_statement,
            "geodesic_metrics": trace_res["metrics"],
            "trajectory_steps": trace_res["trajectory_points"],
            "hansard_dialogues": hansard_pairs
        }, f, indent=2)
        
    print(f"\nExported Cycle 6 metrics to: {out_file}")

if __name__ == "__main__":
    run_cycle_6_experiment()
