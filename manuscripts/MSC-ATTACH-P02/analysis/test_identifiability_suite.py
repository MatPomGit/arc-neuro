"""Test causal fitting, generator recovery and failure-aware M02 reporting."""

import copy
import json
from pathlib import Path
import unittest

import numpy as np

from controller_identifiability_split import fit_validate_test, split_indices
from controller_identifiability_suite import (
    CANDIDATES, evaluate, generate, matrices, observe, summarize, validate_spec,
)


class IdentifiabilitySuiteTests(unittest.TestCase):
    """Check meaningful scientific boundaries of the development benchmark."""

    def setUp(self) -> None:
        """Load the committed development settings without executing the sweep."""
        path = Path(__file__).parent / "configs/m02_standardized_development.json"
        self.spec = json.loads(path.read_text())
        self.spec["replications"] = 3
        self.condition = self.spec["conditions"][0]

    def test_final_actions_do_not_change_fits_or_validation_choice(self):
        """Changing only future actions cannot alter fitted/selected models."""
        data = generate(self.spec, self.condition, "pid", 12)
        error, action, dt = observe(data, self.condition, 12)
        fit_end, validation_end = split_indices(len(action), *self.spec["split"])
        changed = action.copy()
        changed[validation_end:] += 0.2
        results = []
        for outcome in (action, changed):
            fits = {}
            for name, design in matrices(error, outcome, dt, 0.85, 0.12).items():
                fits[name] = fit_validate_test(design, outcome, fit_end, validation_end)
            results.append(fits)
        for name in CANDIDATES:
            np.testing.assert_equal(
                results[0][name]["coefficients"],
                results[1][name]["coefficients"],
            )
            self.assertEqual(
                results[0][name]["validation_rmse"],
                results[1][name]["validation_rmse"],
            )
        def select(fits: dict) -> str:
            return min(CANDIDATES, key=lambda n: fits[n]["validation_rmse"])
        self.assertEqual(select(results[0]), select(results[1]))
        self.assertNotEqual(
            results[0]["pid"]["final_test_rmse"],
            results[1]["pid"]["final_test_rmse"],
        )

    def test_noiseless_equations_recover_known_coefficients(self):
        """Correctly specified dense oracle fits recover each generator's terms."""
        self.spec["action_noise_sd"] = 0
        for name in ("p", "pi", "pid", "arx", "nonlinear", "switching"):
            data = generate(self.spec, self.condition, name, 23)
            error, action, dt = observe(data, self.condition, 23)
            design = matrices(error, action, dt, 0.85, 0.12)[name]
            fit = fit_validate_test(design, action, 108, 144)
            np.testing.assert_allclose(
                fit["coefficients"], data["true_coefficients"], atol=1e-10
            )
            self.assertLess(fit["final_test_rmse"], 1e-10)

    def test_exact_pid_reduction_has_same_observable_actions_as_p(self):
        """A nominal PID label cannot distinguish exact zero-gain reduction."""
        condition = self.condition | {"reduced_pid": True}
        pid = generate(self.spec, condition, "pid", 5)
        p = generate(self.spec, condition, "p", 5)
        np.testing.assert_array_equal(pid["action"], p["action"])
        self.assertEqual(pid["effective"], "p")

    def test_gaps_change_elapsed_time_without_imputed_records(self):
        """Retained snapshots have actual elapsed intervals and reproducible gaps."""
        data = generate(self.spec, self.condition, "pi", 11)
        condition = self.condition | {"stride": 3, "missingness": 0.25}
        a = observe(data, condition, 11)
        b = observe(data, condition, 11)
        for x, y in zip(a, b):
            np.testing.assert_array_equal(x, y)
        self.assertEqual(a[2][0], 1)
        self.assertTrue(np.all(a[2][1:] >= 3))
        self.assertLess(len(a[0]), len(data["action"]) / 3)

    def test_failed_trajectory_remains_in_attempted_denominator(self):
        """Sparse trajectories cannot silently disappear from recovery counts."""
        failed = self.condition | {"steps": 15, "stride": 15}
        row = evaluate(self.spec, failed, "p", 0)
        result = summarize([row], self.spec)[0]
        self.assertEqual(result["attempted"], 1)
        self.assertEqual(result["selection_failures"], 1)
        self.assertEqual(result["paired_n"], 0)
        self.assertIsNone(result["paired_delta_mean"])

    def test_invalid_design_and_rank_deficiency_are_explicit(self):
        """Invalid settings fail early and singular models have visible status."""
        bad = copy.deepcopy(self.spec)
        bad["conditions"][0]["noise_sd"] = float("nan")
        with self.assertRaises(ValueError):
            validate_spec(bad)
        self.spec["action_noise_sd"] = 0
        row = evaluate(self.spec, self.condition, "intercept", 0)
        self.assertEqual(row["fits"]["ar"]["status"], "rank_deficient")
        self.assertEqual(row["selected"], "intercept")

    def test_final_scoring_can_be_deferred_until_selection(self):
        """The suite can freeze its choice before requesting any final loss."""
        X = np.arange(30, dtype=float)[:, None]
        y = X[:, 0] * 0.2
        fit = fit_validate_test(X, y, 18, 24, evaluate_final=False)
        self.assertIsNone(fit["final_test_rmse"])
        self.assertLess(fit["validation_rmse"], 1e-10)


if __name__ == "__main__":
    unittest.main()
