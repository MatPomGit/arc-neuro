# SPDX-License-Identifier: Apache-2.0
# Modified in ARC Neuro: resolve the migrated configuration relative to this module.
"""Prospective METHOD calibration using actual M02 closed-loop triads.

Separate reference and calibration streams. Descriptive pilot only, never
reuse streams for a preregistered confirmatory experiment.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np

from controller_identifiability_robustness import evaluate, validate_robustness
from m02_interval_calibration import intervals


def paired_delta(spec, condition, generator, replicate):
    """Use only independent-role validation-RMSE comparisons."""
    records, _, _ = evaluate(spec, condition, generator, replicate)
    if not records or records[0]["failure"]:
        return None
    selected = [
        s for s in records[0]["scores"]
        if s["mode"] == "independent" and s["criterion"] == "validation_rmse"
    ]
    if len(selected) != 1:
        raise RuntimeError("Expected exactly one independent RMSE contrast")
    return selected[0]["paired_delta"]


def sample_stream(base_spec, condition, generator, seed, requested):
    spec = dict(base_spec)
    spec["seed"] = seed
    # Each replicate has fit, validation and final innovations at role offsets.
    # Respect the robustness implementation's 10,000-replicate role separation.
    if requested >= 10_000:
        raise ValueError("One stream cannot reach 10,000 replicates")
    values, failures = [], 0
    for replicate in range(requested):
        value = paired_delta(spec, condition, generator, replicate)
        if value is None or not np.isfinite(value):
            failures += 1
        else:
            values.append(float(value))
    return np.array(values), failures


def calibrate(spec, conditions, generators, reference_n, trials,
              sample_n, bootstraps, seed, coverage):
    if reference_n < 3 or trials < 2 or sample_n < 3 or bootstraps < 20:
        raise ValueError("Invalid calibration sizes")
    if (reference_n >= 10_000 or sample_n >= 10_000):
        raise ValueError("Role streams require fewer than 10,000 replicates")
    result = []
    for ci, condition in enumerate(conditions):
        for gi, generator in enumerate(generators):
            # Widely separated seed blocks ensure distinct reference and
            # calibration samples, even within one dataset.
            block = seed + ci * 1_000_000_000 + gi * 100_000_000
            reference, ref_failed = sample_stream(
                spec, condition, generator, block, reference_n
            )
            if len(reference) < 3:
                raise RuntimeError("Too few reference pairs for " + condition["id"])
            truth = float(reference.mean())
            reference_se = float(reference.std(ddof=1) / np.sqrt(len(reference)))
            counts = {m: [0, 0, 0.0, 0] for m in
                      ("normal", "percentile", "studentized")}
            failures = 0
            for trial in range(trials):
                # trial seed blocks exceed total within-stream role offsets.
                trial_seed = block + 10_000_000 + trial * 100_000
                values, failed = sample_stream(spec, condition, generator,
                                               trial_seed, sample_n)
                failures += failed
                if len(values) < 3:
                    continue
                bootstrap_rng = np.random.default_rng(
                    np.random.SeedSequence([seed, ci, gi, trial, 31])
                )
                for method, (low, high) in intervals(
                    values, coverage, bootstraps, bootstrap_rng
                ).items():
                    if np.isfinite(low) and np.isfinite(high):
                        counts[method][0] += int(low <= truth <= high)
                        counts[method][1] += 1
                        counts[method][2] += high - low
                        counts[method][3] += int(low > 0 or high < 0)
            for method, (covered, eligible, width, excludes_zero) in counts.items():
                result.append({
                    "condition": condition["id"], "generator": generator,
                    "method": method, "reference_n": len(reference),
                    "reference_failures": ref_failed, "reference_mean": truth,
                    "reference_mc_se": reference_se,
                    "requested_calibration_trials": trials,
                    "requested_pairs_per_trial": sample_n,
                    "failed_calibration_triads": failures,
                    "valid_intervals": eligible,
                    "coverage_against_estimated_reference": covered / eligible if eligible else None,
                    "mean_width": width / eligible if eligible else None,
                    "excluded_zero_fraction": excludes_zero / eligible if eligible else None,
                    "nominal_coverage": coverage,
                    "status": "exploratory_closed_loop_method_calibration",
                })
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, default=Path(__file__).resolve().parent / "configs/m02_robustness_development.json")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--conditions", nargs="+", default=["reference", "heavy_tail", "combined"])
    p.add_argument("--generators", nargs="+", default=["p", "pid"])
    p.add_argument("--reference-n", type=int, default=200)
    p.add_argument("--trials", type=int, default=20)
    p.add_argument("--sample-n", type=int, default=20)
    p.add_argument("--bootstraps", type=int, default=199)
    p.add_argument("--seed", type=int, default=260810000)
    p.add_argument("--coverage", type=float, default=0.95)
    args = p.parse_args()
    spec = json.loads(args.config.read_text(encoding="utf-8"))
    validate_robustness(spec)
    by_id = {c["id"]: c for c in spec["conditions"]}
    if len(set(args.conditions)) != len(args.conditions) or any(
        c not in by_id for c in args.conditions
    ):
        raise ValueError("Unknown or duplicate conditions")
    if len(set(args.generators)) != len(args.generators) or any(
        g not in spec["generators"] for g in args.generators
    ):
        raise ValueError("Unknown or duplicate generators")
    if not 0 < args.coverage < 1:
        raise ValueError("Coverage must be in (0, 1)")
    rows = calibrate(spec, [by_id[c] for c in args.conditions], args.generators,
                     args.reference_n, args.trials, args.sample_n,
                     args.bootstraps, args.seed, args.coverage)
    args.output.mkdir(parents=True, exist_ok=True)
    path = args.output / "closed_loop_coverage.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    commit = subprocess.run(["git", "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=True).stdout.strip()
    (args.output / "metadata.json").write_text(json.dumps({
        "status": "exploratory_closed_loop_method_calibration",
        "source_commit": commit,
        "config_sha256": hashlib.sha256(args.config.read_bytes()).hexdigest(),
        "output_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "reference_truth": "independent Monte Carlo estimate, not exact; uncertainty given",
        "warning": "Reference uncertainty can distort apparent interval coverage. "
                   "Not eligible for confirmatory inference or automatic OSF submission.",
        "args": vars(args) | {"config": str(args.config), "output": str(args.output)},
    }, indent=2) + "\n", encoding="utf-8")
    print("Completed closed-loop method calibration:", path)


if __name__ == "__main__":
    main()
