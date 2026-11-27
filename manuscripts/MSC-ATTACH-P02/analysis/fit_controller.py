"""Estimate P, PI, or PID coefficients from repeated observations.

Expected CSV columns:
- true_error or observed_error
- action

Optional columns:
- dt
- context_* (numeric predictors available before action)

The script constructs a leaky integral and derivative from the observed error
series and compares P, PI, PID with temporally ordered train/test splits.
It is intentionally dependency-light and uses NumPy linear least squares.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np


def read_csv(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("CSV contains no rows")

    names = rows[0].keys()
    error_name = "observed_error" if "observed_error" in names else "true_error"
    if error_name not in names or "action" not in names:
        raise ValueError("CSV must contain observed_error or true_error, and action")

    error = np.asarray([float(row[error_name]) for row in rows], dtype=float)
    action = np.asarray([float(row["action"]) for row in rows], dtype=float)
    if "dt" in names:
        dt = np.asarray([float(row["dt"]) for row in rows], dtype=float)
    else:
        dt = np.ones(len(rows), dtype=float)
    context_names = sorted(name for name in names if name.startswith("context_"))
    context = np.asarray(
        [[float(row[name]) for name in context_names] for row in rows],
        dtype=float,
    ).reshape(len(rows), len(context_names))
    return {"error": error, "action": action, "dt": dt, "context": context}


def features(
    error: np.ndarray,
    dt: np.ndarray,
    mode: str,
    integral_leak: float,
    reference_dt: float = 1.0,
) -> tuple[np.ndarray, list[str]]:
    error = np.asarray(error, dtype=float)
    dt = np.asarray(dt, dtype=float)
    if error.ndim != 1 or dt.shape != error.shape or not np.all(np.isfinite(error)):
        raise ValueError("error and dt must be finite aligned vectors")
    if not np.all(np.isfinite(dt)) or np.any(dt <= 0) or reference_dt <= 0:
        raise ValueError("dt and reference_dt must be positive and finite")
    if not 0 <= integral_leak <= 1:
        raise ValueError("integral_leak must be in [0, 1]")
    p = error.copy()
    i = np.zeros_like(error)
    d = np.zeros_like(error)

    for t in range(len(error)):
        i[t] = (integral_leak ** (dt[t] / reference_dt) * (i[t - 1] if t else 0.0)
                + error[t] * dt[t])
        if t:
            d[t] = (error[t] - error[t - 1]) / dt[t]

    if mode == "p":
        return np.column_stack([p]), ["kp"]
    if mode == "pi":
        return np.column_stack([p, i]), ["kp", "ki"]
    if mode == "pid":
        return np.column_stack([p, i, d]), ["kp", "ki", "kd"]
    raise ValueError("mode must be p, pi, or pid")


def fit_and_score(
    X: np.ndarray,
    y: np.ndarray,
    train_fraction: float = 0.70,
) -> dict:
    if len(y) < 5 or X.ndim != 2 or X.shape[0] != len(y):
        raise ValueError("at least five aligned observations are required")
    if not np.all(np.isfinite(X)) or not np.all(np.isfinite(y)):
        raise ValueError("predictors and actions must be finite")
    split = max(3, min(len(y) - 2, int(len(y) * train_fraction)))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    X_train_aug = np.column_stack([np.ones(len(X_train)), X_train])
    X_test_aug = np.column_stack([np.ones(len(X_test)), X_test])

    coef, *_ = np.linalg.lstsq(X_train_aug, y_train, rcond=None)
    pred_train = X_train_aug @ coef
    pred_test = X_test_aug @ coef

    rmse_train = float(np.sqrt(np.mean((y_train - pred_train) ** 2)))
    rmse_test = float(np.sqrt(np.mean((y_test - pred_test) ** 2)))

    baseline = np.full_like(y_test, y_train.mean())
    baseline_rmse = float(np.sqrt(np.mean((y_test - baseline) ** 2)))

    return {
        "intercept": float(coef[0]),
        "coefficients": coef[1:].tolist(),
        "train_rmse": rmse_train,
        "test_rmse": rmse_test,
        "baseline_test_rmse": baseline_rmse,
        "test_improvement_vs_mean": baseline_rmse - rmse_test,
        "train_n": int(len(y_train)),
        "test_n": int(len(y_test)),
    }


def compare_models(
    error: np.ndarray,
    action: np.ndarray,
    dt: np.ndarray,
    integral_leak: float,
    reference_dt: float = 1.0,
    context: np.ndarray | None = None,
) -> dict[str, dict]:
    action = np.asarray(action, dtype=float)
    if context is None:
        context = np.empty((len(action), 0))
    context = np.asarray(context, dtype=float)
    if context.ndim != 2 or context.shape[0] != len(action):
        raise ValueError("context must have one row per action")
    # The lag is observed by decision time, including at the start of each test block.
    lagged_action = np.r_[0.0, action[:-1]]
    results = {
        "context": fit_and_score(context, action),
        "autoregressive": fit_and_score(np.column_stack([context, lagged_action]), action),
    }
    results["context"]["parameter_names"] = [f"context_{i}" for i in range(context.shape[1])]
    results["autoregressive"]["parameter_names"] = results["context"]["parameter_names"] + ["previous_action"]
    for mode in ("p", "pi", "pid"):
        X, names = features(error, dt, mode, integral_leak, reference_dt)
        names = [f"context_{i}" for i in range(context.shape[1])] + names
        scored = fit_and_score(np.column_stack([context, X]), action)
        scored["parameter_names"] = names
        scored["parameter_estimates"] = dict(
            zip(names, scored["coefficients"])
        )
        results[mode] = scored
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate nested ARC P/PI/PID action models."
    )
    parser.add_argument("csv", type=Path)
    parser.add_argument("--integral-leak", type=float, default=0.85)
    parser.add_argument("--reference-dt", type=float, default=1.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = read_csv(args.csv)
    results = compare_models(
        data["error"],
        data["action"],
        data["dt"],
        args.integral_leak,
        args.reference_dt,
        data["context"],
    )

    text = json.dumps(results, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
