# SPDX-License-Identifier: Apache-2.0
"""Configuration-driven ARC simulation experiments.

All experiment-defining values live in JSON files under the adjacent configs directory.
The plotting code is intentionally thin so manuscript results can be traced to
named configuration files.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from arc_model import ARCConfig, ARCTraits, ControllerGains, impulse, simulate
from fit_controller import compare_models


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def make_traits(values: dict) -> ARCTraits:
    return ARCTraits(**values)


def make_config(values: dict) -> ARCConfig:
    return ARCConfig(**values)


def save_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def phase_map(spec: dict, out: Path) -> None:
    config = make_config(spec["simulation"])
    fixed = spec["fixed_traits"].copy()
    x_name = spec["x"]["name"]
    y_name = spec["y"]["name"]
    x_values = np.linspace(spec["x"]["min"], spec["x"]["max"], spec["x"]["n"])
    y_values = np.linspace(spec["y"]["min"], spec["y"]["max"], spec["y"]["n"])
    shock = impulse(config, **spec["perturbation"])
    seed0 = int(spec["seed"])

    matrix = np.zeros((len(y_values), len(x_values)))
    rows: list[dict] = []

    for iy, y in enumerate(y_values):
        for ix, x in enumerate(x_values):
            values = fixed | {x_name: float(x), y_name: float(y)}
            result = simulate(
                make_traits(values),
                config,
                perturbation=shock,
                seed=seed0 + iy * len(x_values) + ix,
            )
            matrix[iy, ix] = result.metrics[spec["display_metric"]]
            rows.append(
                {
                    x_name: float(x),
                    y_name: float(y),
                    "regime": result.regime,
                    **result.metrics,
                }
            )

    fig, ax = plt.subplots(figsize=(7.2, 5.8))
    image = ax.imshow(
        matrix,
        origin="lower",
        extent=[x_values.min(), x_values.max(), y_values.min(), y_values.max()],
        aspect="auto",
    )
    fig.colorbar(image, ax=ax, label=spec["display_metric"])
    ax.set_xlabel(spec["x"]["label"])
    ax.set_ylabel(spec["y"]["label"])
    ax.set_title(spec["title"])
    fig.tight_layout()
    fig.savefig(out / spec["figure"], dpi=220)
    plt.close(fig)
    save_rows(out / spec["csv"], rows)


def recovery_profiles(spec: dict, out: Path) -> None:
    config = make_config(spec["simulation"])
    shock = impulse(config, **spec["perturbation"])
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    rows: list[dict] = []

    for index, profile in enumerate(spec["profiles"]):
        result = simulate(
            make_traits(profile["traits"]),
            config,
            perturbation=shock,
            seed=int(spec["seed"]) + index,
        )
        ax.plot(
            result.series["time"],
            result.series["true_error"],
            label=f'{profile["name"]} ({result.regime})',
        )
        rows.append(
            {
                "profile": profile["name"],
                "regime": result.regime,
                **result.metrics,
            }
        )

    ax.axvline(spec["perturbation"]["step"], linestyle="--", linewidth=1)
    ax.axhline(0.0, linewidth=0.8)
    ax.set_xlabel("Simulation step")
    ax.set_ylabel("Relational discrepancy e")
    ax.set_title(spec["title"])
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / spec["figure"], dpi=220)
    plt.close(fig)
    save_rows(out / spec["csv"], rows)


def control_responsiveness(spec: dict, out: Path) -> None:
    C_values = np.linspace(spec["C"]["min"], spec["C"]["max"], spec["C"]["n"])
    b_values = np.linspace(
        spec["responsiveness"]["min"],
        spec["responsiveness"]["max"],
        spec["responsiveness"]["n"],
    )
    matrix = np.zeros((len(b_values), len(C_values)))
    rows: list[dict] = []
    seed0 = int(spec["seed"])

    for iy, b in enumerate(b_values):
        sim_values = spec["simulation"].copy()
        sim_values["responsiveness"] = float(b)
        config = make_config(sim_values)
        shock = impulse(config, **spec["perturbation"])

        for ix, C in enumerate(C_values):
            traits = spec["fixed_traits"] | {"C": float(C)}
            result = simulate(
                make_traits(traits),
                config,
                perturbation=shock,
                seed=seed0 + iy * len(C_values) + ix,
            )
            matrix[iy, ix] = result.metrics[spec["display_metric"]]
            rows.append(
                {
                    "C": float(C),
                    "responsiveness": float(b),
                    "regime": result.regime,
                    **result.metrics,
                }
            )

    fig, ax = plt.subplots(figsize=(7.2, 5.8))
    image = ax.imshow(
        matrix,
        origin="lower",
        extent=[C_values.min(), C_values.max(), b_values.min(), b_values.max()],
        aspect="auto",
    )
    fig.colorbar(image, ax=ax, label=spec["display_metric"])
    ax.set_xlabel("Relational-control propensity C")
    ax.set_ylabel("Responsiveness b")
    ax.set_title(spec["title"])
    fig.tight_layout()
    fig.savefig(out / spec["figure"], dpi=220)
    plt.close(fig)
    save_rows(out / spec["csv"], rows)


def parameter_recovery(spec: dict, out: Path) -> None:
    config = make_config(spec["simulation"])
    shock = impulse(config, **spec["perturbation"])
    rows: list[dict] = []
    rng = np.random.default_rng(int(spec["seed"]))

    for index in range(int(spec["n_runs"])):
        kp = float(rng.uniform(*spec["gain_ranges"]["kp"]))
        ki = float(rng.uniform(*spec["gain_ranges"]["ki"]))
        kd = float(rng.uniform(*spec["gain_ranges"]["kd"]))
        gains = ControllerGains(
            kp=kp,
            ki=ki,
            kd=kd,
            integral_leak=float(spec["integral_leak"]),
        )
        interval_values = np.asarray(spec.get("interval_values", [config.dt]), dtype=float)
        intervals = rng.choice(interval_values, size=config.steps)
        result = simulate(
            make_traits(spec["traits"]),
            config,
            perturbation=shock,
            gains=gains,
            seed=int(spec["seed"]) + index,
            intervals=intervals,
        )

        # Oracle: remove the known simulated gain modulation and strategy gate.
        # This checks numerical identifiability under the generating equation,
        # not whether human actions expose the latent controller coefficients.
        modifier = result.series["kp_effective"] / kp
        oracle = compare_models(
            result.series["estimated_error"],
            result.series["raw_control"] / modifier,
            intervals,
            gains.integral_leak,
            config.dt,
        )
        behavioral = compare_models(
            result.series["true_error"],
            result.series["action"],
            intervals,
            gains.integral_leak,
            config.dt,
        )
        pid_est = oracle["pid"]["parameter_estimates"]

        rows.append(
            {
                "run": index,
                "kp_true": kp,
                "ki_true": ki,
                "kd_true": kd,
                "kp_est": pid_est.get("kp", float("nan")),
                "ki_est": pid_est.get("ki", float("nan")),
                "kd_est": pid_est.get("kd", float("nan")),
                "oracle_pid_test_rmse": oracle["pid"]["test_rmse"],
                "behavior_context_rmse": behavioral["context"]["test_rmse"],
                "behavior_ar_rmse": behavioral["autoregressive"]["test_rmse"],
                "behavior_p_rmse": behavioral["p"]["test_rmse"],
                "behavior_pi_rmse": behavioral["pi"]["test_rmse"],
                "behavior_pid_rmse": behavioral["pid"]["test_rmse"],
                **result.metrics,
            }
        )

    save_rows(out / spec["csv"], rows)


def run_config(path: Path, out: Path) -> None:
    spec = load_json(path)
    out.mkdir(parents=True, exist_ok=True)
    experiment = spec["experiment"]

    if experiment == "phase_map":
        phase_map(spec, out)
    elif experiment == "recovery_profiles":
        recovery_profiles(spec, out)
    elif experiment == "control_responsiveness":
        control_responsiveness(spec, out)
    elif experiment == "parameter_recovery":
        parameter_recovery(spec, out)
    else:
        raise ValueError(f"Unknown experiment: {experiment}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one configured ARC experiment.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[3] / "build/MSC-ATTACH-P02/experiments")
    args = parser.parse_args()
    run_config(args.config, args.output)


if __name__ == "__main__":
    main()
