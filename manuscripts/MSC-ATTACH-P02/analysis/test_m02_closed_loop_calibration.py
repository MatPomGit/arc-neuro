"""Tests for actual M02 independent-role calibration wrapper."""
import json
from pathlib import Path
import unittest

from m02_closed_loop_calibration import paired_delta, sample_stream, calibrate, stream_seed, wilson


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

    def test_invalid_reference_size(self):
        with self.assertRaises(ValueError):
            calibrate(self.spec, [self.condition], ["p"],
                      2, 2, 3, 20, 90, 0.95)


if __name__ == "__main__":
    unittest.main()
