import unittest

from simulation import simulate


class CategoryRiskTests(unittest.TestCase):
    def test_seed_and_category_sparsity(self):
        skewed = (0.01, 0.04, 0.10, 0.25, 0.60)
        balanced = (0.10, 0.20, 0.40, 0.20, 0.10)
        risk = simulate(150, skewed, 21, reps=100)
        self.assertEqual(risk, simulate(150, skewed, 21, reps=100))
        self.assertGreater(risk, simulate(150, balanced, 21, reps=100))
        self.assertGreater(risk, simulate(600, skewed, 21, reps=100))
