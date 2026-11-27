"""Monte Carlo screening for the ARC 2.0 H1 pilot design.

This is intentionally a lightweight planning model. It approximates the primary
within-person discrepancy-to-action test with participant fixed effects and a
cluster-robust covariance estimator.

It is NOT a substitute for a Monte Carlo study using the exact preregistered
DSEM/multilevel estimator. Its purpose is to reject obviously inadequate
N/T/compliance combinations before running the heavier final design analysis.

Usage:
    python manuscripts/MSC-ATTACH-P01/analysis/h1_design_simulation.py \
        --config manuscripts/MSC-ATTACH-P01/protocol/design_config.json \
        --output build/MSC-ATTACH-P01/design_results.csv
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import NormalDist

import numpy as np


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def simulate_panel(
    *,
    n_people: int,
    days: int,
    prompts_per_day: int,
    compliance: float,
    beta_e: float,
    phi_action: float,
    rho_e: float,
    beta_context: float,
    random_slope_sd: float,
    residual_sd: float,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return participant id, lagged e/context/action, and subsequent action."""

    total_t = days * prompts_per_day

    discrepancy = np.zeros((n_people, total_t), dtype=float)
    context = np.zeros((n_people, total_t), dtype=float)
    action = np.zeros((n_people, total_t), dtype=float)

    discrepancy[:, 0] = rng.normal(size=n_people)
    context[:, 0] = rng.normal(size=n_people)
    action[:, 0] = rng.normal(size=n_people)

    random_intercept = rng.normal(0.0, 0.35, size=n_people)
    random_slope = rng.normal(0.0, random_slope_sd, size=n_people)

    e_innovation_sd = np.sqrt(max(1.0 - rho_e**2, 1e-8))

    for t in range(1, total_t):
        discrepancy[:, t] = (
            rho_e * discrepancy[:, t - 1]
            + rng.normal(0.0, e_innovation_sd, size=n_people)
        )
        context[:, t] = (
            0.25 * context[:, t - 1]
            + rng.normal(0.0, np.sqrt(1.0 - 0.25**2), size=n_people)
        )
        action[:, t] = (
            random_intercept
            + phi_action * action[:, t - 1]
            + (beta_e + random_slope) * discrepancy[:, t - 1]
            + beta_context * context[:, t - 1]
            + rng.normal(0.0, residual_sd, size=n_people)
        )

    observed = rng.random((n_people, total_t)) < compliance

    valid = np.zeros((n_people, total_t), dtype=bool)
    for t in range(1, total_t):
        same_day = (t // prompts_per_day) == ((t - 1) // prompts_per_day)
        if same_day:
            valid[:, t] = observed[:, t] & observed[:, t - 1]

    person_id, current_t = np.where(valid)

    return (
        person_id.astype(int),
        discrepancy[person_id, current_t - 1],
        context[person_id, current_t - 1],
        action[person_id, current_t - 1],
        action[person_id, current_t],
    )


def fixed_effect_cluster_fit(
    person_id: np.ndarray,
    e_lag: np.ndarray,
    context_lag: np.ndarray,
    action_lag: np.ndarray,
    action_next: np.ndarray,
) -> tuple[float, float, float]:
    """Participant-FE OLS with CR1 cluster-robust SE.

    All columns are within-person demeaned. The first coefficient is the
    screening estimate of the H1 discrepancy effect.
    """

    unique, inverse = np.unique(person_id, return_inverse=True)
    g = len(unique)
    n = len(action_next)
    if g < 3 or n < 10:
        return float("nan"), float("nan"), float("nan")

    x = np.column_stack((e_lag, context_lag, action_lag))
    y = action_next.astype(float)

    counts = np.bincount(inverse).astype(float)
    y_mean = np.bincount(inverse, weights=y) / counts
    y_dm = y - y_mean[inverse]

    x_dm = np.empty_like(x, dtype=float)
    for j in range(x.shape[1]):
        x_mean = np.bincount(inverse, weights=x[:, j]) / counts
        x_dm[:, j] = x[:, j] - x_mean[inverse]

    xtx = x_dm.T @ x_dm
    try:
        xtx_inv = np.linalg.inv(xtx)
    except np.linalg.LinAlgError:
        return float("nan"), float("nan"), float("nan")

    beta = xtx_inv @ (x_dm.T @ y_dm)
    residual = y_dm - x_dm @ beta

    scores = np.column_stack(
        [
            np.bincount(
                inverse,
                weights=x_dm[:, j] * residual,
                minlength=g,
            )
            for j in range(x.shape[1])
        ]
    )
    meat = scores.T @ scores

    k = x.shape[1]
    correction = (g / (g - 1.0)) * ((n - 1.0) / max(n - k, 1.0))
    covariance = correction * (xtx_inv @ meat @ xtx_inv)
    se = np.sqrt(np.maximum(np.diag(covariance), 0.0))

    beta_e = float(beta[0])
    se_e = float(se[0])
    z = beta_e / se_e if se_e > 0 else float("nan")
    return beta_e, se_e, z


def one_replication(
    *,
    n_people: int,
    config: dict,
    compliance: float,
    beta_e: float,
    rng: np.random.Generator,
) -> dict:
    panel = simulate_panel(
        n_people=n_people,
        days=int(config["days"]),
        prompts_per_day=int(config["prompts_per_day"]),
        compliance=float(compliance),
        beta_e=float(beta_e),
        phi_action=float(config["action_autoregression"]),
        rho_e=float(config["discrepancy_autoregression"]),
        beta_context=float(config["context_effect"]),
        random_slope_sd=float(config["random_slope_sd"]),
        residual_sd=float(config["residual_sd"]),
        rng=rng,
    )

    person_id, e_lag, context_lag, action_lag, action_next = panel
    beta_hat, se_hat, z = fixed_effect_cluster_fit(
        person_id, e_lag, context_lag, action_lag, action_next
    )

    counts = np.bincount(person_id, minlength=n_people)
    min_pairs = int(config["minimum_valid_lag_pairs"])
    confirmatory_people = int(np.sum(counts >= min_pairs))

    alpha = float(config["alpha_two_sided"])
    critical_z = NormalDist().inv_cdf(1.0 - alpha / 2.0)

    return {
        "detected": bool(np.isfinite(z) and abs(z) >= critical_z),
        "correct_direction": bool(np.isfinite(beta_hat) and beta_hat > 0),
        "beta_hat": beta_hat,
        "se_hat": se_hat,
        "valid_pairs_total": int(len(person_id)),
        "median_pairs": float(np.median(counts)),
        "p10_pairs": float(np.quantile(counts, 0.10)),
        "confirmatory_people": confirmatory_people,
        "confirmatory_n_met": bool(
            confirmatory_people >= int(config["minimum_confirmatory_individuals"])
        ),
    }


def summarize(values: list[dict]) -> dict:
    def mean(key: str) -> float:
        data = np.asarray([v[key] for v in values], dtype=float)
        return float(np.nanmean(data))

    return {
        "detection_probability": mean("detected"),
        "correct_direction_probability": mean("correct_direction"),
        "mean_beta_hat": mean("beta_hat"),
        "mean_se_hat": mean("se_hat"),
        "mean_valid_pairs_total": mean("valid_pairs_total"),
        "mean_median_pairs_person": mean("median_pairs"),
        "mean_p10_pairs_person": mean("p10_pairs"),
        "mean_confirmatory_people": mean("confirmatory_people"),
        "probability_confirmatory_n_met": mean("confirmatory_n_met"),
    }


def run(config: dict) -> list[dict]:
    rng = np.random.default_rng(int(config["seed"]))
    replications = int(config["replications"])
    rows: list[dict] = []

    for couples in config["candidate_couples"]:
        n_people = int(couples) * 2
        for compliance in config["compliance_rates"]:
            for beta_e in config["standardized_discrepancy_effects"]:
                values = [
                    one_replication(
                        n_people=n_people,
                        config=config,
                        compliance=float(compliance),
                        beta_e=float(beta_e),
                        rng=rng,
                    )
                    for _ in range(replications)
                ]
                summary = summarize(values)
                rows.append(
                    {
                        "couples": int(couples),
                        "people": n_people,
                        "days": int(config["days"]),
                        "prompts_per_day": int(config["prompts_per_day"]),
                        "planned_timepoints": int(config["days"])
                        * int(config["prompts_per_day"]),
                        "compliance": float(compliance),
                        "beta_e": float(beta_e),
                        "replications": replications,
                        **summary,
                        "meets_detection_target": (
                            summary["detection_probability"]
                            >= float(config["target_detection_probability"])
                        ),
                    }
                )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    rows = run(config)
    write_csv(args.output, rows)

    feasible = [
        row
        for row in rows
        if row["meets_detection_target"]
        and row["probability_confirmatory_n_met"] >= 0.80
    ]

    print(f"Scenarios evaluated: {len(rows)}")
    print(f"Scenarios meeting both screening criteria: {len(feasible)}")
    for row in feasible[:20]:
        print(
            "couples={couples}, compliance={compliance:.2f}, "
            "beta_e={beta_e:.2f}, detect={detection_probability:.3f}, "
            "P(N_confirmatory)={probability_confirmatory_n_met:.3f}".format(**row)
        )


if __name__ == "__main__":
    main()
