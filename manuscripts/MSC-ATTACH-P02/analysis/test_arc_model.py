"""Regression and falsifiability-oriented tests for ARC."""

import math
import unittest

import numpy as np

from arc_model import (
    ARCConfig,
    ARCTraits,
    ControllerGains,
    impulse,
    simulate,
)
from fit_controller import compare_models, features
from sampling_sensitivity import observed_intervals, rows_for_config, summarize
from controller_discrimination import best_model, rows_for_config as discrimination_rows, summarize as discrimination_summary
from controller_identifiability_split import rows_for_config as identifiability_rows, summarize as identifiability_summary
from emotion_regulation_scenarios import run_scenarios, summarize as scenario_summary


class ARCModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = ARCConfig(
            steps=120,
            process_noise=0.0,
            perception_noise=0.0,
        )
        self.shock = impulse(self.config, step=30, magnitude=-0.25)

    def test_reproducible_given_same_seed(self) -> None:
        a = simulate(ARCTraits(), self.config, self.shock, seed=11)
        b = simulate(ARCTraits(), self.config, self.shock, seed=11)
        np.testing.assert_allclose(a.series["action"], b.series["action"])

    def test_external_target_schedule_is_used(self) -> None:
        target = np.linspace(0.25, 0.75, self.config.steps)
        result = simulate(
            ARCTraits(),
            self.config,
            self.shock,
            target_state=target,
            seed=2,
        )
        np.testing.assert_allclose(result.series["target_state"], target)

    def test_p_mode_zeroes_integral_and_derivative_gains(self) -> None:
        config = ARCConfig(
            steps=80,
            process_noise=0.0,
            perception_noise=0.0,
            controller_mode="p",
        )
        gains = ControllerGains(kp=0.7, ki=0.5, kd=0.4)
        result = simulate(
            ARCTraits(),
            config,
            impulse(config, step=20, magnitude=-0.2),
            gains=gains,
            seed=3,
        )
        self.assertAlmostEqual(result.metrics["mean_ki"], 0.0)
        self.assertAlmostEqual(result.metrics["mean_kd"], 0.0)

    def test_recovery_rate_positive_for_default_profile(self) -> None:
        result = simulate(ARCTraits(), self.config, self.shock, seed=4)
        self.assertTrue(math.isfinite(result.metrics["kappa"]))
        self.assertGreater(result.metrics["kappa"], 0.0)

    def test_m_reduces_perception_error_under_same_seed(self) -> None:
        noisy_config = ARCConfig(
            steps=100,
            process_noise=0.0,
            perception_noise=0.15,
        )
        shock = impulse(noisy_config, step=25, magnitude=-0.2)
        low = simulate(
            ARCTraits(M=0.0),
            noisy_config,
            shock,
            seed=10,
        )
        high = simulate(
            ARCTraits(M=1.0),
            noisy_config,
            shock,
            seed=10,
        )
        low_error = np.mean(
            np.abs(low.series["estimated_state"] - low.series["relation_state"])
        )
        high_error = np.mean(
            np.abs(high.series["estimated_state"] - high.series["relation_state"])
        )
        self.assertGreater(low_error, high_error)

    def test_outputs_are_bounded_where_expected(self) -> None:
        result = simulate(ARCTraits(C=1.0), self.config, self.shock, seed=5)
        self.assertGreaterEqual(float(result.series["relation_state"].min()), 0.0)
        self.assertLessEqual(float(result.series["relation_state"].max()), 1.0)
        self.assertGreaterEqual(result.metrics["arc_instability_index"], 0.0)
        self.assertLessEqual(result.metrics["arc_instability_index"], 1.0)

    def test_irregular_intervals_match_leaky_integral_and_elapsed_time(self) -> None:
        config = ARCConfig(steps=10, dt=1.0, process_noise=0.0, perception_noise=0.0)
        intervals = np.array([1.0, 2.0] + [1.0] * 8)
        gains = ControllerGains(kp=0.0, ki=0.0, kd=0.0, integral_leak=0.5)
        target = np.full(10, 0.6)
        result = simulate(ARCTraits(), config, target_state=target,
                          initial_state=0.5, gains=gains, intervals=intervals)
        self.assertAlmostEqual(result.series["i_term"][0], 0.1)
        self.assertAlmostEqual(result.series["i_term"][1], 0.1 * 0.5**2 + 0.2)
        self.assertAlmostEqual(result.series["time"][2], 3.0)
        X, _ = features(result.series["estimated_error"], intervals, "pid", 0.5)
        np.testing.assert_allclose(X[:, 1], result.series["i_term"])
        np.testing.assert_allclose(X[:, 2], result.series["d_term"])

    def test_target_shift_is_not_action_efficacy(self) -> None:
        config = ARCConfig(steps=10, process_noise=0.0, perception_noise=0.0)
        target = np.array([0.5, 0.8] + [0.8] * 8)
        result = simulate(ARCTraits(), config, target_state=target,
                          gains=ControllerGains(kp=0), seed=5)
        self.assertAlmostEqual(result.series["fixed_target_efficacy"][0], 0)
        self.assertAlmostEqual(result.series["regulatory_efficacy"][0], -0.3)
        self.assertAlmostEqual(result.series["target_change"][0], 0.3)
        self.assertAlmostEqual(result.series["action_effect_oracle"][0], 0)

    def test_oracle_parameter_recovery_and_behavioral_baselines(self) -> None:
        config = ARCConfig(steps=100, process_noise=0, perception_noise=0.02)
        gains = ControllerGains(kp=0.65, ki=0.07, kd=0.04)
        intervals = np.resize(np.array([0.5, 1.0, 2.0]), 100)
        result = simulate(ARCTraits(), config, impulse(config, step=25),
                          gains=gains, intervals=intervals, seed=15)
        modifier = result.series["kp_effective"] / gains.kp
        oracle = compare_models(result.series["estimated_error"],
                                result.series["raw_control"] / modifier,
                                intervals, gains.integral_leak)
        self.assertLess(oracle["pid"]["test_rmse"], 1e-10)
        for name, expected in (("kp", gains.kp), ("ki", gains.ki), ("kd", gains.kd)):
            self.assertAlmostEqual(oracle["pid"]["parameter_estimates"][name], expected)
        observed = compare_models(result.series["true_error"],
                                  result.series["action"], intervals, gains.integral_leak)
        self.assertIn("context", observed)
        self.assertIn("autoregressive", observed)

    def test_invalid_intervals_and_leak_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ControllerGains(kp=0.5, integral_leak=1.1)
        with self.assertRaises(ValueError):
            simulate(config=self.config, intervals=np.zeros(self.config.steps))

    def test_missing_observations_use_elapsed_time_and_reproducible_grid(self) -> None:
        times = np.array([0.0, 1.0, 3.0, 4.0, 6.0, 7.0])
        np.testing.assert_allclose(
            observed_intervals(times, np.array([0, 2, 3, 4, 5]), 1.0),
            [1.0, 3.0, 1.0, 2.0, 1.0],
        )
        spec = {
            "seed": 17, "n_runs": 2, "traits": {},
            "simulation": {"steps": 40, "process_noise": 0.003},
            "perturbation": {"step": 10, "magnitude": -0.2},
            "gain_ranges": {"kp": [0.3, 0.6], "ki": [0.01, 0.1], "kd": [0.01, 0.1]},
            "integral_leak": 0.85,
            "schedules": {"fixed": [1.0]},
            "measurement_noise": [0.0, 0.04], "missingness": [0.0, 0.3],
        }
        rows = rows_for_config(spec)
        self.assertEqual(rows, rows_for_config(spec))
        self.assertEqual(len(rows), 8)
        self.assertEqual(len(summarize(rows)), 4)
        self.assertTrue(all(r["observed_n"] == 40 for r in rows if r["missingness"] == 0))

    def test_generator_modes_and_simpler_tie_rule(self) -> None:
        self.assertEqual(best_model({"p": {"test_rmse": .2},
                                     "pi": {"test_rmse": .2}}, ("p", "pi")), "p")
        spec = {
            "seed": 29, "n_runs": 2, "traits": {},
            "simulation": {"steps": 40, "process_noise": 0.003},
            "perturbation": {"step": 10, "magnitude": -0.2},
            "gain_ranges": {"kp": [0.4, 0.6], "ki": [0.03, 0.09], "kd": [0.03, 0.09]},
            "integral_leak": 0.85, "measurement_noise": [0.0, 0.04],
        }
        rows = discrimination_rows(spec)
        self.assertEqual(rows, discrimination_rows(spec))
        self.assertEqual(len(rows), 12)
        self.assertEqual(len(discrimination_summary(rows)), 6)
        self.assertTrue(all(r["ki_true"] == 0 for r in rows if r["generator"] == "p"))
        self.assertTrue(all(r["kd_true"] == 0 for r in rows if r["generator"] != "pid"))

    def test_three_way_identifiability_split_is_reproducible(self) -> None:
        spec = {
            "seed": 41,
            "n_runs": 2,
            "traits": {},
            "simulation": {"steps": 60, "dt": 1, "process_noise": 0.003, "perception_noise": 0.02},
            "perturbation": {"step": 15, "magnitude": -0.2},
            "gain_ranges": {"kp": [0.4, 0.6], "ki": [0.03, 0.09], "kd": [0.03, 0.09]},
            "integral_leak": 0.85,
            "measurement_noise": [0.0, 0.04],
            "split": {"fit_fraction": 0.60, "validation_fraction": 0.20},
        }
        rows = identifiability_rows(spec)
        self.assertEqual(rows, identifiability_rows(spec))
        self.assertEqual(len(rows), 12)
        self.assertEqual(len(identifiability_summary(rows)), 6)
        self.assertTrue(all(row["fit_n"] == 36 for row in rows))
        self.assertTrue(all(row["validation_n"] == 12 for row in rows))
        self.assertTrue(all(row["final_test_n"] == 12 for row in rows))
        self.assertTrue(all(
            row["selected_all"] in ("context", "autoregressive", "p", "pi", "pid")
            for row in rows
        ))

    def test_matched_impulse_across_profile_grid(self) -> None:
        spec = {
            "seed": 31, "n_runs": 2,
            "traits": {"L": .55, "U": .35, "C": .5, "S": .55, "M": .5, "F": .5},
            "simulation": {"steps": 40, "dt": 1, "process_noise": 0,
                           "perception_noise": 0},
            "perturbation": {"step": 10, "magnitude": -.2},
            "groups": {"estimation_flexibility": {
                "axes": ["M", "F"],
                "levels": {"M": {"low": .15, "high": .85},
                           "F": {"low": .15, "high": .85}},
            }},
        }
        runs, series = run_scenarios(spec)
        self.assertEqual(len(runs), 8)
        self.assertEqual(len(scenario_summary(runs)), 4)
        shocked = [row for row in series if row["step"] == 11]
        self.assertEqual(len(shocked), 4)
        for row in shocked:
            self.assertAlmostEqual(row["abs_error_mean"], .2)


if __name__ == "__main__":
    unittest.main()
