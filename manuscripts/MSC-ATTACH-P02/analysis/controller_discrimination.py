"""Stress test whether observable actions distinguish generating P, PI and PID.

The same gains and random seed are reused across modes, but feedback makes their
generated trajectories different. Noise is added only to the analyst's error.
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


MODELS = ("context", "autoregressive", "p", "pi", "pid")
NESTED = ("p", "pi", "pid")


def best_model(fit: dict, candidates: tuple[str, ...]) -> str:
    """Minimum test RMSE; ties favor the earlier, simpler candidate."""
    return min(candidates, key=lambda name: fit[name]["test_rmse"])


def rows_for_config(spec: dict) -> list[dict]:
    traits = ARCTraits(**spec["traits"])
    base = spec["simulation"]
    n = int(spec["n_runs"])
    seed = int(spec["seed"])
    rows: list[dict] = []
    for run in range(n):
        rng = np.random.default_rng(seed + run)
        gains = ControllerGains(
            **{key: float(rng.uniform(*spec["gain_ranges"][key]))
               for key in ("kp", "ki", "kd")},
            integral_leak=float(spec["integral_leak"]),
        )
        # Identical analyst measurement error draws across modes and noise arms.
        measurement_draws = rng.standard_normal(int(base["steps"]))
        for mode in NESTED:
            config = ARCConfig(**(base | {"controller_mode": mode}))
            result = simulate(
                traits, config, impulse(config, **spec["perturbation"]),
                gains=gains, seed=seed + run,
            )
            for noise in spec["measurement_noise"]:
                error = result.series["true_error"] + noise * measurement_draws
                fit = compare_models(
                    error, result.series["action"],
                    np.full(config.steps, config.dt), gains.integral_leak, config.dt,
                )
                rows.append({
                    "run": run, "generator": mode, "measurement_noise": noise,
                    "kp_true": gains.kp, "ki_true": gains.ki if mode != "p" else 0.0,
                    "kd_true": gains.kd if mode == "pid" else 0.0,
                    "best_nested": best_model(fit, NESTED),
                    "best_including_baselines": best_model(fit, MODELS),
                    **{f"{name}_rmse": fit[name]["test_rmse"] for name in MODELS},
                })
    return rows


def summarize(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple, list[dict]] = {}
    for row in rows:
        grouped.setdefault((row["generator"], row["measurement_noise"]), []).append(row)
    summary = []
    for (mode, noise), group in sorted(grouped.items()):
        summary.append({
            "generator": mode, "measurement_noise": noise, "n_runs": len(group),
            **{f"mean_{name}_rmse": float(np.mean([r[f"{name}_rmse"] for r in group]))
               for name in MODELS},
            **{f"selected_{name}": sum(r["best_nested"] == name for r in group)
               for name in NESTED},
            "baseline_selected": sum(r["best_including_baselines"] not in NESTED for r in group),
            "pi_better_than_p": sum(r["pi_rmse"] < r["p_rmse"] for r in group),
            "pid_better_than_pi": sum(r["pid_rmse"] < r["pi_rmse"] for r in group),
        })
    return summary


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
    write_csv(args.output / "discrimination_trajectories.csv", rows)
    write_csv(args.output / "discrimination_summary.csv", summarize(rows))
    metadata = {
        "model_version": MODEL_VERSION,
        "config_sha256": hashlib.sha256(args.config.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "numpy": importlib.metadata.version("numpy"),
        "seed": spec["seed"], "n_runs_per_generator": spec["n_runs"],
        "rng": "numpy.random.default_rng / PCG64 family",
        "outputs": ["discrimination_trajectories.csv", "discrimination_summary.csv"],
    }
    (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
