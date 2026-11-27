"""Unit tests for distribution-only coverage calibration."""
import unittest
import numpy as np
from m02_interval_calibration import calibrate, intervals, draw


class TestCalibration(unittest.TestCase):
    def test_reproducible_seed(self):
        self.assertEqual(
            calibrate(seed=17, trials=20, n_values=(10,), bootstraps=20),
            calibrate(seed=17, trials=20, n_values=(10,), bootstraps=20),
        )

    def test_intervals(self):
        x = np.random.default_rng(1).normal(size=35)
        ci = intervals(x, .95, 100, np.random.default_rng(2))
        self.assertEqual(set(ci), {"normal", "percentile", "studentized"})
        for low, high in ci.values():
            self.assertLessEqual(low, high)

    def test_scenario_shape(self):
        self.assertEqual(
            draw(np.random.default_rng(1), "skewed", 3, 20).shape, (3, 20)
        )

    def test_invalid_config(self):
        with self.assertRaises(ValueError):
            calibrate(trials=1)


if __name__ == "__main__":
    unittest.main()
