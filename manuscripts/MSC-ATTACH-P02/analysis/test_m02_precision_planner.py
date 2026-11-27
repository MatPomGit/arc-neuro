"""Pure standard-library tests for prospective M02 precision planning."""
import unittest
from m02_precision_planner import plan, required_attempts, wilson_half_width


class PrecisionPlannerTests(unittest.TestCase):
    def test_minimum_is_verified(self):
        for comparisons in (1, 8, 512):
            n = required_attempts(0.025, 0.95, comparisons)
            confidence = 1 - 0.05 / comparisons
            self.assertLessEqual(wilson_half_width(n, 0.5, confidence), 0.025)
            self.assertGreater(wilson_half_width(n - 1, 0.5, confidence), 0.025)

    def test_multiplicity_needs_more_attempts(self):
        self.assertGreater(required_attempts(0.025, 0.95, 512),
                           required_attempts(0.025, 0.95, 1))

    def test_triad_and_cell_accounting(self):
        p = plan(0.025, 0.95, 1, 8, 64, 3, 0.75)
        self.assertEqual(p["total_generated_trajectories"],
                         3 * p["total_attempted_triads"])
        self.assertEqual(p["cells"], 512)
        self.assertEqual(p["status"], "planning_only_not_preregistered")

    def test_rejects_invalid_inputs(self):
        for args in [(0, 0.95, 1), (0.025, 1.0, 1),
                     (0.025, 0.95, 0)]:
            with self.assertRaises(ValueError):
                required_attempts(*args)
        with self.assertRaises(ValueError):
            plan(0.025, 0.95, 1, 8, 64, 3, 0)


if __name__ == "__main__":
    unittest.main()
