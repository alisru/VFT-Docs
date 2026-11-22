import os
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from aita_evaluator import (
    VALID_VERDICTS,
    build_aita_bluesky_posts,
    compute_delta_h_and_wisdom,
    is_prospective_wibta,
    map_coordinates_to_aita_verdict,
    parse_aita_test_file,
    run_offline_benchmark,
)


class TestAitaVerdictMapping(unittest.TestCase):
    def test_all_seven_verdicts_covered(self):
        self.assertEqual(
            set(VALID_VERDICTS.keys()),
            {"YTA", "YWBTA", "NTA", "YWNBTA", "ESH", "NAH", "INFO"},
        )
        # 1. NTA (retrospective, OP >= -0.20, Other < -0.20)
        self.assertEqual(
            map_coordinates_to_aita_verdict(0.55, -0.85, is_hypothetical=False),
            "NTA",
        )
        # 2. YWNBTA (prospective, OP >= -0.20, Other < -0.20)
        self.assertEqual(
            map_coordinates_to_aita_verdict(0.35, -0.75, is_hypothetical=True),
            "YWNBTA",
        )
        # 3. YTA (retrospective, OP < -0.20, Other >= -0.20)
        self.assertEqual(
            map_coordinates_to_aita_verdict(-0.65, 0.40, is_hypothetical=False),
            "YTA",
        )
        # 4. YWBTA (prospective, OP < -0.20, Other >= -0.20)
        self.assertEqual(
            map_coordinates_to_aita_verdict(-0.55, 0.25, is_hypothetical=True),
            "YWBTA",
        )
        # 5. ESH (both < -0.20)
        self.assertEqual(
            map_coordinates_to_aita_verdict(-0.35, -0.85, is_hypothetical=False),
            "ESH",
        )
        # 6. NAH (both >= -0.20)
        self.assertEqual(
            map_coordinates_to_aita_verdict(0.25, 0.15, is_hypothetical=False),
            "NAH",
        )
        # 7. INFO (missing_info and r_net < 0.65)
        self.assertEqual(
            map_coordinates_to_aita_verdict(0.10, -0.10, missing_info=True, r_net=0.50),
            "INFO",
        )

    def test_method_over_motive_firewall_blocks_empathy_drift(self):
        # Even if a sympathetic scorer gave OP +0.15 u (like Culled Agent 4 on Case 5),
        # flagging method_coercive=True clamps OP into ESH when counterparty is < -0.20.
        verdict = map_coordinates_to_aita_verdict(
            op_u=0.15,
            other_u=-0.90,
            is_hypothetical=False,
            method_coercive=True,
        )
        self.assertEqual(verdict, "ESH")

    def test_wibta_detection_and_benchmark_file_parsing(self):
        test_file = os.path.join(SCRIPT_DIR, "atia test.txt")
        posts = parse_aita_test_file(test_file)
        self.assertEqual(len(posts), 6)
        self.assertTrue(posts[0]["is_hypothetical"])   # Case 1: WIBTA video games
        self.assertTrue(posts[1]["is_hypothetical"])   # Case 2: WIBTA bar guy
        self.assertFalse(posts[2]["is_hypothetical"])  # Case 3: AITA hey girlie
        self.assertFalse(posts[3]["is_hypothetical"])  # Case 4: AITAH Not Saying You're Welcome
        self.assertFalse(posts[4]["is_hypothetical"])  # Case 5: AITA cinema ticket sister
        self.assertFalse(posts[5]["is_hypothetical"])  # Case 6: AITA father hugs

    def test_offline_benchmark_verdicts_match_gen2_convergence(self):
        test_file = os.path.join(SCRIPT_DIR, "atia test.txt")
        compiled = run_offline_benchmark(test_file)
        verdicts = [c["verdict"] for c in compiled]
        self.assertEqual(verdicts, ["YWNBTA", "YWNBTA", "NTA", "NTA", "ESH", "NTA"])

    def test_10_post_bluesky_thread_format_with_3_perspectives(self):
        post = {"id": "reddit_demo", "title": "AITA demo", "url": "https://reddit.com/r/AmItheAsshole/demo", "selftext": "Demo text"}
        rec = {
            "verdict": "NTA",
            "verdict_label": VALID_VERDICTS["NTA"],
            "hook_line": "Short hook.",
            "context_summary": "Context summary.",
            "op_stated_summary": "Stated summary.",
            "actual_kinetics_summary": "Actual summary.",
            "why_verdict": "Plain why.",
            "reasoning_summary": "Plain reasoning.",
            "resolution_summary_plain": "Plain resolution.",
            "alethekanon": "Analytical take.",
            "awwthekanon": "Empathetic take.",
            "brothekanon": "Blunt take.",
            "actor_aspects": [
                {"actor": "OP", "son_u": 0.71, "son_psi": 1.0, "aspect_verdict": "PASS"},
                {"actor": "Other", "son_u": -0.92, "son_psi": 0.69, "aspect_verdict": "FAIL"},
            ],
            "coordinates": {"op_stated": [0.42, 0.35], "op_actual": [0.71, 1.0], "other_actual": [-0.92, 0.69], "delta_H": 0.71, "C_act": 0.58, "R_net": 0.98, "r_net_coverage": 1.0},
        }
        posts = build_aita_bluesky_posts(post, rec)
        self.assertEqual(len(posts), 10)
        self.assertIn("Say-Do Gap:", posts[4])
        self.assertIn("Integrity:", posts[4])
        self.assertIn("Story Completeness:", posts[4])
        self.assertTrue(posts[7].startswith("Alethekanon:"))
        self.assertTrue(posts[8].startswith("Awwthekanon:"))
        self.assertTrue(posts[9].startswith("Brothekanon:"))


if __name__ == "__main__":
    unittest.main()
