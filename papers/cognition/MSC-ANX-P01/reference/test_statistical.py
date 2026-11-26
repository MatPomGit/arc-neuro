"""Tests for the optional statistical reference; run in its dedicated venv."""
import unittest
import copy
import math
import numpy as np
import pandas as pd
import statsmodels.api as sm
from design import manifest
from synthetic import synthetic
from statistical import analyze, fit_h1, fit_choice_gee, matrix, participant_rows


class StatisticalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = list(synthetic(2026, 80))

    def test_primary_matches_direct_hc3(self):
        frame, _ = participant_rows(self.records)
        x, _, _ = matrix(frame, ["gad5", "age_years", "sleep_hours", "depression_total",
                                  "baseline_rt_ms"], ("os_family", "browser_family", "task_order"))
        direct = sm.OLS(frame["switch_cost_ms"], x).fit(cov_type="HC3", use_t=True)
        result = fit_h1(self.records)
        self.assertAlmostEqual(result["gad5"]["estimate"], direct.params["gad5"], places=10)
        self.assertAlmostEqual(result["gad5"]["se"], direct.bse["gad5"], places=10)
        self.assertEqual(result["n"], len(frame))
        self.assertIn("os_family", result["omitted_constant"])

    def test_full_report(self):
        report = analyze(self.records)
        self.assertEqual(report["data_origin"], "synthetic")
        self.assertFalse(report["H1_without_baseline"]["baseline"])
        self.assertFalse(report["H1_without_depression"]["depression"])
        for key in ("H2_GEE_sensitivity", "H3_GEE_sensitivity"):
            effect = report[key]["gad5"]
            self.assertGreaterEqual(effect["p_holm_sensitivity"], effect["p"])
            self.assertAlmostEqual(effect["odds_ratio"], math.exp(effect["estimate"]))
            self.assertEqual(report[key]["n_trials"], 80 * 48)

    def test_provenance_duplicate_and_version(self):
        for field, value in (("data_origin", "observed"), ("stimulus_version", "0.0.0")):
            row = dict(self.records[0], **{field: value})
            with self.assertRaises(ValueError):
                participant_rows([row])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            participant_rows([self.records[0], self.records[0]])

    def test_missing_and_task_specific_eligibility(self):
        records = copy.deepcopy(self.records[:2])
        for trial in records[0]["switching"]:
            trial.update(correct=False)
        records[1]["gad7_total"] = None
        with self.assertRaisesRegex(ValueError, "no eligible"):
            participant_rows(records)
        frame, excluded = participant_rows(records, require_switch=False)
        self.assertEqual(len(frame), 1)
        self.assertEqual(excluded[records[1]["participant_id"]], "invalid_gad7")

    def test_rank_guard(self):
        frame = pd.DataFrame({"gad5": [1.,2.,3.,4.], "age": [2.,4.,6.,8.]})
        with self.assertRaisesRegex(ValueError, "rank-deficient"):
            matrix(frame, ["gad5", "age"], [])
        frame["gad5"] = 1.
        with self.assertRaisesRegex(ValueError, "constant estimand"):
            matrix(frame, ["gad5"], [])

    def test_choice_duplicate(self):
        records = copy.deepcopy(self.records)
        trial = next(t for t in records[0]["decisions"] if t["task"] == "risk")
        records[0]["decisions"].append(trial)
        with self.assertRaisesRegex(ValueError, "identity"):
            fit_choice_gee(records, "risk")


if __name__ == "__main__":
    unittest.main()
