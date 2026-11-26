import unittest
import numpy as np
from marginal_rd import estimate_rd


class MarginalRDTests(unittest.TestCase):
    def setUp(self):
        self.p = np.repeat(np.arange(4), 4)
        self.a = np.tile([0, 0, 1, 1], 4)
        self.y = np.array([0,0,1,1, 0,1,1,1, 0,0,0,1, 1,1,0,1])

    def test_known_contrast(self):
        result = estimate_rd(self.p, self.a, self.y)
        self.assertAlmostEqual(result["rd"], .375)
        self.assertGreater(result["se"], 0)
        self.assertLess(result["lower"], result["rd"])
        self.assertGreater(result["upper"], result["rd"])

    def test_label_symmetry(self):
        a = estimate_rd(self.p, self.a, self.y)
        b = estimate_rd(self.p, 1-self.a, self.y)
        self.assertAlmostEqual(a["rd"], -b["rd"])
        self.assertAlmostEqual(a["lower"], -b["upper"])

    def test_permutation(self):
        ix = np.random.default_rng(42).permutation(len(self.p))
        a = estimate_rd(self.p, self.a, self.y)
        b = estimate_rd(self.p[ix], self.a[ix], self.y[ix])
        self.assertAlmostEqual(a["se"], b["se"])

    def test_degenerate(self):
        self.assertIsNone(estimate_rd(self.p, np.zeros_like(self.a), self.y))
        self.assertIsNone(estimate_rd(self.p, self.a, np.ones_like(self.y)))
        self.assertIsNone(estimate_rd([0, 1], [0, 1], [0, 1]))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            estimate_rd([0], [2], [1])
        with self.assertRaises(ValueError):
            estimate_rd([0], [1, 0], [1])


if __name__ == "__main__":
    unittest.main()
