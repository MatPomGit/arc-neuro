# SPDX-License-Identifier: Apache-2.0
# Modified in ARC Neuro: update example commands and protocol paths.
"""History-based IPW-GEE sensitivity for ARC H1 missing prompts.

The primary H1 estimator remains the locked unweighted couple-clustered GEE.
This module implements a prespecified missing-at-random sensitivity analysis
using stabilized inverse-probability-of-observation weights estimated from
training-period response history only.

Important limitation:
The exact-design generator's strongest informative-missingness condition may
depend on contemporaneous values that would be unobserved when a prompt is
missed. That condition is intentionally an MNAR-like stress test. History-based
IPW is not claimed to remove bias under that mechanism.

Usage:
    python manuscripts/MSC-ATTACH-P01/analysis/h1_ipw_sensitivity.py \
        --config manuscripts/MSC-ATTACH-P01/protocol/exact_design_config.json \
        --output-dir /tmp/h1-ipw \
        --couples 72 \
        --compliance 0.75 \
        --missingness 1 \
        --truth M3 \
        --replications 20
"""

from __future__ import annotations

import argparse
import math
import warnings
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

from h1_inference_analysis import (
    holm_adjust,
    one_sided_positive_p,
    sesoi_one_sided_p,
)
from h1_exact_monte_carlo import (
    MODEL_TERMS,
    TRUTH_MAP,
    Scenario,
    build_valid_lags,
    fit_gee,
    load_config,
    model_formula,
    participant_rmse,
    prepare_analysis_data,
    replication_rng,
    simulate_prompt_panel,
    truth_effects,
    write_csv,
)

DENOMINATOR_FORMULA = (
    "observed_int ~ C(prompt_stratum) + day_c + "
    "prior_response_rate + previous_observed + no_observed_history + "
    "history_negative_affect10 + history_abs_e10 + history_abs_action10"
)
NUMERATOR_FORMULA = (
    "observed_int ~ C(prompt_stratum) + day_c"
)


def response_history(
    prompt_data: pd.DataFrame,
    training_days: int,
) -> pd.DataFrame:
    """Create predictors known before each scheduled prompt.

    Last-observed psychological values are carried forward only as predictors
    of response probability. They are never used to reconstruct a missed H1
    response or outcome. The implementation avoids pandas row-object
    conversion in the Monte Carlo hot path.
    """

    rows: list[dict[str, Any]] = []
    ordered = prompt_data.sort_values(
        ["participant_id", "day", "prompt"],
        kind="stable",
    )

    for participant_id, group in ordered.groupby(
        "participant_id",
        sort=False,
        observed=True,
    ):
        couple_id = group["couple_id"].to_numpy(copy=False)
        day_values = group["day"].to_numpy(dtype=np.int64, copy=False)
        prompt_values = group["prompt"].to_numpy(
            dtype=np.int64,
            copy=False,
        )
        observed_values = group["observed"].to_numpy(
            dtype=bool,
            copy=False,
        )
        negative_affect = group["negative_affect"].to_numpy(
            dtype=float,
            copy=False,
        )
        discrepancy = group["e"].to_numpy(dtype=float, copy=False)
        action = group["action"].to_numpy(dtype=float, copy=False)

        prior_total = 0
        prior_observed = 0
        previous_observed = 0
        last_observed_index: int | None = None

        for index in range(len(group)):
            no_history = int(last_observed_index is None)
            if last_observed_index is None:
                hist_negative_affect10 = 0.0
                hist_abs_e10 = 0.0
                hist_abs_action10 = 0.0
            else:
                hist_negative_affect10 = (
                    float(negative_affect[last_observed_index]) - 25.0
                ) / 10.0
                hist_abs_e10 = abs(
                    float(discrepancy[last_observed_index])
                ) / 10.0
                hist_abs_action10 = abs(
                    float(action[last_observed_index])
                ) / 10.0

            prior_response_rate = (
                prior_observed / prior_total
                if prior_total
                else 1.0
            )
            day = int(day_values[index])
            prompt = int(prompt_values[index])
            current_observed = int(bool(observed_values[index]))
            rows.append(
                {
                    "couple_id": couple_id[index],
                    "participant_id": participant_id,
                    "day": day,
                    "prompt_stratum": prompt,
                    "observed_int": current_observed,
                    "day_c": (
                        day - (training_days + 1) / 2.0
                    ) / float(training_days),
                    "prior_response_rate": float(
                        prior_response_rate
                    ),
                    "previous_observed": int(previous_observed),
                    "no_observed_history": no_history,
                    "history_negative_affect10": (
                        hist_negative_affect10
                    ),
                    "history_abs_e10": hist_abs_e10,
                    "history_abs_action10": hist_abs_action10,
                }
            )

            prior_total += 1
            prior_observed += current_observed
            previous_observed = current_observed
            if current_observed:
                last_observed_index = index

    return pd.DataFrame.from_records(rows)


def fit_response_models(
    history: pd.DataFrame,
    training_days: int,
) -> tuple[Any, Any]:
    """Fit stabilized-weight numerator and denominator models on training."""

    train = history[history["day"] <= training_days].copy()
    numerator = smf.glm(
        NUMERATOR_FORMULA,
        data=train,
        family=sm.families.Binomial(),
    ).fit(maxiter=100, tol=1e-8)
    denominator = smf.glm(
        DENOMINATOR_FORMULA,
        data=train,
        family=sm.families.Binomial(),
    ).fit(maxiter=100, tol=1e-8)
    return numerator, denominator


def prompt_observation_weights(
    history: pd.DataFrame,
    numerator: Any,
    denominator: Any,
    *,
    probability_floor: float,
) -> pd.DataFrame:
    """Predict stabilized prompt observation weights without holdout fitting."""

    if not 0.0 < probability_floor < 0.5:
        raise ValueError("probability_floor must be in (0, 0.5)")

    result = history.copy()
    p_num_raw = np.asarray(
        numerator.predict(result),
        dtype=float,
    )
    p_den_raw = np.asarray(
        denominator.predict(result),
        dtype=float,
    )
    p_num = np.clip(
        p_num_raw,
        probability_floor,
        1.0 - probability_floor,
    )
    p_den = np.clip(
        p_den_raw,
        probability_floor,
        1.0 - probability_floor,
    )
    result["response_p_numerator_raw"] = p_num_raw
    result["response_p_denominator_raw"] = p_den_raw
    result["response_p_numerator"] = p_num
    result["response_p_denominator"] = p_den
    result["prompt_stabilized_weight"] = p_num / p_den
    return result


def lag_observation_weights(
    prompt_weights: pd.DataFrame,
    lag_data: pd.DataFrame,
) -> pd.DataFrame:
    """Attach product weights for the two observed prompts defining each lag."""

    keys = ["participant_id", "day", "prompt_stratum"]
    base = prompt_weights[
        keys + ["prompt_stabilized_weight"]
    ].copy()

    next_weights = base.rename(
        columns={"prompt_stabilized_weight": "next_prompt_weight"}
    )
    current_weights = base.rename(
        columns={"prompt_stabilized_weight": "current_prompt_weight"}
    )
    current_weights["prompt_stratum"] = (
        current_weights["prompt_stratum"].astype(int) + 1
    )

    result = lag_data[keys].copy()
    result = result.merge(
        current_weights,
        on=keys,
        how="left",
        validate="one_to_one",
    )
    result = result.merge(
        next_weights,
        on=keys,
        how="left",
        validate="one_to_one",
    )
    if result[
        ["current_prompt_weight", "next_prompt_weight"]
    ].isna().any().any():
        raise ValueError("missing prompt observation weight for a valid lag")

    result["ipw_raw"] = (
        result["current_prompt_weight"]
        * result["next_prompt_weight"]
    )
    return result[keys + ["ipw_raw"]]


def attach_truncated_ipw(
    train: pd.DataFrame,
    test: pd.DataFrame,
    lag_weights: pd.DataFrame,
    *,
    lower_quantile: float,
    upper_quantile: float,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    """Truncate and normalize weights using training lags only."""

    if not 0.0 <= lower_quantile < upper_quantile <= 1.0:
        raise ValueError("invalid weight truncation quantiles")

    keys = ["participant_id", "day", "prompt_stratum"]
    weighted_train = train.merge(
        lag_weights,
        on=keys,
        how="left",
        validate="one_to_one",
    )
    weighted_test = test.merge(
        lag_weights,
        on=keys,
        how="left",
        validate="one_to_one",
    )
    if weighted_train["ipw_raw"].isna().any():
        raise ValueError("missing IPW for one or more training lags")
    if weighted_test["ipw_raw"].isna().any():
        raise ValueError("missing IPW for one or more test lags")

    lower = float(
        weighted_train["ipw_raw"].quantile(lower_quantile)
    )
    upper = float(
        weighted_train["ipw_raw"].quantile(upper_quantile)
    )
    train_truncated = weighted_train["ipw_raw"].clip(
        lower=lower,
        upper=upper,
    )
    test_truncated = weighted_test["ipw_raw"].clip(
        lower=lower,
        upper=upper,
    )
    normalization = float(train_truncated.mean())
    if not math.isfinite(normalization) or normalization <= 0:
        raise ValueError("invalid mean stabilized weight")

    weighted_train["ipw"] = train_truncated / normalization
    weighted_test["ipw"] = test_truncated / normalization

    weights = weighted_train["ipw"].to_numpy(dtype=float)
    ess = float(
        weights.sum() ** 2 / np.square(weights).sum()
    )
    raw_train = weighted_train["ipw_raw"]
    truncated_fraction = float(
        ((raw_train < lower) | (raw_train > upper)).mean()
    )
    diagnostics = {
        "ipw_lower_bound": lower,
        "ipw_upper_bound": upper,
        "ipw_raw_training_max": float(raw_train.max()),
        "ipw_truncated_fraction": truncated_fraction,
        "ipw_training_mean": float(
            weighted_train["ipw"].mean()
        ),
        "ipw_training_max": float(
            weighted_train["ipw"].max()
        ),
        "ipw_training_ess": ess,
        "ipw_training_ess_fraction": (
            ess / len(weighted_train)
            if len(weighted_train)
            else float("nan")
        ),
    }
    return weighted_train, weighted_test, diagnostics


def fit_weighted_gee(
    model_name: str,
    train: pd.DataFrame,
) -> Any:
    """Fit the locked GEE mean model with stabilized observation weights.

    The weighted sensitivity uses the ordinary robust sandwich covariance.
    In statsmodels 0.15.0, combining observation weights with the
    bias-reduced covariance fails inside the finite-cluster covariance
    calculation. The primary unweighted H1 GEE remains bias-reduced.
    Weighted finite-cluster coverage is therefore evaluated explicitly in
    the targeted Monte Carlo.
    """

    model = smf.gee(
        model_formula(model_name),
        groups="couple_id",
        data=train,
        weights=train["ipw"],
        family=sm.families.Gaussian(),
        cov_struct=sm.cov_struct.Independence(),
    )
    return model.fit(
        cov_type="robust",
        maxiter=100,
        ctol=1e-8,
    )


def build_ipw_analysis_data(
    prompt_data: pd.DataFrame,
    config: dict[str, Any],
    *,
    probability_floor: float,
    lower_quantile: float,
    upper_quantile: float,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    """Prepare leakage-safe weighted train/test lag data."""

    lag_data = build_valid_lags(prompt_data, config)
    train, test = prepare_analysis_data(
        prompt_data,
        lag_data,
        config,
    )
    history = response_history(
        prompt_data,
        int(config["training_days"]),
    )
    numerator, denominator = fit_response_models(
        history,
        int(config["training_days"]),
    )
    predicted = prompt_observation_weights(
        history,
        numerator,
        denominator,
        probability_floor=probability_floor,
    )
    lag_weights = lag_observation_weights(
        predicted,
        lag_data,
    )
    weighted_train, weighted_test, diagnostics = (
        attach_truncated_ipw(
            train,
            test,
            lag_weights,
            lower_quantile=lower_quantile,
            upper_quantile=upper_quantile,
        )
    )
    den_raw = predicted["response_p_denominator_raw"]
    floor = float(probability_floor)
    diagnostics.update(
        {
            "response_denominator_raw_min": float(
                den_raw.min()
            ),
            "response_denominator_raw_p01": float(
                den_raw.quantile(0.01)
            ),
            "response_probability_floor_fraction": float(
                (
                    (den_raw < floor)
                    | (den_raw > 1.0 - floor)
                ).mean()
            ),
        }
    )
    return weighted_train, weighted_test, diagnostics


RELATIONAL_PARAMETERS = (
    "r_hat_wp10",
    "r_star_wp10",
    "e_wp10",
    "e_positive_wp10",
    "e_negative_wp10",
)


def add_parameter_operating_metrics(
    row: dict[str, Any],
    result: Any,
    *,
    analysis_label: str,
    model_name: str,
    truth_name: str,
    config: dict[str, Any],
) -> None:
    """Add coefficient, bias, coverage, and type-I diagnostics."""

    effects = truth_effects(config, truth_name)
    for name in RELATIONAL_PARAMETERS:
        if name not in result.params.index:
            continue
        prefix = f"{analysis_label}_{model_name}_{name}"
        estimate = float(result.params[name])
        se = float(result.bse[name])
        pvalue = float(result.pvalues[name])
        row[f"{prefix}_estimate"] = estimate
        row[f"{prefix}_se"] = se
        row[f"{prefix}_pvalue"] = pvalue
        row[f"{prefix}_significant_05"] = bool(pvalue < 0.05)

        truth: float | None = None
        if truth_name == "M0":
            truth = 0.0
        elif truth_name == model_name:
            truth_key = TRUTH_MAP.get(
                truth_name,
                {},
            ).get(f"{model_name}:{name}")
            if truth_key is not None:
                truth = float(effects[truth_key])

        if truth is None:
            continue
        row[f"{prefix}_truth"] = truth
        row[f"{prefix}_bias"] = estimate - truth
        row[f"{prefix}_covered95"] = bool(
            estimate - 1.959963984540054 * se
            <= truth
            <= estimate + 1.959963984540054 * se
        )


def add_structural_contrast_metrics(
    row: dict[str, Any],
    result: Any,
    *,
    analysis_label: str,
    model_name: str,
) -> None:
    """Add M2 symmetry and M4 asymmetry contrasts for sensitivity analysis."""

    covariance = result.cov_params()
    critical90 = 1.6448536269514722

    if model_name == "M2":
        names = ("r_hat_wp10", "r_star_wp10")
        if all(name in result.params.index for name in names):
            estimate = float(
                result.params["r_hat_wp10"]
                + result.params["r_star_wp10"]
            )
            variance = float(
                covariance.loc["r_hat_wp10", "r_hat_wp10"]
                + covariance.loc["r_star_wp10", "r_star_wp10"]
                + 2.0 * covariance.loc["r_hat_wp10", "r_star_wp10"]
            )
            se = math.sqrt(max(variance, 0.0))
            prefix = f"{analysis_label}_M2_d_sym"
            row[f"{prefix}_estimate"] = estimate
            row[f"{prefix}_se"] = se
            row[f"{prefix}_ci90_low"] = estimate - critical90 * se
            row[f"{prefix}_ci90_high"] = estimate + critical90 * se

    if model_name == "M4":
        names = ("e_positive_wp10", "e_negative_wp10")
        if all(name in result.params.index for name in names):
            estimate = float(
                result.params["e_positive_wp10"]
                + result.params["e_negative_wp10"]
            )
            variance = float(
                covariance.loc["e_positive_wp10", "e_positive_wp10"]
                + covariance.loc["e_negative_wp10", "e_negative_wp10"]
                + 2.0 * covariance.loc[
                    "e_positive_wp10", "e_negative_wp10"
                ]
            )
            se = math.sqrt(max(variance, 0.0))
            prefix = f"{analysis_label}_M4_d_asym"
            row[f"{prefix}_estimate"] = estimate
            row[f"{prefix}_se"] = se
            row[f"{prefix}_ci90_low"] = estimate - critical90 * se
            row[f"{prefix}_ci90_high"] = estimate + critical90 * se


def add_revised_primary_inference(
    row: dict[str, Any],
    config: dict[str, Any],
    *,
    label: str,
) -> None:
    """Apply revised H1-P1/H1-P2 Holm+SESOI inference to one analysis."""

    final = dict(config.get("final_design", {}))
    alpha = float(final.get("familywise_alpha", 0.05))
    sesoi = float(final.get("primary_sesoi_beta", 0.5))
    specs = {
        "H1_P1": ("M2", "r_star_wp10"),
        "H1_P2": ("M3", "e_wp10"),
    }

    raw: dict[str, float] = {}
    for h, (model, parameter) in specs.items():
        prefix = f"{label}_{model}_{parameter}"
        estimate = float(row.get(f"{prefix}_estimate", float("nan")))
        se = float(row.get(f"{prefix}_se", float("nan")))
        p2 = float(row.get(f"{prefix}_pvalue", float("nan")))
        low95 = (
            estimate - 1.959963984540054 * se
            if np.isfinite(estimate) and np.isfinite(se)
            else float("nan")
        )
        p1 = one_sided_positive_p(estimate, p2)
        p_sesoi = sesoi_one_sided_p(estimate, se, sesoi)
        raw[h] = p_sesoi
        row[f"{label}_{h}_ci95_low"] = low95
        row[f"{label}_{h}_p_one_sided_zero"] = p1
        row[f"{label}_{h}_p_one_sided_sesoi"] = p_sesoi
        row[f"{label}_{h}_ci95_above_sesoi"] = bool(
            np.isfinite(low95) and low95 > sesoi
        )

    adjusted = holm_adjust(raw)
    support: dict[str, bool] = {}
    for h, (model, _) in specs.items():
        converged = bool(row.get(f"{model}_{label}_converged", False))
        value = adjusted[h]
        supported = bool(
            converged
            and np.isfinite(value)
            and value < alpha
        )
        support[h] = supported
        row[f"{label}_{h}_p_holm"] = value
        row[f"{label}_{h}_supported"] = supported

    n_supported = int(support["H1_P1"]) + int(support["H1_P2"])
    row[f"{label}_H1_primary_result"] = (
        "full_support"
        if n_supported == 2
        else "partial_support"
        if n_supported == 1
        else "no_confirmatory_support"
    )


def paired_rmse_delta(
    left: pd.Series,
    right: pd.Series,
) -> float:
    """Return mean participant-paired RMSE(left - right)."""

    paired = pd.concat(
        [left.rename("left"), right.rename("right")],
        axis=1,
        join="inner",
    ).dropna()
    if not len(paired):
        return float("nan")
    return float(
        (paired["left"] - paired["right"]).mean()
    )


def add_architecture_decisions(
    row: dict[str, Any],
    rmses: dict[str, pd.Series],
    config: dict[str, Any],
    *,
    label: str,
) -> None:
    """Add legacy sequential RMSE diagnostics for one analysis."""

    comparisons = (
        ("M1", "M0", "delta_M1_M0"),
        ("M2", "M1", "delta_M2_M1"),
        ("M3", "M2", "delta_M3_M2"),
        ("M4", "M3", "delta_M4_M3"),
        ("M4", "M2", "delta_M4_M2"),
    )
    for left, right, name in comparisons:
        value = (
            paired_rmse_delta(rmses[left], rmses[right])
            if left in rmses and right in rmses
            else float("nan")
        )
        row[f"{label}_{name}"] = value

    for margin_value in config["candidate_rmse_margins"]:
        margin = float(margin_value)
        suffix = str(margin).replace(".", "p")
        d10 = float(row[f"{label}_delta_M1_M0"])
        d21 = float(row[f"{label}_delta_M2_M1"])
        d32 = float(row[f"{label}_delta_M3_M2"])
        d43 = float(row[f"{label}_delta_M4_M3"])
        d42 = float(row[f"{label}_delta_M4_M2"])

        h1a1 = np.isfinite(d10) and d10 <= -margin
        h1a2 = np.isfinite(d21) and d21 <= -margin
        m3_noninferior = np.isfinite(d32) and d32 <= margin
        m4_better = np.isfinite(d43) and d43 <= -margin
        m4_noninferior = np.isfinite(d42) and d42 <= margin

        row[f"{label}_h1a1_margin_{suffix}"] = bool(h1a1)
        row[f"{label}_h1a2_margin_{suffix}"] = bool(h1a2)
        row[
            f"{label}_m3_noninferior_margin_{suffix}"
        ] = bool(m3_noninferior)
        row[
            f"{label}_m4_better_m3_margin_{suffix}"
        ] = bool(m4_better)
        row[
            f"{label}_m4_noninferior_m2_margin_{suffix}"
        ] = bool(m4_noninferior)

        if not h1a2:
            decision = "no_target_increment"
        elif m4_better and m4_noninferior:
            decision = "M4_asymmetric"
        elif m3_noninferior:
            decision = "M3_signed_discrepancy"
        else:
            decision = "M2_separate_components"
        row[
            f"{label}_representation_margin_{suffix}"
        ] = decision


def evaluate_ipw_replication(
    config: dict[str, Any],
    scenario: Scenario,
    rng: np.random.Generator,
    *,
    probability_floor: float,
    lower_quantile: float,
    upper_quantile: float,
) -> dict[str, Any]:
    """Compare primary and weighted GEE in one simulated replication."""

    prompt_data = simulate_prompt_panel(config, scenario, rng)
    lag_data = build_valid_lags(prompt_data, config)
    train, test = prepare_analysis_data(
        prompt_data,
        lag_data,
        config,
    )
    weighted_train, weighted_test, diagnostics = (
        build_ipw_analysis_data(
            prompt_data,
            config,
            probability_floor=probability_floor,
            lower_quantile=lower_quantile,
            upper_quantile=upper_quantile,
        )
    )

    row: dict[str, Any] = {
        "couples": scenario.couples,
        "compliance_target": scenario.compliance,
        "missingness_strength": scenario.missingness_strength,
        "truth": scenario.truth,
        **diagnostics,
    }

    primary_rmses: dict[str, pd.Series] = {}
    ipw_rmses: dict[str, pd.Series] = {}

    for model_name in MODEL_TERMS:
        with warnings.catch_warnings(record=True) as primary_warnings:
            warnings.simplefilter("always")
            primary = fit_gee(model_name, train)
        with warnings.catch_warnings(record=True) as ipw_warnings:
            warnings.simplefilter("always")
            weighted = fit_weighted_gee(
                model_name,
                weighted_train,
            )

        row[f"{model_name}_primary_converged"] = bool(
            primary.converged
        )
        row[f"{model_name}_ipw_converged"] = bool(
            weighted.converged
        )
        row[f"{model_name}_primary_warnings"] = len(
            primary_warnings
        )
        row[f"{model_name}_ipw_warnings"] = len(
            ipw_warnings
        )

        primary_rmse = participant_rmse(
            test,
            np.asarray(primary.predict(test)),
            int(config["minimum_holdout_lag_pairs"]),
        )
        weighted_rmse = participant_rmse(
            weighted_test,
            np.asarray(weighted.predict(weighted_test)),
            int(config["minimum_holdout_lag_pairs"]),
        )
        common = primary_rmse.index.intersection(
            weighted_rmse.index
        )
        primary_rmses[model_name] = primary_rmse.loc[common]
        ipw_rmses[model_name] = weighted_rmse.loc[common]
        row[f"{model_name}_primary_mean_rmse"] = float(
            primary_rmse.loc[common].mean()
        )
        row[f"{model_name}_ipw_mean_rmse"] = float(
            weighted_rmse.loc[common].mean()
        )
        row[f"{model_name}_ipw_minus_primary_rmse"] = float(
            (
                weighted_rmse.loc[common]
                - primary_rmse.loc[common]
            ).mean()
        )

        add_parameter_operating_metrics(
            row,
            primary,
            analysis_label="primary",
            model_name=model_name,
            truth_name=scenario.truth,
            config=config,
        )
        add_parameter_operating_metrics(
            row,
            weighted,
            analysis_label="ipw",
            model_name=model_name,
            truth_name=scenario.truth,
            config=config,
        )

        add_structural_contrast_metrics(
            row,
            primary,
            analysis_label="primary",
            model_name=model_name,
        )
        add_structural_contrast_metrics(
            row,
            weighted,
            analysis_label="ipw",
            model_name=model_name,
        )

    add_revised_primary_inference(
        row,
        config,
        label="primary",
    )
    add_revised_primary_inference(
        row,
        config,
        label="ipw",
    )
    row["revised_H1_primary_ipw_agreement"] = bool(
        row["primary_H1_primary_result"]
        == row["ipw_H1_primary_result"]
    )

    # Legacy sequential RMSE decisions are retained for historical diagnostic
    # comparison only and are not the primary sensitivity conclusion.
    add_architecture_decisions(
        row,
        primary_rmses,
        config,
        label="primary",
    )
    add_architecture_decisions(
        row,
        ipw_rmses,
        config,
        label="ipw",
    )
    for margin_value in config["candidate_rmse_margins"]:
        suffix = str(float(margin_value)).replace(".", "p")
        primary_decision = row[
            f"primary_representation_margin_{suffix}"
        ]
        ipw_decision = row[
            f"ipw_representation_margin_{suffix}"
        ]
        row[
            f"legacy_decision_agreement_margin_{suffix}"
        ] = bool(primary_decision == ipw_decision)

    return row


def run(
    config: dict[str, Any],
    *,
    couples: int,
    compliance: float,
    missingness: float,
    truth: str,
    rep_start: int,
    replications: int,
    probability_floor: float,
    lower_quantile: float,
    upper_quantile: float,
) -> list[dict[str, Any]]:
    """Run one targeted deterministic IPW sensitivity scenario."""

    if truth not in MODEL_TERMS:
        raise ValueError(f"unsupported truth: {truth}")
    scenario = Scenario(
        int(couples),
        float(compliance),
        float(missingness),
        truth,
    )
    truth_index = list(config["truth_scenarios"]).index(truth)
    rows: list[dict[str, Any]] = []
    for rep in range(rep_start, rep_start + replications):
        rng = replication_rng(
            config,
            scenario,
            truth_index,
            rep,
        )
        row = evaluate_ipw_replication(
            config,
            scenario,
            rng,
            probability_floor=probability_floor,
            lower_quantile=lower_quantile,
            upper_quantile=upper_quantile,
        )
        row["replication"] = rep
        rows.append(row)
    return rows


def summarize_ipw_rows(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Aggregate IPW operating characteristics by truncation scenario."""

    frame = pd.DataFrame(rows)
    keys = [
        "couples",
        "compliance_target",
        "missingness_strength",
        "truth",
        "truncation_lower_quantile",
        "truncation_upper_quantile",
    ]
    summaries: list[dict[str, Any]] = []
    for values, group in frame.groupby(
        keys,
        dropna=False,
        sort=True,
    ):
        summary = dict(zip(keys, values, strict=True))
        summary["replications"] = int(len(group))
        for column in group.columns:
            if column in keys:
                continue
            if pd.api.types.is_bool_dtype(group[column]):
                summary[f"p_{column}"] = float(
                    group[column].astype(float).mean()
                )
            elif pd.api.types.is_numeric_dtype(group[column]):
                summary[f"mean_{column}"] = float(
                    pd.to_numeric(
                        group[column],
                        errors="coerce",
                    ).mean()
                )
        decision_columns = [
            column
            for column in group.columns
            if (
                "representation_margin_" in column
                and (
                    column.startswith("primary_")
                    or column.startswith("ipw_")
                )
            )
        ]
        for column in decision_columns:
            frequencies = group[column].value_counts(
                normalize=True,
                dropna=False,
            )
            for value, probability in frequencies.items():
                summary[
                    f"p_{column}_{value}"
                ] = float(probability)
        summaries.append(summary)
    return summaries


def main() -> None:
    """Run targeted IPW-GEE missingness sensitivity."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--couples", type=int, required=True)
    parser.add_argument("--compliance", type=float, required=True)
    parser.add_argument("--missingness", type=float, required=True)
    parser.add_argument("--truth", choices=tuple(MODEL_TERMS), required=True)
    parser.add_argument("--rep-start", type=int, default=0)
    parser.add_argument("--replications", type=int, default=20)
    parser.add_argument("--probability-floor", type=float, default=None)
    parser.add_argument("--lower-quantile", type=float, default=None)
    parser.add_argument("--upper-quantile", type=float, default=None)
    parser.add_argument(
        "--all-truncation-candidates",
        action="store_true",
        help=(
            "Run every truncation pair in exact_design_config.json "
            "on identical deterministic replications."
        ),
    )
    args = parser.parse_args()

    config = load_config(args.config)
    ipw_config = config["ipw_sensitivity"]
    probability_floor = (
        float(args.probability_floor)
        if args.probability_floor is not None
        else float(ipw_config["probability_floor"])
    )
    if args.all_truncation_candidates and (
        args.lower_quantile is not None
        or args.upper_quantile is not None
    ):
        raise ValueError(
            "explicit truncation quantiles cannot be combined with "
            "--all-truncation-candidates"
        )

    if args.all_truncation_candidates:
        candidates = [
            (float(pair[0]), float(pair[1]))
            for pair in ipw_config[
                "candidate_truncation_quantiles"
            ]
        ]
    else:
        provisional = ipw_config[
            "provisional_truncation_quantiles"
        ]
        candidates = [
            (
                float(args.lower_quantile)
                if args.lower_quantile is not None
                else float(provisional[0]),
                float(args.upper_quantile)
                if args.upper_quantile is not None
                else float(provisional[1]),
            )
        ]

    rows: list[dict[str, Any]] = []
    for lower_quantile, upper_quantile in candidates:
        candidate_rows = run(
            config,
            couples=args.couples,
            compliance=args.compliance,
            missingness=args.missingness,
            truth=args.truth,
            rep_start=args.rep_start,
            replications=args.replications,
            probability_floor=probability_floor,
            lower_quantile=lower_quantile,
            upper_quantile=upper_quantile,
        )
        for row in candidate_rows:
            row["truncation_lower_quantile"] = lower_quantile
            row["truncation_upper_quantile"] = upper_quantile
        rows.extend(candidate_rows)

    summaries = summarize_ipw_rows(rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        args.output_dir / "h1_ipw_sensitivity.csv",
        rows,
    )
    write_csv(
        args.output_dir / "h1_ipw_sensitivity_summary.csv",
        summaries,
    )
    print(f"IPW sensitivity replications written: {len(rows)}")
    print(f"IPW sensitivity summaries written: {len(summaries)}")


if __name__ == "__main__":
    main()
