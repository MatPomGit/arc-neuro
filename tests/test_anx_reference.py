"""Offline contracts for the public, synthetic-only ANX prospective reference."""
import sys
import unittest
from collections import Counter
from pathlib import Path
from statistics import median

P = Path(__file__).resolve().parents[1] / "manuscripts/MSC-ANX-P01/reference"
sys.path.insert(0, str(P))
try:
    from design import manifest, category, balance_metrics, balance_violations
    from audit_design import sweep
    from power import complete_n, approximate_power, simulate
    from synthetic import synthetic, summarize
finally:
    sys.path.remove(str(P))


class AnxReferenceTests(unittest.TestCase):
    def test_reproducibility(self):
        self.assertEqual(manifest(42), manifest(42))
        self.assertNotEqual(manifest(42), manifest(43))
        with self.assertRaises(ValueError):
            manifest(-1)

    def test_counterbalancing(self):
        m = [manifest(i) for i in range(16)]
        self.assertEqual(len({(tuple(x["switching"][0]["mapping"]),
                               x["switching"][0]["rule"], tuple(x["task_order"])) for x in m}), 16)

    def test_switch_counts_and_cues(self):
        for seed in range(12):
            rows = manifest(seed)["switching"]
            self.assertEqual(len(rows), 240)
            mixed = [r for r in rows if r["mixed"]]
            self.assertEqual(Counter(r["transition"] for r in mixed),
                             {"switch": 94, "repeat": 94, "undefined": 4})
            for a, b in zip(rows, rows[1:]):
                self.assertEqual(b["correct_key"], category(b["rule"], b["stimulus"]) ^ b["mapping"][b["rule"]])
                if a["block"] == b["block"]:
                    self.assertNotEqual(a["cue"], b["cue"])
                    self.assertEqual(a["rule"] != b["rule"], b["transition"] == "switch")

    def test_seed_sweep(self):
        report = sweep(0, 2048)
        self.assertEqual(report["passed"], 2048, report["failures"][:10])
        self.assertEqual(report["ranges"]["switch.stimulus_repeat"], [12, 12])
        self.assertEqual(report["ranges"]["repeat.stimulus_repeat"], [12, 12])

    def test_balance_validator_rejects_bad_contrast(self):
        metrics = balance_metrics(manifest(42)["switching"])
        self.assertFalse(balance_violations(metrics))
        metrics["switch"]["stimulus_repeat"] = 0
        self.assertIn("switch:stimulus_repeat", balance_violations(metrics))
        metrics["switch"]["response_repeat"] = 60
        self.assertIn("switch:response_repeat", balance_violations(metrics))

    def test_decision_design(self):
        rows = manifest(9)["decisions"]
        self.assertEqual(len(rows), 96)
        self.assertEqual(set(Counter((r["task"], r["contrast"], r["level"], r["target_side"]) for r in rows).values()), {2})
        for r in rows:
            a, b = r["target_outcomes"]
            c, d = r["reference_outcomes"]
            self.assertGreaterEqual(a, 0)
            if r["task"] == "risk":
                self.assertEqual((a+b-c-d)/2, r["ev_difference"])
                self.assertEqual(((b-a)/2)**2-((d-c)/2)**2, r["variance_difference"])
            else:
                self.assertIsNone(r["target_p"])
                self.assertNotIn("ev_difference", r)
                lo, hi = r["ambiguity_bounds"]
                self.assertAlmostEqual(lo+hi, 1)
                self.assertAlmostEqual(hi-lo, r["ambiguity_width"])

    def test_summary_known_cost(self):
        rows = []
        for r in manifest(3)["switching"]:
            rows.append(dict(r, correct=True, timeout=False, focus_lost=False, technical_error=False,
                             rt_ms=700 if r["mixed"] and r["transition"]=="switch" else 600))
        q = summarize(rows)
        self.assertEqual(q["switch_cost_ms"], 100)
        self.assertEqual(q["baseline_rt_ms"], 600)
        self.assertEqual(q["accuracy"], 1)
        for r in rows:
            if r["transition"] == "switch":
                r.update(timeout=True, correct=False, rt_ms=None)
        q = summarize(rows)
        self.assertFalse(q["eligible"])
        self.assertIsNone(q["switch_cost_ms"])
        self.assertEqual(q["accuracy"], .5)

    def test_invalid_rt(self):
        rows = [dict(r, correct=True, timeout=False, focus_lost=False, technical_error=False,
                     rt_ms=100) for r in manifest(3)["switching"]]
        self.assertIsNone(summarize(rows)["accuracy"])
        self.assertIsNone(summarize(rows)["baseline_rt_ms"])

    def test_synthetic_provenance(self):
        a = list(synthetic(17, 3))
        self.assertEqual(a, list(synthetic(17, 3)))
        self.assertEqual(len({r["participant_id"] for r in a}), 3)
        for r in a:
            self.assertEqual(r["data_origin"], "synthetic")
            self.assertTrue(0 <= r["gad7_total"] <= 21)
            self.assertEqual(len(r["decisions"]), 96)
            self.assertEqual(len(r["switching"]), 240)

    def test_power(self):
        self.assertEqual([complete_n(r) for r in (.1,.15,.2)], [791,355,202])
        self.assertAlmostEqual(approximate_power(355, 0), .05)
        self.assertGreaterEqual(approximate_power(355, .15), .8)
        a = simulate(444, .15, repetitions=1000)
        self.assertEqual(a, simulate(444, .15, repetitions=1000))
        self.assertTrue(.73 < a["power"] < .87)
        self.assertTrue(345 < a["mean_complete"] < 365)
        with self.assertRaises(ValueError):
            simulate(444, .15, attrition=1)


if __name__ == "__main__":
    unittest.main()
