import unittest
import numpy as np
from simulate_power import surface, interaction, simulate

class SimulationTests(unittest.TestCase):
    def test_additivity(self):
        for scenario in ("null", "additive"):
            np.testing.assert_allclose(interaction(surface(scenario, .3)), 0, atol=1e-12)

    def test_interaction(self):
        for scenario in ("interaction", "peak"):
            self.assertGreater(np.linalg.norm(interaction(surface(scenario, .3))), 0)

    def test_centering(self):
        x = interaction(np.random.default_rng(42).normal(size=(5,4,4)))
        np.testing.assert_allclose(x.sum(axis=-1), 0, atol=1e-12)
        np.testing.assert_allclose(x.sum(axis=-2), 0, atol=1e-12)

    def test_reproducibility(self):
        args = (20, 50, .3, 42, "interaction", .5, 4)
        self.assertEqual(simulate(*args), simulate(*args))

    def test_null_calibration(self):
        p, _ = simulate(40, 2000, .3, 42, "null", .5, 4)
        self.assertTrue(.025 < p < .075, p)

if __name__ == "__main__":
    unittest.main()
