# SPDX-License-Identifier: Apache-2.0
# Modified in ARC Neuro: locate the migrated configuration.
"""Tests for the ARC H1 exact-design Monte Carlo."""

from pathlib import Path
import csv
import tempfile
import unittest

import numpy as np
import pandas as pd

from h1_asymmetry_operating_characteristics import (
    classify_asymmetry_interval,
    candidate_guardrails,
)
from h1_decision_analysis import (
    binomial_precision,
    long_decisions,
    sesoi_operating_characteristics,
)
from h1_exact_monte_carlo import (
    MODEL_TERMS,
    Scenario,
    build_valid_lags,
    load_config,
    model_formula,
    paired_rmse_difference,
    improvement_status,
    noninferiority_status,
    prepare_analysis_data,
    replication_rng,
    run,
    schedule_times,
    simulate_prompt_panel,
)
from h1_inference_analysis import (
    classify_replication,
    holm_adjust,
    one_sided_positive_p,
    sesoi_one_sided_p,
)
from h1_ipw_sensitivity import (
    attach_truncated_ipw,
    build_ipw_analysis_data,
    fit_weighted_gee,
    response_history,
)
from merge_h1_exact_results import (
    json_scalar,
    merge_files,
    validate_expected_replications,
    validate_unique_replications,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "protocol" / "exact_design_config.json"


class ExactDesignMonteCarloTests(unittest.TestCase):
    """Check locked model structure and leakage safeguards."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the repository exact-design configuration once."""

        cls.config = load_config(CONFIG_PATH)

    def test_model_family_is_locked_to_m0_m4(self) -> None:
        """Require the preregistered five-model family."""

        self.assertEqual(
            tuple(MODEL_TERMS),
            ("M0", "M1", "M2", "M3", "M4"),
        )
        self.assertNotIn("r_star_wp10", model_formula("M1"))
        self.assertIn("r_star_wp10", model_formula("M2"))
        self.assertIn("e_wp10", model_formula("M3"))
        self.assertIn("e_positive_wp10", model_formula("M4"))
        self.assertIn("e_negative_wp10", model_formula("M4"))

    def test_schedule_respects_locked_strata_and_spacing(self) -> None:
        """Match the preregistered six-strata sampling rule."""

        rng = np.random.default_rng(20260928)
        times = schedule_times(self.config, rng)
        self.assertEqual(len(times), self.config["prompts_per_day"])
        width = (
            self.config["waking_hours"]
            / self.config["prompts_per_day"]
        )
        for index, value in enumerate(times):
            self.assertGreaterEqual(value, index * width)
            self.assertLess(value, (index + 1) * width)
        self.assertTrue(
            np.all(
                np.diff(times)
                >= self.config["minimum_prompt_separation_hours"] - 1e-12
            )
        )

    def test_valid_lags_respect_locked_response_interval(self) -> None:
        """Require simulated confirmatory lags to follow the 1-4 h rule."""

        scenario = Scenario(4, 0.95, 0.0, "M3")
        rng = np.random.default_rng(20260929)
        prompts = simulate_prompt_panel(self.config, scenario, rng)
        lags = build_valid_lags(prompts, self.config)
        self.assertGreater(len(lags), 0)
        self.assertTrue(
            (
                lags["elapsed_hours"]
                >= self.config["valid_lag_min_hours"]
            ).all()
        )
        self.assertTrue(
            (
                lags["elapsed_hours"]
                <= self.config["valid_lag_max_hours"]
            ).all()
        )

    def test_valid_lag_builder_returns_record_rows_on_pandas3(self) -> None:
        """Keep pandas 3 compatibility while excluding prompt 1 -> 2."""

        prompts = pd.DataFrame([
            {
                "couple_id": "c1", "member": 0, "participant_id": "c1p0",
                "day": 1, "prompt": 1, "observed": True,
                "response_hour": 1.0, "action": 0.0, "r_hat": 50.0,
                "r_star": 60.0, "e": 10.0, "e_positive": 10.0,
                "e_negative": 0.0, "negative_affect": 20.0,
                "stressor": 0.0, "contact": 1.0,
            },
            {
                "couple_id": "c1", "member": 0, "participant_id": "c1p0",
                "day": 1, "prompt": 2, "observed": True,
                "response_hour": 3.0, "action": 1.0, "r_hat": 52.0,
                "r_star": 60.0, "e": 8.0, "e_positive": 8.0,
                "e_negative": 0.0, "negative_affect": 18.0,
                "stressor": 0.0, "contact": 1.0,
            },
            {
                "couple_id": "c1", "member": 0, "participant_id": "c1p0",
                "day": 1, "prompt": 3, "observed": True,
                "response_hour": 5.0, "action": 2.0, "r_hat": 54.0,
                "r_star": 60.0, "e": 6.0, "e_positive": 6.0,
                "e_negative": 0.0, "negative_affect": 16.0,
                "stressor": 0.0, "contact": 1.0,
            },
        ])
        lags = build_valid_lags(prompts, self.config)
        self.assertEqual(len(lags), 1)
        self.assertEqual(lags.iloc[0]["participant_id"], "c1p0")
        self.assertEqual(int(lags.iloc[0]["prompt_stratum"]), 3)
        self.assertAlmostEqual(float(lags.iloc[0]["elapsed_hours"]), 2.0)

    def test_valid_lag_builder_does_not_cross_participant_or_day(self) -> None:
        """Keep array-based lag construction within participant-day boundaries."""

        prompts = pd.DataFrame([
            {
                "couple_id": "c1", "member": 0, "participant_id": "c1p0",
                "day": 1, "prompt": 2, "observed": True,
                "response_hour": 3.0, "action": 1.0, "r_hat": 52.0,
                "r_star": 60.0, "e": 8.0, "e_positive": 8.0,
                "e_negative": 0.0, "negative_affect": 18.0,
                "stressor": 0.0, "contact": 1.0,
            },
            {
                "couple_id": "c1", "member": 1, "participant_id": "c1p1",
                "day": 1, "prompt": 1, "observed": True,
                "response_hour": 1.0, "action": -1.0, "r_hat": 45.0,
                "r_star": 50.0, "e": 5.0, "e_positive": 5.0,
                "e_negative": 0.0, "negative_affect": 25.0,
                "stressor": 1.0, "contact": 0.0,
            },
            {
                "couple_id": "c1", "member": 0, "participant_id": "c1p0",
                "day": 1, "prompt": 1, "observed": True,
                "response_hour": 1.0, "action": 0.0, "r_hat": 50.0,
                "r_star": 60.0, "e": 10.0, "e_positive": 10.0,
                "e_negative": 0.0, "negative_affect": 20.0,
                "stressor": 0.0, "contact": 1.0,
            },
            {
                "couple_id": "c1", "member": 0, "participant_id": "c1p0",
                "day": 1, "prompt": 3, "observed": True,
                "response_hour": 5.0, "action": 2.0, "r_hat": 54.0,
                "r_star": 60.0, "e": 6.0, "e_positive": 6.0,
                "e_negative": 0.0, "negative_affect": 16.0,
                "stressor": 0.0, "contact": 1.0,
            },
            {
                "couple_id": "c1", "member": 0, "participant_id": "c1p0",
                "day": 2, "prompt": 1, "observed": True,
                "response_hour": 1.5, "action": 2.0, "r_hat": 55.0,
                "r_star": 60.0, "e": 5.0, "e_positive": 5.0,
                "e_negative": 0.0, "negative_affect": 15.0,
                "stressor": 0.0, "contact": 1.0,
            },
        ])
        lags = build_valid_lags(prompts, self.config)
        self.assertEqual(len(lags), 1)
        self.assertEqual(lags.iloc[0]["participant_id"], "c1p0")
        self.assertEqual(int(lags.iloc[0]["day"]), 1)
        self.assertEqual(int(lags.iloc[0]["prompt_stratum"]), 3)

    def test_holdout_means_use_training_prompts_only(self) -> None:
        """Prevent temporal leakage into within/between decomposition."""

        scenario = Scenario(4, 0.9, 0.0, "M3")
        rng = np.random.default_rng(20260927)
        prompts = simulate_prompt_panel(self.config, scenario, rng)
        lags = build_valid_lags(prompts, self.config)
        _, test = prepare_analysis_data(prompts, lags, self.config)

        training = prompts[
            (prompts["day"] <= self.config["training_days"])
            & prompts["observed"]
        ]
        expected = (
            training.groupby("participant_id")["r_hat"].mean()
            / 10.0
        )

        observed = (
            test[["participant_id", "r_hat_mean10"]]
            .drop_duplicates()
            .set_index("participant_id")["r_hat_mean10"]
        )
        common = expected.index.intersection(observed.index)
        self.assertGreater(len(common), 0)
        np.testing.assert_allclose(
            observed.loc[common].sort_index(),
            expected.loc[common].sort_index(),
            rtol=0.0,
            atol=1e-12,
        )

    def test_paired_rmse_difference_reports_uncertainty(self) -> None:
        """Require paired RMSE comparisons to expose a confidence interval."""

        left = pd.Series([2.0, 3.0, 4.0], index=["p1", "p2", "p3"])
        right = pd.Series([3.0, 4.0, 5.0], index=["p1", "p2", "p3"])
        mean, se, low, high, n = paired_rmse_difference(left, right)
        self.assertEqual(n, 3)
        self.assertAlmostEqual(mean, -1.0)
        self.assertAlmostEqual(se, 0.0)
        self.assertAlmostEqual(low, -1.0)
        self.assertAlmostEqual(high, -1.0)

    def test_paired_rmse_difference_clusters_by_couple(self) -> None:
        """Use dyads, not participants, as predictive uncertainty units."""

        index = pd.MultiIndex.from_tuples(
            [("c1", "p1"), ("c1", "p2"), ("c2", "p3"), ("c2", "p4")],
            names=["couple_id", "participant_id"],
        )
        left = pd.Series([2.0, 4.0, 5.0, 7.0], index=index)
        right = pd.Series([3.0, 3.0, 6.0, 6.0], index=index)
        mean, se, low, high, n = paired_rmse_difference(left, right)
        self.assertEqual(n, 2)
        self.assertAlmostEqual(mean, 0.0)
        self.assertGreaterEqual(se, 0.0)
        self.assertLessEqual(low, mean)
        self.assertGreaterEqual(high, mean)

    def test_three_state_rmse_evidence_logic(self) -> None:
        """Do not equate lack of improvement evidence with simpler-model support."""

        self.assertEqual(
            improvement_status(-0.6, -0.3, 0.25),
            "material_improvement",
        )
        self.assertEqual(
            improvement_status(-0.2, 0.1, 0.25),
            "no_material_improvement",
        )
        self.assertEqual(
            improvement_status(-0.4, -0.1, 0.25),
            "inconclusive",
        )
        self.assertEqual(
            noninferiority_status(-0.2, 0.2, 0.25),
            "noninferior",
        )
        self.assertEqual(
            noninferiority_status(0.3, 0.5, 0.25),
            "materially_inferior",
        )
        self.assertEqual(
            noninferiority_status(0.1, 0.4, 0.25),
            "inconclusive",
        )

    def test_config_contains_prespecified_margin_grids(self) -> None:
        """Keep RMSE and coefficient-scale calibration candidates explicit."""

        self.assertGreater(len(self.config["candidate_rmse_margins"]), 1)
        self.assertGreater(len(self.config["candidate_sesoi_beta"]), 1)
        self.assertTrue(all(v > 0 for v in self.config["candidate_sesoi_beta"]))

    def test_decision_analysis_separates_insufficient_data(self) -> None:
        """Do not misclassify insufficient replications as model errors."""

        row = {
            "couples": 72,
            "people": 144,
            "compliance_target": 0.75,
            "missingness_strength": 1.0,
            "truth": "M3",
            "replication": 0,
            "all_models_converged": True,
            "people_with_minimum_lags": 99,
            "representation_margin_0p25": "M3_signed_discrepancy",
        }
        for pair in ("M1_M0", "M2_M1", "M3_M2", "M4_M3", "M4_M2"):
            row[f"delta_{pair}_n"] = 120
        long = long_decisions(pd.DataFrame([row]))
        self.assertEqual(
            long.iloc[0]["decision"],
            "inconclusive_data_insufficient",
        )
        self.assertTrue(bool(long.iloc[0]["inconclusive"]))

    def test_asymmetry_interval_has_three_state_logic(self) -> None:
        """Classify M4 asymmetry without converting overlap into evidence."""

        self.assertEqual(
            classify_asymmetry_interval(-0.2, 0.2, 0.5),
            "symmetry_compatible",
        )
        self.assertEqual(
            classify_asymmetry_interval(0.6, 1.0, 0.5),
            "asymmetry_material",
        )
        self.assertEqual(
            classify_asymmetry_interval(0.2, 0.8, 0.5),
            "inconclusive",
        )

    def test_asymmetry_guardrails_do_not_choose_a_winner(self) -> None:
        """Report candidate suitability without automatic tolerance selection."""

        oc = pd.DataFrame([
            {
                "tolerance": 0.5, "truth": "M3",
                "symmetry_compatible_rate": 0.90,
                "asymmetry_material_rate": 0.02,
                "inconclusive_rate": 0.08,
            },
            {
                "tolerance": 0.5, "truth": "M4",
                "symmetry_compatible_rate": 0.01,
                "asymmetry_material_rate": 0.85,
                "inconclusive_rate": 0.14,
            },
        ])
        cfg = {
            "asymmetry_validation": {
                "operating_characteristic_guardrails": {
                    "minimum_M3_symmetry_compatibility_rate": 0.80,
                    "maximum_M3_false_asymmetry_rate": 0.05,
                    "minimum_M4_material_asymmetry_rate": 0.80,
                    "maximum_M4_false_symmetry_rate": 0.05,
                }
            }
        }
        result = candidate_guardrails(oc, cfg)
        self.assertEqual(len(result), 1)
        self.assertTrue(bool(result.iloc[0]["passes_all_guardrails"]))
        self.assertNotIn("selected", result.columns)

    def test_sesoi_directional_test_uses_relevance_null(self) -> None:
        """Test H0 beta <= SESOI rather than only beta <= 0."""

        p_at_zero = sesoi_one_sided_p(0.5, 0.2, 0.5)
        p_above = sesoi_one_sided_p(1.5, 0.2, 0.5)
        self.assertAlmostEqual(p_at_zero, 0.5)
        self.assertLess(p_above, 1e-5)

    def test_holm_adjustment_for_two_co_primary_tests(self) -> None:
        """Control the revised H1 co-primary family with Holm."""

        adjusted = holm_adjust({"H1_P1": 0.01, "H1_P2": 0.04})
        self.assertAlmostEqual(adjusted["H1_P1"], 0.02)
        self.assertAlmostEqual(adjusted["H1_P2"], 0.04)

    def test_directional_p_conversion_respects_sign(self) -> None:
        """Convert symmetric Wald p values to positive-direction tests."""

        self.assertAlmostEqual(one_sided_positive_p(1.0, 0.04), 0.02)
        self.assertAlmostEqual(one_sided_positive_p(-1.0, 0.04), 0.98)

    def test_revised_h1_primary_classification_is_not_rmse_gated(self) -> None:
        """Support co-primary H1 directly from coefficients, not M1-first RMSE."""

        row = pd.Series({
            "couples": 84,
            "people": 168,
            "compliance_target": 0.75,
            "missingness_strength": 1.0,
            "truth": "M3",
            "replication": 0,
            "people_with_minimum_lags": 150,
            "M2_converged": True,
            "M3_converged": True,
            "M2_r_star_wp10_estimate": 2.0,
            "M2_r_star_wp10_se": 0.2,
            "M2_r_star_wp10_pvalue": 1e-8,
            "M3_e_wp10_estimate": 1.5,
            "M3_e_wp10_se": 0.2,
            "M3_e_wp10_pvalue": 1e-8,
            "M2_d_sym_estimate": 0.1,
            "M2_d_sym_se": 0.2,
            "delta_M1_M0": 0.5,
            "delta_M1_M0_ci_low": 0.1,
            "delta_M1_M0_ci_high": 0.9,
            "delta_M1_M0_n": 84,
        })
        result = classify_replication(row, self.config)
        self.assertEqual(result["H1_primary_result"], "full_support")
        self.assertTrue(result["H1_P1_supported"])
        self.assertTrue(result["H1_P2_supported"])
        self.assertEqual(
            result["M2_symmetry_result"],
            "symmetry_compatible",
        )

    def test_operating_characteristics_report_mc_precision(self) -> None:
        """Attach Monte Carlo sampling precision to decision probabilities."""

        probability, se, low, high = binomial_precision(800, 1000)
        self.assertAlmostEqual(probability, 0.8)
        self.assertGreater(se, 0.0)
        self.assertLess(low, probability)
        self.assertGreater(high, probability)

    def test_sesoi_classifies_symmetry_interval(self) -> None:
        """Recognize a symmetry interval contained inside the SESOI region."""

        frame = pd.DataFrame([{
            "couples": 72,
            "compliance_target": 0.75,
            "missingness_strength": 0.0,
            "truth": "M3",
            "M2_d_sym_ci_low": -0.2,
            "M2_d_sym_ci_high": 0.2,
        }])
        result = sesoi_operating_characteristics(frame, [0.5])
        self.assertAlmostEqual(
            float(result.iloc[0]["symmetry_equivalence_rate"]),
            1.0,
        )

    def test_smoke_run_fits_all_models(self) -> None:
        """Run one deterministic M0 and M3 smoke replication."""

        rows = run(self.config, replications=1, smoke=True)
        self.assertEqual(len(rows), 2)
        self.assertEqual(
            {row["truth"] for row in rows},
            {"M0", "M3"},
        )
        for row in rows:
            self.assertTrue(row["all_models_converged"])
            self.assertGreater(row["train_lags"], 0)
            self.assertGreater(row["test_lags"], 0)

    def test_response_history_uses_only_prior_observed_values(self) -> None:
        """Do not use the current prompt response to predict itself."""

        scenario = Scenario(4, 0.90, 1.0, "M3")
        rng = np.random.default_rng(20260930)
        prompts = simulate_prompt_panel(self.config, scenario, rng)
        history = response_history(
            prompts,
            int(self.config["training_days"]),
        )
        participant = history["participant_id"].iloc[0]
        subset = history[
            history["participant_id"] == participant
        ].sort_values(["day", "prompt_stratum"])
        first = subset.iloc[0]
        self.assertEqual(first["no_observed_history"], 1)
        self.assertAlmostEqual(float(first["prior_response_rate"]), 1.0)

    def test_ipw_weights_are_finite_and_training_normalized(self) -> None:
        """Construct leakage-safe stabilized weights for valid lags."""

        scenario = Scenario(12, 0.85, 1.0, "M3")
        rng = np.random.default_rng(20261001)
        prompts = simulate_prompt_panel(self.config, scenario, rng)
        train, test, diagnostics = build_ipw_analysis_data(
            prompts,
            self.config,
            probability_floor=0.02,
            lower_quantile=0.01,
            upper_quantile=0.99,
        )
        self.assertGreater(len(train), 0)
        self.assertGreater(len(test), 0)
        self.assertTrue(np.isfinite(train["ipw"]).all())
        self.assertTrue((train["ipw"] > 0).all())
        self.assertAlmostEqual(
            float(train["ipw"].mean()),
            1.0,
            places=10,
        )
        self.assertGreater(
            diagnostics["ipw_training_ess_fraction"],
            0.0,
        )
        self.assertLessEqual(
            diagnostics["ipw_training_ess_fraction"],
            1.0 + 1e-12,
        )

    def test_weighted_gee_fits_with_locked_covariance(self) -> None:
        """Verify statsmodels weighted GEE under the pinned H1 setup."""

        scenario = Scenario(20, 0.85, 0.0, "M3")
        rng = np.random.default_rng(20261002)
        prompts = simulate_prompt_panel(self.config, scenario, rng)
        train, test, _ = build_ipw_analysis_data(
            prompts,
            self.config,
            probability_floor=0.02,
            lower_quantile=0.01,
            upper_quantile=0.99,
        )
        result = fit_weighted_gee("M3", train)
        self.assertTrue(result.converged)
        self.assertEqual(result.cov_type, "robust")
        prediction = np.asarray(result.predict(test))
        self.assertEqual(len(prediction), len(test))
        self.assertTrue(np.isfinite(prediction).all())

    def test_ipw_truncation_uses_training_bounds_only(self) -> None:
        """Apply train-derived bounds unchanged to the holdout."""

        train = pd.DataFrame(
            {
                "participant_id": ["p1", "p1", "p2"],
                "day": [1, 2, 3],
                "prompt_stratum": [2, 3, 4],
            }
        )
        test = pd.DataFrame(
            {
                "participant_id": ["p1"],
                "day": [12],
                "prompt_stratum": [2],
            }
        )
        weights = pd.DataFrame(
            {
                "participant_id": ["p1", "p1", "p2", "p1"],
                "day": [1, 2, 3, 12],
                "prompt_stratum": [2, 3, 4, 2],
                "ipw_raw": [0.5, 1.0, 2.0, 100.0],
            }
        )
        weighted_train, weighted_test, diagnostics = (
            attach_truncated_ipw(
                train,
                test,
                weights,
                lower_quantile=0.0,
                upper_quantile=1.0,
            )
        )
        self.assertAlmostEqual(
            diagnostics["ipw_upper_bound"],
            2.0,
        )
        self.assertLess(
            float(weighted_test["ipw"].iloc[0]),
            10.0,
        )
        self.assertAlmostEqual(
            float(weighted_train["ipw"].mean()),
            1.0,
            places=12,
        )

    def test_replication_rng_uses_absolute_replication_id(self) -> None:
        """Require deterministic chunk-safe random streams."""

        scenario = Scenario(72, 0.75, 1.0, "M3")
        truth_index = list(self.config["truth_scenarios"]).index("M3")
        first = replication_rng(
            self.config,
            scenario,
            truth_index,
            125,
        ).normal(size=8)
        repeated = replication_rng(
            self.config,
            scenario,
            truth_index,
            125,
        ).normal(size=8)
        other = replication_rng(
            self.config,
            scenario,
            truth_index,
            126,
        ).normal(size=8)
        np.testing.assert_array_equal(first, repeated)
        self.assertFalse(np.array_equal(first, other))

    def test_merge_rejects_overlapping_replication_keys(self) -> None:
        """Do not silently double-weight duplicated compute."""

        frame = pd.DataFrame(
            [
                {
                    "couples": 72,
                    "compliance_target": 0.75,
                    "missingness_strength": 1.0,
                    "truth": "M3",
                    "replication": 10,
                },
                {
                    "couples": 72,
                    "compliance_target": 0.75,
                    "missingness_strength": 1.0,
                    "truth": "M3",
                    "replication": 10,
                },
            ]
        )
        with self.assertRaises(ValueError):
            validate_unique_replications(frame)

    def test_streaming_merge_handles_many_single_row_files_without_pandas(self) -> None:
        """Merge deterministic one-row chunks with the stdlib CSV path."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inputs = []
            fieldnames = [
                "couples",
                "people",
                "compliance_target",
                "missingness_strength",
                "truth",
                "replication",
                "M4_converged",
                "M4_d_asym_estimate",
                "M4_d_asym_se",
            ]
            for rep in range(8):
                path = root / f"rep-{rep:04d}.csv"
                with path.open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({
                        "couples": 84,
                        "people": 168,
                        "compliance_target": 0.75,
                        "missingness_strength": 0,
                        "truth": "M4",
                        "replication": rep,
                        "M4_converged": True,
                        "M4_d_asym_estimate": 0.8,
                        "M4_d_asym_se": 0.1,
                    })
                inputs.append(path)

            output = root / "merged"
            manifest = merge_files(inputs, output, 8)
            self.assertEqual(manifest["input_rows"], 8)
            self.assertEqual(manifest["scenario_count"], 1)
            self.assertFalse(manifest["pandas_used_for_merge"])
            self.assertTrue(
                (output / "h1_exact_replications.csv").stat().st_size > 0
            )
            self.assertTrue(
                (output / "h1_exact_summary.csv").stat().st_size > 0
            )
            self.assertEqual(
                manifest["coverage"][0]["missing_count"],
                0,
            )

    def test_streaming_merge_unions_m3_m4_optional_columns(self) -> None:
        """Allow truth-specific metric columns while keeping strict keys."""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            common = [
                "couples",
                "people",
                "compliance_target",
                "missingness_strength",
                "truth",
                "replication",
            ]
            specs = [
                (
                    "M3",
                    ["M3_e_wp10_truth", "M3_e_wp10_bias"],
                    {"M3_e_wp10_truth": "1.5", "M3_e_wp10_bias": "0.01"},
                ),
                (
                    "M4",
                    [
                        "M4_e_positive_wp10_truth",
                        "M4_e_positive_wp10_bias",
                        "M4_e_negative_wp10_truth",
                    ],
                    {
                        "M4_e_positive_wp10_truth": "2.0",
                        "M4_e_positive_wp10_bias": "0.02",
                        "M4_e_negative_wp10_truth": "-1.2",
                    },
                ),
            ]
            inputs = []
            for index, (truth, optional, values) in enumerate(specs):
                path = root / f"{truth}.csv"
                fields = common + optional
                with path.open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fields)
                    writer.writeheader()
                    row = {
                        "couples": 84,
                        "people": 168,
                        "compliance_target": 0.75,
                        "missingness_strength": 0,
                        "truth": truth,
                        "replication": 0,
                        **values,
                    }
                    writer.writerow(row)
                inputs.append(path)

            output = root / "merged"
            manifest = merge_files(inputs, output, 1)
            self.assertEqual(manifest["input_rows"], 2)
            with (output / "h1_exact_replications.csv").open(
                "r", newline="", encoding="utf-8"
            ) as handle:
                reader = csv.DictReader(handle)
                fields = set(reader.fieldnames or [])
                rows = list(reader)

            self.assertIn("M3_e_wp10_truth", fields)
            self.assertIn("M4_e_positive_wp10_truth", fields)
            self.assertEqual(len(rows), 2)
            m3 = next(row for row in rows if row["truth"] == "M3")
            m4 = next(row for row in rows if row["truth"] == "M4")
            self.assertEqual(m3["M4_e_positive_wp10_truth"], "")
            self.assertEqual(m4["M3_e_wp10_truth"], "")

    def test_merge_manifest_scalars_are_json_native(self) -> None:
        """Convert NumPy scalar keys to JSON-serializable Python values."""

        self.assertIsInstance(json_scalar(np.int64(72)), int)
        self.assertIsInstance(json_scalar(np.float64(0.75)), float)
        self.assertEqual(json_scalar(np.int64(72)), 72)
        self.assertEqual(json_scalar(np.float64(0.75)), 0.75)

    def test_merge_requires_complete_expected_range(self) -> None:
        """Validate an exact 0..N-1 replication range."""

        frame = pd.DataFrame(
            [
                {
                    "couples": 72,
                    "compliance_target": 0.75,
                    "missingness_strength": 1.0,
                    "truth": "M3",
                    "replication": rep,
                }
                for rep in range(4)
            ]
        )
        coverage = validate_expected_replications(frame, 4)
        self.assertEqual(len(coverage), 1)
        self.assertEqual(coverage[0]["rows"], 4)

        incomplete = frame[frame["replication"] != 2]
        with self.assertRaises(ValueError):
            validate_expected_replications(incomplete, 4)


if __name__ == "__main__":
    unittest.main()
