import json
import os
import sys
import unittest

AITA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AITA_SUBDIR = os.path.join(AITA_DIR, "aita")
if AITA_SUBDIR not in sys.path:
    sys.path.insert(0, AITA_SUBDIR)

from aita_eca_matcher import (
    SignatureE,
    aggregate_multi_actor_verdict,
    aggregate_verdict,
    assess_episode_repair,
    build_eca_register_49,
    compute_mismatch_tuple,
    compute_r_net,
    compute_son_potential_vector,
    duty_gated_upsilon,
    evaluate_actor_aspect,
    match_eca_anchors,
)


class TestAitaV28Suite(unittest.TestCase):
    def test_49_eca_register_complete_metadata(self):
        reg = build_eca_register_49()
        self.assertEqual(reg["total_anchors"], 49)
        self.assertEqual(len(reg["anchors"]), 49)
        required = {
            "anchor_id", "reference_event", "S", "N", "T", "C", "R", "D",
            "F_benefit", "F_will", "Power", "Ability", "Choice_delta",
            "upsilon", "psi", "upsilon_eff",
            "functional_explanation", "boundary_condition", "contrastive_event",
        }
        for a in reg["anchors"]:
            self.assertTrue(required.issubset(a.keys()), f"Missing keys in {a.get('anchor_id')}")

    def test_11_tuple_mismatch_keeps_fb_fw_and_p_a_independent(self):
        s_a = SignatureE(S=2, N=1, T=1, C=3, R=2, D="Rejected", F_benefit="-", F_will="+")
        s_b = SignatureE(S=2, N=1, T=1, C=3, R=2, D="Rejected", F_benefit="+", F_will="+")
        # P=2.0 vs P=1.0 is 2 ordinal steps apart -> dP=2; A=1.0 vs A=0.5 is 1 step -> dA=1
        mk = compute_mismatch_tuple(s_a, s_b, ev_p=2.0, anc_p=1.0, ev_a=1.0, anc_a=0.5)
        self.assertEqual(len(mk), 11)
        self.assertEqual(mk[0], 1)  # dF_b = 1
        self.assertEqual(mk[1], 0)  # dF_w = 0
        self.assertEqual(mk[5], 2)  # dP = 2
        self.assertEqual(mk[6], 1)  # dA = 1

    def test_all_seven_verdicts_and_unknown_duty_propagation(self):
        self.assertEqual(aggregate_verdict((0.55, 0.55), (-0.85, -0.85), False)["verdict"], "NTA")
        self.assertEqual(aggregate_verdict((0.35, 0.35), (-0.80, -0.80), True)["verdict"], "YWNBTA")
        self.assertEqual(aggregate_verdict((-0.75, -0.75), (0.40, 0.40), False)["verdict"], "YTA")
        self.assertEqual(aggregate_verdict((-0.60, -0.60), (0.25, 0.25), True)["verdict"], "YWBTA")
        self.assertEqual(aggregate_verdict((-0.35, -0.35), (-0.90, -0.90), False)["verdict"], "ESH")
        self.assertEqual(aggregate_verdict((0.15, 0.15), (0.10, 0.10), False)["verdict"], "NAH")
        self.assertEqual(aggregate_verdict((0.05, 0.05), (-0.10, -0.10), False, info_branches_flip=True)["verdict"], "INFO")

        # Unknown duty propagation: u=0.0, psi=-2.0 -> D=0 gives 0.0 (NAH), D=1 gives -0.75 (YTA) -> Conditional INFO!
        du = duty_gated_upsilon(0.0, -2.0, "Unknown")
        self.assertEqual(du["duty_status"], "Unknown")
        self.assertEqual(du["u_eff_interval"], [-0.75, 0.0])
        res = aggregate_verdict(tuple(du["u_eff_interval"]), (0.30, 0.30), is_hypothetical=False)
        self.assertEqual(res["verdict"], "INFO")
        self.assertIn("Conditional", res["certainty"])

    def test_r_net_excludes_na_planes_and_reports_coverage(self):
        # 5 assessable planes (2 are None / N/A)
        res = compute_r_net([1.0, None, 0.65, 1.0, 1.35, None, 1.0])
        self.assertEqual(res["assessable_count"], 5)
        self.assertAlmostEqual(res["coverage"], 5 / 7, places=3)
        self.assertAlmostEqual(res["R_net"], (0.65 * 1.35) ** (1.0 / 5.0), places=3)
        self.assertTrue(any("[N/A - UNASSESSABLE]" in f for f in res["fault_flags"]))
        self.assertTrue(any("[OMISSION FAULT]" in f for f in res["fault_flags"]))
        self.assertTrue(any("[RIGIDITY FAULT]" in f for f in res["fault_flags"]))

    def test_strict_interpolation_and_repair_preservation(self):
        reg = build_eca_register_49()["anchors"]
        sig = SignatureE(S=2, N=1, T=1, C=3, R=2, D="Rejected", F_benefit="-", F_will="+")
        m = match_eca_anchors(sig, register=reg, ev_p=1.5, ev_a=1.0, ev_dp_choice=-0.8, top_k=3)
        self.assertEqual(m["matches"][0]["anchor_id"], "ECA_-1_+1")

        # Conflicting consent/duty should NOT linearly interpolate; returns interval
        sig_conflict = SignatureE(S=2, N=1, T=1, C=1, R=2, D="Unknown", F_benefit="-", F_will="+")
        m2 = match_eca_anchors(sig_conflict, register=reg, ev_p=1.5, ev_a=1.0, ev_dp_choice=-0.5, top_k=3)
        self.assertFalse(m2["interpolated"])
        self.assertEqual(len(m2["u_interval"]), 2)

        rep = assess_episode_repair(-1.0, "R2", "Refunded full ticket price", "Stopped pressuring sibling")
        self.assertEqual(rep["original_breach_u"], -1.0)
        self.assertTrue(rep["event_vector_preserved"])

    def test_son_potential_continuous_coords_and_multi_aspect_actors(self):
        # Fractional 18-variable forces prevent corner collapse into 0.5 / 1.0
        forces_op = {"GG": [0.7, 0.0, 0.2], "GP": [0.5, 0.0, 0.0], "LG": [0.2, 0.0, 0.3], "BP": [0.1, 0.0, 0.0]}
        son = compute_son_potential_vector(forces_op)
        self.assertTrue(son["anti_corner_collapse_ok"])
        self.assertGreater(son["u"], 0.4)
        self.assertNotIn(son["u"], (-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0))

        # Multi-aspect: OP + Primary Counterparty + Independent Mediator
        op_asp = evaluate_actor_aspect(
            "OP", "OP", forces_op,
            SignatureE(S=1, N=1, T=0, C=0, R=0, D="Rejected", F_benefit="+", F_will="+"),
        )
        other_asp = evaluate_actor_aspect(
            "Aunt", "Primary Counterparty",
            {"LE": [1.1, 0.0, 0.2], "GE": [0.4, 0.0, 0.0], "BP": [0.6, 0.0, 0.0]},
            SignatureE(S=2, N=2, T=2, C=3, R=2, D="Confirmed", F_benefit="-", F_will="+"),
        )
        child_asp = evaluate_actor_aspect(
            "Lily (9yo)", "Protected Minor",
            {"GP": [0.6, 0.0, 0.0], "LG": [0.4, 0.0, 0.1], "GG": [0.2, 0.0, 0.0]},
            SignatureE(S=0, N=1, T=0, C=0, R=0, D="Rejected", F_benefit="+", F_will="+"),
        )
        agg = aggregate_multi_actor_verdict(op_asp, [other_asp, child_asp], is_hypothetical=False)
        self.assertEqual(agg["verdict"], "NTA")
        self.assertEqual(agg["actor_count"], 3)
        self.assertEqual(child_asp["aspect_verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
