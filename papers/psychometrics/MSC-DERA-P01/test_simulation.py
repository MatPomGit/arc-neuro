import unittest

from simulation import simulate


class CategoryRiskTests(unittest.TestCase):
    def test_seed_and_category_sparsity(self):
        skewed = (0.01, 0.02, 0.04, 0.08, 0.15, 0.25, 0.45)
        balanced = (0.10, 0.12, 0.15, 0.26, 0.15, 0.12, 0.10)
        risk = simulate(150, skewed, 21, reps=100)
        self.assertEqual(risk, simulate(150, skewed, 21, reps=100))
        self.assertGreater(risk, simulate(150, balanced, 21, reps=100))
        self.assertGreater(risk, simulate(1200, skewed, 21, reps=100))
