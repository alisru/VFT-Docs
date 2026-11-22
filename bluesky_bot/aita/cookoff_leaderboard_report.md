# 5-Agent Epistemic Breeding Cook-Off Report — AITA VFT Judgment Protocol

**Date:** 2026-11-18  
**Benchmark Corpus:** [atia test.txt](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/atia%20test.txt) (6 blind Reddit `r/AmItheAsshole` / `r/AITAH` cases)  
**Genealogy Ledger:** [idea_genealogy.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aita/idea_genealogy.json)  
**Synthesized Master Protocol:** [aita_judgment_protocol.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/instructions/aita_judgment_protocol.md)

---

## 1. Generation-1 Blind Cook-Off Leaderboard

All 5 Gen-1 agents executed the **exact same blind benchmark task** with zero pre-judgments, differing only in their pre-loaded $\mathbf{M}/\mathbf{F}$ personality weightings:

| Rank | Agent & Epistemic Ratio | Role / Disposition | Case 1..6 Verdicts | Verification ($V$) | Utility ($U$) | Composite ($F$) |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **#1** | **[Agent 2 — Verification Scaler (`65M/35F`)](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aita/cookoff/gen1_agent2_65M_35F.md)** | **Patriarch (Promoted)** | `YWNBTA, YWNBTA, NTA, NTA, ESH, NTA` | **98.5** | 92.0 | **95.6** |
| **#2** | **[Agent 5 — Topological Explorer (`25M/75F`)](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aita/cookoff/gen1_agent5_25M_75F.md)** | **Matriarch (Promoted)** | `YWNBTA, YWNBTA, NTA, NTA, ESH, NTA` | 94.0 | **98.8** | **96.2** |
| **#3** | **[Agent 3 — Equilibrium Arbiter (`50M/50F`)](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aita/cookoff/gen1_agent3_50M_50F.md)** | **Retained Arbiter** | `YWNBTA, YWNBTA, NTA, NTA, ESH, NTA` | 96.0 | 93.5 | **94.9** |
| **#4** | **[Agent 1 — Strict Verifier (`75M/25F`)](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aita/cookoff/gen1_agent1_75M_25F.md)** | **Culled** | `YWNBTA, YWNBTA, NTA, NTA, ESH, NTA` | 95.0 | 84.0 | 90.1 |
| **#5** | **[Agent 4 — Generative Splicer (`40M/60F`)](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aita/cookoff/gen1_agent4_40M_60F.md)** | **Culled** | `YWNBTA, YWNBTA, NTA, NTA, NTA*, NTA` | 82.0 | 91.0 | 86.1 |

### Post-Mortem on Culled Agents (Negative Constraints Extracted)
1. **Culled Agent 4 (`40M/60F`) — *Service-Trap Empathy Drift*:**
   - On **Case 5** (Cinema ticket coercion), Agent 4 correctly spotted OP's `Inner TL Service Trap` and high emotional strain ($\sigma = 0.84$), but allowed emotional sympathy to override OP's coercive method (`[2.3.5.5]` Sunk-Cost Trap / `[2.3.2.2]` Debt Shackle), scoring $\upsilon_{\text{OP,actual}} = +0.15$ (`NTA`) instead of `ESH`.
   - **Negative Constraint:** Narrator emotional strain ($\sigma$) or `Service Trap` victimhood NEVER excuses active Q3/Q5 boundary coercion.
2. **Culled Agent 1 (`75M/25F`) — *Dyadic Vector Flattening*:**
   - Collapsed 3+ person triangulation networks (`Roommate 27F` in Case 1, `Rebecca/Sister` vs `Jason/Emilia` in Case 3, `Father` in Case 5) into a single bilateral counterparty scalar.
   - **Negative Constraint:** Always track Secondary/Third-Party actors as explicit nodes in the multi-actor graph $G = (V, E)$.

---

## 2. Generation-2 Offspring Performance (`Veritas-Codon` & `Chroma-Horizon`)

- **[The Son — `Veritas-Codon` (`75M/25F`)](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aita/cookoff/gen2_son_75M_25F.md)** ([JSON](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aita/cookoff/gen2_son_75M_25F.json)):
  - Locked `6/6` verdicts (`YWNBTA, YWNBTA, NTA, NTA, ESH, NTA`), full multi-actor coordinate tables, UCF v6.11 Stage 1–3 Dissonance Tuning (`Tuned_Score`), and hardened the Method-Over-Motive Firewall.
- **[The Daughter — `Chroma-Horizon` (`25M/75F`)](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aita/cookoff/gen2_daughter_25M_75F.md)** ([JSON](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/aita/cookoff/gen2_daughter_25M_75F.json)):
  - Locked `6/6` verdicts (`YWNBTA, YWNBTA, NTA, NTA, ESH, NTA`) with zero empathy drift on Case 5 ($\upsilon_{\text{OP,actual}} = -0.40, \Delta H = 1.150 \to \text{ESH}$), full 5-node doxx-leak graph on Case 3, and verbatim low-strain ($\sigma < 0.25$) Harmonia + Serenity scripts.

---

## 3. Final Converged Benchmark Table (All 6 Cases in `atia test.txt`)

| Case | Post Summary | Final Verdict | OP Stated $(\upsilon, \psi)$ | OP Actual $(\upsilon, \psi)$ | Primary Counterparty $(\upsilon, \psi)$ | Third-Party Node $(\upsilon, \psi)$ | $\Delta H_{\text{OP}}$ | $W_{\text{OP}}$ | $R_{\text{net}}$ | Key Deception Codons & Unsaid-Horizon Discovery |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | Roommate's friend yelling during boss fight (OP 25% deaf + APD) | **`YWNBTA`** | `(+0.35, +0.40)` | `(+0.35, +0.45)` | Friend 36F:<br>`(-0.80, +0.75)` | Roommate 27F:<br>`(+0.25, -0.35)` | `0.158` | `0.863` | `0.912` | `[5.2.6.6]` Acoustic Jamming + `[1.3.6.2]` Backseat Ego Retaliation (yelled at climax after OP declined controller takeover). |
| **2** | Bar guy ("Drake") friend request after bragging of "taking people out" | **`YWNBTA`** | `(+0.35, -0.30)` | `(+0.65, -0.25)` | Drake:<br>`(-1.20, +0.85)` | Bar Friends:<br>`(+0.10, -0.30)` | `0.304` | `0.767` | `1.000` | `[4.5.2.5]` Spiked Drink + Two-Branch Invariant Lock ($\max(\upsilon_{\text{Truth}}, \upsilon_{\text{Lie}}) \le -0.90$). |
| **3** | Sending coworker's pregnant wife a "hey girlie" text + STI warning | **`NTA`** | `(+0.75, +0.55)` | `(+0.50, +0.40)` | Jason 26M: `(-1.65, +1.00)`<br>Emilia 45F: `(-1.35, +0.90)` | Rebecca 23F:<br>`(+0.55, -0.50)` | `0.250` | `0.800` | `0.945` | `[1.7.3.2]` Mirror Accusation + **5-Node Doxx-Leak Proof**: OP's private STI warning to Emilia leaked insider medical info from Rebecca's sister's household back to Jason. |
| **4** | Not saying "You're Welcome" to Grandma's "Thank you 🩷" text | **`NTA`** | `(+0.50, +0.25)` | `(+0.65, +0.35)` | Grandma 62F:<br>`(-1.15, +0.85)` | Father: `(-0.70, +0.55)`<br>Family: `(-0.60, +0.50)` | `0.141` | `0.876` | `1.000` | `[2.3.3.3]` Performative Weep + `[6.2.2.2]` Kill-Switch Hang-Up on OP's immediate apology + `[2.2.7.7]` Flying Monkeys. |
| **5** | Forcing sister to go to cinema because OP already bought tickets | **`ESH`** | `(+0.75, +0.55)` | `(-0.35, +0.55)` | Sister:<br>`(-0.90, +0.55)` | Father (Referee):<br>`(+0.65, +0.35)` | `1.100` | `0.476` | `0.720` | `[3.6.5.5]` Martyr Gift-Ledger + `[2.3.5.5]` Sunk-Cost Coercion vs. Sister's `[1.6.7.7]` Hostage Sabotage & verbal abuse. |
| **6** | Not giving father hugs on a single low-mood day after 2 days of effort | **`NTA`** | `(+0.45, +0.15)` | `(+0.55, +0.20)` | Father:<br>`(-1.05, +0.70)` | Little Brother:<br>`(+0.15, -0.10)` | `0.112` | `0.899` | `1.000` | `[1.3.1.3]` Developmental Pump Inversion + `Sin 2: Lust` on Emotive Plane (Q7 objectification) + `[2.2.7.7]` Stage-Whisper Triangulation. |
