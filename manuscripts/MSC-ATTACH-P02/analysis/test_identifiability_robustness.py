"""Verify independent-role isolation and exploratory inference assumptions."""

import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import numpy as np

from controller_identifiability_robustness import (
    bootstrap_interval,
    conditional_information,
    evaluate,
    information_criteria,
    interval_label,
    observe_extended,
    quantize,
    validate_robustness,
)
from controller_identifiability_suite import generate, observe


class RobustnessTests(unittest.TestCase):
    """Check scientific boundaries rather than fixed Monte Carlo outcomes."""

    def setUp(self) -> None:
        """Load the executable pre-run development settings."""
        path = (
            Path(__file__).parent / "configs/m02_robustness_development.json"
        )
        self.spec = json.loads(path.read_text())
        self.condition = self.spec["conditions"][0]

    def test_independent_final_actions_cannot_change_any_selection(self):
        """A changed final trajectory affects loss but never fitted choices."""
        seeds = [self.spec["seed"] + role * 10_000 for role in range(3)]
        original = [
            observe_extended(
                generate(self.spec, self.condition, "pid", seed),
                self.condition,
                seed,
            )
            for seed in seeds
        ]
        changed = copy.deepcopy(original)
        changed[2][1][144:] += 2.0
        results = []
        for observations in (original, changed):
            with patch(
                "controller_identifiability_robustness.observe_extended",
                side_effect=observations,
            ):
                results.append(
                    evaluate(self.spec, self.condition, "pid", 0)[0][0]
                )
        for old, new in zip(results[0]["scores"], results[1]["scores"]):
            self.assertEqual(old["selected"], new["selected"])
            self.assertEqual(old["competitor"], new["competitor"])
        old = [s for s in results[0]["scores"] if s["mode"] == "independent"]
        new = [s for s in results[1]["scores"] if s["mode"] == "independent"]
        self.assertNotEqual(
            old[0]["final_rmse_selected"], new[0]["final_rmse_selected"]
        )
        self.assertEqual(len(set(results[0]["seeds"])), 3)

    def test_default_observation_is_byte_identical(self):
        """The extension cannot silently change the archived observation model.
        """
        data = generate(self.spec, self.condition, "pid", 71)
        for old, new in zip(
            observe(data, self.condition, 71),
            observe_extended(data, self.condition, 71),
        ):
            np.testing.assert_array_equal(old, new)

    def test_information_penalties_and_invalid_variance(self):
        """Parameter penalties count the fitted error variance as well."""
        aic, bic = information_criteria(10.0, 100, 3)
        self.assertAlmostEqual(aic, 100 * np.log(0.1) + 8)
        self.assertAlmostEqual(bic, 100 * np.log(0.1) + 4 * np.log(100))
        self.assertEqual(information_criteria(0.0, 100, 3), (None, None))
        self.assertEqual(information_criteria(10.0, 3, 3), (None, None))

    def test_profiles_have_quadratic_known_sigma_curvature(self):
        """Profiling nuisance terms recovers the fixed-design Gaussian curve.
        """
        rng = np.random.default_rng(42)
        X = np.column_stack([np.ones(100), rng.normal(size=(100, 3))])
        y = X @ np.array([0.1, 0.6, 0.06, 0.08])
        info, profiles = conditional_information(X, y, 0.005)
        self.assertGreater(info["information_min"], 0)
        np.testing.assert_allclose(
            [p["profile_deviance"] for p in profiles[:41]],
            np.linspace(-4, 4, 41) ** 2,
            atol=1e-9,
        )
        X[:, 3] = X[:, 2]
        info, profiles = conditional_information(X, y, 0.005)
        self.assertLess(info["rank"], info["columns"])
        self.assertEqual(profiles, [])

    def test_bootstrap_retains_pair_units_and_insufficient_status(self):
        """A constant paired advantage remains constant under resampling."""
        values = np.full(20, -0.002)
        first = bootstrap_interval(values, 200, 51, 0.95)
        second = bootstrap_interval(values, 200, 51, 0.95)
        self.assertEqual(first, second)
        np.testing.assert_allclose(first, [-0.002, -0.002])
        self.assertEqual(
            interval_label(*first, 0.005), "development_equivalent"
        )
        self.assertEqual(interval_label(-0.006, 0.001, 0.005), "inconclusive")
        self.assertEqual(
            bootstrap_interval(values[:1], 200, 51, 0.95), (None, None)
        )

    def test_quantization_and_irregular_observation_preserve_timing(self):
        """Bounded categories and irregular timestamps are explicit transforms.
        """
        values = quantize(np.linspace(-1, 1, 301), 7, 0.25)
        self.assertEqual(len(np.unique(values)), 7)
        self.assertGreaterEqual(values.min(), -0.25)
        self.assertLessEqual(values.max(), 0.25)
        condition = self.condition | {"irregular": True, "stride": 3}
        data = generate(self.spec, condition, "pi", 12)
        error, action, dt = observe_extended(data, condition, 12)
        self.assertEqual(len(error), len(action))
        self.assertTrue(np.all(dt > 0))
        self.assertGreater(len(np.unique(dt[1:])), 1)

    def test_configuration_rejects_infinite_variance_and_bad_bins(self):
        """Invalid heavy-tail and quantization settings fail before simulation.
        """
        for change in (
            {"noise_distribution": "student_t", "noise_df": 2},
            {"quantization_levels": 1, "quantization_bound": 0.25},
        ):
            spec = copy.deepcopy(self.spec)
            spec["conditions"][0].update(change)
            with self.assertRaises(ValueError):
                validate_robustness(spec)


if __name__ == "__main__":
    unittest.main()
