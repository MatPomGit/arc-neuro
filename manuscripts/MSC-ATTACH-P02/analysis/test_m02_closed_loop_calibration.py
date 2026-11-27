"""Tests for actual M02 independent-role calibration wrapper."""
import json
from pathlib import Path
import unittest

from m02_closed_loop_calibration import paired_delta, sample_stream, calibrate, stream_seed, wilson, equivalence_diagnostics


class ClosedLoopCalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(
            (Path(__file__).parent / "configs/m02_robustness_development.json").read_text()
        )
        cls.condition = cls.spec["conditions"][0]

    def test_repeatable_paired_difference(self):
        a = paired_delta({**self.spec, "seed": 90001000},
                         self.condition, "p", 0)
        b = paired_delta({**self.spec, "seed": 90001000},
                         self.condition, "p", 0)
        self.assertEqual(a, b)

    def test_stream_accounting(self):
        values, failed = sample_stream(
            self.spec, self.condition, "p", 90001000, 3
        )
        self.assertEqual(len(values) + failed, 3)

    def test_micro_pilot_reports_reference_uncertainty(self):
        rows = calibrate(
            self.spec, [self.condition], ["p"],
            reference_n=3, trials=2, sample_n=3,
            bootstraps=20, seed=91001000, coverage=0.95
        )
        self.assertEqual(len(rows), 3)
        self.assertIn("reference_mc_se", rows[0])
        self.assertEqual(rows[0]["status"],
                         "exploratory_closed_loop_method_calibration")

    def test_seed_blocks_disjoint_at_large_trial_count(self):
        trials = 2000
        starts = [stream_seed(260810000, cell, trial, trials)
                  for cell in range(6) for trial in range(trials + 1)]
        self.assertEqual(len(set(starts)), len(starts))
        self.assertTrue(all(b-a >= 10_000_000
                            for a,b in zip(starts, starts[1:])))

    def test_wilson_and_failure_accounting(self):
        self.assertEqual(wilson(0, 0), (None, None))
        low, high = wilson(19, 20)
        self.assertLess(low, 0.95)
        self.assertGreater(high, 0.95)
        rows = calibrate(self.spec, [self.condition], ["p"],
                         4, 3, 4, 20, 91001000, 0.95)
        for row in rows:
            self.assertEqual(row["valid_intervals"] +
                             row["invalid_or_insufficient_trials"], 3)
            if row["valid_intervals"]:
                self.assertLessEqual(row["fraction_containing_reference_band"],
                                     row["coverage_against_estimated_reference"])
                self.assertLessEqual(row["coverage_against_estimated_reference"],
                                     row["fraction_overlapping_reference_band"])

    def test_equivalence_classification_is_conservative(self):
        outside = equivalence_diagnostics(1, 4, 5, 0.006, 0.009, 0.005)
        self.assertEqual(outside["reference_band_class"], "outside")
        self.assertEqual(outside["apparent_false_equivalence_fraction_valid"], 0.25)
        self.assertEqual(outside["equivalence_fraction_attempted"], 0.2)
        ambiguous = equivalence_diagnostics(1, 4, 5, 0.004, 0.006, 0.005)
        self.assertIsNone(ambiguous["apparent_false_equivalence_fraction_valid"])
        self.assertIsNone(ambiguous["apparent_equivalence_detection_fraction_valid"])
        inside = equivalence_diagnostics(2, 4, 5, -0.003, 0.004, 0.005)
        self.assertEqual(inside["apparent_equivalence_detection_fraction_valid"], 0.5)

    def test_bounded_multicell_calibration_pilot(self):
        # Actual simulator; small CI smoke only, not a coverage assessment.
        conditions = [c for c in self.spec["conditions"]
                      if c["id"] in ("reference", "heavy_tail")]
        rows = calibrate(self.spec, conditions, ["p", "pid"],
                         12, 4, 6, 39, 731001000, 0.95)
        self.assertEqual(len(rows), 12)
        for row in rows:
            diagnostic = json.loads(row["equivalence_diagnostics_json"])
            self.assertEqual(len(diagnostic), len(self.spec["epsilon_grid"]))
            self.assertEqual(row["reference_n"] + row["reference_failures"], 12)
            for item in diagnostic:
                self.assertLessEqual(item["equivalence_declarations"], row["valid_intervals"])
            self.assertEqual(sorted(x["equivalence_declarations"] for x in diagnostic),
                             [x["equivalence_declarations"] for x in diagnostic])
        print("M02_CALIBRATION_SMOKE " + json.dumps(rows, allow_nan=False))

    def test_invalid_reference_size(self):
        with self.assertRaises(ValueError):
            calibrate(self.spec, [self.condition], ["p"],
                      2, 2, 3, 20, 90, 0.95)


if __name__ == "__main__":
    unittest.main()
