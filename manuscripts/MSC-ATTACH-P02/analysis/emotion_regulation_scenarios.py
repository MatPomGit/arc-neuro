"""Matched-seed ARC perturbation scenarios for visualizing regulation dynamics.

The discrepancy is a relational-state proxy, not a measured emotional intensity.
Strategy curves are probabilities; actions use expected policy alignment, not the
sampled strategy label. Profile contrasts are model consequences, not causal
effects estimated from people.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["svg.hashsalt"] = "arc-emotion-regulation"

from arc_model import MODEL_VERSION, ARCConfig, ARCTraits, impulse, simulate


SERIES = ("true_error", "estimated_error", "action", "pi_secure",
          "pi_hyperactivation", "pi_deactivation")


def scenario_specs(spec: dict) -> list[dict]:
    scenarios = []
    for group, settings in spec["groups"].items():
        first, second = settings["axes"]
        for first_level, first_value in settings["levels"][first].items():
            for second_level, second_value in settings["levels"][second].items():
                traits = dict(spec["traits"])
                config = dict(spec["simulation"])
                for name, value in ((first, first_value), (second, second_value)):
                    (config if name == "responsiveness" else traits)[name] = value
                scenarios.append({
                    "group": group,
                    "scenario": f"{first}_{first_level}__{second}_{second_level}",
                    "label": f"{first}={first_value:g}, {second}={second_value:g}",
                    "traits": traits, "simulation": config,
                })
    return scenarios


def run_scenarios(spec: dict) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    trajectories: list[dict] = []
    shock_step = int(spec["perturbation"]["step"])
    for profile in scenario_specs(spec):
        config = ARCConfig(**profile["simulation"])
        shock = impulse(config, **spec["perturbation"])
        all_series: dict[str, list[np.ndarray]] = {key: [] for key in SERIES}
        for run in range(int(spec["n_runs"])):
            result = simulate(
                ARCTraits(**profile["traits"]), config, shock,
                seed=int(spec["seed"]) + run,
            )
            for key in SERIES:
                all_series[key].append(result.series[key])
            post = slice(shock_step + 1, None)
            rows.append({
                "group": profile["group"], "scenario": profile["scenario"],
                "run": run, "error_auc": result.metrics["error_auc"],
                "settling_time": result.metrics["settling_time"],
                "mean_abs_action_post": float(np.mean(np.abs(result.series["action"][post]))),
                "mean_secure_probability_post": float(np.mean(result.series["pi_secure"][post])),
                "mean_action_effect_post": float(np.mean(result.series["action_effect_oracle"][post])),
            })
        for step in range(config.steps):
            row = {"group": profile["group"], "scenario": profile["scenario"],
                   "label": profile["label"], "step": step,
                   "time": step * config.dt}
            for key, values in all_series.items():
                matrix = np.asarray(values)
                if key == "true_error":
                    absolute = np.abs(matrix[:, step])
                    row["abs_error_mean"] = float(np.mean(absolute))
                    row["abs_error_p10"] = float(np.quantile(absolute, .1))
                    row["abs_error_p90"] = float(np.quantile(absolute, .9))
                row[f"{key}_mean"] = float(np.mean(matrix[:, step]))
            trajectories.append(row)
    return rows, trajectories


def summarize(rows: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        groups.setdefault((row["group"], row["scenario"]), []).append(row)
    return [
        {
            "group": group, "scenario": scenario, "n_runs": len(data),
            "mean_error_auc": float(np.mean([r["error_auc"] for r in data])),
            "mean_settling_time": float(np.mean([r["settling_time"] for r in data])),
            "settled_n": sum(np.isfinite(r["settling_time"]) for r in data),
            "mean_abs_action_post": float(np.mean([r["mean_abs_action_post"] for r in data])),
            "mean_secure_probability_post": float(np.mean([r["mean_secure_probability_post"] for r in data])),
            "mean_action_effect_post": float(np.mean([r["mean_action_effect_post"] for r in data])),
        }
        for (group, scenario), data in sorted(groups.items())
    ]


def plot_group(rows: list[dict], group: str, shock_step: int, output: Path) -> None:
    keys = ("abs_error_mean", "pi_secure_mean") if group == "estimation_flexibility" else ("abs_error_mean", "action_mean")
    labels = ("Absolute relational discrepancy", "Secure strategy probability") if group == "estimation_flexibility" else ("Absolute relational discrepancy", "Signed regulatory action")
    fig, axes = plt.subplots(2, 1, figsize=(8, 6.2), sharex=True, layout="constrained")
    profiles = sorted({r["scenario"] for r in rows if r["group"] == group})
    shock_time = next(r["time"] for r in rows if r["group"] == group and r["step"] == shock_step + 1)
    dt = next(r["time"] for r in rows if r["group"] == group and r["step"] == 1)
    colors = ("#305f9a", "#e17a32", "#4a8b69", "#a75079")
    for ax, key, ylabel in zip(axes, keys, labels):
        for scenario, color in zip(profiles, colors):
            subset = [r for r in rows if r["group"] == group and r["scenario"] == scenario]
            x = np.asarray([r["time"] for r in subset])
            y = np.asarray([r[key] for r in subset])
            ax.plot(x, y, label=subset[0]["label"], color=color, linewidth=1.8)
            if key == "abs_error_mean":
                lo = np.asarray([r["abs_error_p10"] for r in subset])
                hi = np.asarray([r["abs_error_p90"] for r in subset])
                ax.fill_between(x, lo, hi, color=color, alpha=.09, linewidth=0)
        ax.axvline(shock_time, color="#555", linestyle="--", linewidth=1)
        ax.set_ylabel(ylabel)
        ax.grid(alpha=.15)
        ax.set_xlim(max(0, shock_time - 7 * dt), shock_time + 39 * dt)
    axes[0].legend(ncol=2, fontsize=8, loc="upper right")
    axes[1].set_xlabel("Simulation time (one unit per step)")
    for suffix in ("svg", "pdf"):
        fig.savefig(output / f"{group}.{suffix}")
    plt.close(fig)


def write_csv(path: Path, rows: list[dict]) -> None:
    opener = gzip.open if path.suffix == ".gz" else Path.open
    with opener(path, "wt" if path.suffix == ".gz" else "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        if path.suffix == ".gz":
            writer.writerows({key: format(value, ".9g") if isinstance(value, float) else value
                              for key, value in row.items()} for row in rows)
        else:
            writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads(args.config.read_text(encoding="utf-8"))
    args.output.mkdir(parents=True, exist_ok=True)
    rows, trajectories = run_scenarios(spec)
    summary = summarize(rows)
    write_csv(args.output / "scenario_runs.csv", rows)
    write_csv(args.output / "scenario_summary.csv", summary)
    write_csv(args.output / "scenario_timeseries.csv.gz", trajectories)
    for group in spec["groups"]:
        plot_group(trajectories, group, int(spec["perturbation"]["step"]), args.output)
    metadata = {
        "model_version": MODEL_VERSION,
        "config_sha256": hashlib.sha256(args.config.read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "numpy": importlib.metadata.version("numpy"),
        "matplotlib": importlib.metadata.version("matplotlib"),
        "rng": "numpy.random.default_rng / PCG64 family",
        "seed": spec["seed"], "n_runs_per_scenario": spec["n_runs"],
        "outputs": [p.name for p in sorted(args.output.iterdir()) if p.is_file()],
    }
    (args.output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
