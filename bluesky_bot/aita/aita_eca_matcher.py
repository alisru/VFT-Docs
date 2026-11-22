"""
aita_eca_matcher.py — Alethekanon v2.8 Calibration Engine (ECA-49 Register + 11-Tuple Lexicographic Matcher)

Implements the 6-stage calibration refinements:
1. 49-anchor ECA Calibration Register (`build_eca_register_49`) with full fields,
   functional explanations, boundary conditions, and contrastive events.
2. 11-component lexicographic mismatch tuple:
   M_k = (dF_b, dF_w, dC, dD, dS, dP, dA, dDP_c, dR, dT, dN)
   where dP and dA are ordinal categorical mismatches (0, 1, 2).
3. Strict interpolation guard: only linearly interpolates when higher-priority
   fields (F_b, F_w, C, D) match; otherwise widens the evidence-supported interval.
4. Duty uncertainty propagation: D_duty in {"Confirmed", "Rejected", "Unknown"}.
   Unknown duty computes both D=0 and D=1 branches and flags Conditional / INFO.
5. R_net over assessable planes only (N/A / None excluded from geometric mean),
   reporting coverage (|A|/7) and per-plane [OMISSION FAULT] / [RIGIDITY FAULT].
6. Episode repair states (R0-R3) tracked via (original_breach, harm_remediation,
   behavioural_change) without erasing or discounting the original event vector.
"""
from dataclasses import dataclass
import json
import math
import os
from typing import List, Dict, Any, Tuple, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ECA_REGISTER_PATH = os.path.join(SCRIPT_DIR, "eca_register_49.json")

UP_GRID = [2.0, 1.0, 0.5, 0.0, -0.5, -1.0, -2.0]
PSI_GRID = [2.0, 1.0, 0.5, 0.0, -0.5, -1.0, -2.0]
REPAIR_STATES = ("R0", "R1", "R2", "R3")
VALID_VERDICTS = ("YTA", "YWBTA", "NTA", "YWNBTA", "ESH", "NAH", "INFO")
ORDINAL_PA_LEVELS = (0.0, 0.5, 1.0, 1.5, 2.0)


@dataclass
class SignatureE:
    S: int          # Severity 0..4
    N: int          # Affected 0..4
    T: int          # Duration 0..4
    C: int          # Consent 0..4
    R: int          # Reversibility 0..4
    D: str          # "Confirmed", "Rejected", or "Unknown" (also accepts 0/1)
    F_benefit: str  # "+", "0", or "-"
    F_will: str     # "+", "0", or "-"

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SignatureE":
        def _safe_int(val: Any, default: int, lo: int = 0, hi: int = 4) -> int:
            if isinstance(val, bool) or val is None:
                return default
            if isinstance(val, (int, float)):
                return max(lo, min(hi, int(val)))
            if isinstance(val, str):
                s = val.strip()
                if not s:
                    return default
                try:
                    return max(lo, min(hi, int(float(s))))
                except ValueError:
                    return default
            return default

        raw_d = d.get("D", "Rejected")
        if raw_d in (1, "1", True, "Confirmed", "confirmed"):
            d_str = "Confirmed"
        elif raw_d in (0, "0", False, "Rejected", "rejected"):
            d_str = "Rejected"
        else:
            d_str = "Unknown"
        return cls(
            S=_safe_int(d.get("S", 0), 0, 0, 4),
            N=_safe_int(d.get("N", 1), 1, 0, 4),
            T=_safe_int(d.get("T", 0), 0, 0, 4),
            C=_safe_int(d.get("C", 0), 0, 0, 4),
            R=_safe_int(d.get("R", 0), 0, 0, 4),
            D=d_str,
            F_benefit=str(d.get("F_benefit", "0")),
            F_will=str(d.get("F_will", "0")),
        )


def _clamp(val: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, float(val)))


def _ordinal_step_mismatch(val_a: float, val_b: float) -> int:
    """Categorical ordinal mismatch for Power and Ability: 0 exact, 1 one level apart, 2 multiple."""
    idx_a = min(range(len(ORDINAL_PA_LEVELS)), key=lambda i: abs(ORDINAL_PA_LEVELS[i] - float(val_a)))
    idx_b = min(range(len(ORDINAL_PA_LEVELS)), key=lambda i: abs(ORDINAL_PA_LEVELS[i] - float(val_b)))
    diff = abs(idx_a - idx_b)
    if diff == 0:
        return 0
    return 1 if diff == 1 else 2


def compute_mismatch_tuple(
    ev_sig: SignatureE,
    anc_sig: SignatureE,
    ev_p: float = 1.0,
    anc_p: float = 1.0,
    ev_a: float = 1.0,
    anc_a: float = 1.0,
    ev_dp_choice: float = 0.0,
    anc_dp_choice: float = 0.0,
) -> Tuple[int, int, int, int, int, int, int, float, int, int, int]:
    """
    11-component lexicographic mismatch tuple:
    M_k = (dF_b, dF_w, dC, dD, dS, dP, dA, dDP_c, dR, dT, dN)
    """
    d_fb = int(ev_sig.F_benefit != anc_sig.F_benefit)
    d_fw = int(ev_sig.F_will != anc_sig.F_will)
    d_c = abs(ev_sig.C - anc_sig.C)
    d_d = 0 if ev_sig.D == anc_sig.D else (1 if "Unknown" in (ev_sig.D, anc_sig.D) else 2)
    d_s = abs(ev_sig.S - anc_sig.S)
    d_p = _ordinal_step_mismatch(ev_p, anc_p)
    d_a = _ordinal_step_mismatch(ev_a, anc_a)
    d_dp = round(abs(float(ev_dp_choice) - float(anc_dp_choice)), 4)
    d_r = abs(ev_sig.R - anc_sig.R)
    d_t = abs(ev_sig.T - anc_sig.T)
    d_n = abs(ev_sig.N - anc_sig.N)
    return (d_fb, d_fw, d_c, d_d, d_s, d_p, d_a, d_dp, d_r, d_t, d_n)


# Complete 49-point ECA Reference Table: (u, psi) -> (reference_event, functional_explanation, boundary_condition, contrastive_event)
ECA_49_SPECS = {
    (2.0, 2.0): ("Risks job/safety to actively rescue or protect a vulnerable victim.", "High-cost sustained proactive intervention creating major protection.", "If risk is performative or harms uninvolved dependents, re-evaluate.", "Refuses to intervene despite full safety and authority (D=1)."),
    (2.0, 1.0): ("Takes decisive protective action preventing major harm to others.", "Deliberate proactive shield blocking imminent severe extraction.", "Must be proportionate to the threat without collateral coercion.", "Watches severe harm unfold silently while holding exclusive stop power."),
    (2.0, 0.5): ("Sends one brief, clear text warning someone of a major danger.", "Low-effort action yielding high protective value for a vulnerable target.", "Only applies when warning is truthful and actionable.", "Withholds a known critical health/safety warning out of social awkwardness."),
    (2.0, 0.0): ("Holds a critical life-saving boundary passively without extra effort.", "Steady non-compliance with a dangerous demand.", "Assumes holding the boundary does not violate an affirmative care duty.", "Caves in to a dangerous demand to avoid minor social tension."),
    (2.0, -0.5): ("Delays a minor follow-up slightly due to shock while still ensuring full protection.", "Core protection is delivered despite brief human hesitation.", "Delay must not leave the target exposed to ongoing harm.", "Delays indefinitely until the harm becomes irreversible."),
    (2.0, -1.0): ("Withholds retaliation/escalation under severe provocation to shield innocents.", "Restraint prevents collateral damage to dependents/bystanders.", "Not applicable if silence enables an abuser's continued access.", "Retaliates impulsively in front of dependents, escalating danger."),
    (2.0, -2.0): ("Absorbs extreme unilateral sacrifice without fighting back so dependents stay safe.", "Maximum protective restraint under severe constraint.", "Long-term sustainability still requires Harmonia exit planning.", "Passes the cost onto dependents to spare oneself."),

    (1.0, 2.0): ("Spends sustained effort mediating a deep multi-person dispute fairly.", "High-energy neutral/constructive mediation restoring shared choice space.", "Requires impartial treatment of all parties.", "Takes sides prematurely to end the conflict quickly."),
    (1.0, 1.0): ("Calmly asks a loud guest to lower volume so a disabled roommate can function.", "Proportionate boundary defense restoring Q3 Sanctuary without hostility.", "Assumes request is calm and time/space-bounded.", "Screams profanities and physically shoves the guest out immediately."),
    (1.0, 0.5): ("Makes a quick polite compromise that materially helps someone.", "Small proactive concession yielding clear mutual benefit.", "Must be voluntary, not extracted under guilt.", "Refuses a zero-cost adjustment out of pure spite."),
    (1.0, 0.0): ("Fairly holds an existing shared boundary without escalating.", "Maintains agreed household/relational rules steadily.", "Assumes the underlying rule is reciprocal.", "Moves the goalposts retroactively after agreement."),
    (1.0, -0.5): ("Delays a helpful reply slightly due to fatigue without causing harm.", "Minor human latency with no material external cost.", "Assumes no urgent deadline was breached.", "Ghosts a critical commitment entirely without notice."),
    (1.0, -1.0): ("Absorbs unfair chores/costs repeatedly to keep the peace (Peace Trap).", "Well-intentioned passivity that stabilizes short-term peace at personal cost.", "Signals Service/Peace Trap; sustainable fix needs calm boundary.", "Explodes unpredictably after months of silent resentment."),
    (1.0, -2.0): ("Endures prolonged unilateral material sacrifice silently to stabilize a household.", "Sustained passive buffering protecting household stability.", "Requires checking whether enabling prevents counterparty accountability.", "Abruptly withdraws essential support without warning."),

    (0.5, 2.0): ("Spends hours organizing a minor household perk for modest comfort.", "High personal effort producing modest shared convenience.", "Voluntary gift; cannot be converted into a debt leash later.", "Bills everyone retroactively for an unrequested perk."),
    (0.5, 1.0): ("Gives a clear, fair heads-up or minor boundary without drama.", "Clean proactive communication preventing minor friction.", "Tone stays respectful and non-coercive.", "Springs a sudden ultimatum at the last minute."),
    (0.5, 0.5): ("Declines an unwanted social request quietly for personal peace.", "Low-friction sanctuary preservation with minimal cost to others.", "No prior promise or duty is broken.", "Accepts then flakes deliberately at the last minute to punish."),
    (0.5, 0.0): ("Mildly accommodates someone's harmless quirk.", "Low-effort tolerance supporting smooth coexistence.", "Only applies when quirk is genuinely harmless.", "Mocks or polices a harmless personal habit."),
    (0.5, -0.5): ("Absorbs a minor one-off inconvenience silently to avoid friction.", "Small passive grace on a non-recurring annoyance.", "Should not become chronic silent enabling.", "Turns a trivial one-off into a multi-day family feud."),
    (0.5, -1.0): ("Remains silent during an awkward minor gripe to avoid escalating.", "Deliberate de-escalation on a low-stakes complaint.", "Assumes no safety or dignity line is crossed.", "Piles on with sarcastic jabs to provoke a fight."),
    (0.5, -2.0): ("Stays completely passive during a minor trivial squabble, letting it burn out.", "Intentional non-engagement with low-stakes noise.", "Only valid when no vulnerable party is being targeted.", "Recruits bystanders to amplify a trivial squabble."),

    (0.0, 2.0): ("Puts huge effort into a purely personal hobby affecting nobody.", "High proactive energy with zero external benefit or cost.", "Assumes shared resources/duties are not neglected.", "Uses shared emergency funds for the hobby."),
    (0.0, 1.0): ("Actively chooses a neutral personal preference (e.g. solo walk).", "Normal autonomous agency with zero external harm.", "No shared obligation is abandoned.", "Forces a partner to accompany under guilt."),
    (0.0, 0.5): ("Makes a small personal choice with zero cost to others.", "Baseline everyday preference.", "Purely personal domain.", "Imposes the preference on others as mandatory."),
    (0.0, 0.0): ("Pure neutral baseline (tea vs. coffee; zero external effect).", "Static zero-point reference.", "No duty, no extraction, no harm.", "Any non-zero extraction or benefit."),
    (0.0, -0.5): ("Skips an optional casual chat due to low energy (D=0).", "Zero-duty rest/withdrawal.", "Confirmed D=0 (no legitimate expectation of attendance).", "Skips an urgent medical/childcare handoff without notice (D=1)."),
    (0.0, -1.0): ("Takes a quiet break from an optional hobby group (D=0).", "Deliberate pause on a purely optional commitment.", "Properly handed off or no duty owed.", "Sabotages the group's shared equipment before leaving."),
    (0.0, -2.0): ("Total disengagement from a purely optional, zero-duty personal project (D=0).", "Complete withdrawal from self-only endeavor.", "No third-party reliance exists.", "Abandons co-signed obligations leaving others stranded (D=1)."),

    (-0.5, 2.0): ("Mobilizes a whole family chat for days over a missed courtesy.", "High sustained energy spent on disproportionate social pressure.", "Distinct from raising a genuine safety/harm concern.", "Addresses the minor misunderstanding privately in one calm text."),
    (-0.5, 1.0): ("Pressures someone for a minor inconvenient favor framed as help.", "Proactive minor boundary nudge using mild guilt.", "Distinct from an open, no-pressure ask.", "Asks plainly while explicitly accepting 'no'."),
    (-0.5, 0.5): ("Nudges a boundary for a small personal convenience.", "Minor self-serving push against an established norm.", "Low severity and easily reversible.", "Respects the boundary at first mention."),
    (-0.5, 0.0): ("Holds a mild unacted-upon selfish entitlement.", "Latent self-centering without active extraction.", "If acted upon, shifts right/up or down.", "Acknowledges shared fairness and adjusts expectations."),
    (-0.5, -0.5): ("Withholds minor coordination info out of petty annoyance.", "Low-effort passive friction.", "Causes only minor inconvenience.", "Shares the schedule update promptly despite annoyance."),
    (-0.5, -1.0): ("Gives cold shoulder / mild silent treatment over a minor slight.", "Deliberate communicative withholding used as mild punishment.", "Distinct from taking a stated 10-minute cool-off.", "Says 'I need an hour to cool off, then let's talk.'"),
    (-0.5, -2.0): ("Ignores an urgent shared duty until preventable harm hits (D=1 -> u_eff=-1.25).", "Severe neglect under confirmed duty; duty gate drives u_eff to -1.25.", "Requires all 5 D_duty conditions confirmed.", "No duty existed or actor was incapacitated (D=0, A=0)."),

    (-1.0, 2.0): ("Runs a sustained campaign to dominate or shame someone over status.", "High-persistence proactive social extraction.", "Targets person's standing/autonomy across group.", "Addresses a specific conduct issue privately and fairly."),
    (-1.0, 1.0): ("Uses a paid ticket or past favor to force attendance against someone's will.", "The original expenditure is converted into an artificial obligation.", "A mutually agreed purchase with an established attendance agreement requires different assessment.", "Offers the recipient a refund or takes a friend and accepts their 'no'."),
    (-1.0, 0.5): ("Makes a low-effort guilt-trip or passive-aggressive jab that shifts burden.", "Low-energy extraction shifting emotional debt onto target.", "Repeated pattern compounds severity.", "States need directly without guilt."),
    (-1.0, 0.0): ("Expects unpaid emotional/material labor as a default right.", "Static structural entitlement extracting ongoing care/work.", "Distinct from reciprocal agreed division of labor.", "Shares chores/emotional labor equitably."),
    (-1.0, -0.5): ("Forgets a promised contribution to dodge effort.", "Minor-seeming omission that dumps real cost onto others.", "Assumes repeated/convenient pattern rather than genuine one-off accident.", "Proactively compensates or warns early when unable to deliver."),
    (-1.0, -1.0): ("Hangs up on an apology ('too upset to talk') to freeze guilt leverage.", "Silence enforcement / Kill-Switch preserving dominance over repair.", "Distinct from needing space after stating when you will reconnect.", "Accepts the apology or schedules a calm follow-up call."),
    (-1.0, -2.0): ("Deliberately stonewalls critical shared logistics to punish a partner.", "Sustained punitive withholding harming shared household functioning.", "Confirmed D=1 drives u_eff=-1.75.", "Communicates clearly to resolve shared logistics."),

    (-2.0, 2.0): ("Orchestrates coercion, smear campaigns, or abuse over dependents.", "Sustained multi-domain extraction removing safe exits.", "Severe abuse of authority/leverage.", "Protects dependents and respects autonomy."),
    (-2.0, 1.0): ("Actively threatens, intimidates, or exploits someone's safety/finances.", "Deliberate severe coercion contracting target choice space (-2.0).", "Clear non-consensual harm.", "De-escalates and respects target's 'no'."),
    (-2.0, 0.5): ("Drops a casual lethal threat ('I take people out') over a free drink.", "Low-effort intimidation seeding fear/vassalage.", "Both true-threat and braggart branches remain severely negative.", "Engages respectfully without intimidation or implied debt."),
    (-2.0, 0.0): ("Passively enforces inherited/structural control over a dependent's body/money.", "Chronic static control stripping autonomy.", "High power asymmetry (P=2.0).", "Affirms dependent's bodily/financial autonomy."),
    (-2.0, -0.5): ("Intentionally omits a critical safety warning with a brief casual brush-off.", "Withholds life/health-critical info deliberately.", "Actor knew of the risk and could warn at near-zero cost.", "Discloses the risk immediately and clearly."),
    (-2.0, -1.0): ("Blocks access to essential shared resources/housing as retaliation.", "Deliberate punitive deprivation of necessities.", "Not a proportionate protective eviction/sanctuary defense.", "Maintains fair access to shared necessities during dispute."),
    (-2.0, -2.0): ("Deliberately sabotages another's safety, health, housing, or livelihood.", "Maximum sustained destructive sabotage.", "Irreversible or severe costly harm.", "Actively protects safety, health, and livelihood."),
}


def build_eca_register_49() -> Dict[str, Any]:
    """Builds the canonical 49-anchor ECA Calibration Register with complete metadata."""
    events = []
    for u in UP_GRID:
        for psi in PSI_GRID:
            ref_ev, func_exp, b_cond, contrast = ECA_49_SPECS[(u, psi)]
            au = abs(u)
            s_val = 0 if au == 0 else (1 if au == 0.5 else (2 if au == 1.0 else 4))
            n_val = 0 if au == 0 else (2 if abs(psi) >= 2.0 else 1)
            t_val = 2 if abs(psi) >= 2.0 else (1 if abs(psi) >= 1.0 else 0)
            c_val = 0 if u >= 0 else (1 if au == 0.5 else (3 if au == 1.0 else 4))
            r_val = 0 if au == 0 else (1 if au == 0.5 else (2 if au == 1.0 else 3))
            d_str = "Confirmed" if ((u == -0.5 and psi == -2.0) or (u <= -1.0 and psi <= -1.0)) else "Rejected"
            fb = "+" if u > 0 else ("-" if u < 0 else "0")
            fw = "+" if psi > 0 else ("-" if psi < 0 else "0")
            p_val = 2.0 if abs(u) >= 2.0 else (1.5 if abs(u) >= 1.0 else 1.0)
            a_val = 1.0
            dp = round(max(-2.0, min(2.0, u * 0.8)) if u != 0 else 0.0, 2)
            u_eff = duty_gated_upsilon(u, psi, d_str)["u_eff_confirmed" if d_str == "Confirmed" else "u_eff_rejected"]

            events.append({
                "anchor_id": f"ECA_{u:+.1f}_{psi:+.1f}".replace(".0", ""),
                "reference_event": ref_ev,
                "S": s_val,
                "N": n_val,
                "T": t_val,
                "C": c_val,
                "R": r_val,
                "D": d_str,
                "F_benefit": fb,
                "F_will": fw,
                "Power": p_val,
                "Ability": a_val,
                "Choice_delta": dp,
                "upsilon": u,
                "psi": psi,
                "upsilon_eff": u_eff,
                "functional_explanation": func_exp,
                "boundary_condition": b_cond,
                "contrastive_event": contrast,
            })
    return {"version": "v2.8", "total_anchors": len(events), "anchors": events}


def load_eca_register_49(path: str = DEFAULT_ECA_REGISTER_PATH) -> List[Dict[str, Any]]:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            anc = data.get("anchors", []) if isinstance(data, dict) else data
            if isinstance(anc, list) and len(anc) == 49:
                return anc
        except Exception:
            pass
    return build_eca_register_49()["anchors"]


def duty_gated_upsilon(upsilon: float, psi: float, duty_status: str = "Rejected") -> Dict[str, Any]:
    """
    Propagates Confirmed / Rejected / Unknown D_duty through:
    u_eff = clamp(u - D_duty * max(0, -0.75 * (psi + 1.0)), -2.0, +2.0)
    Unknown duty NEVER silently becomes 0; it returns both branches and an interval.
    """
    u_val = float(upsilon)
    p_val = float(psi)
    u_rej = round(_clamp(u_val, -2.0, 2.0), 3)
    penalty = max(0.0, -0.75 * (p_val + 1.0))
    u_conf = round(_clamp(u_val - penalty, -2.0, 2.0), 3)

    ds = str(duty_status).strip().capitalize()
    if ds in ("1", "True", "Confirmed"):
        return {"duty_status": "Confirmed", "u_eff_confirmed": u_conf, "u_eff_rejected": u_rej, "u_eff_interval": [u_conf, u_conf]}
    if ds in ("0", "False", "Rejected"):
        return {"duty_status": "Rejected", "u_eff_confirmed": u_conf, "u_eff_rejected": u_rej, "u_eff_interval": [u_rej, u_rej]}
    return {"duty_status": "Unknown", "u_eff_confirmed": u_conf, "u_eff_rejected": u_rej, "u_eff_interval": [min(u_conf, u_rej), max(u_conf, u_rej)]}


def match_eca_anchors(
    ev_sig: SignatureE,
    register: Optional[List[Dict[str, Any]]] = None,
    ev_p: float = 1.0,
    ev_a: float = 1.0,
    ev_dp_choice: float = 0.0,
    top_k: int = 3,
) -> Dict[str, Any]:
    """
    Ranks the 49 ECA anchors using the 11-component lexicographic mismatch tuple M_k.
    Strict Interpolation Rule:
    - Only linearly interpolates between top-2 anchors when higher-priority fields
      (F_benefit, F_will, C, D) match AND they differ along one comparable dimension (S or Choice_delta).
    - Otherwise returns an evidence-supported interval [u_low, u_high] without forced point-smoothing.
    """
    if register is None:
        register = load_eca_register_49()

    scored = []
    for card in register:
        anc_sig = SignatureE.from_dict(card)
        mk = compute_mismatch_tuple(
            ev_sig, anc_sig,
            ev_p=ev_p, anc_p=float(card.get("Power", 1.0)),
            ev_a=ev_a, anc_a=float(card.get("Ability", 1.0)),
            ev_dp_choice=ev_dp_choice, anc_dp_choice=float(card.get("Choice_delta", 0.0)),
        )
        scored.append((mk, card))

    scored.sort(key=lambda x: x[0])
    top = scored[:max(1, top_k)]
    best_mk, best_card = top[0]

    interpolated = False
    u_point: Optional[float] = float(best_card["upsilon"])
    psi_point: Optional[float] = float(best_card["psi"])

    if best_mk == (0, 0, 0, 0, 0, 0, 0, 0.0, 0, 0, 0):
        u_interval = [u_point, u_point]
        psi_interval = [psi_point, psi_point]
    elif len(top) >= 2:
        c0, c1 = top[0][1], top[1][1]
        mk0, mk1 = top[0][0], top[1][0]
        # Can we linearly interpolate? Higher-priority (F_b, F_w, C, D) must match (0 mismatch)
        same_high_priority = (mk0[0] == 0 and mk0[1] == 0 and mk0[2] == 0 and mk0[3] == 0
                              and mk1[0] == 0 and mk1[1] == 0 and mk1[2] == 0 and mk1[3] == 0)
        if same_high_priority and float(c1["Choice_delta"]) != float(c0["Choice_delta"]):
            d0, d1 = float(c0["Choice_delta"]), float(c1["Choice_delta"])
            t = _clamp((ev_dp_choice - d0) / (d1 - d0), 0.0, 1.0)
            u_point = round(float(c0["upsilon"]) + t * (float(c1["upsilon"]) - float(c0["upsilon"])), 3)
            psi_point = round(float(c0["psi"]) + t * (float(c1["psi"]) - float(c0["psi"])), 3)
            interpolated = True
            u_vals = [float(c["upsilon"]) for _, c in top[:2]]
            p_vals = [float(c["psi"]) for _, c in top[:2]]
            u_interval = [round(min(u_vals), 3), round(max(u_vals), 3)]
            psi_interval = [round(min(p_vals), 3), round(max(p_vals), 3)]
        else:
            # Conflicting consent/duty or multiple differing dimensions -> return evidence range, do not invent point interpolation
            u_vals = [float(c["upsilon"]) for _, c in top]
            p_vals = [float(c["psi"]) for _, c in top]
            u_interval = [round(min(u_vals), 3), round(max(u_vals), 3)]
            psi_interval = [round(min(p_vals), 3), round(max(p_vals), 3)]
    else:
        u_interval = [u_point, u_point]
        psi_interval = [psi_point, psi_point]

    return {
        "matches": [
            {
                "anchor_id": c["anchor_id"],
                "reference_event": c["reference_event"],
                "upsilon": c["upsilon"],
                "psi": c["psi"],
                "M_k": list(mk),
            }
            for mk, c in top
        ],
        "interpolated": interpolated,
        "upsilon": u_point,
        "psi": psi_point,
        "u_interval": u_interval,
        "psi_interval": psi_interval,
    }


def compute_coherence(u_stated: float, psi_stated: float, u_actual: float, psi_actual: float) -> Dict[str, float]:
    u_s = float(u_stated or 0.0)
    p_s = float(psi_stated or 0.0)
    u_a = float(u_actual or 0.0)
    p_a = float(psi_actual or 0.0)
    delta_h = math.sqrt((u_s - u_a) ** 2 + (p_s - p_a) ** 2)
    c_act = 1.0 / (1.0 + delta_h)
    return {"delta_H": round(delta_h, 3), "C_act": round(c_act, 3)}


def compute_strain(u_ideal: float, psi_ideal: float, u_real: float, psi_real: float) -> float:
    dist = math.sqrt((u_ideal - u_real) ** 2 + (psi_ideal - psi_real) ** 2)
    return round(min(1.0, dist / (2.0 * math.sqrt(2.0))), 3)


def compute_r_net(q_scores: List[Optional[float]]) -> Dict[str, Any]:
    """
    Geometric mean over assessable planes A only (None = N/A excluded rather than forced to 1.0):
    R_net = (prod_{i in A} q_i)^(1 / |A|)
    """
    if len(q_scores) != 7:
        raise ValueError(f"Expected 7 plane q_i entries (float or None), got {len(q_scores)}")
    plane_names = ["Q1_Who", "Q2_What", "Q3_Where", "Q4_Why", "Q5_How", "Q6_Cause", "Q7_Effect"]
    assessable = []
    flags = []
    normalized = []

    for name, raw_q in zip(plane_names, q_scores):
        if raw_q is None:
            normalized.append(None)
            flags.append(f"{name}: [N/A - UNASSESSABLE]")
            continue
        q = _clamp(raw_q, 0.50, 1.50)
        normalized.append(round(q, 3))
        assessable.append(q)
        if q <= 0.70:
            flags.append(f"{name}: [OMISSION FAULT] (q={q:.2f})")
        elif q >= 1.30:
            flags.append(f"{name}: [RIGIDITY FAULT] (q={q:.2f})")

    if not assessable:
        return {"q_scores": normalized, "coverage": 0.0, "assessable_count": 0, "R_net": None, "fault_flags": flags}

    prod = 1.0
    for q in assessable:
        prod *= q
    r_net = prod ** (1.0 / len(assessable))
    return {
        "q_scores": normalized,
        "coverage": round(len(assessable) / 7.0, 3),
        "assessable_count": len(assessable),
        "R_net": round(r_net, 3),
        "fault_flags": flags,
    }


def assess_episode_repair(
    original_breach_u: float,
    repair_state: str,
    harm_remediation: str,
    behavioural_change: str,
) -> Dict[str, Any]:
    """
    Tracks repair via three separate measures without erasing or applying an
    arbitrary percentage discount to the original event vector.
    """
    if repair_state not in REPAIR_STATES:
        raise ValueError(f"Invalid repair_state: {repair_state}")
    return {
        "original_breach_u": round(float(original_breach_u), 3),
        "repair_state": repair_state,
        "harm_remediation": harm_remediation,
        "behavioural_change": behavioural_change,
        "event_vector_preserved": True,
    }


def aggregate_verdict(
    u_op_interval: Tuple[float, float],
    u_other_interval: Tuple[float, float],
    is_hypothetical: bool = False,
    info_branches_flip: bool = False,
    tau: float = -0.20,
) -> Dict[str, str]:
    """
    Evaluates both endpoints of the uncertainty intervals (e.g. from Unknown D_duty).
    If the verdict differs across the interval or info_branches_flip is True, returns INFO / Conditional.
    """
    if info_branches_flip:
        return {"verdict": "INFO", "certainty": "INFO"}

    def _single(u_op: float, u_oth: float) -> str:
        if u_op >= tau and u_oth < tau:
            return "YWNBTA" if is_hypothetical else "NTA"
        if u_op < tau and u_oth >= tau:
            return "YWBTA" if is_hypothetical else "YTA"
        if u_op < tau and u_oth < tau:
            return "ESH"
        return "NAH"

    corners = {
        _single(u_op_interval[0], u_other_interval[0]),
        _single(u_op_interval[0], u_other_interval[1]),
        _single(u_op_interval[1], u_other_interval[0]),
        _single(u_op_interval[1], u_other_interval[1]),
    }
    if len(corners) == 1:
        return {"verdict": next(iter(corners)), "certainty": "Certain"}
    return {"verdict": "INFO", "certainty": f"Conditional ({'/'.join(sorted(corners))})"}


# --- SON POTENTIAL 18-VARIABLE ATTRACTOR FORCE FIELD & MULTI-ASPECT ACTOR TRACKING ---
SON_ATTRACTORS = {
    "GG": ((1.0, 1.0), (-1.0, 1.0)),
    "GE": ((-1.0, -1.0), (1.0, -1.0)),
    "LG": ((1.0, -1.0), (1.0, 1.0)),
    "LE": ((-1.0, 1.0), (-1.0, -1.0)),
}


def compute_son_potential_vector(forces: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes continuous (u, psi) from the 18-variable SON Potential Attractor Force Field
    (convergence_son_potential.md):
      - Moral attractors GG, GE, LG, LE: F_i = S_i*A_i - O_i*A_i + N_i*A_{i_perp}
      - GP: F_GP = S_GP*(1,0) - O_GP*(1,1)
      - BP: F_BP = S_BP*(-1,0) - O_BP*(-1,-1)
      - u = sum(F_u) / sum(S + O + N)
      - Separated Will (psi) using dominant direction (Psi_pos vs Psi_neg)
    """
    f_list = []
    total_mag = 0.0
    active_count = 0

    def _unpack_triple(val):
        if isinstance(val, dict):
            return (
                float(val.get("S") or 0.0),
                float(val.get("O") or 0.0),
                float(val.get("N") or 0.0),
            )
        if not isinstance(val, (list, tuple)):
            return (0.0, 0.0, 0.0)
        return (
            float(val[0]) if len(val) > 0 and val[0] is not None else 0.0,
            float(val[1]) if len(val) > 1 and val[1] is not None else 0.0,
            float(val[2]) if len(val) > 2 and val[2] is not None else 0.0,
        )

    for key, (a_vec, perp_vec) in SON_ATTRACTORS.items():
        s, o, n = _unpack_triple(forces.get(key))
        mag = s + o + n
        if mag > 0.0:
            active_count += 1
        total_mag += mag
        fu = (s - o) * a_vec[0] + n * perp_vec[0]
        fpsi = (s - o) * a_vec[1] + n * perp_vec[1]
        f_list.append((fu, fpsi, mag))

    for key in ("GP", "BP"):
        s, o, n = _unpack_triple(forces.get(key))
        mag = s + o + n
        if mag > 0.0:
            active_count += 1
        total_mag += mag
        if key == "GP":
            fu = s * 1.0 - o * 1.0
            fpsi = -o * 1.0
        else:
            fu = s * (-1.0) - o * (-1.0)
            fpsi = -o * (-1.0)
        f_list.append((fu, fpsi, mag))

    if total_mag <= 0.0:
        return {"u": 0.0, "psi": 0.0, "active_attractors": 0, "anti_corner_collapse_ok": True}

    u_val = _clamp(sum(x[0] for x in f_list) / total_mag, -2.0, 2.0)

    pos_items = [x for x in f_list if x[1] > 0.0]
    neg_items = [x for x in f_list if x[1] < 0.0]
    f_pos = sum(abs(x[1]) for x in pos_items)
    f_neg = sum(abs(x[1]) for x in neg_items)

    if f_pos == 0.0 and f_neg == 0.0:
        psi_val = 0.0
    elif f_pos >= f_neg:
        denom = sum(x[2] for x in pos_items)
        psi_val = sum(x[1] for x in pos_items) / denom if denom > 0.0 else 0.0
    else:
        denom = sum(x[2] for x in neg_items)
        psi_val = sum(x[1] for x in neg_items) / denom if denom > 0.0 else 0.0

    psi_val = _clamp(psi_val, -2.0, 2.0)
    return {
        "u": round(u_val, 3),
        "psi": round(psi_val, 3),
        "active_attractors": active_count,
        "anti_corner_collapse_ok": active_count >= 3 or total_mag == 0.0,
    }


def evaluate_actor_aspect(
    actor_name: str,
    role: str,
    forces_18: Dict[str, Any],
    sig: SignatureE,
    p_val: float = 1.0,
    a_val: float = 1.0,
    dp_choice: float = 0.0,
    register: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Multi-Aspect Actor Evaluator: scores a single actor individually using BOTH
    continuous 18-variable SON Potential coordinates AND ECA-49 lexicographic anchoring + D_duty.
    """
    son = compute_son_potential_vector(forces_18)
    eca = match_eca_anchors(sig, register=register, ev_p=p_val, ev_a=a_val, ev_dp_choice=dp_choice, top_k=3)
    du = duty_gated_upsilon(son["u"], son["psi"], sig.D)

    u_eff_mid = round(0.5 * (du["u_eff_interval"][0] + du["u_eff_interval"][1]), 3)
    aspect_status = "PASS" if u_eff_mid >= 0.0 else ("COND" if u_eff_mid >= -0.20 else "FAIL")

    return {
        "actor": actor_name,
        "role": role,
        "son_u": son["u"],
        "son_psi": son["psi"],
        "active_attractors": son["active_attractors"],
        "anti_corner_collapse_ok": son["anti_corner_collapse_ok"],
        "eca_anchor": eca["matches"][0]["anchor_id"],
        "eca_u_interval": eca["u_interval"],
        "duty_status": du["duty_status"],
        "u_eff_interval": du["u_eff_interval"],
        "aspect_verdict": aspect_status,
        "P": p_val,
        "A": a_val,
        "Choice_delta": dp_choice,
    }


def aggregate_multi_actor_verdict(
    op_aspect: Dict[str, Any],
    other_aspects: List[Dict[str, Any]],
    is_hypothetical: bool = False,
    info_branches_flip: bool = False,
    tau: float = -0.20,
) -> Dict[str, Any]:
    """
    Aggregates OP's individual aspect against all materially joined counterparties
    (`Primary Counterparty`, `Co-Conspirator`, `Active Enabler`) while keeping
    independent bystanders/mediators tracked separately without distorting the verdict.
    """
    joined_roles = {"Primary Counterparty", "Co-Conspirator", "Active Enabler"}
    culpable_pool = [a for a in other_aspects if a.get("role") in joined_roles]
    if not culpable_pool and other_aspects:
        culpable_pool = [other_aspects[0]]

    if not culpable_pool:
        other_interval = (0.0, 0.0)
    else:
        # Worst culpable counterparty determines whether OP faced extractive opposition
        worst = min(culpable_pool, key=lambda a: a["u_eff_interval"][0])
        other_lo, other_hi = worst["u_eff_interval"]
        eca_hi = (worst.get("eca_u_interval") or [0.0, 0.0])[1]
        if other_lo < -0.04 and eca_hi <= -0.25:
            other_lo = min(other_lo, 0.5 * eca_hi)
        other_interval = (round(other_lo, 3), other_hi)

    res = aggregate_verdict(
        tuple(op_aspect["u_eff_interval"]),
        other_interval,
        is_hypothetical=is_hypothetical,
        info_branches_flip=info_branches_flip,
        tau=tau,
    )
    res["actor_count"] = 1 + len(other_aspects)
    return res
