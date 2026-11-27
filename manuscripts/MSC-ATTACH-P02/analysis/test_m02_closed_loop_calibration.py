"""Tests for actual M02 independent-role calibration wrapper."""
import json
from pathlib import Path
import unittest

from m02_closed_loop_calibration import paired_delta, sample_stream, calibrate


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

    def test_invalid_reference_size(self):
        with self.assertRaises(ValueError):
            calibrate(self.spec, [self.condition], ["p"],
                      2, 2, 3, 20, 90, 0.95)


if __name__ == "__main__":
    unittest.main()
