"""
End-to-End Training Engine & Pipeline for the Fractal Polytrope Transformer Kernel.
Self-contained module with zero external dependencies (pure Python & NumPy).
"""

import json
import os
import re
import time
import numpy as np
import pathlib

class SimpleTokenizer:
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

    def encode(self, text, max_len=16):
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        tokens = [self.word2idx.get(w, 1) for w in words[:max_len]]
        if len(tokens) < max_len:
            tokens = tokens + [0] * (max_len - len(tokens))
        return np.array(tokens, dtype=np.int32)

class Adam:
    def __init__(self, params, lr=0.01, beta1=0.9, beta2=0.999, eps=1e-8):
        self.params = params
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = [np.zeros_like(p) for p in params]
        self.v = [np.zeros_like(p) for p in params]
        self.t = 0

    def step(self, grads):
        self.t += 1
        for i in range(len(self.params)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * grads[i]
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * (grads[i] ** 2)
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            self.params[i] -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

class PolytropeTransformerModel:
    def __init__(self, vocab_size=500, d_model=32, d_hidden=64, seq_len=16):
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.d_hidden = d_hidden
        self.seq_len = seq_len
        
        np.random.seed(42)
        self.embedding = np.random.randn(vocab_size, d_model) * 0.1
        self.W_q = np.random.randn(d_model, d_model) * 0.1
        self.W_k = np.random.randn(d_model, d_model) * 0.1
        self.W_v = np.random.randn(d_model, d_model) * 0.1
        
        self.W_ff1 = np.random.randn(d_model, d_hidden) * 0.1
        self.b_ff1 = np.zeros(d_hidden)
        self.W_ff2 = np.random.randn(d_hidden, d_model) * 0.1
        self.b_ff2 = np.zeros(d_model)
        
        self.W_geo = np.random.randn(d_model, 3) * 0.1
        self.b_geo = np.zeros(3)
        self.W_qplane = np.random.randn(d_model, 7) * 0.1
        self.b_qplane = np.zeros(7)
        
        self.params = [
            self.embedding,
            self.W_q, self.W_k, self.W_v,
            self.W_ff1, self.b_ff1, self.W_ff2, self.b_ff2,
            self.W_geo, self.b_geo,
            self.W_qplane, self.b_qplane
        ]
        self.optimizer = Adam(self.params, lr=0.01)

    def softmax(self, x, axis=-1):
        e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
        return e_x / np.sum(e_x, axis=axis, keepdims=True)

    def forward(self, token_ids):
        B, L = token_ids.shape
        self.E = self.embedding[token_ids]
        self.Q = self.E @ self.W_q
        self.K = self.E @ self.W_k
        self.V = self.E @ self.W_v
        
        scale = np.sqrt(self.d_model)
        self.scores = (self.Q @ self.K.transpose(0, 2, 1)) / scale
        self.attn_weights = self.softmax(self.scores, axis=-1)
        self.ctx = self.attn_weights @ self.V
        
        self.post_attn = self.E + self.ctx
        self.H_ff = np.tanh(self.post_attn @ self.W_ff1 + self.b_ff1)
        self.ff_out = self.H_ff @ self.W_ff2 + self.b_ff2
        self.H_out = self.post_attn + self.ff_out
        
        self.pooled = np.mean(self.H_out, axis=1)
        self.pred_coords = 2.0 * np.tanh(self.pooled @ self.W_geo + self.b_geo)
        self.pred_q = self.softmax(self.pooled @ self.W_qplane + self.b_qplane, axis=-1)
        return self.pred_coords, self.pred_q

    def train_step(self, token_ids, target_coords, target_q, lambda_modal=0.5, lambda_plane=0.5):
        B = len(token_ids)
        pred_coords, pred_q = self.forward(token_ids)
        loss_coords = np.mean((pred_coords - target_coords) ** 2)
        grad_coords = 2.0 * (pred_coords - target_coords) / B
        
        loss_modal = 0.0
        grad_modal = np.zeros_like(pred_coords)
        if B >= 4:
            can_be = pred_coords[0, :2]
            was_like = pred_coords[1, :2]
            is_not = pred_coords[2, :2]
            is_like = pred_coords[3, :2]
            loss_modal = float(np.sum((can_be + was_like) ** 2) + np.sum((is_not + is_like) ** 2))
            grad_modal[0, :2] += 2.0 * (can_be + was_like)
            grad_modal[1, :2] += 2.0 * (can_be + was_like)
            grad_modal[2, :2] += 2.0 * (is_not + is_like)
            grad_modal[3, :2] += 2.0 * (is_not + is_like)

        loss_q = -np.mean(np.sum(target_q * np.log(pred_q + 1e-12), axis=-1))
        grad_q_logits = (pred_q - target_q) / B
        total_loss = loss_coords + lambda_modal * loss_modal + lambda_plane * loss_q
        
        grad_coords_total = grad_coords + lambda_modal * grad_modal
        dtanh = (1.0 - (pred_coords / 2.0) ** 2) * 2.0
        grad_coords_pre = grad_coords_total * dtanh
        grad_W_geo = self.pooled.T @ grad_coords_pre
        grad_b_geo = np.sum(grad_coords_pre, axis=0)
        grad_W_qplane = self.pooled.T @ grad_q_logits
        grad_b_qplane = np.sum(grad_q_logits, axis=0)
        
        grad_pooled = grad_coords_pre @ self.W_geo.T + grad_q_logits @ self.W_qplane.T
        grad_H_out = np.tile(grad_pooled[:, None, :] / self.seq_len, (1, self.seq_len, 1))
        grad_ff_out = grad_H_out
        grad_post_attn = grad_H_out.copy()
        grad_W_ff2 = np.sum(self.H_ff.transpose(0, 2, 1) @ grad_ff_out, axis=0)
        grad_b_ff2 = np.sum(grad_ff_out, axis=(0, 1))
        grad_H_ff = grad_ff_out @ self.W_ff2.T
        grad_pre_ff = grad_H_ff * (1.0 - self.H_ff ** 2)
        grad_W_ff1 = np.sum(self.post_attn.transpose(0, 2, 1) @ grad_pre_ff, axis=0)
        grad_b_ff1 = np.sum(grad_pre_ff, axis=(0, 1))
        grad_post_attn += grad_pre_ff @ self.W_ff1.T
        
        grad_E = grad_post_attn.copy()
        grad_ctx = grad_post_attn
        grad_W_v = np.sum(self.E.transpose(0, 2, 1) @ (self.attn_weights.transpose(0, 2, 1) @ grad_ctx), axis=0)
        grad_V = self.attn_weights.transpose(0, 2, 1) @ grad_ctx
        grad_attn_weights = grad_ctx @ self.V.transpose(0, 2, 1)
        grad_scores = (self.attn_weights * (grad_attn_weights - np.sum(grad_attn_weights * self.attn_weights, axis=-1, keepdims=True))) / np.sqrt(self.d_model)
        grad_Q = grad_scores @ self.K
        grad_K = grad_scores.transpose(0, 2, 1) @ self.Q
        grad_W_q = np.sum(self.E.transpose(0, 2, 1) @ grad_Q, axis=0)
        grad_W_k = np.sum(self.E.transpose(0, 2, 1) @ grad_K, axis=0)
        grad_E += grad_Q @ self.W_q.T + grad_K @ self.W_k.T + grad_V @ self.W_v.T
        
        grad_embedding = np.zeros_like(self.embedding)
        for b in range(B):
            for l in range(self.seq_len):
                tok = token_ids[b, l]
                grad_embedding[tok] += grad_E[b, l]
                
        grads = [
            grad_embedding,
            grad_W_q, grad_W_k, grad_W_v,
            grad_W_ff1, grad_b_ff1, grad_W_ff2, grad_b_ff2,
            grad_W_geo, grad_b_geo,
            grad_W_qplane, grad_b_qplane
        ]
        self.optimizer.step(grads)
        return float(total_loss), float(loss_coords), float(loss_modal), float(loss_q)

    def save_weights(self, filepath):
        np.savez(filepath,
                 embedding=self.embedding,
                 W_q=self.W_q, W_k=self.W_k, W_v=self.W_v,
                 W_ff1=self.W_ff1, b_ff1=self.b_ff1,
                 W_ff2=self.W_ff2, b_ff2=self.b_ff2,
                 W_geo=self.W_geo, b_geo=self.b_geo,
                 W_qplane=self.W_qplane, b_qplane=self.b_qplane)

    def load_weights(self, filepath):
        data = np.load(filepath)
        self.embedding = data['embedding']
        self.W_q = data['W_q']
        self.W_k = data['W_k']
        self.W_v = data['W_v']
        self.W_ff1 = data['W_ff1']
        self.b_ff1 = data['b_ff1']
        self.W_ff2 = data['W_ff2']
        self.b_ff2 = data['b_ff2']
        self.W_geo = data['W_geo']
        self.b_geo = data['b_geo']
        self.W_qplane = data['W_qplane']
        self.b_qplane = data['b_qplane']

def load_news_dataset(filepath, limit=100):
    samples = []
    if not os.path.exists(filepath):
        return samples
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            try:
                data = json.loads(line)
                quote = data.get("quote", "").strip()
                headline = data.get("headline", "").strip()
                text = quote if len(quote) > 15 else headline
                if text: samples.append(text)
            except Exception: continue
            if len(samples) >= limit: break
    return samples

def annotate_sample(text):
    text_lower = text.lower()
    action_score = sum(w in text_lower for w in ["produce", "train", "keep", "increase", "make", "create", "spread", "benefit", "national"])
    drag_score = sum(w in text_lower for w in ["problem", "shortage", "fail", "fatal", "crash", "dying", "toll", "decline", "urgent"])
    psi = float(np.clip((action_score - drag_score) * 0.7, -1.8, 1.8))
    
    inclusive_score = sum(w in text_lower for w in ["benefits", "economic", "best practice", "domestic", "community", "national", "our", "families"])
    exclusive_score = sum(w in text_lower for w in ["foreign", "tension", "restriction", "chineseowned", "visas", "threat", "clinic"])
    upsilon = float(np.clip((inclusive_score - exclusive_score) * 0.7, -1.8, 1.8))
    
    cause_score = sum(w in text_lower for w in ["why", "explanation", "reassessment", "training", "needs", "heading home"])
    effect_score = sum(w in text_lower for w in ["produces", "consequences", "dying", "benefits", "planes in the air", "spread"])
    z = float(np.clip((effect_score - cause_score) * 0.6, -1.5, 1.5))
    
    q = np.array([0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2], dtype=np.float64)
    if any(w in text_lower for w in ["leader", "government", "albanese", "who", "we", "he", "authority"]):
        q[0] += 0.6  # Q1 Metaphysical
    if any(w in text_lower for w in ["could", "possible", "pilot shortage", "potential", "needs"]):
        q[1] += 0.5  # Q2 Possible
    if any(w in text_lower for w in ["planes", "air", "flights", "road", "crash", "kempsey", "airport"]):
        q[2] += 0.8  # Q3 Physical
    if any(w in text_lower for w in ["meaning", "best practice", "purpose", "why"]):
        q[3] += 0.4  # Q4 Lyrical
    if any(w in text_lower for w in ["economic", "benefits", "training", "jobs", "count", "toll"]):
        q[4] += 0.6  # Q5 Logical
    if any(w in text_lower for w in ["why", "explanation", "reassessment", "sequence", "history"]):
        q[5] += 0.5  # Q6 Historical
    if any(w in text_lower for w in ["dying", "fatal", "tragic", "carnage", "consequences", "tension"]):
        q[6] += 0.8  # Q7 Emotive
    q = q / np.sum(q)
    return np.array([upsilon, psi, z], dtype=np.float64), q

def build_and_train_pipeline():
    news_path = "albanese_statements_news.jsonl"
    texts = load_news_dataset(news_path, limit=60)
    annotations = [annotate_sample(t) for t in texts]
    tokenizer = SimpleTokenizer(vocab_size=350)
    tokenizer.fit(texts)
    X_train = np.array([tokenizer.encode(t, max_len=16) for t in texts])
    y_coords = np.array([ann[0] for ann in annotations])
    y_q = np.array([ann[1] for ann in annotations])
    
    model = PolytropeTransformerModel(vocab_size=len(tokenizer.word2idx) + 10, d_model=32, d_hidden=64, seq_len=16)
    for epoch in range(1, 51):
        indices = np.random.permutation(len(X_train))
        for b in range(len(X_train) // 12):
            b_idx = indices[b * 12 : (b + 1) * 12]
            model.train_step(X_train[b_idx], y_coords[b_idx], y_q[b_idx])
    model.save_weights("polytrope_weights.npz")
    print("Model trained and weights saved.")

if __name__ == "__main__":
    build_and_train_pipeline()
