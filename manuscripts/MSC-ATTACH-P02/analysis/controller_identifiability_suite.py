"""Run the standardized closed-loop development benchmark for M02.

This supplements the historical ARC-agent pipeline; it does not change ARC
semantics. Generators and candidates use documented dimensionless equations.
Run with --config, --output and --source-commit. All results are developmental.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path
from statistics import NormalDist

import numpy as np

from controller_identifiability_split import fit_validate_test, split_indices
from fit_controller import features


CANDIDATES = ("intercept", "ar", "p", "pi", "pid", "arx", "nonlinear", "switching")
NESTED = ("p", "pi", "pid")


def validate_spec(spec: dict) -> None:
    """Reject incomplete or nonfinite numeric development configurations."""
    if spec.get("evidence_status") != "development_only":
        raise ValueError("this suite accepts development-only designs")
    if not isinstance(spec["replications"], int) or spec["replications"] < 2:
        raise ValueError("at least two independent replications are required")
    if not spec["generators"] or any(g not in CANDIDATES for g in spec["generators"]):
        raise ValueError("unknown or empty generator set")
    if len(set(spec["generators"])) != len(spec["generators"]):
        raise ValueError("duplicate generators")
    if not spec["conditions"]:
        raise ValueError("empty condition list")
    if len(spec["split"]) != 2 or not np.all(np.isfinite(spec["split"])):
        raise ValueError("two finite split fractions are required")
    split_indices(100, *spec["split"])
    if len({c["id"] for c in spec["conditions"]}) != len(spec["conditions"]):
        raise ValueError("duplicate condition IDs")
    numeric = [spec["epsilon"], spec["coverage"], spec["integral_leak"],
               spec["action_noise_sd"], spec["process_noise_sd"],
               spec["excitation_sd"], spec["nonlinear_width"],
               *spec["gains"].values()]
    if not np.all(np.isfinite(numeric)):
        raise ValueError("all numeric settings must be finite")
    if spec["epsilon"] <= 0 or not 0 < spec["coverage"] < 1:
        raise ValueError("positive epsilon and coverage in (0,1) required")
    if not 0 <= spec["integral_leak"] <= 1 or spec["nonlinear_width"] <= 0:
        raise ValueError("invalid memory leak or nonlinear width")
    for key in ("action_noise_sd", "process_noise_sd", "excitation_sd"):
        if spec[key] < 0:
            raise ValueError("noise/excitation SD must be nonnegative")
    for condition in spec["conditions"]:
        steps, stride = condition["steps"], condition["stride"]
        if not isinstance(steps, int) or steps < 15:
            raise ValueError("steps must be an integer >=15")
        if not isinstance(stride, int) or stride < 1:
            raise ValueError("stride must be a positive integer")
        values = [condition[k] for k in ("missingness", "noise_sd", "feedback", "clip")]
        if not np.all(np.isfinite(values)):
            raise ValueError("condition settings must be finite")
        if not 0 <= condition["missingness"] < 1 or condition["noise_sd"] < 0:
            raise ValueError("invalid missingness or noise SD")
        if condition["feedback"] < 0 or condition["clip"] <= 0:
            raise ValueError("invalid feedback or clipping bound")


def generate(spec: dict, condition: dict, generator: str, seed: int) -> dict:
    """Generate [steps] error/action vectors and true effective coefficients.

    A unit-time feedback plant follows x[t+1]=x[t]+feedback*a[t]+noise.
    The reference target contains persistent exogenous excitation. Actions
    have additive noise and symmetric clipping; plant state is not clipped.
    Generator streams are paired across families and observation conditions.
    """
    n = condition["steps"]
    rng = np.random.default_rng(seed)
    # Separate streams preserve common draws when trajectory length changes.
    target = np.sin(np.arange(n) / 13.0) * 0.12
    target += rng.normal(0, spec["excitation_sd"], n)
    action_noise = np.random.default_rng(seed + 1_000_000).normal(
        0, spec["action_noise_sd"], n
    )
    process_noise = np.random.default_rng(seed + 2_000_000).normal(
        0, spec["process_noise_sd"], n
    )
    gains = spec["gains"].copy()
    if condition.get("reduced_pid") and generator == "pid":
        gains["ki"] = gains["kd"] = 0.0
    reduced_pid = condition.get("reduced_pid") and generator == "pid"
    effective = "p" if reduced_pid else generator
    error = np.empty(n)
    action = np.empty(n)
    state, integral, previous_error, previous_action = 0.0, 0.0, 0.0, 0.0
    clipped = 0
    for t in range(n):
        error[t] = target[t] - state
        integral = spec["integral_leak"] * integral + error[t]
        derivative = error[t] - previous_error if t else 0.0
        if generator == "intercept":
            raw = 0.0
        elif generator == "ar":
            raw = gains["rho"] * previous_action
        elif generator in NESTED:
            raw = gains["kp"] * error[t]
            if generator in ("pi", "pid"):
                raw += gains["ki"] * integral
            if generator == "pid":
                raw += gains["kd"] * derivative
        elif generator == "arx":
            raw = gains["kp"] * error[t] + gains["rho"] * previous_action
        elif generator == "nonlinear":
            raw = gains["amplitude"] * np.tanh(error[t] / spec["nonlinear_width"])
        else:
            slope = gains["kp_positive"] if error[t] >= 0 else gains["kp_negative"]
            raw = slope * error[t]
        noisy = raw + action_noise[t]
        action[t] = np.clip(noisy, -condition["clip"], condition["clip"])
        clipped += abs(noisy) > condition["clip"]
        state += condition["feedback"] * action[t] + process_noise[t]
        previous_error, previous_action = error[t], action[t]
    coefficients = {
        "intercept": [], "ar": [gains["rho"]], "p": [gains["kp"]],
        "pi": [gains["kp"], gains["ki"]],
        "pid": [gains["kp"], gains["ki"], gains["kd"]],
        "arx": [gains["kp"], gains["rho"]],
        "nonlinear": [gains["amplitude"]],
        "switching": [gains["kp_positive"], gains["kp_negative"]],
    }
    return {"error": error, "action": action, "effective": effective,
            "clipping_fraction": clipped / n,
            "true_coefficients": [0.0, *coefficients[generator]]}


def observe(generated: dict, condition: dict, seed: int) -> tuple:
    """Return observed [n] error/action/elapsed-time vectors after MCAR gaps.

    Always retain time zero. Reconstruct histories from retained snapshots,
    never from hidden integral/action values. No interpolation is performed.
    """
    n = len(generated["error"])
    indices = np.arange(0, n, condition["stride"])
    missing_draws = np.random.default_rng(seed + 3_000_000).random(n)
    indices = indices[missing_draws[indices] >= condition["missingness"]]
    indices = np.unique(np.r_[0, indices])
    noise = np.random.default_rng(seed + 4_000_000).standard_normal(n)
    error = generated["error"][indices] + condition["noise_sd"] * noise[indices]
    action = generated["action"][indices]
    dt = np.r_[1.0, np.diff(indices).astype(float)]
    return error, action, dt


def matrices(error: np.ndarray, action: np.ndarray, dt: np.ndarray,
             leak: float, width: float) -> dict:
    """Build causal [observations, features] conditional-prediction matrices."""
    lag = np.r_[0.0, action[:-1]]
    out = {"intercept": np.empty((len(action), 0)), "ar": lag[:, None]}
    for name in NESTED:
        out[name] = features(error, dt, name, leak)[0]
    out["arx"] = np.column_stack([error, lag])
    out["nonlinear"] = np.tanh(error / width)[:, None]
    out["switching"] = np.column_stack([np.maximum(error, 0), np.minimum(error, 0)])
    return out


def evaluate(spec: dict, condition: dict, generator: str, replicate: int) -> dict:
    """Keep one attempted trajectory with per-candidate fit/status diagnostics."""
    seed = spec["seed"] + replicate
    generated = generate(spec, condition, generator, seed)
    error, action, dt = observe(generated, condition, seed)
    row = {"condition": condition["id"], "generator": generator,
           "effective_generator": generated["effective"], "replicate": replicate,
           "seed": seed, "attempted": True, "observed_n": len(action),
           "realized_missingness": 1 - len(action) / len(
               np.arange(0, condition["steps"], condition["stride"])
           ),
           "clipping_fraction": generated["clipping_fraction"],
           "true_coefficients": generated["true_coefficients"], "fits": {},
           "selected": None, "nested_selected": None, "competitor": None,
           "paired_delta": None, "near_tie": None, "failure_reason": None}
    try:
        fit_end, validation_end = split_indices(len(action), *spec["split"])
    except ValueError:
        row["failure_reason"] = "insufficient_observations"
        return row
    designs = matrices(
        error, action, dt, spec["integral_leak"], spec["nonlinear_width"]
    )
    for name in CANDIDATES:
        try:
            fit = fit_validate_test(
                designs[name], action, fit_end, validation_end, evaluate_final=False
            )
            full_rank = fit["fit_rank"] == fit["fit_columns"]
            fit["status"] = "ok" if full_rank else "rank_deficient"
            row["fits"][name] = fit
        except np.linalg.LinAlgError:
            row["fits"][name] = {"status": "numerical_failure"}
    valid = [name for name in CANDIDATES if row["fits"][name]["status"] == "ok"]
    if not valid:
        row["failure_reason"] = "no_evaluable_candidate"
        return row
    # Candidate order is fixed; test loss is never accessed by this selection.
    def select(names: list[str]) -> str:
        """Choose an eligible candidate using validation loss only."""
        return min(names, key=lambda name: row["fits"][name]["validation_rmse"])
    row["selected"] = select(valid)
    nested = [name for name in valid if name in NESTED]
    row["nested_selected"] = select(nested) if nested else None
    competitors = [name for name in valid if name != generator]
    row["competitor"] = select(competitors) if competitors else None
    # Only now expose final actions to frozen fitted candidates and choices.
    for name in valid:
        design = np.column_stack([np.ones(len(action)), designs[name]])
        prediction = design[validation_end:] @ row["fits"][name]["coefficients"]
        row["fits"][name]["final_test_rmse"] = float(np.sqrt(np.mean(
            (action[validation_end:] - prediction) ** 2
        )))
    if generator in valid and row["competitor"]:
        row["paired_delta"] = (row["fits"][generator]["final_test_rmse"]
                               - row["fits"][row["competitor"]]["final_test_rmse"])
        row["near_tie"] = abs(row["paired_delta"]) < spec["epsilon"]
    return row


def wilson(successes: int, n: int, coverage: float) -> tuple:
    """Return a Wilson interval for independent attempted-trajectory recovery."""
    if not n:
        return None, None
    z = NormalDist().inv_cdf((1 + coverage) / 2)
    p = successes / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    radius = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return float(center - radius), float(center + radius)


def summarize(rows: list[dict], spec: dict) -> list[dict]:
    """Summarize recovery and pointwise developmental paired-loss intervals."""
    groups = {}
    for row in rows:
        groups.setdefault((row["condition"], row["generator"]), []).append(row)
    summaries = []
    z = NormalDist().inv_cdf((1 + spec["coverage"]) / 2)
    for (condition, generator), group in sorted(groups.items()):
        n = len(group)
        correct = sum(r["selected"] == generator for r in group)
        effective = sum(r["selected"] == r["effective_generator"] for r in group)
        evaluable = sum(r["selected"] is not None for r in group)
        delta = np.array([
            r["paired_delta"] for r in group if r["paired_delta"] is not None
        ])
        low, high = wilson(correct, n, spec["coverage"])
        mean = float(delta.mean()) if len(delta) else None
        ci_low = ci_high = None
        label = "insufficient_paired_replications"
        if len(delta) >= 2:
            radius = z * float(delta.std(ddof=1)) / np.sqrt(len(delta))
            ci_low, ci_high = mean - radius, mean + radius
            epsilon = spec["epsilon"]
            if ci_low > -epsilon and ci_high < epsilon:
                label = "development_equivalent"
            elif ci_high < -epsilon:
                label = "generator_predictively_better"
            elif ci_low > epsilon:
                label = "competitor_predictively_better"
            else:
                label = "inconclusive"
        summaries.append({
            "condition": condition, "generator": generator, "attempted": n,
            "evaluable": evaluable, "selection_failures": n - evaluable,
            "nominal_correct": correct, "effective_correct": effective,
            "recovery_attempted": correct / n,
            "recovery_evaluable": correct / evaluable if evaluable else None,
            "recovery_low": low, "recovery_high": high,
            "paired_n": len(delta), "paired_delta_mean": mean,
            "paired_delta_low": ci_low, "paired_delta_high": ci_high,
            "near_ties": sum(r["near_tie"] is True for r in group),
            "equivalence_status": label,
            "mean_clipping_fraction": float(np.mean([
                r["clipping_fraction"] for r in group
            ])),
            "mean_observed_n": float(np.mean([r["observed_n"] for r in group])),
            "candidate_failures": sum(
                f["status"] != "ok" for r in group for f in r["fits"].values()
            ),
        })
    return summaries


def csv_write(path: Path, rows: list[dict]) -> None:
    """Write nonempty flat records, preserving unavailable fields as blanks."""
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run(spec: dict, output: Path, source_commit: str) -> list[dict]:
    """Execute the design and archive records, summaries and content hashes."""
    validate_spec(spec)
    output.mkdir(parents=True, exist_ok=True)
    rows = [evaluate(spec, condition, generator, replicate)
            for condition in spec["conditions"] for generator in spec["generators"]
            for replicate in range(spec["replications"])]
    summary = summarize(rows, spec)
    with (output / "trajectories.jsonl").open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, allow_nan=False) + "\n")
    csv_write(output / "summary.csv", summary)
    confusion = []
    for condition in spec["conditions"]:
        for generator in spec["generators"]:
            group = [
                r for r in rows if r["condition"] == condition["id"]
                and r["generator"] == generator
            ]
            for selected in (*CANDIDATES, "failed"):
                count = sum((r["selected"] or "failed") == selected for r in group)
                confusion.append({"condition": condition["id"], "generator": generator,
                                  "selected": selected, "count": count,
                                  "attempted": len(group)})
    csv_write(output / "confusion.csv", confusion)
    parameters = []
    for condition in spec["conditions"]:
        for generator in spec["generators"]:
            group = [
                r for r in rows if r["condition"] == condition["id"]
                and r["generator"] == generator
                and r["fits"].get(generator, {}).get("status") == "ok"
            ]
            if not group:
                continue
            for index in range(len(group[0]["true_coefficients"])):
                truth = group[0]["true_coefficients"][index]
                values = np.array([
                    r["fits"][generator]["coefficients"][index] for r in group
                ])
                parameters.append({
                    "condition": condition["id"], "generator": generator,
                    "coefficient_index": index, "true_value": truth,
                    "n_evaluable": len(values), "mean_estimate": values.mean(),
                    "bias": values.mean() - truth,
                    "sd": values.std(ddof=1) if len(values) > 1 else None,
                    "coverage": None, "coverage_status": "not_implemented",
                })
    if parameters:
        csv_write(output / "parameters.csv", parameters)
    config_text = json.dumps(spec, indent=2) + "\n"
    (output / "config.json").write_text(config_text)
    source_files = [
        Path(__file__),
        Path(__file__).with_name("controller_identifiability_split.py"),
        Path(__file__).with_name("fit_controller.py"),
    ]

    def checksum(path: Path) -> str:
        """Hash the exact archived bytes."""
        return hashlib.sha256(path.read_bytes()).hexdigest()
    metadata = {"evidence_status": "development_only", "source_commit": source_commit,
                "source_hashes": {p.name: checksum(p) for p in source_files},
                "python": platform.python_version(), "numpy": np.__version__,
                "config_sha256": checksum(output / "config.json"),
                "seed": spec["seed"], "attempted_trajectories": len(rows),
                "prediction": "conditional action given error and past observations",
                "intervals": "pointwise Wilson recovery and normal paired mean",
                "multiplicity": "no confirmatory familywise conclusions",
                "outputs_sha256": {p.name: checksum(p) for p in sorted(output.iterdir())
                                    if p.is_file() and p.name != "metadata.json"}}
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return summary


def main() -> None:
    """Read a development configuration and run the reproducible benchmark."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    summary = run(json.loads(args.config.read_text()), args.output, args.source_commit)
    print(f"Completed {len(summary)} generator-condition cells")


if __name__ == "__main__":
    main()
