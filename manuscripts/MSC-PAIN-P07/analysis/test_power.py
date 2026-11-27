import unittest

import numpy as np

from power import DESIGN, H1, evaluate, fit_choice, generate, wilson


class PowerTests(unittest.TestCase):
    def test_primary_contrast_is_only_cost_by_visibility(self):
        np.testing.assert_allclose(H1 @ DESIGN, [0, 0, 0, 0, 1, 0, 0, 0])

    def test_randomization_counts_and_determinism(self):
        left = generate(np.random.default_rng(19), 160, "small")
        right = generate(np.random.default_rng(19), 160, "small")
        for actual, expected in zip(left, right):
            np.testing.assert_array_equal(actual, expected)
        y, n = left
        self.assertTrue(set(n.sum(axis=1)) == {0, 24})
        self.assertTrue(np.all((y >= 0) & (y <= n)))

    def test_quadrature_agreement_and_recovery(self):
        y, n = generate(np.random.default_rng(23), 1800, "large")
        eta, cov = fit_choice(y, n)
        refined_eta, refined_cov = fit_choice(y, n, nodes=45)
        self.assertAlmostEqual(H1 @ eta, .6, delta=.2)
        self.assertAlmostEqual(H1 @ eta, H1 @ refined_eta, delta=.001)
        self.assertAlmostEqual(H1 @ cov @ H1, H1 @ refined_cov @ H1, delta=.0001)

    def test_failures_remain_in_power_denominator(self):
        result = evaluate("small", 1, 3)
        self.assertEqual(result[4], 3)
        self.assertEqual(result[5], 0.0)
        self.assertGreater(wilson(0, 300)[1], 0)


if __name__ == "__main__":
    unittest.main()
