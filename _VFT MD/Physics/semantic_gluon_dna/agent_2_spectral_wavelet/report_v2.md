# Agent 2 (Round 2): Multi-Scale Spectral Trajectory, Working-Out Continuity & Full IRM Formal Corpus Audit

## 1. Architectural Critique of `unified_gluon_dna_engine.py` & Round 2 Upgrades

### Three Structural Flaws Identified in `unified_gluon_dna_engine.py` (v1.0):
1. **Hardcoded Early-Chat Topic Blindness (False-Intron Collapse)**: `unified_gluon_dna_engine.py` hardcoded 12 genes (`SEQ, IND, CHI, PI, EXP, CIR, LIM, AXI, ROD, DIV, PHY, ALG`) tailored to `chatgpt infinity maths.md`. When run on `irm_formal_corpus` (e.g., Paper 17 Navier-Stokes Regularity, Paper 9 Cohomology/Sheaves, Paper 24/25 Spectral Mass Gap, Levi-Civita fields) and the expanded `arxiv_samples`, entire rigorous proof sections on **vorticity/enstrophy dissipation**, **Sobolev norms**, **non-Archimedean valuations**, **ultrafilter ultrapowers**, and **sheaf cohomology** failed to match the 12 regex lists and were misclassified as `INT` (non-coding introns)!
2. **Declarative Equations Confused with Working-Out Continuity**: In `unified_gluon_dna_engine.py` (lines 274–277), any block without an explicit English modal phrase defaulted to `if '=' in txt or ':' in txt: m_counts['is_like'] = 1`. This treated isolated summary equations in `Comprehensive Report - IRM.md` identically to multi-page chained derivations in `Paper 17 (Navier-Stokes)` or `arXiv` papers.
3. **Missing Equation-to-Inference & Variable Carryover Wave $W_{\text{work}}(t)$**: v1.0 computed symbol density per block in isolation, ignoring whether mathematical variables ($u, \omega, \nu, \epsilon, x_\epsilon, \nabla$) and logical inference operators (`therefore`, `substituting`, `integrating`, `by lemma`, `\implies`) **chain continuously across consecutive blocks**.

### What `gluon_transformer_v2.py` Introduces:
- **16-Channel Mathematical Physics Spectrum + Dynamic TF-IDF Eigen-Topic Discovery**: Expands the core spectrum to 16 channels covering PDE/Navier-Stokes (`T09`), Vorticity/Enstrophy (`T10`), Levi-Civita/Non-Archimedean (`T11`), Ultrafilters/Hyperreals (`T12`), Sheaf/Cohomology (`T13`), and Spectral Mass Gap/Hilbert Operators (`T14`), plus automatic per-document Eigen-Term extraction.
- **Working-Out Continuity Wave $W_{\text{work}}(t)$ vs. Declarative Summary Ratio $\text{DSR}(t)$**:
  $$W_{\text{work}}(t) = \sqrt{\rho_{\text{eq}}(t)\cdot \rho_{\text{chain}}(t)} \cdot \bigl(0.5 + 0.5\,\kappa_{\text{var}}(t)\bigr), \qquad \text{DSR}(t) = \frac{\sum_k w_k(t)}{W_{\text{work}}(t) + 0.15}$$
  where $\rho_{\text{eq}}(t)$ is symbolic equation density, $\rho_{\text{chain}}(t)$ is inference chaining density, and $\kappa_{\text{var}}(t)$ is consecutive-block algebraic variable carryover.

## 2. Working-Out Continuity Index (WOCI) vs. Declarative Summary Ratio Across All Documents

| Document ID | Cat. | Lines | Polarity $\iota_D$ | Working-Out Index (WOCI) | Var Carryover $\kappa_{\text{var}}$ | Chain Persistence $L_{\text{chain}}$ | Declarative Ratio (DSR) | Work / Decl Ratio | Exon Rate (v1 $\to$ v2) | Dominant Work Wavelet |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `chat` | `chat` | 3972 | +0.332 | **0.0443** | 0.059 | 0.00 | 0.836 | **0.053** | 33.7% $\to$ **36.7%** | Section-Arc (s=10) |
| `irm_report` | `irm_report` | 680 | +0.063 | **0.0646** | 0.123 | 0.00 | 1.487 | **0.043** | 67.9% $\to$ **68.6%** | Global-Proof (s=20) |
| `Axiomatic_Foundations_of_Infinitesimal_Reality_Math__The__base_n.d.e.f` | `irm_formal` | 961 | -0.436 | **0.0482** | 0.056 | 0.00 | 0.621 | **0.077** | 20.2% $\to$ **24.9%** | Global-Proof (s=20) |
| `Claude_Engineering___Verification_Log` | `irm_formal` | 3251 | -0.653 | **0.0305** | 0.021 | 0.00 | 0.537 | **0.057** | 29.6% $\to$ **33.5%** | Global-Proof (s=20) |
| `Computational_and_Ontological_Superiority_of_IRM_Over_ZFC` | `irm_formal` | 533 | -0.425 | **0.0891** | 0.261 | 0.00 | 0.758 | **0.117** | 27.7% $\to$ **30.7%** | Global-Proof (s=20) |
| `Developing_Calculus_Towards_Infinitesimal_Reality_Math__IRM__from_Pre-` | `irm_formal` | 299 | +0.005 | **0.0982** | 0.270 | 0.00 | 0.614 | **0.160** | 32.0% $\to$ **36.0%** | Section-Arc (s=10) |
| `Formal_Paper_12__The_Pre-Quotient_Continuum__Levi-Civita_Field_Embeddi` | `irm_formal` | 523 | -0.887 | **0.0910** | 0.088 | 0.00 | 0.909 | **0.100** | 25.2% $\to$ **33.3%** | Lemma-Block (s=5) |
| `Formal_Paper_17__Global_Existence__Uniqueness__and_C___Smoothness_of_t` | `irm_formal` | 929 | -0.182 | **0.0902** | 0.140 | 0.00 | 1.372 | **0.066** | 41.1% $\to$ **65.0%** | Global-Proof (s=20) |
| `Formal_Paper_24__Non-Archimedean_Yang-Mills_Existence_and_Mass_Gap__Ce` | `irm_formal` | 167 | +0.380 | **0.0800** | 0.070 | 0.00 | 1.442 | **0.056** | 45.2% $\to$ **58.3%** | Global-Proof (s=20) |
| `Formal_Paper_25__Non-Archimedean_Spectral_Realization_of_the_Riemann_Z` | `irm_formal` | 267 | +0.286 | **0.1178** | 0.258 | 0.06 | 0.784 | **0.150** | 21.6% $\to$ **39.6%** | Global-Proof (s=20) |
| `Formal_Paper_30__The_Master_Mathematical_Canon_of_Infinitesimal_Realit` | `irm_formal` | 261 | -0.205 | **0.0691** | 0.123 | 0.00 | 1.373 | **0.050** | 58.0% $\to$ **64.9%** | Global-Proof (s=20) |
| `Formal_Paper_7__Discrete_0_2_Bounded_Lattice_Mechanics__The_Try___Catc` | `irm_formal` | 863 | -0.052 | **0.0730** | 0.037 | 0.00 | 0.418 | **0.174** | 15.5% $\to$ **19.7%** | Section-Arc (s=10) |
| `Formal_Paper_9__Higher-Order_Simplicial_Homology__Principal_G-Bundles_` | `irm_formal` | 755 | -0.431 | **0.0737** | 0.080 | 0.00 | 0.536 | **0.138** | 17.7% $\to$ **23.8%** | Global-Proof (s=20) |
| `HYPOTHESIS_semantic_connection` | `irm_formal` | 240 | -0.065 | **0.0170** | 0.000 | 0.00 | 0.574 | **0.030** | 29.4% $\to$ **33.8%** | Global-Proof (s=20) |
| `ORTHODOX_BRIDGE_ZFC` | `irm_formal` | 241 | -0.825 | **0.0355** | 0.066 | 0.00 | 1.134 | **0.031** | 40.3% $\to$ **48.6%** | Global-Proof (s=20) |
| `PM_Prompt__Amended_-_Directive_Matrix_Protocol_` | `irm_formal` | 128 | -0.516 | **0.0208** | 0.000 | 0.00 | 0.174 | **0.119** | 13.3% $\to$ **13.3%** | Global-Proof (s=20) |
| `arxiv_1401.0388v2` | `arxiv` | 3288 | +0.592 | **0.1619** | 0.227 | 0.08 | 0.199 | **0.815** | 4.0% $\to$ **13.2%** | Global-Proof (s=20) |
| `arxiv_1502.06936v2` | `arxiv` | 8249 | +0.174 | **0.2980** | 0.372 | 0.25 | 0.279 | **1.068** | 34.6% $\to$ **40.3%** | Section-Arc (s=10) |
| `arxiv_1505.02628v2` | `arxiv` | 1970 | +0.498 | **0.1822** | 0.268 | 0.00 | 0.359 | **0.508** | 2.3% $\to$ **30.8%** | Global-Proof (s=20) |
| `arxiv_1509.03798v1` | `arxiv` | 877 | -0.310 | **0.3077** | 0.527 | 0.55 | 0.494 | **0.623** | 45.0% $\to$ **64.1%** | Global-Proof (s=20) |
| `arxiv_1701.05187v1` | `arxiv` | 1939 | -0.335 | **0.0838** | 0.141 | 0.00 | 0.171 | **0.490** | 7.9% $\to$ **10.6%** | Global-Proof (s=20) |
| `arxiv_1706.10173v1` | `arxiv` | 5496 | +0.609 | **0.1194** | 0.087 | 0.00 | 0.053 | **2.252** | 0.4% $\to$ **2.8%** | Global-Proof (s=20) |
| `arxiv_1803.06056v2` | `arxiv` | 4985 | +0.768 | **0.2282** | 0.417 | 0.12 | 0.082 | **2.772** | 5.4% $\to$ **8.3%** | Section-Arc (s=10) |
| `arxiv_2208.00415v2` | `arxiv` | 1634 | +0.483 | **0.6563** | 0.602 | 0.90 | 0.397 | **1.653** | 41.8% $\to$ **58.9%** | Global-Proof (s=20) |

### Category-Level Benchmark Comparison (`chat` vs. `irm_report` vs. `irm_formal` vs. `arxiv`):

| Corpus Category | Doc Count | Mean WOCI (Working-Out) | Mean Variable Carryover $\kappa_{\text{var}}$ | Mean Chain Persistence | Mean Declarative Ratio (DSR) | Mean Work/Decl Ratio | Mean v2 Exon Coverage |
|---|---:|---:|---:|---:|---:|---:|---:|
| **chat** | 1 | **0.0443** | 0.0592 | 0.000 | 0.8358 | **0.0530** | 36.7% |
| **irm_report** | 1 | **0.0646** | 0.1231 | 0.000 | 1.4871 | **0.0435** | 68.6% |
| **irm_formal** | 14 | **0.0667** | 0.1050 | 0.004 | 0.8034 | **0.0947** | 37.5% |
| **arxiv** | 8 | **0.2547** | 0.3302 | 0.238 | 0.2543 | **1.2725** | 28.6% |

## 3. 16-Channel Bond & Working-Out Bridge (`chat` $\to$ `irm_report` $\to$ `irm_formal_corpus` vs. `arXiv`)

| Topic Channel $T_k$ | `chat` Work Mass | `irm_report` Work Mass | `irm_formal` Total Work Mass | Formal vs. Report Amplification | Strongest IRM Formal Paper ($\|\mathbf{B}\|_2$) | Strongest `arXiv` Benchmark ($\|\mathbf{B}\|_2$) |
|---|---:|---:|---:|---:|---|---|
| `T01_SEQ_Recursive_Infinity` | 0.0015 | 0.0037 | **0.0123** | **3.4x** | `ORTHODOX_BRIDGE_ZFC` (0.024) | `arxiv_1502.06936v2` (0.016) |
| `T02_IND_Definitive_Shell_Epsilon` | 0.0003 | 0.0025 | **0.0017** | **0.7x** | `Formal_Paper_12__The_Pre-Quotient_Continuum__Levi-Civita_Field_Embeddi` (0.004) | `arxiv_2208.00415v2` (0.001) |
| `T03_CHI_Holographic_Vector_Tensor` | 0.0019 | 0.0035 | **0.0085** | **2.4x** | `Formal_Paper_25__Non-Archimedean_Spectral_Realization_of_the_Riemann_Z` (0.009) | `arxiv_2208.00415v2` (0.001) |
| `T04_PI_CIR_Geometric_Closure` | 0.0000 | 0.0037 | **0.0214** | **5.8x** | `HYPOTHESIS_semantic_connection` (0.026) | `arxiv_2208.00415v2` (0.082) |
| `T05_LIM_Calculus_Derivatives` | 0.0010 | 0.0026 | **0.0215** | **8.1x** | `Developing_Calculus_Towards_Infinitesimal_Reality_Math__IRM__from_Pre-` (0.025) | `arxiv_1502.06936v2` (0.030) |
| `T06_AXI_ZFC_Peano_Foundations` | 0.0008 | 0.0031 | **0.0188** | **6.2x** | `Formal_Paper_30__The_Master_Mathematical_Canon_of_Infinitesimal_Realit` (0.061) | `arxiv_1509.03798v1` (0.028) |
| `T07_DIV_Zero_Horizon_Singularity` | 0.0000 | 0.0000 | **0.0072** | **717.0x** | `Formal_Paper_17__Global_Existence__Uniqueness__and_C___Smoothness_of_t` (0.015) | `arxiv_2208.00415v2` (0.004) |
| `T08_ROD_Radix_Numeral_Carry` | 0.0009 | 0.0000 | **0.0011** | **109.0x** | `PM_Prompt__Amended_-_Directive_Matrix_Protocol_` (0.011) | `arxiv_1509.03798v1` (0.001) |
| `T09_PDE_Navier_Stokes_Fluid` | 0.0000 | 0.0001 | **0.0068** | **84.9x** | `Formal_Paper_17__Global_Existence__Uniqueness__and_C___Smoothness_of_t` (0.032) | `arxiv_1505.02628v2` (0.014) |
| `T10_ENS_Vorticity_Enstrophy_Dissipation` | 0.0000 | 0.0000 | **0.0092** | **229.0x** | `Formal_Paper_17__Global_Existence__Uniqueness__and_C___Smoothness_of_t` (0.039) | `arxiv_2208.00415v2` (0.080) |
| `T11_LCF_Levi_Civita_NonArchimedean` | 0.0001 | 0.0000 | **0.0176** | **1766.0x** | `ORTHODOX_BRIDGE_ZFC` (0.035) | `arxiv_1509.03798v1` (0.053) |
| `T12_ULT_Ultrafilter_Hyperreal_Transfer` | 0.0008 | 0.0002 | **0.0020** | **8.5x** | `ORTHODOX_BRIDGE_ZFC` (0.015) | `arxiv_1509.03798v1` (0.012) |
| `T13_COH_Sheaf_Cohomology_Topology` | 0.0001 | 0.0000 | **0.0127** | **1272.0x** | `Formal_Paper_9__Higher-Order_Simplicial_Homology__Principal_G-Bundles_` (0.020) | `arxiv_1509.03798v1` (0.002) |
| `T14_GAP_Spectral_Mass_Gap_Hilbert` | 0.0000 | 0.0000 | **0.0244** | **2441.0x** | `Formal_Paper_24__Non-Archimedean_Yang-Mills_Existence_and_Mass_Gap__Ce` (0.063) | `arxiv_1401.0388v2` (0.000) |
| `T15_ALG_Ring_Valuation_Isomorphism` | 0.0002 | 0.0000 | **0.0068** | **681.0x** | `Formal_Paper_12__The_Pre-Quotient_Continuum__Levi-Civita_Field_Embeddi` (0.018) | `arxiv_1509.03798v1` (0.008) |
| `T16_PHY_Relativity_Quantum_Action` | 0.0000 | 0.0004 | **0.0210** | **51.3x** | `Formal_Paper_24__Non-Archimedean_Yang-Mills_Existence_and_Mass_Gap__Ce` (0.049) | `arxiv_1803.06056v2` (0.002) |

## 4. Individual IRM Formal Papers & arXiv Controls: Spectral DNA & Dynamic Eigen-Terms

| Document ID | Top 3 Spectral Topic Channels ($\|\mathbf{B}_{D,k}\|_2$) | Top Dynamically Discovered Eigen-Terms (TF-IDF) |
|---|---|---|
| `irm_report` | `T04_PI_CIR_Geometric_Closure` (0.032), `T03_CHI_Holographic_Vector_Tensor` (0.031), `T06_AXI_ZFC_Peano_Foundations` (0.029) | `generative` (31), `circle` (34), `infinitesimal` (71), `indef` (24), `axiom` (37), `definitive` (24) |
| `Axiomatic_Foundations_of_Infinitesimal_Reality_Math__The__base_n.d.e.f` | `T05_LIM_Calculus_Derivatives` (0.014), `T06_AXI_ZFC_Peano_Foundations` (0.012), `T11_LCF_Levi_Civita_NonArchimedean` (0.010) | `infin` (44), `realitynumber` (23), `ultra` (16), `naturals` (17), `reals` (22), `times` (39) |
| `Claude_Engineering___Verification_Log` | `T01_SEQ_Recursive_Infinity` (0.009), `T16_PHY_Relativity_Quantum_Action` (0.007), `T03_CHI_Holographic_Vector_Tensor` (0.006) | `entry` (82), `corpus` (98), `mine` (36), `fail` (63), `floor` (77), `directive` (43) |
| `Computational_and_Ontological_Superiority_of_IRM_Over_ZFC` | `T04_PI_CIR_Geometric_Closure` (0.026), `T01_SEQ_Recursive_Infinity` (0.016), `T06_AXI_ZFC_Peano_Foundations` (0.016) | `text` (121), `infty` (85), `frac` (52), `epsilon` (45), `mathbf` (34), `times` (41) |
| `Developing_Calculus_Towards_Infinitesimal_Reality_Math__IRM__from_Pre-` | `T05_LIM_Calculus_Derivatives` (0.025), `T01_SEQ_Recursive_Infinity` (0.018), `T06_AXI_ZFC_Peano_Foundations` (0.010) | `infty` (64), `delta` (58), `calculus` (28), `text` (36), `frac` (33), `mathcal` (21) |
| `Formal_Paper_12__The_Pre-Quotient_Continuum__Levi-Civita_Field_Embeddi` | `T06_AXI_ZFC_Peano_Foundations` (0.028), `T05_LIM_Calculus_Derivatives` (0.023), `T11_LCF_Levi_Civita_NonArchimedean` (0.022) | `cantor` (44), `mathcal` (33), `mathbb` (41), `civita` (19), `levi` (19), `operatorname` (16) |
| `Formal_Paper_17__Global_Existence__Uniqueness__and_C___Smoothness_of_t` | `T10_ENS_Vorticity_Enstrophy_Dissipation` (0.039), `T09_PDE_Navier_Stokes_Fluid` (0.032), `T04_PI_CIR_Geometric_Closure` (0.021) | `vortex` (64), `cellular` (73), `harmonization` (32), `fluid` (57), `enstrophy` (38), `hydrodynamic` (23) |
| `Formal_Paper_24__Non-Archimedean_Yang-Mills_Existence_and_Mass_Gap__Ce` | `T14_GAP_Spectral_Mass_Gap_Hilbert` (0.063), `T16_PHY_Relativity_Quantum_Action` (0.049), `T11_LCF_Levi_Civita_NonArchimedean` (0.022) | `text` (75), `gauge` (31), `mass` (33), `mathcal` (35), `mills` (21), `wilson` (17) |
| `Formal_Paper_25__Non-Archimedean_Spectral_Realization_of_the_Riemann_Z` | `T14_GAP_Spectral_Mass_Gap_Hilbert` (0.047), `T11_LCF_Levi_Civita_NonArchimedean` (0.016), `T05_LIM_Calculus_Derivatives` (0.012) | `cell` (43), `riemann` (33), `zeta` (24), `adjoint` (24), `frac` (56), `gamma` (39) |
| `Formal_Paper_30__The_Master_Mathematical_Canon_of_Infinitesimal_Realit` | `T06_AXI_ZFC_Peano_Foundations` (0.061), `T16_PHY_Relativity_Quantum_Action` (0.027), `T15_ALG_Ring_Valuation_Isomorphism` (0.016) | `text` (58), `mathcal` (34), `cellular` (21), `axiom` (27), `infty` (36), `operatorname` (14) |
| `Formal_Paper_7__Discrete_0_2_Bounded_Lattice_Mechanics__The_Try___Catc` | `T05_LIM_Calculus_Derivatives` (0.013), `T13_COH_Sheaf_Cohomology_Topology` (0.009), `T01_SEQ_Recursive_Infinity` (0.008) | `discrete` (30), `mathcal` (24), `catch` (11), `boundary` (27), `evaluatoranchor` (9), `quadratic` (10) |
| `Formal_Paper_9__Higher-Order_Simplicial_Homology__Principal_G-Bundles_` | `T13_COH_Sheaf_Cohomology_Topology` (0.020), `T04_PI_CIR_Geometric_Closure` (0.016), `T16_PHY_Relativity_Quantum_Action` (0.014) | `semantic` (32), `homology` (16), `text` (47), `simplicial` (14), `simplex` (15), `curvature` (22) |
| `HYPOTHESIS_semantic_connection` | `T04_PI_CIR_Geometric_Closure` (0.026), `T16_PHY_Relativity_Quantum_Action` (0.011), `T13_COH_Sheaf_Cohomology_Topology` (0.010) | `context` (12), `representation` (12), `transport` (9), `chart` (6), `procrustes` (5), `subbundle` (5) |
| `ORTHODOX_BRIDGE_ZFC` | `T11_LCF_Levi_Civita_NonArchimedean` (0.035), `T06_AXI_ZFC_Peano_Foundations` (0.034), `T01_SEQ_Recursive_Infinity` (0.024) | `corpus` (17), `civita` (14), `levi` (14), `orthodox` (16), `linker` (7), `adic` (9) |
| `PM_Prompt__Amended_-_Directive_Matrix_Protocol_` | `T08_ROD_Radix_Numeral_Carry` (0.011), `T16_PHY_Relativity_Quantum_Action` (0.008), `T05_LIM_Calculus_Derivatives` (0.004) | `directive` (13), `digest` (7), `spreadsheet` (6), `evidence` (8), `engineer` (8), `directives` (5) |
| `arxiv_1401.0388v2` | `T09_PDE_Navier_Stokes_Fluid` (0.013), `T10_ENS_Vorticity_Enstrophy_Dissipation` (0.011), `T05_LIM_Calculus_Derivatives` (0.008) | `alpha` (511), `eqref` (123), `lambda` (205), `langle` (114), `rangle` (114), `weak` (93) |
| `arxiv_1502.06936v2` | `T05_LIM_Calculus_Derivatives` (0.030), `T01_SEQ_Recursive_Infinity` (0.016), `T15_ALG_Ring_Valuation_Isomorphism` (0.007) | `mathrm` (458), `bigskip` (303), `succ` (252), `defy` (233), `infty` (788), `begin` (557) |
| `arxiv_1505.02628v2` | `T10_ENS_Vorticity_Enstrophy_Dissipation` (0.075), `T09_PDE_Navier_Stokes_Fluid` (0.014), `T05_LIM_Calculus_Derivatives` (0.003) | `omega` (252), `eqnarray` (96), `nonumber` (103), `theta` (149), `frac` (207), `nabla` (101) |
| `arxiv_1509.03798v1` | `T11_LCF_Levi_Civita_NonArchimedean` (0.053), `T06_AXI_ZFC_Peano_Foundations` (0.028), `T05_LIM_Calculus_Derivatives` (0.018) | `mathbb` (734), `emph` (213), `enum` (56), `completeness` (74), `item` (90), `ordered` (84) |
| `arxiv_1701.05187v1` | `T05_LIM_Calculus_Derivatives` (0.011), `T12_ULT_Ultrafilter_Hyperreal_Transfer` (0.010), `T06_AXI_ZFC_Peano_Foundations` (0.007) | `emph` (73), `track` (32), `students` (34), `katz` (36), `bibitem` (38), `http` (30) |
| `arxiv_1706.10173v1` | `T09_PDE_Navier_Stokes_Fluid` (0.006), `T10_ENS_Vorticity_Enstrophy_Dissipation` (0.002), `T05_LIM_Calculus_Derivatives` (0.001) | `mbox` (723), `boldmath` (174), `scriptstyle` (168), `vspace` (148), `displaystyle` (70), `mathbb` (196) |
| `arxiv_1803.06056v2` | `T01_SEQ_Recursive_Infinity` (0.008), `T09_PDE_Navier_Stokes_Fluid` (0.004), `T10_ENS_Vorticity_Enstrophy_Dissipation` (0.003) | `nabla` (745), `eqref` (260), `equation` (558), `begin` (437), `infty` (546), `split` (219) |
| `arxiv_2208.00415v2` | `T04_PI_CIR_Geometric_Closure` (0.082), `T10_ENS_Vorticity_Enstrophy_Dissipation` (0.080), `T09_PDE_Navier_Stokes_Fluid` (0.013) | `overline` (426), `mathcal` (698), `align` (286), `varphi` (183), `eqref` (172), `nabla` (192) |

## 5. Residual Unmerged `chat` Windows After Full `irm_formal_corpus` Alignment
When we align the 20 normalized trajectory windows of `chat` against the **entire `irm_formal_corpus`** (instead of only `Comprehensive Report - IRM.md`), concept Jaccard overlap jumps significantly across almost all windows, and every mathematical physics channel receives massive working-out amplification. The table below shows which `chat` windows are now **absorbed by specific formal papers** and which conversational nuances still remain unique to `chat`:

| Window $t \in [t_a, t_b]$ | `chat` Lines | Dominant Topic | `irm_report` Jaccard | `irm_formal` Jaccard | Absorbing Formal Paper | Residual Score v2 |
|---|---|---|---|---:|---|---:|
| $[0.15, 0.20]$ | L604–L802 | `T08_ROD_Radix_Numeral_Carry` | 0.043 | **0.054** | `PM_Prompt__Amended_-_Directive_Matrix_Protocol_` | **0.1371** |
| $[0.20, 0.25]$ | L804–L1006 | `T08_ROD_Radix_Numeral_Carry` | 0.068 | **0.061** | `Axiomatic_Foundations_of_Infinitesimal_Reality_Math__The__base_n.d.e.f` | **0.1356** |
| $[0.81, 0.86]$ | L3210–L3410 | `T03_CHI_Holographic_Vector_Tensor` | 0.037 | **0.069** | `Claude_Engineering___Verification_Log` | **0.0860** |
| $[0.76, 0.81]$ | L3010–L3208 | `T03_CHI_Holographic_Vector_Tensor` | 0.041 | **0.073** | `Formal_Paper_12__The_Pre-Quotient_Continuum__Levi-Civita_Field_Embeddi` | **0.0785** |
| $[0.96, 1.00]$ | L3812–L3972 | `T01_SEQ_Recursive_Infinity` | 0.065 | **0.072** | `Axiomatic_Foundations_of_Infinitesimal_Reality_Math__The__base_n.d.e.f` | **0.0635** |
| $[0.00, 0.05]$ | L1–L201 | `T01_SEQ_Recursive_Infinity` | 0.031 | **0.054** | `Claude_Engineering___Verification_Log` | **0.0564** |
