"""Leakage-resistant generator-discrimination pipeline for manuscript M02.

This module separates coefficient fitting, model selection, and final evaluation.
It is a development pipeline for the expanded identifiability study; the
confirmatory numerical grid remains governed by
manuscripts/02_identifiability/simulation_protocol.yaml.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform

import numpy as np

from arc_model import MODEL_VERSION, ARCConfig, ARCTraits, ControllerGains, impulse, simulate
from fit_controller import features


CANDIDATES = ("context", "autoregressive", "p", "pi", "pid")
NESTED = ("p", "pi", "pid")


def split_indices(n: int, fit_fraction: float, validation_fraction: float) -> tuple[int, int]:
    if n < 15:
        raise ValueError("at least 15 observations are required for a three-way split")
    if not 0 < fit_fraction < 1 or not 0 < validation_fraction < 1:
        raise ValueError("split fractions must lie in (0, 1)")
    fit_end = int(n * fit_fraction)
    validation_end = int(n * (fit_fraction + validation_fraction))
    if fit_end < 5 or validation_end - fit_end < 3 or n - validation_end < 3:
        raise ValueError("split leaves an undersized fit, validation, or final-test block")
    if validation_end >= n:
        raise ValueError("fit_fraction + validation_fraction must be < 1")
    return fit_end, validation_end


def design_matrix(
    name: str,
    error: np.ndarray,
    action: np.ndarray,
    dt: np.ndarray,
    integral_leak: float,
) -> np.ndarray:
    if name == "context":
        return np.empty((len(action), 0))
    if name == "autoregressive":
        return np.r_[0.0, action[:-1]].reshape(-1, 1)
    X, _ = features(error, dt, name, integral_leak)
    return X


def fit_validate_test(
    X: np.ndarray,
    y: np.ndarray,
    fit_end: int,
    validation_end: int,
    evaluate_final: bool = True,
) -> dict:
    """Fit on the first block and score frozen conditional predictions.

    X has shape [observations, features]; y has shape [observations].
    Block boundaries are observation indices. Rank and conditioning describe
    the augmented fitting matrix, including its intercept.
    """
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    if X.ndim != 2 or y.ndim != 1 or X.shape[0] != len(y):
        raise ValueError("X and y must be aligned matrix/vector inputs")
    if not np.all(np.isfinite(X)) or not np.all(np.isfinite(y)):
        raise ValueError("predictors and actions must be finite")
    if not 0 < fit_end < validation_end < len(y):
        raise ValueError("invalid temporal block boundaries")
    X_aug = np.column_stack([np.ones(len(y)), X])
    coef, _, rank, singular = np.linalg.lstsq(
        X_aug[:fit_end], y[:fit_end], rcond=None
    )

    def rmse(start: int, end: int) -> float:
        pred = X_aug[start:end] @ coef
        return float(np.sqrt(np.mean((y[start:end] - pred) ** 2)))

    return {
        "coefficients": coef.tolist(),
        "fit_rmse": rmse(0, fit_end),
        "validation_rmse": rmse(fit_end, validation_end),
        "final_test_rmse": rmse(validation_end, len(y)) if evaluate_final else None,
        "fit_n": fit_end,
        "validation_n": validation_end - fit_end,
        "final_test_n": len(y) - validation_end,
        "fit_rank": int(rank),
        "fit_columns": int(X_aug.shape[1]),
        "fit_condition_number": (
            float(singular[0] / singular[-1])
            if rank == X_aug.shape[1] and singular[-1] > 0 else None
        ),
    }


def compare_three_way(
    error: np.ndarray,
    action: np.ndarray,
    dt: np.ndarray,
    integral_leak: float,
    fit_fraction: float,
    validation_fraction: float,
) -> dict[str, dict]:
    fit_end, validation_end = split_indices(len(action), fit_fraction, validation_fraction)
    return {
        name: fit_validate_test(
            design_matrix(name, error, action, dt, integral_leak),
            action,
            fit_end,
            validation_end,
        )
        for name in CANDIDATES
    }


def best_on_validation(results: dict[str, dict], candidates: tuple[str, ...]) -> str:
    """Minimum validation RMSE; ties favor the earlier, simpler candidate."""
    return min(candidates, key=lambda name: results[name]["validation_rmse"])


def rows_for_config(spec: dict) -> list[dict]:
    traits = ARCTraits(**spec["traits"])
    base = spec["simulation"]
    n = int(spec["n_runs"])
    seed = int(spec["seed"])
    fit_fraction = float(spec["split"]["fit_fraction"])
    validation_fraction = float(spec["split"]["validation_fraction"])
    rows: list[dict] = []

    for run in range(n):
        rng = np.random.default_rng(seed + run)
        gains = ControllerGains(
            **{
                key: float(rng.uniform(*spec["gain_ranges"][key]))
                for key in ("kp", "ki", "kd")
            },
            integral_leak=float(spec["integral_leak"]),
        )
        measurement_draws = rng.standard_normal(int(base["steps"]))

        for generator in NESTED:
            config = ARCConfig(**(base | {"controller_mode": generator}))
            result = simulate(
                traits,
                config,
                impulse(config, **spec["perturbation"]),
                gains=gains,
                seed=seed + run,
            )
            dt = np.full(config.steps, config.dt)

            for noise in spec["measurement_noise"]:
                observed_error = result.series["true_error"] + noise * measurement_draws
                compared = compare_three_way(
                    observed_error,
                    result.series["action"],
                    dt,
                    gains.integral_leak,
                    fit_fraction,
                    validation_fraction,
                )
                selected_nested = best_on_validation(compared, NESTED)
                selected_all = best_on_validation(compared, CANDIDATES)

                row = {
                    "run": run,
                    "generator": generator,
                    "measurement_noise": noise,
                    "selected_nested": selected_nested,
                    "selected_all": selected_all,
                    "nested_correct": selected_nested == generator,
                    "all_correct": selected_all == generator,
                    "selected_nested_final_test_rmse": compared[selected_nested]["final_test_rmse"],
                    "selected_all_final_test_rmse": compared[selected_all]["final_test_rmse"],
                    "generator_final_test_rmse": compared[generator]["final_test_rmse"],
                    "fit_n": compared[generator]["fit_n"],
                    "validation_n": compared[generator]["validation_n"],
                    "final_test_n": compared[generator]["final_test_n"],
                }
                for name in CANDIDATES:
                    row[f"{name}_validation_rmse"] = compared[name]["validation_rmse"]
                    row[f"{name}_final_test_rmse"] = compared[name]["final_test_rmse"]
                rows.append(row)
    return rows


def summarize(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple, list[dict]] = {}
    for row in rows:
        grouped.setdefault((row["generator"], row["measurement_noise"]), []).append(row)

    output = []
    for (generator, noise), group in sorted(grouped.items()):
        output.append({
            "generator": generator,
            "measurement_noise": noise,
            "n_runs": len(group),
            "nested_correct": sum(row["nested_correct"] for row in group),
            "all_correct": sum(row["all_correct"] for row in group),
            "baseline_selected": sum(row["selected_all"] not in NESTED for row in group),
            "mean_selected_final_test_rmse": float(np.mean([
                row["selected_all_final_test_rmse"] for row in group
            ])),
            "mean_generator_final_test_rmse": float(np.mean([
                row["generator_final_test_rmse"] for row in group
            ])),
        })
    return output


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    spec = json.loads(args.config.read_text(encoding="utf-8"))
    rows = rows_for_config(spec)
    summary = summarize(rows)
    write_csv(args.output / "identifiability_trajectories.csv", rows)
    write_csv(args.output / "identifiability_summary.csv", summary)

    metadata = {
        "model_version": MODEL_VERSION,
        "config_sha256": hashlib.sha256(args.config.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "numpy": importlib.metadata.version("numpy"),
        "seed": spec["seed"],
        "n_runs_per_generator": spec["n_runs"],
        "selection_rule": "minimum validation RMSE; ties favor simpler candidate order",
        "final_test_rule": "untouched until model selection is complete",
        "outputs": ["identifiability_trajectories.csv", "identifiability_summary.csv"],
    }
    (args.output / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
