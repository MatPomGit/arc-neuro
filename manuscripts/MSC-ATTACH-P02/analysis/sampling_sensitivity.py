"""Paired synthetic observation-design sensitivity study.

The generated agent is unchanged across observation noise and missingness arms.
Missing observations are removed after simulation; unobserved actions still affect
the agent's state. The fitted integral is reconstructed from observed snapshots.
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
from fit_controller import compare_models


def observed_intervals(times: np.ndarray, indices: np.ndarray, first_dt: float) -> np.ndarray:
    """Elapsed time since the preceding observed decision (first is its step)."""
    times = np.asarray(times, dtype=float)
    indices = np.asarray(indices, dtype=int)
    if indices.ndim != 1 or len(indices) < 5 or indices[0] != 0 or np.any(np.diff(indices) <= 0):
        raise ValueError("indices must contain at least five increasing positions starting at zero")
    dt = np.r_[first_dt, np.diff(times[indices])]
    if not np.all(np.isfinite(dt)) or np.any(dt <= 0):
        raise ValueError("observed intervals must be positive and finite")
    return dt


def rows_for_config(spec: dict) -> list[dict]:
    base = spec["simulation"]
    traits = ARCTraits(**spec["traits"])
    steps = int(base["steps"])
    seed0 = int(spec["seed"])
    rows = []
    for run in range(int(spec["n_runs"])):
        gain_rng = np.random.default_rng(seed0 + run)
        gains = ControllerGains(
            **{key: float(gain_rng.uniform(*spec["gain_ranges"][key]))
               for key in ("kp", "ki", "kd")},
            integral_leak=float(spec["integral_leak"]),
        )
        # Common gains and RNG stream within each run, across all schedules.
        for schedule_index, (schedule, choices) in enumerate(spec["schedules"].items()):
            rng = np.random.default_rng(seed0 + 100000 + run * 10 + schedule_index)
            intervals = rng.choice(np.asarray(choices, dtype=float), size=steps)
            config = ARCConfig(**base)
            generated = simulate(
                traits, config, impulse(config, **spec["perturbation"]),
                gains=gains, intervals=intervals, seed=seed0 + run,
            )
            times = generated.series["time"]
            # Draw once, then threshold it for nested missingness arms.
            missing_draws = rng.random(steps)
            measurement_draws = rng.standard_normal(steps)
            for missingness in spec["missingness"]:
                indices = np.flatnonzero(missing_draws >= missingness)
                indices = np.unique(np.r_[0, indices])
                dt = observed_intervals(times, indices, intervals[0])
                action = generated.series["action"][indices]
                for noise in spec["measurement_noise"]:
                    error = generated.series["true_error"][indices] + noise * measurement_draws[indices]
                    fit = compare_models(error, action, dt, gains.integral_leak, config.dt)
                    rows.append({
                        "run": run, "schedule": schedule,
                        "measurement_noise": noise, "missingness": missingness,
                        "observed_n": len(indices), "elapsed_time": float(times[-1] + intervals[-1]),
                        **{f"{name}_rmse": fit[name]["test_rmse"]
                           for name in ("context", "autoregressive", "p", "pi", "pid")},
                    })
    return rows


def summarize(rows: list[dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for row in rows:
        key = (row["schedule"], row["measurement_noise"], row["missingness"])
        groups.setdefault(key, []).append(row)
    output = []
    for (schedule, noise, missingness), group in sorted(groups.items()):
        output.append({
            "schedule": schedule, "measurement_noise": noise, "missingness": missingness,
            "n_runs": len(group), "mean_observed_n": float(np.mean([r["observed_n"] for r in group])),
            **{f"mean_{name}_rmse": float(np.mean([r[f"{name}_rmse"] for r in group]))
               for name in ("context", "autoregressive", "p", "pi", "pid")},
            "pi_better_than_p": sum(r["pi_rmse"] < r["p_rmse"] for r in group),
            "pid_better_than_pi": sum(r["pid_rmse"] < r["pi_rmse"] for r in group),
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
    write_csv(args.output / "sampling_trajectories.csv", rows)
    write_csv(args.output / "sampling_summary.csv", summary)
    metadata = {
        "model_version": MODEL_VERSION,
        "config_sha256": hashlib.sha256(args.config.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "numpy": importlib.metadata.version("numpy"),
        "seed": spec["seed"],
        "n_runs_per_schedule": spec["n_runs"],
        "rng": "numpy.random.default_rng / PCG64 family",
        "outputs": ["sampling_trajectories.csv", "sampling_summary.csv"],
    }
    (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
