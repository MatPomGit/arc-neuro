import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
import power_simulation as ps


class PowerSimulationTests(unittest.TestCase):
    def test_reproducibility(self):
        args = (12, 24, -1.4, .4, .5, .3, .75, .1)
        a = ps.simulate_trials(np.random.default_rng(42), *args)
        b = ps.simulate_trials(np.random.default_rng(42), *args)
        pd.testing.assert_frame_equal(a, b)

    def test_balanced_eligible_trials(self):
        d = ps.simulate_trials(np.random.default_rng(42),
                               12, 24, -1.4, 0, .5, .3, 1, 0)
        self.assertEqual(len(d), 144)
        self.assertTrue((d.groupby(["person", "tone"]).size() == 6).all())
        self.assertTrue(d.y.isin([0, 1]).all())

    def test_degenerate_fit(self):
        self.assertIsNone(ps.fit_trial(pd.DataFrame(
            dict(person=[0, 1], task=[0, 1], tone=[0, 0], y=[0, 1]))))

    def test_failure_accounting(self):
        with patch.object(ps, "fit_trial", side_effect=[None, (0., 1.), (3., 1.)]):
            out = ps.scenario(8, 8, 0, .5, .3, .75, 0, 3, 42)
        self.assertEqual(out["failed"], 1)
        self.assertEqual(out["rejected"], 1)
        self.assertAlmostEqual(out["coverage"], .5)
        self.assertAlmostEqual(out["rejection_rate"], 1/3)
        self.assertAlmostEqual(out["conditional_rate"], .5)

    def test_all_failed(self):
        with patch.object(ps, "fit_trial", return_value=None):
            out = ps.scenario(8, 8, 0, .5, .3, .75, 0, 2, 42)
        self.assertEqual(out["failure_rate"], 1)
        self.assertIsNone(out["coverage"])
        self.assertIsNone(out["conditional_rate"])

    def test_rng_restored(self):
        state = np.random.get_state()
        with patch.object(ps, "fit_trial", return_value=(0., 1.)):
            ps.scenario(8, 8, 0, .5, .3, .75, 0, 2, 42)
        after = np.random.get_state()
        self.assertEqual(state[0], after[0])
        np.testing.assert_array_equal(state[1], after[1])
        self.assertEqual(state[2:], after[2:])


if __name__ == "__main__":
    unittest.main()
