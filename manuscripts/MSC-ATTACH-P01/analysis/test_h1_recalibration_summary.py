"""Tests for H1 comparable-lag recalibration selection."""

import unittest

import pandas as pd

from h1_recalibration_summary import summarize


class H1RecalibrationSummaryTests(unittest.TestCase):
    def test_selects_smallest_candidate_passing_all_guardrails(self) -> None:
        rows = []
        for n in (72, 84, 96):
            for missingness in (0.0, 1.0):
                for truth in ("M0", "M1", "M2", "M3", "M4"):
                    suff = 0.98 if n == 72 and missingness == 1.0 else 1.0
                    p1 = 0.02 if truth == "M0" else (0.95 if truth == "M2" else 0.10)
                    p2 = 0.03 if truth == "M0" else (0.94 if truth == "M3" else 0.10)
                    rows.append({
                        "couples": n,
                        "compliance_target": 0.75,
                        "missingness_strength": missingness,
                        "truth": truth,
                        "replications": 1000,
                        "primary_data_sufficient_rate": suff,
                        "H1_P1_supported_rate": p1,
                        "H1_P2_supported_rate": p2,
                    })
        config = {
            "candidate_couples": [72, 84, 96],
            "recalibration_guardrails": {
                "minimum_primary_data_sufficiency_rate": 0.99,
                "minimum_H1_P1_power_under_M2": 0.90,
                "minimum_H1_P2_power_under_M3": 0.90,
                "maximum_H1_P1_false_positive_rate_under_M0": 0.075,
                "maximum_H1_P2_false_positive_rate_under_M0": 0.075,
            },
        }
        table, decision = summarize(pd.DataFrame(rows), config)
        self.assertFalse(bool(table.iloc[0]["passes_all_guardrails"]))
        self.assertTrue(bool(table.iloc[1]["passes_all_guardrails"]))
        self.assertEqual(decision["selected_analysis_target_couples"], 84)
        self.assertGreater(
            float(table.iloc[1]["stress_min_data_sufficiency_wilson_low"]),
            0.99,
        )


if __name__ == "__main__":
    unittest.main()
