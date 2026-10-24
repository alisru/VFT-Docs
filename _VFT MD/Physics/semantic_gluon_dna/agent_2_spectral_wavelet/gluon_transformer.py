#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 2: Spectral Wavelet & Continuous Vector Field Transformer
Semantic Gluon Transformer & DNA Reading Head
"""

import os
import re
import json
import math
import glob
from pathlib import Path
import numpy as np

# ---------------------------------------------------------------------------
# 1. CONFIGURATION & CORE DEFINITIONS
# ---------------------------------------------------------------------------

BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics")
AGENT_DIR = BASE_DIR / "semantic_gluon_dna" / "agent_2_spectral_wavelet"
CHAT_PATH = BASE_DIR / "chatgpt infinity maths.md"
IRM_PATH = BASE_DIR / "Comprehensive Report -  Infinity Indefinite Mathematics (IRM).md"
ARXIV_DIR = BASE_DIR / "semantic_gluon_dna" / "arxiv_samples"

GRID_N = 100  # Uniform normalized time grid t in [0, 1]

# 10 Core Semantic Topic Channels T_k
TOPIC_CHANNELS = {
    "T01_Recursive_Sequential_Infinity": [
        r"\binfinit(?:y|ies|e)\b", r"\brecurs(?:ive|ion|ively)\b", r"\bsequence\b",
        r"\bsequential\b", r"\bunbounded\b", r"\bprocess\b", r"\biteration\b",
        r"\bcount(?:ing|able)\b", r"\bstep\b", r"\bprogression\b"
    ],
    "T02_INDEF_Shell_Heartbeat": [
        r"\bindef(?:inite)?\b", r"\bshell\b", r"\bheartbeat\b", r"\bpulse\b",
        r"\bboundary\b", r"\bhorizon\b", r"\boscillat(?:e|ion|ing)\b", r"\bcycle\b",
        r"\bmembrane\b", r"\bstate\s*transition\b", r"\b1/0\b"
    ],
    "T03_Pi_Exploration_Closure": [
        r"\bpi\b", r"\\pi\b", r"3\.14", r"\birrational\b", r"\btranscendental\b",
        r"\bclosure\b", r"\bapproximat(?:e|ion)\b", r"\bdecimal\b", r"\bdigit(?:s)?\b",
        r"\bpolygon\b", r"\bcircumference\b"
    ],
    "T04_Circle_Loop_Formula": [
        r"\bcircle\b", r"\bloop\b", r"\bradius\b", r"\bdiameter\b", r"\bcurvature\b",
        r"\barc\b", r"\brotat(?:e|ion|ional)\b", r"\b2\\pi\b", r"\bsphere\b",
        r"\btorus\b", r"\bclosed\s*path\b"
    ],
    "T05_Holographic_Chi_Vectors": [
        r"\bchi\b", r"\\chi\b", r"\bholograph(?:ic|y)\b", r"\bvector\b",
        r"\btensor\b", r"\bfield\b", r"\bprojection\b", r"\bphase\b",
        r"\bwave(?:let)?\b", r"\bduality\b", r"\bspin(?:or)?\b"
    ],
    "T06_Calculus_Limits_Derivatives": [
        r"\blimit(?:s)?\b", r"\\lim\b", r"\bderivative(?:s)?\b", r"\bintegral(?:s)?\b",
        r"\bdifferential\b", r"\binfinitesimal(?:s)?\b", r"\bcalculus\b",
        r"\bconverg(?:e|ence|ent)\b", r"\bdiverg(?:e|ence|ent)\b", r"\bcontinuous\b",
        r"\bseries\b"
    ],
    "T07_Standard_Math_Axioms": [
        r"\baxiom(?:s|atic)?\b", r"\bcantor\b", r"\bzfc\b", r"\bset\s*theory\b",
        r"\bcardinal(?:ity)?\b", r"\bordinal(?:s)?\b", r"\baleph\b", r"\bbijection\b",
        r"\btheorem\b", r"\bproof\b", r"\bformal(?:ism)?\b", r"\bhilbert\b"
    ],
    "T08_Dimensional_Geometry": [
        r"\bdimension(?:s|al)?\b", r"\bgeometr(?:y|ic)\b", r"\bmanifold\b",
        r"\btopology\b", r"\bspace(?:time)?\b", r"\bmetric\b", r"\bcoordinate(?:s)?\b",
        r"\beuclidean\b", r"\bplane\b", r"\bvolume\b", r"\bsurface\b"
    ],
    "T09_Division_By_Zero_Indeterminate": [
        r"\bzero\b", r"\bdivi(?:de|sion)\s*by\s*zero\b", r"\bindeterminate\b",
        r"\bundefined\b", r"\bsingularit(?:y|ies)\b", r"\b0/0\b", r"\bnull\b",
        r"\bvoid\b", r"\borigin\b", r"\binverse\b"
    ],
    "T10_Information_Entropy_Dynamics": [
        r"\bמידע\b", r"\binformation\b", r"\bentrop(?:y|ic)\b", r"\benergy\b",
        r"\bquantum\b", r"\bstate(?:s)?\b", r"\boperator(?:s)?\b", r"\bsystem\b",
        r"\bdynamic(?:s|al)?\b", r"\bcomplexity\b", r"\bmeasure(?:ment)?\b"
    ]
}

# 8 Modal States mapped into 4D Gluon Charge Vector:
# sigma = [c (Constructive: is_like/may_be), p (Productive: will_be/can_be),
#          r (Reductive: is_not/cant_be), g (Grounding/Historical: was_like/wont_be)]
MODAL_PATTERNS = {
    # Constructive (c): Analogical & Exploratory (is_like, may_be)
    "is_like": [
        r"\bis\s+like\b", r"\bsimilar\s+to\b", r"\banalog(?:ous|y)\b", r"\brepresent(?:s|ed)?\b",
        r"\bcorrespond(?:s)?\s+to\b", r"\bacts\s+as\b", r"\bmirror(?:s)?\b", r"\bequivalent\s+to\b",
        r"\bmeans\b", r"\bviewed\s+as\b", r"\bbehaves\s+like\b"
    ],
    "may_be": [
        r"\bmay\s+be\b", r"\bmight\b", r"\bcould\s+be\b", r"\bperhaps\b", r"\bpossibl(?:e|y)\b",
        r"\bsuggest(?:s|ing)?\b", r"\bwhat\s+if\b", r"\bsuppose\b", r"\bimagine\b",
        r"\bhypothesi(?:s|ze)\b", r"\bpotential(?:ly)?\b"
    ],
    # Productive (p): Generative & Operational (will_be, can_be)
    "will_be": [
        r"\bwill\s+be\b", r"\bbecomes\b", r"\bgenerat(?:es|ing)\b", r"\bproduc(?:es|ing)\b",
        r"\byields\b", r"\bleads\s+to\b", r"\bresults\s+in\b", r"\bemerges\b",
        r"\bcreates\b", r"\btherefore\b", r"\bthus\b", r"\bhence\b", r"\bmust\b"
    ],
    "can_be": [
        r"\bcan\s+be\b", r"\ballows\b", r"\benables\b", r"\bcapable\b", r"\bdefine(?:d|s)?\b",
        r"\bconstruct(?:ed|s)?\b", r"\bformulat(?:e|ed|es)\b", r"\bexpress(?:ed|es)?\b",
        r"\bcalculat(?:e|ed)\b", r"\bderive(?:d|s)?\b", r"\bsolve(?:d|s)?\b"
    ],
    # Reductive (r): Critical & Exclusive (is_not, cant_be)
    "is_not": [
        r"\bis\s+not\b", r"\bisn't\b", r"\bnot\s+a\b", r"\brather\s+than\b", r"\binstead\s+of\b",
        r"\bfails\b", r"\bfallacy\b", r"\berror\b", r"\bcontradict(?:s|ion)?\b",
        r"\bparadox\b", r"\bflaw(?:ed)?\b", r"\bincomplete\b", r"\bwrong\b", r"\bfalse\b"
    ],
    "cant_be": [
        r"\bcannot\b", r"\bcan't\b", r"\bimpossible\b", r"\bnever\b", r"\bno\s+longer\b",
        r"\bprohibit(?:s|ed)?\b", r"\bviolat(?:es|ion)\b", r"\bundefined\b", r"\bdoes\s+not\b",
        r"\bdoesn't\b", r"\binvalid\b", r"\breject(?:s|ed)?\b"
    ],
    # Grounding / Inertial (g): Historical & Terminal (was_like, wont_be)
    "was_like": [
        r"\bwas\b", r"\bwere\b", r"\bhistorical(?:ly)?\b", r"\btraditional(?:ly)?\b",
        r"\bclassical(?:ly)?\b", r"\bstandard\b", r"\bconventional(?:ly)?\b",
        r"\bpreviously\b", r"\boriginal(?:ly)?\b", r"\bestablished\b", r"\bknown\b"
    ],
    "wont_be": [
        r"\bwon't\b", r"\bwill\s+not\b", r"\brefuse(?:s)?\b", r"\bstagnant\b",
        r"\bstatic\b", r"\bfixed\b", r"\bsettled\b", r"\bclosed\b", r"\blimited\s+to\b",
        r"\brestrict(?:ed|s)?\b", r"\bbound(?:ed)?\b", r"\bconstant\b"
    ]
}

COMPILED_TOPICS = {
    k: [re.compile(p, re.IGNORECASE) for p in pats]
    for k, pats in TOPIC_CHANNELS.items()
}
COMPILED_MODALS = {
    k: [re.compile(p, re.IGNORECASE) for p in pats]
    for k, pats in MODAL_PATTERNS.items()
}
EQ_PATTERN = re.compile(r"(\$\$[\s\S]*?\$\$|\$[^$\n]+\$|\\[a-zA-Z]+|[=+\-*/^]{1,2}|\b\d+/\d+\b)")


# ---------------------------------------------------------------------------
# 2. DOCUMENT CHUNKING & CONTINUOUS VECTOR FIELD EXTRACTION
# ---------------------------------------------------------------------------

def load_document_blocks(filepath: Path):
    """
    Splits document into fine-grained paragraph/turn blocks while preserving
    exact line ranges (start_line, end_line) and raw text.
    """
    text = filepath.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    total_lines = max(len(lines), 1)

    blocks = []
    curr_lines = []
    start_line = 1

    for idx, line in enumerate(lines, start=1):
        if line.strip() == "":
            if curr_lines:
                blocks.append({
                    "start_line": start_line,
                    "end_line": idx - 1,
                    "text": "\n".join(curr_lines)
                })
                curr_lines = []
            start_line = idx + 1
        else:
            if not curr_lines:
                start_line = idx
            curr_lines.append(line)

    if curr_lines:
        blocks.append({
            "start_line": start_line,
            "end_line": total_lines,
            "text": "\n".join(curr_lines)
        })

    if not blocks:
        blocks = [{"start_line": 1, "end_line": 1, "text": text}]

    # Assign normalized center time t_b in [0, 1]
    for b in blocks:
        mid_line = 0.5 * (b["start_line"] + b["end_line"])
        b["t_center"] = float(np.clip((mid_line - 1.0) / max(total_lines - 1.0, 1.0), 0.0, 1.0))
        words = re.findall(r"\w+", b["text"])
        b["word_count"] = max(len(words), 1)

    return blocks, total_lines


def compute_block_features(blocks):
    """
    Computes topic weights, 8 modal state counts, 4D gluon charges,
    and symbolic equation density for each raw block.
    """
    topic_keys = list(TOPIC_CHANNELS.keys())
    K = len(topic_keys)
    M = len(blocks)

    raw_w = np.zeros((M, K), dtype=float)
    raw_modals = {m: np.zeros(M, dtype=float) for m in MODAL_PATTERNS.keys()}
    raw_eq_density = np.zeros(M, dtype=float)
    t_centers = np.zeros(M, dtype=float)

    for i, b in enumerate(blocks):
        txt = b["text"]
        wc = b["word_count"]
        t_centers[i] = b["t_center"]

        # Topic hits normalized by sqrt(word_count) to balance short equations & paragraphs
        norm_factor = math.sqrt(wc)
        for k_idx, tk in enumerate(topic_keys):
            hits = sum(len(rx.findall(txt)) for rx in COMPILED_TOPICS[tk])
            raw_w[i, k_idx] = hits / norm_factor

        for mk, rxs in COMPILED_MODALS.items():
            mhits = sum(len(rx.findall(txt)) for rx in rxs)
            raw_modals[mk][i] = mhits / norm_factor

        eq_hits = len(EQ_PATTERN.findall(txt))
        raw_eq_density[i] = eq_hits / norm_factor

    return t_centers, raw_w, raw_modals, raw_eq_density


def gaussian_resample_to_grid(t_centers, values_matrix, t_grid, bandwidth=0.025):
    """
    Resamples an irregularly spaced time series (M, ...) onto a uniform
    continuous grid t_grid of length GRID_N using a Gaussian kernel smoother.
    """
    # diff shape: (GRID_N, M)
    diff = t_grid[:, None] - t_centers[None, :]
    weights = np.exp(-0.5 * (diff / bandwidth) ** 2)
    w_sum = np.sum(weights, axis=1, keepdims=True) + 1e-12
    weights_norm = weights / w_sum
    if values_matrix.ndim == 1:
        return weights_norm @ values_matrix
    return weights_norm @ values_matrix


def ricker_wavelet_transform(signal_1d, scales):
    """
    Computes Continuous Wavelet Transform (CWT) using the Mexican Hat (Ricker)
    wavelet in phase space over the 100-point grid.
    """
    N = len(signal_1d)
    sig_centered = signal_1d - np.mean(signal_1d)
    cwt = np.zeros((len(scales), N), dtype=float)
    t_idx = np.arange(N, dtype=float)

    for s_idx, a in enumerate(scales):
        for tau in range(N):
            u = (t_idx - tau) / a
            # Ricker wavelet: (1 - u^2) * exp(-u^2 / 2) / sqrt(a)
            psi = (1.0 - u ** 2) * np.exp(-0.5 * (u ** 2)) / math.sqrt(a)
            cwt[s_idx, tau] = np.sum(sig_centered * psi)
    return cwt


# ---------------------------------------------------------------------------
# 3. FULL DOCUMENT SPECTRAL WAVELET & PATH INTEGRAL ENGINE
# ---------------------------------------------------------------------------

def analyze_document(doc_id: str, filepath: Path):
    blocks, total_lines = load_document_blocks(filepath)
    t_centers, raw_w, raw_modals, raw_eq = compute_block_features(blocks)

    t_grid = np.linspace(0.0, 1.0, GRID_N)
    dt = 1.0 / (GRID_N - 1)
    topic_keys = list(TOPIC_CHANNELS.keys())
    K = len(topic_keys)

    # Resample topic weight tensor W(t) -> shape (GRID_N, K)
    W_t = gaussian_resample_to_grid(t_centers, raw_w, t_grid, bandwidth=0.025)

    # Resample 8 modal states onto grid
    modals_t = {
        mk: gaussian_resample_to_grid(t_centers, arr, t_grid, bandwidth=0.025)
        for mk, arr in raw_modals.items()
    }
    eq_t = gaussian_resample_to_grid(t_centers, raw_eq, t_grid, bandwidth=0.025)

    # Global 4D Gluon Charge components at time t (before topic modulation)
    c_base = modals_t["is_like"] + modals_t["may_be"]
    p_base = modals_t["will_be"] + modals_t["can_be"]
    r_base = modals_t["is_not"] + modals_t["cant_be"]
    g_base = modals_t["was_like"] + modals_t["wont_be"]

    # Topic-specific 4D Gluon Charge Tensor sigma_k(t) = [c_k(t), p_k(t), r_k(t), g_k(t)]
    # We compute local co-occurrence of topic k and modal state m at the block level,
    # then smooth onto t_grid so each topic has its own genuine 4D gluon trajectory!
    sigma_k_t = np.zeros((K, GRID_N, 4), dtype=float)
    iota_k_t = np.zeros((K, GRID_N), dtype=float)

    raw_c = raw_modals["is_like"] + raw_modals["may_be"]
    raw_p = raw_modals["will_be"] + raw_modals["can_be"]
    raw_r = raw_modals["is_not"] + raw_modals["cant_be"]
    raw_g = raw_modals["was_like"] + raw_modals["wont_be"]
    raw_sigma_block = np.stack([raw_c, raw_p, raw_r, raw_g], axis=1)  # (M, 4)
    # Add small baseline prior so normalized charge is well-defined when a block has pure equations
    raw_sigma_sum = np.sum(raw_sigma_block, axis=1, keepdims=True) + 1e-9
    raw_sigma_unit = raw_sigma_block / raw_sigma_sum

    for k_idx in range(K):
        # Weight block modal distribution by topic activation in that block
        wk_col = raw_w[:, k_idx:k_idx+1] + 1e-4
        weighted_modal = wk_col * (raw_sigma_block + 0.05 * raw_sigma_unit)
        resampled_4d = gaussian_resample_to_grid(t_centers, weighted_modal, t_grid, bandwidth=0.028)
        # Normalize 4D gluon charge vector at each time step t
        norms = np.sum(resampled_4d, axis=1, keepdims=True) + 1e-12
        sigma_normed = resampled_4d / norms
        sigma_k_t[k_idx] = sigma_normed

        c_kt, p_kt, r_kt, g_kt = sigma_normed[:, 0], sigma_normed[:, 1], sigma_normed[:, 2], sigma_normed[:, 3]
        iota_k_t[k_idx] = ((c_kt + p_kt) - (r_kt + g_kt)) / (c_kt + p_kt + r_kt + g_kt + 1e-12)

    # Path Integral for Total Bond Tensor B_{D, k} = \int_0^1 w_k(t) \vec{\sigma}_k(t) dt
    bond_tensors = {}
    for k_idx, tk in enumerate(topic_keys):
        wk_t = W_t[:, k_idx]  # (GRID_N,)
        integrand = wk_t[:, None] * sigma_k_t[k_idx]  # (GRID_N, 4)
        B_vec = np.trapz(integrand, t_grid, axis=0)  # 4D vector [B_c, B_p, B_r, B_g]
        B_mag = float(np.linalg.norm(B_vec))
        B_l1 = float(np.sum(B_vec)) + 1e-12
        net_iota = float(((B_vec[0] + B_vec[1]) - (B_vec[2] + B_vec[3])) / B_l1)
        # Spectral Phase phi in degrees: atan2(Productive - Reductive, Constructive - Grounding)
        spec_phase_rad = math.atan2(B_vec[1] - B_vec[2], B_vec[0] - B_vec[3])
        spec_phase_deg = math.degrees(spec_phase_rad)

        # Wavelet multi-scale energy for topic trajectory wk_t * iota_k_t
        polarized_wave = wk_t * iota_k_t[k_idx]
        cwt_k = ricker_wavelet_transform(polarized_wave, scales=[2.0, 5.0, 10.0, 20.0])
        scale_energies = [float(np.mean(cwt_k[s] ** 2)) for s in range(4)]

        bond_tensors[tk] = {
            "B_vector_cprg": [round(float(x), 5) for x in B_vec],
            "B_magnitude_L2": round(B_mag, 5),
            "total_topic_mass": round(float(np.trapz(wk_t, t_grid)), 5),
            "net_polarity_iota": round(net_iota, 4),
            "spectral_phase_deg": round(spec_phase_deg, 2),
            "wavelet_scale_energy_high_to_low_freq": [round(e, 6) for e in scale_energies]
        }

    # Global Document 4D Gluon Trajectory \vec{\sigma}_{doc}(t)
    doc_sigma_raw = np.stack([c_base, p_base, r_base, g_base], axis=1)
    doc_sigma_t = doc_sigma_raw / (np.sum(doc_sigma_raw, axis=1, keepdims=True) + 1e-12)
    doc_iota_t = ((doc_sigma_t[:, 0] + doc_sigma_t[:, 1]) - (doc_sigma_t[:, 2] + doc_sigma_t[:, 3]))

    # Field Kinematics over t in [0, 1]
    # 1. Semantic Velocity ||d\vec{\sigma}/dt||
    d_sigma_dt = np.gradient(doc_sigma_t, dt, axis=0)
    semantic_velocity_t = np.linalg.norm(d_sigma_dt, axis=1)

    # 2. Topic Breadth Wave (Effective number of active topics via exponential Shannon entropy)
    W_prob = (W_t + 1e-6) / np.sum(W_t + 1e-6, axis=1, keepdims=True)
    shannon_H = -np.sum(W_prob * np.log(W_prob), axis=1)
    topic_breadth_t = np.exp(shannon_H)  # Effective active channels in [1, K]

    # 3. Topic Divergence / Flux ||dW/dt||
    dW_dt = np.gradient(W_t, dt, axis=0)
    topic_flux_t = np.linalg.norm(dW_dt, axis=1)

    # 4. Structural Breakdown Index (SBI):
    # High topic dispersion/breadth + high Reductive/Exclusive shear (r_t) + high velocity
    reductive_fraction_t = doc_sigma_t[:, 2]
    norm_breadth = topic_breadth_t / K
    norm_vel = semantic_velocity_t / (np.max(semantic_velocity_t) + 1e-9)
    breakdown_index_t = norm_breadth * reductive_fraction_t * (0.5 + 0.5 * norm_vel)

    # 5. Complexity Wave: combined symbolic equation density + topic breadth * productive-constructive drive
    inclusive_fraction_t = doc_sigma_t[:, 0] + doc_sigma_t[:, 1]
    complexity_wave_t = (eq_t / (np.max(eq_t) + 1e-9)) * 0.5 + 0.5 * norm_breadth * inclusive_fraction_t

    # Global Wavelet Transform of Document Inclusive-Exclusive Polarity
    doc_cwt = ricker_wavelet_transform(doc_iota_t, scales=[2.0, 5.0, 10.0, 20.0])
    dominant_scale_idx = int(np.argmax(np.mean(doc_cwt ** 2, axis=1)))
    scale_names = ["Micro-Turn (s=2)", "Meso-Section (s=5)", "Macro-Arc (s=10)", "Global-Epoch (s=20)"]

    kinematics_summary = {
        "mean_semantic_velocity": round(float(np.mean(semantic_velocity_t)), 4),
        "max_semantic_velocity": round(float(np.max(semantic_velocity_t)), 4),
        "peak_velocity_t": round(float(t_grid[int(np.argmax(semantic_velocity_t))]), 2),
        "mean_topic_breadth_active_channels": round(float(np.mean(topic_breadth_t)), 3),
        "mean_equation_density": round(float(np.mean(eq_t)), 4),
        "mean_structural_breakdown_index": round(float(np.mean(breakdown_index_t)), 4),
        "max_structural_breakdown_index": round(float(np.max(breakdown_index_t)), 4),
        "peak_breakdown_t": round(float(t_grid[int(np.argmax(breakdown_index_t))]), 2),
        "mean_complexity_wave": round(float(np.mean(complexity_wave_t)), 4),
        "net_document_polarity_iota": round(float(np.trapz(doc_iota_t, t_grid)), 4),
        "dominant_wavelet_band": scale_names[dominant_scale_idx],
        "wavelet_band_energies": {
            scale_names[i]: round(float(np.mean(doc_cwt[i] ** 2)), 6) for i in range(4)
        }
    }

    return {
        "doc_id": doc_id,
        "filepath": str(filepath),
        "total_lines": total_lines,
        "num_blocks": len(blocks),
        "blocks": blocks,
        "t_grid": t_grid,
        "W_t": W_t,
        "sigma_k_t": sigma_k_t,
        "iota_k_t": iota_k_t,
        "doc_sigma_t": doc_sigma_t,
        "doc_iota_t": doc_iota_t,
        "semantic_velocity_t": semantic_velocity_t,
        "topic_breadth_t": topic_breadth_t,
        "eq_t": eq_t,
        "breakdown_index_t": breakdown_index_t,
        "complexity_wave_t": complexity_wave_t,
        "bond_tensors": bond_tensors,
        "kinematics_summary": kinematics_summary
    }


# ---------------------------------------------------------------------------
# 4. CROSS-SPECTRAL TRAJECTORY ALIGNMENT & UNMERGED INSIGHT DETECTOR
# ---------------------------------------------------------------------------

def compute_cross_spectral_alignment(chat_data, irm_data):
    """
    Computes cross-correlation and spectral coherence between `chat` and `irm`
    across all topic channels T_k, and pinpoints exact time windows in `chat`
    with high Productive/Constructive bond energy that have low or missing
    representation in `irm`.
    """
    topic_keys = list(TOPIC_CHANNELS.keys())
    t_grid = chat_data["t_grid"]
    K = len(topic_keys)

    topic_alignments = {}
    unmerged_windows = []

    for k_idx, tk in enumerate(topic_keys):
        # Inclusive (Constructive + Productive) topic bond energy wave E_k^+(t) = w_k(t) * (c_k(t) + p_k(t))
        chat_inc_k = chat_data["W_t"][:, k_idx] * (
            chat_data["sigma_k_t"][k_idx, :, 0] + chat_data["sigma_k_t"][k_idx, :, 1]
        )
        irm_inc_k = irm_data["W_t"][:, k_idx] * (
            irm_data["sigma_k_t"][k_idx, :, 0] + irm_data["sigma_k_t"][k_idx, :, 1]
        )

        # Zero-lag Pearson correlation on normalized time grid
        c_std = np.std(chat_inc_k)
        i_std = np.std(irm_inc_k)
        if c_std > 1e-9 and i_std > 1e-9:
            zero_lag_corr = float(np.corrcoef(chat_inc_k, irm_inc_k)[0, 1])
        else:
            zero_lag_corr = 0.0

        # Max cross-correlation across all time lags tau in [-0.5, +0.5]
        c_norm = (chat_inc_k - np.mean(chat_inc_k)) / (c_std + 1e-9)
        i_norm = (irm_inc_k - np.mean(irm_inc_k)) / (i_std + 1e-9)
        xcorr = np.correlate(c_norm, i_norm, mode="full") / GRID_N
        lags = np.arange(-GRID_N + 1, GRID_N) / float(GRID_N - 1)
        best_idx = int(np.argmax(xcorr))
        max_corr = float(xcorr[best_idx])
        best_lag = float(lags[best_idx])

        # Total inclusive energy integrals
        chat_E_int = float(np.trapz(chat_inc_k, t_grid))
        irm_E_int = float(np.trapz(irm_inc_k, t_grid))
        retention_ratio = irm_E_int / (chat_E_int + 1e-9)

        topic_alignments[tk] = {
            "zero_lag_correlation": round(zero_lag_corr, 4),
            "max_lag_correlation": round(max_corr, 4),
            "optimal_time_shift_dt": round(best_lag, 3),
            "chat_inclusive_energy_integral": round(chat_E_int, 5),
            "irm_inclusive_energy_integral": round(irm_E_int, 5),
            "irm_to_chat_density_ratio": round(retention_ratio, 4)
        }

    # Pinpoint exact time windows in `chat` where high Constructive+Productive
    # energy in `chat` is unmerged or severely attenuated in `irm`.
    # Since `irm` can reorganize topics in time, a topic idea at chat(t) is
    # truly missing/under-represented in `irm` when:
    #   (a) chat_inc_k(t) is at a strong local peak, AND
    #   (b) Either the global IRM energy for topic k is lower than chat's local peak,
    #       OR the local structural correspondence at that normalized trajectory window is near zero.
    chat_blocks = chat_data["blocks"]
    irm_blocks = irm_data["blocks"]

    # Build token sets for all IRM blocks to also measure lexical-concept overlap
    stop_words = {
        "the", "and", "that", "this", "with", "from", "have", "what", "when", "where",
        "which", "while", "into", "your", "you", "are", "for", "not", "can", "will",
        "just", "like", "more", "than", "then", "them", "they", "their", "there",
        "about", "would", "could", "should", "does", "doesn", "don", "but", "also"
    }

    def get_content_tokens(text):
        toks = set(re.findall(r"[a-zA-Z]{4,}", text.lower()))
        return toks - stop_words

    irm_all_tokens_by_block = [get_content_tokens(b["text"]) for b in irm_blocks]

    # Divide t in [0, 1] into 20 contiguous windows of width 0.05 (5 grid points each)
    num_windows = 20
    pts_per_win = GRID_N // num_windows

    for w_idx in range(num_windows):
        i_start = w_idx * pts_per_win
        i_end = min((w_idx + 1) * pts_per_win, GRID_N - 1)
        t_a = float(t_grid[i_start])
        t_b = float(t_grid[i_end])

        # Find dominant topic(s) in chat during [t_a, t_b]
        win_chat_inc = np.zeros(K, dtype=float)
        win_irm_inc = np.zeros(K, dtype=float)
        for k_idx in range(K):
            c_slice = chat_data["W_t"][i_start:i_end+1, k_idx] * (
                chat_data["sigma_k_t"][k_idx, i_start:i_end+1, 0] +
                chat_data["sigma_k_t"][k_idx, i_start:i_end+1, 1]
            )
            i_slice = irm_data["W_t"][i_start:i_end+1, k_idx] * (
                irm_data["sigma_k_t"][k_idx, i_start:i_end+1, 0] +
                irm_data["sigma_k_t"][k_idx, i_start:i_end+1, 1]
            )
            win_chat_inc[k_idx] = float(np.mean(c_slice))
            win_irm_inc[k_idx] = float(np.mean(i_slice))

        top_k_idx = int(np.argmax(win_chat_inc))
        top_topic = topic_keys[top_k_idx]
        chat_peak_val = win_chat_inc[top_k_idx]
        irm_corresponding_val = win_irm_inc[top_k_idx]

        # Find chat blocks in [t_a, t_b]
        win_blocks = [
            b for b in chat_blocks
            if (b["t_center"] >= t_a and b["t_center"] <= t_b)
        ]
        if not win_blocks:
            continue

        line_start = min(b["start_line"] for b in win_blocks)
        line_end = max(b["end_line"] for b in win_blocks)

        # Compute maximum Jaccard concept similarity between this chat window and ANY block in IRM
        win_text = "\n".join(b["text"] for b in win_blocks)
        win_tokens = get_content_tokens(win_text)
        max_jaccard = 0.0
        for irm_toks in irm_all_tokens_by_block:
            if not win_tokens or not irm_toks:
                continue
            inter = len(win_tokens & irm_toks)
            union = len(win_tokens | irm_toks)
            jacc = inter / union if union > 0 else 0.0
            if jacc > max_jaccard:
                max_jaccard = jacc

        # Unmerged Energy Score: high chat inclusive energy * (1 - max_jaccard) * trajectory deficit
        trajectory_deficit = max(0.0, chat_peak_val - 0.5 * irm_corresponding_val)
        unmerged_score = float(chat_peak_val * (1.0 - max_jaccard) + 0.5 * trajectory_deficit)

        # Pick best representative snippet from win_blocks
        best_block = max(win_blocks, key=lambda b: len(b["text"]))
        snippet = re.sub(r"\s+", " ", best_block["text"]).strip()
        if len(snippet) > 220:
            snippet = snippet[:217] + "..."

        unmerged_windows.append({
            "window_index": w_idx + 1,
            "t_range": [round(t_a, 2), round(t_b, 2)],
            "chat_lines": [line_start, line_end],
            "dominant_topic": top_topic,
            "chat_productive_constructive_energy": round(chat_peak_val, 4),
            "irm_trajectory_energy_at_t": round(irm_corresponding_val, 4),
            "max_concept_jaccard_in_irm": round(max_jaccard, 4),
            "unmerged_insight_score": round(unmerged_score, 4),
            "representative_excerpt": snippet
        })

    # Sort windows by unmerged_insight_score descending
    unmerged_windows_sorted = sorted(
        unmerged_windows, key=lambda x: x["unmerged_insight_score"], reverse=True
    )

    return {
        "topic_spectral_alignment": topic_alignments,
        "top_unmerged_chat_windows": unmerged_windows_sorted[:8],
        "all_window_profiles": unmerged_windows
    }


# ---------------------------------------------------------------------------
# 5. MAIN EXECUTION & REPORT GENERATION
# ---------------------------------------------------------------------------

def generate_markdown_report(docs_analyzed, cross_spectral, output_md_path: Path):
    chat_d = docs_analyzed["chat"]
    irm_d = docs_analyzed["irm"]
    arxiv_keys = [k for k in docs_analyzed.keys() if k not in ("chat", "irm")]

    lines = []
    lines.append("# Agent 2: Spectral Wavelet & Continuous Vector Field Transformer Report")
    lines.append("")
    lines.append("## 1. Architectural Overview: Continuous Path Integrals & Spectral Wavelets")
    lines.append(
        "The **Agent 2 Reading Head** models every document $D$ not as a static bag of tokens, "
        "but as a **continuous semantic vector field** evolving over normalized document time $t \\in [0, 1]$ "
        "(resampled onto a uniform $N=100$ Gaussian-smoothed phase grid). At every instant $t$ and across "
        "$K=10$ semantic topic channels $T_k$, the reading head evaluates:"
    )
    lines.append("- **Instantaneous Topic Density** $w_k(t) \\ge 0$")
    lines.append(
        "- **4D Gluon Charge State** $\\vec{\\sigma}_k(t) = [c_k(t), p_k(t), r_k(t), g_k(t)]^T$ mapped from the "
        "8 modal operators (`is_like`/`may_be` $\\to c$, `will_be`/`can_be` $\\to p$, `is_not`/`cant_be` $\\to r$, `was_like`/`wont_be` $\\to g$)"
    )
    lines.append(
        "- **Instantaneous Inclusive–Exclusive Polarity** $\\iota_k(t) = \\frac{(c_k(t)+p_k(t)) - (r_k(t)+g_k(t))}{c_k(t)+p_k(t)+r_k(t)+g_k(t)}$"
    )
    lines.append(
        "- **Total Bond Tensor Path Integral**: $\\mathbf{B}_{D,k} = \\int_0^1 w_k(t)\\,\\vec{\\sigma}_k(t)\\,dt$, "
        "yielding Total Connection Magnitude $\\|\\mathbf{B}_{D,k}\\|_2$, Net Polarity $\\iota_{D,k}$, and "
        "Spectral Phase $\\phi_{D,k} = \\text{atan2}(B_p - B_r, B_c - B_g)$."
    )
    lines.append("")

    # Table 1: Global Field Kinematics across all 5 documents
    lines.append("## 2. Comparative Field Kinematics (`chat` vs. `irm` vs. `arXiv` Controls)")
    lines.append("")
    lines.append(
        "| Document ID | Lines | Blocks | Net Polarity $\\iota_D$ | Mean Velocity $\\|d\\vec{\\sigma}/dt\\|$ | "
        "Active Topic Breadth | Eq. Density | Mean Breakdown Index | Peak Breakdown $t^*$ | Dominant Wavelet Band |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")

    for doc_id, d in docs_analyzed.items():
        ks = d["kinematics_summary"]
        lines.append(
            f"| `{doc_id}` | {d['total_lines']} | {d['num_blocks']} | "
            f"**{ks['net_document_polarity_iota']:+.4f}** | {ks['mean_semantic_velocity']:.4f} | "
            f"{ks['mean_topic_breadth_active_channels']:.2f} / 10 | {ks['mean_equation_density']:.4f} | "
            f"{ks['mean_structural_breakdown_index']:.4f} | $t={ks['peak_breakdown_t']:.2f}$ | "
            f"{ks['dominant_wavelet_band']} |"
        )
    lines.append("")

    # Kinematic Insights
    lines.append("### Key Kinematic Signatures Discovered:")
    lines.append(
        f"1. **Exploratory Phase Velocity (`chat`) vs. Crystallized Report (`irm`)**: "
        f"`chat` spans {chat_d['total_lines']} lines ({chat_d['num_blocks']} conversational blocks) with high "
        f"multi-scale wavelet oscillation across micro-turns (`{chat_d['kinematics_summary']['dominant_wavelet_band']}`), "
        f"whereas `irm` compresses the trajectory into {irm_d['total_lines']} lines with a higher symbolic equation "
        f"density ({irm_d['kinematics_summary']['mean_equation_density']:.4f} vs. {chat_d['kinematics_summary']['mean_equation_density']:.4f}) "
        f"and stronger net inclusive polarity ($\\iota = {irm_d['kinematics_summary']['net_document_polarity_iota']:+.4f}$ vs. "
        f"${chat_d['kinematics_summary']['net_document_polarity_iota']:+.4f}$)."
    )
    lines.append(
        f"2. **Structural Breakdown Index (SBI)**: Peak breakdown in `chat` occurs at normalized time "
        f"$t^* = {chat_d['kinematics_summary']['peak_breakdown_t']:.2f}$ "
        f"(max SBI $= {chat_d['kinematics_summary']['max_structural_breakdown_index']:.4f}$), where high topic dispersion "
        f"collides with intense Reductive/Exclusive shear (`is_not`/`cant_be`) during debates over standard Cantor/limit axioms."
    )
    lines.append("")

    # Table 2: Total Bond Tensor B_{D,k} Comparison between chat and irm
    lines.append("## 3. Total Bond Tensor $\\mathbf{B}_{D,k} = \\int_0^1 w_k(t)\\vec{\\sigma}_k(t)\\,dt$ (`chat` vs. `irm`)")
    lines.append("")
    lines.append(
        "| Topic Channel $T_k$ | `chat` $\\|\\mathbf{B}\\|_2$ | `chat` $\\iota_{D,k}$ | `chat` Phase $\\phi$ | "
        "`irm` $\\|\\mathbf{B}\\|_2$ | `irm` $\\iota_{D,k}$ | `irm` Phase $\\phi$ | Cross-Corr $r_0$ | Max Lag Corr $r_{\\max}$ ($\\Delta t$) |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")

    for tk in TOPIC_CHANNELS.keys():
        bc = chat_d["bond_tensors"][tk]
        bi = irm_d["bond_tensors"][tk]
        ca = cross_spectral["topic_spectral_alignment"][tk]
        lines.append(
            f"| `{tk}` | {bc['B_magnitude_L2']:.4f} | {bc['net_polarity_iota']:+.3f} | {bc['spectral_phase_deg']:+.1f}° | "
            f"{bi['B_magnitude_L2']:.4f} | {bi['net_polarity_iota']:+.3f} | {bi['spectral_phase_deg']:+.1f}° | "
            f"{ca['zero_lag_correlation']:+.3f} | {ca['max_lag_correlation']:+.3f} ({ca['optimal_time_shift_dt']:+.2f}) |"
        )
    lines.append("")

    # Section 4: Unmerged Insights (High Productive/Constructive Bond Strength in chat, low in IRM)
    lines.append("## 4. Cross-Spectral Trajectory Alignment & Unmerged Insights (`chat` $\\setminus$ `irm`)")
    lines.append(
        "By evaluating the inclusive bond flux $E_k^+(t) = w_k(t)\\cdot(c_k(t) + p_k(t))$ across 20 contiguous "
        "normalized time windows $t \\in [t_a, t_b]$ and cross-checking against `irm` both spectrally and lexically "
        "(Jaccard concept overlap), the reading head isolates the exact regions of `chat` containing **high "
        "Constructive/Productive gluon energy that were left unmerged or compressed out of `irm`**:"
    )
    lines.append("")
    lines.append(
        "| Rank | Time Window $t \\in [t_a, t_b]$ | `chat` Line Range | Dominant Topic Channel | "
        "`chat` $E^+(t)$ | `irm` $E^+(t)$ | Max IRM Concept Overlap | Unmerged Score |"
    )
    lines.append("|---:|---|---|---|---:|---:|---:|---:|")

    for rank, win in enumerate(cross_spectral["top_unmerged_chat_windows"], start=1):
        lines.append(
            f"| {rank} | $[{win['t_range'][0]:.2f}, {win['t_range'][1]:.2f}]$ | "
            f"L{win['chat_lines'][0]}–L{win['chat_lines'][1]} | `{win['dominant_topic']}` | "
            f"{win['chat_productive_constructive_energy']:.4f} | {win['irm_trajectory_energy_at_t']:.4f} | "
            f"{win['max_concept_jaccard_in_irm']:.3f} | **{win['unmerged_insight_score']:.4f}** |"
        )
    lines.append("")

    lines.append("### Detailed Excerpts of Top Unmerged Productive/Constructive Windows in `chat`:")
    for rank, win in enumerate(cross_spectral["top_unmerged_chat_windows"][:5], start=1):
        lines.append(
            f"- **Window #{rank} ($t \\in [{win['t_range'][0]:.2f}, {win['t_range'][1]:.2f}]$, "
            f"Lines {win['chat_lines'][0]}–{win['chat_lines'][1]}, `{win['dominant_topic']}`, "
            f"Unmerged Score: `{win['unmerged_insight_score']:.4f}`)**:\n"
            f"  > *\"{win['representative_excerpt']}\"*"
        )
    lines.append("")

    # Section 5: ArXiv Control Comparison
    lines.append("## 5. Spectral Comparison with `arXiv` Physics/Math Control Papers")
    lines.append("")
    lines.append("| Control Document | Top 3 Bond Tensor Channels ($\\|\\mathbf{B}_{D,k}\\|_2$) | Mean Gluon Vector $[c, p, r, g]$ |")
    lines.append("|---|---|---|")
    for ak in arxiv_keys:
        ad = docs_analyzed[ak]
        sorted_b = sorted(
            ad["bond_tensors"].items(),
            key=lambda kv: kv[1]["B_magnitude_L2"],
            reverse=True
        )[:3]
        top3_str = ", ".join(f"`{k}` ({v['B_magnitude_L2']:.3f})" for k, v in sorted_b)
        mean_sig = np.mean(ad["doc_sigma_t"], axis=0)
        sig_str = f"[{mean_sig[0]:.3f}, {mean_sig[1]:.3f}, {mean_sig[2]:.3f}, {mean_sig[3]:.3f}]"
        lines.append(f"| `{ak}` | {top3_str} | `{sig_str}` |")
    lines.append("")

    output_md_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    AGENT_DIR.mkdir(parents=True, exist_ok=True)

    docs_to_run = {
        "chat": CHAT_PATH,
        "irm": IRM_PATH
    }
    for md_file in sorted(ARXIV_DIR.glob("*.md")):
        docs_to_run[md_file.stem] = md_file

    docs_analyzed = {}
    for doc_id, fpath in docs_to_run.items():
        if fpath.exists():
            docs_analyzed[doc_id] = analyze_document(doc_id, fpath)

    cross_spectral = compute_cross_spectral_alignment(
        docs_analyzed["chat"], docs_analyzed["irm"]
    )

    # Prepare serializable JSON output (downsample 100-pt curves to 20-pt summary + full 100-pt global vectors)
    json_out = {
        "agent": "Agent 2: Spectral Wavelet & Continuous Vector Field Transformer",
        "grid_points_N": GRID_N,
        "topic_channels": list(TOPIC_CHANNELS.keys()),
        "documents": {},
        "cross_spectral_chat_vs_irm": cross_spectral
    }

    for doc_id, d in docs_analyzed.items():
        idx_20 = np.linspace(0, GRID_N - 1, 20, dtype=int)
        json_out["documents"][doc_id] = {
            "filepath": d["filepath"],
            "total_lines": d["total_lines"],
            "num_blocks": d["num_blocks"],
            "kinematics_summary": d["kinematics_summary"],
            "bond_tensors": d["bond_tensors"],
            "trajectories_20pt": {
                "t": [round(float(x), 3) for x in d["t_grid"][idx_20]],
                "doc_iota_t": [round(float(x), 4) for x in d["doc_iota_t"][idx_20]],
                "semantic_velocity_t": [round(float(x), 4) for x in d["semantic_velocity_t"][idx_20]],
                "topic_breadth_t": [round(float(x), 3) for x in d["topic_breadth_t"][idx_20]],
                "breakdown_index_t": [round(float(x), 4) for x in d["breakdown_index_t"][idx_20]],
                "complexity_wave_t": [round(float(x), 4) for x in d["complexity_wave_t"][idx_20]]
            }
        }

    results_json_path = AGENT_DIR / "results.json"
    report_md_path = AGENT_DIR / "report.md"

    results_json_path.write_text(json.dumps(json_out, indent=2), encoding="utf-8")
    generate_markdown_report(docs_analyzed, cross_spectral, report_md_path)

    # Print concise summary to stdout
    print("=== AGENT 2: SPECTRAL WAVELET & CONTINUOUS VECTOR FIELD SUMMARY ===")
    for doc_id, d in docs_analyzed.items():
        ks = d["kinematics_summary"]
        print(
            f"[{doc_id}] lines={d['total_lines']} blocks={d['num_blocks']} "
            f"iota={ks['net_document_polarity_iota']:+.4f} "
            f"vel={ks['mean_semantic_velocity']:.4f} "
            f"breadth={ks['mean_topic_breadth_active_channels']:.2f} "
            f"max_SBI={ks['max_structural_breakdown_index']:.4f}@t={ks['peak_breakdown_t']:.2f} "
            f"band={ks['dominant_wavelet_band']}"
        )
    print("\n--- TOP 5 UNMERGED PRODUCTIVE/CONSTRUCTIVE WINDOWS IN CHAT ---")
    for rank, w in enumerate(cross_spectral["top_unmerged_chat_windows"][:5], start=1):
        print(
            f"#{rank}: t=[{w['t_range'][0]:.2f},{w['t_range'][1]:.2f}] "
            f"Lines L{w['chat_lines'][0]}-L{w['chat_lines'][1]} | "
            f"Topic={w['dominant_topic']} | "
            f"Chat_E+={w['chat_productive_constructive_energy']:.4f} vs IRM_E+={w['irm_trajectory_energy_at_t']:.4f} | "
            f"Jaccard={w['max_concept_jaccard_in_irm']:.3f} | Score={w['unmerged_insight_score']:.4f}"
        )
    print(f"\nSaved: {results_json_path}")
    print(f"Saved: {report_md_path}")


if __name__ == "__main__":
    main()
