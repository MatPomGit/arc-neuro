# SPDX-License-Identifier: Apache-2.0
# Modified in ARC Neuro: update example commands and protocol paths.
"""Exact-design Monte Carlo for the ARC 2.0 H1 pilot.

Primary estimator: Gaussian GEE with identity link, couple-level clustering,
independence working correlation, and bias-reduced sandwich covariance.
The generator is intentionally richer than the fitted mean model and includes
couple/person random intercepts, participant-specific relational slope
heterogeneity, unequal intervals, dyadic/shared stress, and optional
state-dependent missingness.

Usage:
    python manuscripts/MSC-ATTACH-P01/analysis/h1_exact_monte_carlo.py \
        --config manuscripts/MSC-ATTACH-P01/protocol/exact_design_config.json \
        --output-dir manuscripts/MSC-ATTACH-P01/build/h1_exact_results
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import warnings
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

def suppress_windows_crash_dialogs() -> None:
    """Disable modal Windows crash dialogs for Monte Carlo worker processes.

    Native numerical-library faults must terminate the worker so the parent
    scheduler can retry or fall back to an isolated replication. Interactive
    WER/JIT dialogs would otherwise block unattended long-running simulations.
    """

    if sys.platform != "win32":
        return
    import ctypes

    sem_failcriticalerrors = 0x0001
    sem_nogpfault_errorbox = 0x0002
    sem_noopenfile_errorbox = 0x8000
    ctypes.windll.kernel32.SetErrorMode(
        sem_failcriticalerrors
        | sem_nogpfault_errorbox
        | sem_noopenfile_errorbox
    )


suppress_windows_crash_dialogs()

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import t as student_t

CONTINUOUS_MEAN_VARS = (
    "r_hat", "r_star", "e", "e_positive", "e_negative",
    "negative_affect", "action",
)
BINARY_MEAN_VARS = ("stressor", "contact")

COMMON_FORMULA = (
    "action_lag_wp10 + action_lag_mean10 + "
    "negative_affect_wp10 + negative_affect_mean10 + "
    "stressor_wp + stressor_mean + contact_wp + contact_mean + "
    "C(prompt_stratum) + elapsed_c"
)
MODEL_TERMS = {
    "M0": "",
    "M1": "r_hat_wp10 + r_hat_mean10",
    "M2": (
        "r_hat_wp10 + r_hat_mean10 + "
        "r_star_wp10 + r_star_mean10"
    ),
    "M3": "e_wp10 + e_mean10",
    "M4": (
        "e_positive_wp10 + e_positive_mean10 + "
        "e_negative_wp10 + e_negative_mean10"
    ),
}
TRUTH_MAP = {
    "M0": {},
    "M1": {"M1:r_hat_wp10": "state"},
    "M2": {
        "M2:r_hat_wp10": "state",
        "M2:r_star_wp10": "target",
    },
    "M3": {"M3:e_wp10": "discrepancy"},
    "M4": {
        "M4:e_positive_wp10": "positive",
        "M4:e_negative_wp10": "negative",
    },
}


@dataclass(frozen=True)
class Scenario:
    """One Monte Carlo scenario."""

    couples: int
    compliance: float
    missingness_strength: float
    truth: str


def expit(value: float) -> float:
    """Return a stable logistic transform."""

    clipped = max(-30.0, min(30.0, value))
    return 1.0 / (1.0 + math.exp(-clipped))


def logit(probability: float) -> float:
    """Return the logit of an open-unit probability."""

    if not 0.0 < probability < 1.0:
        raise ValueError("probability must be strictly between 0 and 1")
    return math.log(probability / (1.0 - probability))


def load_config(path: Path) -> dict[str, Any]:
    """Load and validate the exact-design configuration."""

    config = json.loads(path.read_text(encoding="utf-8"))
    if int(config["days"]) <= int(config["training_days"]):
        raise ValueError("days must exceed training_days")
    prompts = int(config["prompts_per_day"])
    if prompts < 2:
        raise ValueError("prompts_per_day must be at least 2")
    waking_hours = float(config["waking_hours"])
    if waking_hours <= 0:
        raise ValueError("waking_hours must be positive")
    minimum_separation = float(
        config["minimum_prompt_separation_hours"]
    )
    if minimum_separation <= 0:
        raise ValueError(
            "minimum_prompt_separation_hours must be positive"
        )
    stratum_width = waking_hours / prompts
    if minimum_separation >= 2.0 * stratum_width:
        raise ValueError(
            "minimum prompt separation is incompatible with adjacent strata"
        )
    response_window = float(config["response_window_minutes"])
    reminder_after = float(config["reminder_after_minutes"])
    if not 0 < reminder_after < response_window:
        raise ValueError(
            "reminder_after_minutes must fall inside the response window"
        )
    lag_min = float(config["valid_lag_min_hours"])
    lag_max = float(config["valid_lag_max_hours"])
    if not 0 < lag_min < lag_max:
        raise ValueError("valid lag bounds must satisfy 0 < min < max")
    if int(config["replications"]) <= 0:
        raise ValueError("replications must be positive")
    if any(
        float(value) < 0
        for value in config["candidate_rmse_margins"]
    ):
        raise ValueError("candidate RMSE margins must be non-negative")
    if "ipw_sensitivity" in config:
        ipw = config["ipw_sensitivity"]
        floor = float(ipw["probability_floor"])
        if not 0.0 < floor < 0.5:
            raise ValueError(
                "ipw probability_floor must be in (0, 0.5)"
            )
        candidates = [
            tuple(float(value) for value in pair)
            for pair in ipw["candidate_truncation_quantiles"]
        ]
        for lower, upper in candidates:
            if not 0.0 <= lower < upper <= 1.0:
                raise ValueError(
                    "invalid IPW truncation quantile pair"
                )
        provisional = tuple(
            float(value)
            for value in ipw["provisional_truncation_quantiles"]
        )
        if provisional not in candidates:
            raise ValueError(
                "provisional IPW truncation must be one of the candidates"
            )
    unsupported = set(config["truth_scenarios"]) - set(MODEL_TERMS)
    if unsupported:
        raise ValueError(f"unsupported truth scenarios: {sorted(unsupported)}")
    return config


def schedule_times(
    config: dict[str, Any],
    rng: np.random.Generator,
) -> np.ndarray:
    """Return one prompt time per equal stratum under locked spacing rules."""

    n = int(config["prompts_per_day"])
    waking_hours = float(config["waking_hours"])
    minimum_separation = float(
        config["minimum_prompt_separation_hours"]
    )
    stratum_width = waking_hours / n
    starts = np.arange(n, dtype=float) * stratum_width

    for _ in range(10_000):
        times = starts + rng.uniform(
            0.0,
            stratum_width,
            size=n,
        )
        if np.all(np.diff(times) >= minimum_separation):
            return times

    raise RuntimeError(
        "unable to generate a prompt schedule satisfying the locked "
        "minimum separation"
    )


def truth_effects(
    config: dict[str, Any],
    truth: str,
) -> dict[str, float]:
    """Return one truth scenario as floats."""

    values = config["truth_scenarios"][truth]
    required = {"state", "target", "discrepancy", "positive", "negative"}
    missing = required - set(values)
    if missing:
        raise ValueError(f"truth {truth} missing {sorted(missing)}")
    return {key: float(values[key]) for key in required}


def simulate_prompt_panel(
    config: dict[str, Any],
    scenario: Scenario,
    rng: np.random.Generator,
) -> pd.DataFrame:
    """Simulate prompt-level dyadic ESM data."""

    dyn = config["dynamics"]
    ctx = config["context_effects"]
    re_sd = config["random_effect_sd"]
    miss = config["missingness"]
    effects = truth_effects(config, scenario.truth)
    days = int(config["days"])
    prompts = int(config["prompts_per_day"])

    records: list[dict[str, Any]] = []
    person_index = 0

    for couple_index in range(scenario.couples):
        couple_id = f"c{couple_index:04d}"
        couple_action = rng.normal(
            0.0,
            float(re_sd["couple_action_intercept"]),
        )
        couple_state = rng.normal(
            0.0,
            float(re_sd["couple_state_mean"]),
        )
        couple_target = (
            float(dyn["between_state_target_correlation"]) * couple_state
            + rng.normal(
                0.0,
                float(re_sd["couple_target_residual"]),
            )
        )
        schedules = [
            schedule_times(config, rng)
            for _ in range(days)
        ]
        shared_stress = rng.random((days, prompts)) < float(
            dyn["shared_stressor_probability"]
        )

        for member in range(2):
            participant_id = f"p{person_index:05d}"
            person_index += 1
            person_action = rng.normal(
                0.0,
                float(re_sd["person_action_intercept"]),
            )
            random_slope = rng.normal(
                0.0,
                float(re_sd["person_relational_slope"]),
            )
            response_propensity = rng.normal(
                0.0,
                float(re_sd["response_propensity"]),
            )
            state_mean = (
                float(dyn["state_grand_mean"])
                + couple_state
                + rng.normal(
                    0.0,
                    float(re_sd["person_state_mean"]),
                )
            )
            target_mean = (
                float(dyn["target_grand_mean"])
                + couple_target
                + rng.normal(
                    0.0,
                    float(re_sd["person_target_mean"]),
                )
            )
            e_mean = target_mean - state_mean
            state_z = rng.normal()
            target_z = rng.normal()
            previous_action = rng.normal(
                0.0,
                float(dyn["initial_action_sd"]),
            )

            for day_idx in range(days):
                previous_prompt: dict[str, Any] | None = None
                scheduled_times = schedules[day_idx]

                for prompt_idx in range(prompts):
                    scheduled_hour = float(
                        scheduled_times[prompt_idx]
                    )
                    stressor = int(
                        shared_stress[day_idx, prompt_idx]
                        or rng.random()
                        < float(dyn["individual_stressor_probability"])
                    )
                    contact = int(
                        rng.random()
                        < float(dyn["contact_probability"])
                    )

                    rho_state = float(dyn["state_ar"])
                    state_z = (
                        rho_state * state_z
                        + rng.normal(
                            0.0,
                            math.sqrt(
                                max(1.0 - rho_state**2, 1e-8)
                            ),
                        )
                        - float(dyn["stressor_state_shift"]) * stressor
                    )
                    target_z = (
                        float(dyn["target_ar"]) * target_z
                        + float(dyn["state_to_target_coupling"]) * state_z
                        + rng.normal(
                            0.0,
                            float(dyn["target_innovation_sd"]),
                        )
                    )
                    r_hat = float(
                        np.clip(
                            state_mean
                            + float(dyn["state_within_sd"]) * state_z,
                            0.0,
                            100.0,
                        )
                    )
                    r_star = float(
                        np.clip(
                            target_mean
                            + float(dyn["target_within_sd"]) * target_z,
                            0.0,
                            100.0,
                        )
                    )
                    discrepancy = r_star - r_hat
                    e_positive = max(discrepancy, 0.0)
                    e_negative = max(-discrepancy, 0.0)
                    negative_affect = float(
                        np.clip(
                            float(dyn["negative_affect_base"])
                            + float(
                                dyn["negative_affect_stressor"]
                            ) * stressor
                            + float(
                                dyn["negative_affect_discrepancy"]
                            ) * abs(discrepancy)
                            + rng.normal(
                                0.0,
                                float(
                                    dyn["negative_affect_noise_sd"]
                                ),
                            ),
                            0.0,
                            100.0,
                        )
                    )

                    if prompt_idx == 0:
                        elapsed_hours = np.nan
                        action_unclipped = (
                            couple_action
                            + person_action
                            + float(
                                dyn["overnight_action_persistence"]
                            ) * previous_action
                            + rng.normal(
                                0.0,
                                float(dyn["action_residual_sd"]),
                            )
                        )
                    else:
                        assert previous_prompt is not None
                        elapsed_hours = float(
                            scheduled_times[prompt_idx]
                            - scheduled_times[prompt_idx - 1]
                        )
                        state_dev10 = (
                            previous_prompt["r_hat"] - state_mean
                        ) / 10.0
                        target_dev10 = (
                            previous_prompt["r_star"] - target_mean
                        ) / 10.0
                        discrepancy_dev10 = (
                            previous_prompt["e"] - e_mean
                        ) / 10.0
                        positive_dev10 = (
                            previous_prompt["e_positive"]
                            - max(e_mean, 0.0)
                        ) / 10.0
                        negative_dev10 = (
                            previous_prompt["e_negative"]
                            - max(-e_mean, 0.0)
                        ) / 10.0
                        relational = (
                            effects["state"] * state_dev10
                            + effects["target"] * target_dev10
                            + effects["discrepancy"]
                            * discrepancy_dev10
                            + effects["positive"]
                            * positive_dev10
                            + effects["negative"]
                            * negative_dev10
                        )
                        if scenario.truth == "M1":
                            relational += (
                                random_slope * state_dev10
                            )
                        elif scenario.truth == "M2":
                            relational += (
                                random_slope
                                * (target_dev10 - state_dev10)
                                / 2.0
                            )
                        elif scenario.truth == "M3":
                            relational += (
                                random_slope * discrepancy_dev10
                            )
                        elif scenario.truth == "M4":
                            relational += (
                                random_slope * positive_dev10
                                + 0.5
                                * random_slope
                                * negative_dev10
                            )

                        action_unclipped = (
                            couple_action
                            + person_action
                            + float(dyn["action_ar"])
                            * previous_action
                            + relational
                            + float(
                                ctx["negative_affect_per_10"]
                            )
                            * (
                                previous_prompt["negative_affect"]
                                - float(
                                    dyn["negative_affect_base"]
                                )
                            )
                            / 10.0
                            + float(ctx["stressor"])
                            * previous_prompt["stressor"]
                            + float(ctx["contact"])
                            * previous_prompt["contact"]
                            + float(ctx["elapsed_hour"])
                            * (
                                elapsed_hours
                                - float(
                                    config["elapsed_reference_hours"]
                                )
                            )
                            + rng.normal(
                                0.0,
                                float(dyn["action_residual_sd"]),
                            )
                        )

                    action = float(
                        np.clip(
                            action_unclipped,
                            -100.0,
                            100.0,
                        )
                    )
                    strength = float(
                        scenario.missingness_strength
                    )
                    observation_logit = (
                        logit(float(scenario.compliance))
                        + response_propensity
                        - strength
                        * float(
                            miss["negative_affect_logit_per_10"]
                        )
                        * (
                            negative_affect
                            - float(
                                dyn["negative_affect_base"]
                            )
                        )
                        / 10.0
                        - strength
                        * float(
                            miss["abs_discrepancy_logit_per_10"]
                        )
                        * abs(discrepancy)
                        / 10.0
                        - strength
                        * float(
                            miss["abs_action_logit_per_10"]
                        )
                        * abs(action)
                        / 10.0
                    )
                    observed = bool(
                        rng.random()
                        < expit(observation_logit)
                    )
                    response_window_hours = (
                        float(config["response_window_minutes"]) / 60.0
                    )
                    if observed:
                        response_latency_hours = float(
                            rng.beta(2.0, 5.0)
                            * response_window_hours
                        )
                        response_hour = (
                            scheduled_hour + response_latency_hours
                        )
                    else:
                        response_latency_hours = float("nan")
                        response_hour = float("nan")
                    prompt = {
                        "couple_id": couple_id,
                        "member": member,
                        "participant_id": participant_id,
                        "day": day_idx + 1,
                        "prompt": prompt_idx + 1,
                        "r_hat": r_hat,
                        "r_star": r_star,
                        "e": discrepancy,
                        "e_positive": e_positive,
                        "e_negative": e_negative,
                        "negative_affect": negative_affect,
                        "stressor": stressor,
                        "contact": contact,
                        "action": action,
                        "action_was_clipped": int(
                            action != action_unclipped
                        ),
                        "scheduled_hour": scheduled_hour,
                        "scheduled_elapsed_hours": elapsed_hours,
                        "response_latency_hours": response_latency_hours,
                        "response_hour": response_hour,
                        "observed": observed,
                    }
                    records.append(prompt)
                    previous_prompt = prompt
                    previous_action = action

    return pd.DataFrame.from_records(records)


def _valid_lag_indices(
    participant_codes: np.ndarray,
    day: np.ndarray,
    prompt: np.ndarray,
    observed: np.ndarray,
    response_hour: np.ndarray,
    min_hours: float,
    max_hours: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return comparable same-day adjacent-prompt lag indices.

    Prompt 1 -> 2 is excluded because the source action at prompt 1
    summarizes the overnight/first-of-day interval rather than the
    standardized same-day interval used by prompts 2 -> 6.
    """

    elapsed = response_hour[1:] - response_hour[:-1]
    valid = (
        (participant_codes[1:] == participant_codes[:-1])
        & (day[1:] == day[:-1])
        & (prompt[1:] == prompt[:-1] + 1)
        & (prompt[:-1] >= 2)
        & observed[:-1]
        & observed[1:]
        & (elapsed >= min_hours)
        & (elapsed <= max_hours)
    )
    return np.flatnonzero(valid), elapsed


def build_valid_lags(
    prompt_data: pd.DataFrame,
    config: dict[str, Any],
) -> pd.DataFrame:
    """Build same-day t->t+1 rows under locked response-time rules.

    The implementation is intentionally array-based. Repeated row-object
    conversion through pandas to_dict/itertuples produced native Windows
    crashes in long Monte Carlo runs. The lag definition itself is unchanged.
    """

    output_columns = [
        "couple_id",
        "member",
        "participant_id",
        "day",
        "prompt_stratum",
        "elapsed_hours",
        "action_next",
        "action_lag",
        "r_hat",
        "r_star",
        "e",
        "e_positive",
        "e_negative",
        "negative_affect",
        "stressor",
        "contact",
    ]
    if prompt_data.empty:
        return pd.DataFrame(columns=output_columns)

    ordered = prompt_data.sort_values(
        ["participant_id", "day", "prompt"],
        kind="stable",
    ).reset_index(drop=True)

    participant_codes = pd.factorize(
        ordered["participant_id"],
        sort=False,
    )[0].astype(np.int64, copy=False)
    day = ordered["day"].to_numpy(dtype=np.int64, copy=False)
    prompt = ordered["prompt"].to_numpy(dtype=np.int64, copy=False)
    observed = ordered["observed"].to_numpy(
        dtype=bool,
        copy=False,
    )
    response_hour = ordered["response_hour"].to_numpy(
        dtype=float,
        copy=False,
    )

    current_idx, elapsed = _valid_lag_indices(
        participant_codes,
        day,
        prompt,
        observed,
        response_hour,
        float(config["valid_lag_min_hours"]),
        float(config["valid_lag_max_hours"]),
    )
    next_idx = current_idx + 1
    if len(current_idx) == 0:
        return pd.DataFrame(columns=output_columns)

    def current(name: str) -> np.ndarray:
        return ordered[name].to_numpy(copy=False)[current_idx]

    def nxt(name: str) -> np.ndarray:
        return ordered[name].to_numpy(copy=False)[next_idx]

    return pd.DataFrame({
        "couple_id": current("couple_id"),
        "member": current("member").astype(int, copy=False),
        "participant_id": current("participant_id"),
        "day": nxt("day").astype(int, copy=False),
        "prompt_stratum": nxt("prompt").astype(int, copy=False),
        "elapsed_hours": elapsed[current_idx].astype(float, copy=False),
        "action_next": nxt("action").astype(float, copy=False),
        "action_lag": current("action").astype(float, copy=False),
        "r_hat": current("r_hat").astype(float, copy=False),
        "r_star": current("r_star").astype(float, copy=False),
        "e": current("e").astype(float, copy=False),
        "e_positive": current("e_positive").astype(float, copy=False),
        "e_negative": current("e_negative").astype(float, copy=False),
        "negative_affect": current("negative_affect").astype(float, copy=False),
        "stressor": current("stressor").astype(float, copy=False),
        "contact": current("contact").astype(float, copy=False),
    }, columns=output_columns)


def prepare_analysis_data(
    prompt_data: pd.DataFrame,
    lag_data: pd.DataFrame,
    config: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create leakage-safe training and temporal-holdout rows."""

    training_days = int(config["training_days"])
    observed_training = prompt_data[
        (prompt_data["day"] <= training_days)
        & prompt_data["observed"]
    ].copy()
    mean_vars = (
        list(CONTINUOUS_MEAN_VARS)
        + list(BINARY_MEAN_VARS)
    )
    means = (
        observed_training.groupby(
            "participant_id",
            observed=True,
        )[mean_vars]
        .mean()
        .add_suffix("_mean")
    )

    prepared: list[pd.DataFrame] = []
    for frame in (
        lag_data[
            lag_data["day"] <= training_days
        ].copy(),
        lag_data[
            lag_data["day"] > training_days
        ].copy(),
    ):
        data = frame.join(
            means,
            on="participant_id",
            how="inner",
        )
        for variable in CONTINUOUS_MEAN_VARS:
            source = (
                "action_lag"
                if variable == "action"
                else variable
            )
            mean_name = f"{variable}_mean"
            data[f"{source}_wp10"] = (
                data[source] - data[mean_name]
            ) / 10.0
            data[f"{source}_mean10"] = (
                data[mean_name] / 10.0
            )
        for variable in BINARY_MEAN_VARS:
            data[f"{variable}_wp"] = (
                data[variable]
                - data[f"{variable}_mean"]
            )
        data["elapsed_c"] = (
            data["elapsed_hours"]
            - float(config["elapsed_reference_hours"])
        )
        prepared.append(data)
    return prepared[0], prepared[1]


def model_formula(model_name: str) -> str:
    """Return the locked fixed-mean formula for one H1 model."""

    if model_name not in MODEL_TERMS:
        raise ValueError(
            f"unsupported model: {model_name}"
        )
    formula = f"action_next ~ {COMMON_FORMULA}"
    if MODEL_TERMS[model_name]:
        formula += f" + {MODEL_TERMS[model_name]}"
    return formula


def fit_gee(
    model_name: str,
    train: pd.DataFrame,
) -> Any:
    """Fit the confirmatory couple-clustered Gaussian GEE."""

    model = smf.gee(
        model_formula(model_name),
        groups="couple_id",
        data=train,
        family=sm.families.Gaussian(),
        cov_struct=sm.cov_struct.Independence(),
    )
    return model.fit(
        cov_type="bias_reduced",
        maxiter=100,
        ctol=1e-8,
    )


def participant_rmse(
    data: pd.DataFrame,
    prediction: np.ndarray,
    minimum_pairs: int,
) -> pd.Series:
    """Return participant-specific holdout RMSE with couple identity."""

    values = data[
        ["couple_id", "participant_id", "action_next"]
    ].copy()
    values["prediction"] = np.asarray(prediction)
    values["squared_error"] = (
        values["action_next"] - values["prediction"]
    ) ** 2
    grouped = values.groupby(
        ["couple_id", "participant_id"],
        observed=True,
    )
    counts = grouped.size()
    rmse = grouped["squared_error"].mean().pow(0.5)
    return rmse[counts >= minimum_pairs]


def paired_rmse_difference(
    left: pd.Series,
    right: pd.Series,
) -> tuple[float, float, float, float, int]:
    """Return couple-clustered paired RMSE difference and t-based 95% CI."""

    paired = pd.concat(
        [left.rename("left"), right.rename("right")],
        axis=1,
        join="inner",
    ).dropna()
    if paired.empty:
        nan = float("nan")
        return nan, nan, nan, nan, 0

    difference = paired["left"] - paired["right"]
    if isinstance(difference.index, pd.MultiIndex):
        couple_level = (
            "couple_id"
            if "couple_id" in difference.index.names
            else difference.index.names[0]
        )
        difference = difference.groupby(level=couple_level).mean()

    n = int(len(difference))
    mean = float(difference.mean())
    if n < 2:
        return mean, float("nan"), float("nan"), float("nan"), n
    se = float(difference.std(ddof=1) / math.sqrt(n))
    critical = float(student_t.ppf(0.975, df=n - 1))
    return (
        mean,
        se,
        mean - critical * se,
        mean + critical * se,
        n,
    )


def improvement_status(
    ci_low: float,
    ci_high: float,
    margin: float,
) -> str:
    """Classify whether a complex model materially improves RMSE."""

    if not (np.isfinite(ci_low) and np.isfinite(ci_high)):
        return "inconclusive"
    if ci_high <= -margin:
        return "material_improvement"
    if ci_low > -margin:
        return "no_material_improvement"
    return "inconclusive"


def noninferiority_status(
    ci_low: float,
    ci_high: float,
    margin: float,
) -> str:
    """Classify noninferiority of left-minus-right RMSE."""

    if not (np.isfinite(ci_low) and np.isfinite(ci_high)):
        return "inconclusive"
    if ci_high <= margin:
        return "noninferior"
    if ci_low > margin:
        return "materially_inferior"
    return "inconclusive"


def add_coefficient_metrics(
    row: dict[str, Any],
    result: Any,
    model_name: str,
    truth_name: str,
    config: dict[str, Any],
) -> None:
    """Add relational coefficient operating characteristics."""

    effects = truth_effects(config, truth_name)
    names = (
        "r_hat_wp10",
        "r_star_wp10",
        "e_wp10",
        "e_positive_wp10",
        "e_negative_wp10",
    )
    for name in names:
        if name not in result.params.index:
            continue
        prefix = f"{model_name}_{name}"
        estimate = float(result.params[name])
        se = float(result.bse[name])
        pvalue = float(result.pvalues[name])
        row[f"{prefix}_estimate"] = estimate
        row[f"{prefix}_se"] = se
        row[f"{prefix}_pvalue"] = pvalue
        row[f"{prefix}_significant_05"] = bool(
            pvalue < 0.05
        )
        truth_key = TRUTH_MAP.get(
            truth_name,
            {},
        ).get(f"{model_name}:{name}")
        if truth_key is None:
            continue
        truth = float(effects[truth_key])
        row[f"{prefix}_truth"] = truth
        row[f"{prefix}_bias"] = estimate - truth
        row[f"{prefix}_covered95"] = bool(
            estimate - 1.959963984540054 * se
            <= truth
            <= estimate + 1.959963984540054 * se
        )

    if model_name == "M2":
        required = ("r_hat_wp10", "r_star_wp10")
        if all(name in result.params.index for name in required):
            covariance = result.cov_params()
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
            critical = 1.959963984540054
            row["M2_d_sym_estimate"] = estimate
            row["M2_d_sym_se"] = se
            row["M2_d_sym_ci_low"] = estimate - critical * se
            row["M2_d_sym_ci_high"] = estimate + critical * se

    if model_name == "M4":
        required = ("e_positive_wp10", "e_negative_wp10")
        if all(name in result.params.index for name in required):
            covariance = result.cov_params()
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
            critical95 = 1.959963984540054
            critical90 = 1.6448536269514722
            row["M4_d_asym_estimate"] = estimate
            row["M4_d_asym_se"] = se
            row["M4_d_asym_ci90_low"] = estimate - critical90 * se
            row["M4_d_asym_ci90_high"] = estimate + critical90 * se
            row["M4_d_asym_ci95_low"] = estimate - critical95 * se
            row["M4_d_asym_ci95_high"] = estimate + critical95 * se


def evaluate_replication(
    config: dict[str, Any],
    scenario: Scenario,
    rng: np.random.Generator,
) -> dict[str, Any]:
    """Simulate, fit M0-M4, and evaluate one replication."""

    prompt_data = simulate_prompt_panel(
        config,
        scenario,
        rng,
    )
    lag_data = build_valid_lags(prompt_data, config)
    train, test = prepare_analysis_data(
        prompt_data,
        lag_data,
        config,
    )
    row: dict[str, Any] = {
        "couples": scenario.couples,
        "people": scenario.couples * 2,
        "compliance_target": scenario.compliance,
        "missingness_strength": (
            scenario.missingness_strength
        ),
        "truth": scenario.truth,
        "prompt_observed_rate": float(
            prompt_data["observed"].mean()
        ),
        "action_clipping_rate": float(
            prompt_data["action_was_clipped"].mean()
        ),
        "train_lags": int(len(train)),
        "test_lags": int(len(test)),
        "numpy_version": np.__version__,
        "pandas_version": pd.__version__,
        "statsmodels_version": sm.__version__,
    }
    counts = lag_data.groupby(
        "participant_id",
        observed=True,
    ).size()
    row["median_valid_lags_person"] = (
        float(counts.median())
        if len(counts)
        else 0.0
    )
    row["people_with_minimum_lags"] = int(
        (
            counts
            >= int(config["minimum_valid_lag_pairs"])
        ).sum()
    )

    rmses: dict[str, pd.Series] = {}
    for model_name in MODEL_TERMS:
        try:
            with warnings.catch_warnings(
                record=True
            ) as caught:
                warnings.simplefilter("always")
                result = fit_gee(
                    model_name,
                    train,
                )
            row[f"{model_name}_converged"] = bool(
                result.converged
            )
            row[f"{model_name}_warnings"] = len(
                caught
            )
            prediction = np.asarray(
                result.predict(test)
            )
            rmse = participant_rmse(
                test,
                prediction,
                int(
                    config[
                        "minimum_holdout_lag_pairs"
                    ]
                ),
            )
            rmses[model_name] = rmse
            row[
                f"{model_name}_mean_participant_rmse"
            ] = (
                float(rmse.mean())
                if len(rmse)
                else float("nan")
            )
            add_coefficient_metrics(
                row,
                result,
                model_name,
                scenario.truth,
                config,
            )
        except Exception as exc:
            row[f"{model_name}_converged"] = False
            row[f"{model_name}_warnings"] = -1
            row[f"{model_name}_error"] = (
                f"{type(exc).__name__}: {exc}"
            )

    row["all_models_converged"] = bool(
        all(
            row.get(
                f"{name}_converged",
                False,
            )
            for name in MODEL_TERMS
        )
    )

    for left, right, name in (
        ("M1", "M0", "delta_M1_M0"),
        ("M2", "M1", "delta_M2_M1"),
        ("M3", "M2", "delta_M3_M2"),
        ("M4", "M3", "delta_M4_M3"),
        ("M4", "M2", "delta_M4_M2"),
    ):
        if left not in rmses or right not in rmses:
            for suffix in ("", "_se", "_ci_low", "_ci_high", "_n"):
                row[f"{name}{suffix}"] = (
                    0 if suffix == "_n" else float("nan")
                )
            continue
        mean, se, ci_low, ci_high, n_pairs = paired_rmse_difference(
            rmses[left],
            rmses[right],
        )
        row[name] = mean
        row[f"{name}_se"] = se
        row[f"{name}_ci_low"] = ci_low
        row[f"{name}_ci_high"] = ci_high
        row[f"{name}_n"] = n_pairs

    for margin in config["candidate_rmse_margins"]:
        margin = float(margin)
        suffix = str(margin).replace(".", "p")

        def interval(name: str) -> tuple[float, float]:
            return (
                float(row.get(f"{name}_ci_low", float("nan"))),
                float(row.get(f"{name}_ci_high", float("nan"))),
            )

        d10_lo, d10_hi = interval("delta_M1_M0")
        d21_lo, d21_hi = interval("delta_M2_M1")
        d32_lo, d32_hi = interval("delta_M3_M2")
        d43_lo, d43_hi = interval("delta_M4_M3")
        d42_lo, d42_hi = interval("delta_M4_M2")

        s10 = improvement_status(d10_lo, d10_hi, margin)
        s21 = improvement_status(d21_lo, d21_hi, margin)
        s43 = improvement_status(d43_lo, d43_hi, margin)
        s32 = noninferiority_status(d32_lo, d32_hi, margin)
        s42 = noninferiority_status(d42_lo, d42_hi, margin)

        row[f"status_M1_M0_margin_{suffix}"] = s10
        row[f"status_M2_M1_margin_{suffix}"] = s21
        row[f"status_M4_M3_margin_{suffix}"] = s43
        row[f"status_M3_M2_margin_{suffix}"] = s32
        row[f"status_M4_M2_margin_{suffix}"] = s42

        if s10 == "no_material_improvement":
            decision = "M0_no_state_increment"
        elif s10 == "inconclusive":
            decision = "inconclusive_M1_M0"
        elif s21 == "no_material_improvement":
            decision = "M1_state_only"
        elif s21 == "inconclusive":
            decision = "inconclusive_M2_M1"
        elif s43 == "material_improvement":
            if s42 == "noninferior":
                decision = "M4_asymmetric"
            elif s42 == "materially_inferior":
                decision = "M2_separate_components"
            else:
                decision = "inconclusive_M4_M2"
        elif s43 == "inconclusive":
            decision = "inconclusive_M4_M3"
        elif s32 == "noninferior":
            decision = "M3_signed_discrepancy"
        elif s32 == "materially_inferior":
            decision = "M2_separate_components"
        else:
            decision = "inconclusive_M3_M2"

        row[f"representation_margin_{suffix}"] = decision

    return row


def scenario_grid(
    config: dict[str, Any],
) -> list[Scenario]:
    """Return the full factorial scenario grid."""

    return [
        Scenario(
            int(c),
            float(p),
            float(m),
            str(t),
        )
        for c in config["candidate_couples"]
        for p in config["compliance_rates"]
        for m in config["missingness_strengths"]
        for t in config["truth_scenarios"]
    ]


def replication_rng(
    config: dict[str, Any],
    scenario: Scenario,
    truth_index: int,
    rep: int,
) -> np.random.Generator:
    """Return a loop-order-independent random generator."""

    seed = np.random.SeedSequence([
        int(config["seed"]),
        scenario.couples,
        int(
            round(
                scenario.compliance * 1000
            )
        ),
        int(
            round(
                scenario.missingness_strength
                * 1000
            )
        ),
        truth_index,
        rep,
    ])
    return np.random.default_rng(seed)


def summarize_rows(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Aggregate replication rows by design scenario."""

    frame = pd.DataFrame(rows)
    keys = [
        "couples",
        "people",
        "compliance_target",
        "missingness_strength",
        "truth",
    ]
    summaries: list[dict[str, Any]] = []
    for values, group in frame.groupby(
        keys,
        dropna=False,
    ):
        summary = dict(
            zip(keys, values, strict=True)
        )
        summary["replications"] = int(
            len(group)
        )
        for column in group.columns:
            if (
                column in keys
                or not pd.api.types.is_numeric_dtype(
                    group[column]
                )
            ):
                continue
            summary[f"mean_{column}"] = float(
                pd.to_numeric(
                    group[column],
                    errors="coerce",
                ).mean()
            )
        for column in [
            value
            for value in group
            if value.startswith(
                "representation_margin_"
            )
        ]:
            freq = group[column].value_counts(
                normalize=True,
                dropna=False,
            )
            for value, probability in freq.items():
                summary[
                    f"p_{column}_{value}"
                ] = float(probability)
        summaries.append(summary)
    return summaries


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
) -> None:
    """Write rows using the union of observed fields."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    if not rows:
        path.write_text(
            "",
            encoding="utf-8",
        )
        return
    fields = sorted(
        {
            key
            for row in rows
            for key in row
        }
    )
    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def filter_scenarios(
    scenarios: list[Scenario],
    *,
    couples: int | None,
    compliance: float | None,
    missingness: float | None,
    truth: str | None,
) -> list[Scenario]:
    """Filter scenarios for targeted design-development runs."""

    selected = scenarios
    if couples is not None:
        selected = [
            scenario
            for scenario in selected
            if scenario.couples == couples
        ]
    if compliance is not None:
        selected = [
            scenario
            for scenario in selected
            if math.isclose(
                scenario.compliance,
                compliance,
            )
        ]
    if missingness is not None:
        selected = [
            scenario
            for scenario in selected
            if math.isclose(
                scenario.missingness_strength,
                missingness,
            )
        ]
    if truth is not None:
        if truth not in MODEL_TERMS:
            raise ValueError(
                f"unsupported truth filter: {truth}"
            )
        selected = [
            scenario
            for scenario in selected
            if scenario.truth == truth
        ]
    if not selected:
        raise ValueError(
            "scenario filters selected no design scenarios"
        )
    return selected


def run(
    config: dict[str, Any],
    replications: int,
    smoke: bool,
    *,
    couples: int | None = None,
    compliance: float | None = None,
    missingness: float | None = None,
    truth: str | None = None,
    rep_start: int = 0,
) -> list[dict[str, Any]]:
    """Run exact-design scenarios for a deterministic replication range.

    Replication IDs are absolute within each scenario. This makes separate
    chunks reproducible and mergeable regardless of execution order.
    """

    scenarios = scenario_grid(config)
    if smoke:
        smoke_couples = int(
            config.get(
                "smoke_couples",
                20,
            )
        )
        scenarios = [
            Scenario(
                smoke_couples,
                float(
                    config["compliance_rates"][1]
                ),
                float(
                    config[
                        "missingness_strengths"
                    ][0]
                ),
                truth_name,
            )
            for truth_name in ("M0", "M3")
        ]
        replications = min(
            replications,
            1,
        )
    else:
        scenarios = filter_scenarios(
            scenarios,
            couples=couples,
            compliance=compliance,
            missingness=missingness,
            truth=truth,
        )
    truth_order = {
        truth_name: index
        for index, truth_name in enumerate(
            config["truth_scenarios"]
        )
    }
    if rep_start < 0:
        raise ValueError("rep_start must be non-negative")
    rows: list[dict[str, Any]] = []
    for scenario in scenarios:
        for rep in range(rep_start, rep_start + replications):
            rng = replication_rng(
                config,
                scenario,
                truth_order[scenario.truth],
                rep,
            )
            row = evaluate_replication(
                config,
                scenario,
                rng,
            )
            row["replication"] = rep
            rows.append(row)
    return rows


def main() -> None:
    """Run the command-line Monte Carlo workflow."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--replications",
        type=int,
        default=None,
        help="Number of replications per selected scenario in this chunk.",
    )
    parser.add_argument(
        "--rep-start",
        type=int,
        default=0,
        help=(
            "Absolute zero-based replication index for this chunk. "
            "Use distinct non-overlapping ranges for parallel batches."
        ),
    )
    parser.add_argument(
        "--couples",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--compliance",
        type=float,
        default=None,
    )
    parser.add_argument(
        "--missingness",
        type=float,
        default=None,
    )
    parser.add_argument(
        "--truth",
        choices=tuple(MODEL_TERMS),
        default=None,
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
    )
    args = parser.parse_args()
    config = load_config(args.config)
    replications = (
        int(args.replications)
        if args.replications is not None
        else int(config["replications"])
    )
    rows = run(
        config,
        replications,
        args.smoke,
        couples=args.couples,
        compliance=args.compliance,
        missingness=args.missingness,
        truth=args.truth,
        rep_start=int(args.rep_start),
    )
    summaries = summarize_rows(rows)
    write_csv(
        args.output_dir
        / "h1_exact_replications.csv",
        rows,
    )
    write_csv(
        args.output_dir
        / "h1_exact_summary.csv",
        summaries,
    )
    print(
        f"Replications written: {len(rows)}"
    )
    print(
        "Replication range: "
        f"{int(args.rep_start)}.."
        f"{int(args.rep_start) + replications - 1}"
    )
    print(
        "Scenario summaries written: "
        f"{len(summaries)}"
    )


if __name__ == "__main__":
    main()
