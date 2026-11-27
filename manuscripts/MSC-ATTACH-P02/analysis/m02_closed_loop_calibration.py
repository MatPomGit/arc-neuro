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
from statistics import NormalDist

import numpy as np

from controller_identifiability_robustness import evaluate, validate_robustness
from m02_interval_calibration import intervals


# Each stream consumes offsets up to 5,029,998 in the current generator.
# Allocate nonoverlapping blocks across reference, trials, and cells.
STREAM_STRIDE = 10_000_000


def stream_seed(seed, cell_index, stream_index, trials):
    if seed < 0 or cell_index < 0 or not 0 <= stream_index <= trials:
        raise ValueError("Invalid seed allocation")
    return seed + (cell_index * (trials + 1) + stream_index) * STREAM_STRIDE


def wilson(hits, n):
    if n == 0:
        return None, None
    z = NormalDist().inv_cdf(0.975)
    rate = hits / n
    denominator = 1 + z*z/n
    center = (rate + z*z/(2*n))/denominator
    half = z*np.sqrt(rate*(1-rate)/n + z*z/(4*n*n))/denominator
    return max(0.0, float(center-half)), min(1.0, float(center+half))


def reference_class(low, high, epsilon):
    """Classify an approximate reference band, not the unknown true mean."""
    if -epsilon < low and high < epsilon:
        return "inside"
    if low >= epsilon or high <= -epsilon:
        return "outside"
    return "ambiguous"


def equivalence_diagnostics(hits, valid, trials, ref_low, ref_high, epsilon):
    status = reference_class(ref_low, ref_high, epsilon)
    low, high = wilson(hits, valid)
    return {
        "epsilon": epsilon,
        "reference_band_class": status,
        "equivalence_declarations": hits,
        "equivalence_fraction_valid": hits / valid if valid else None,
        "equivalence_fraction_attempted": hits / trials,
        "equivalence_wilson_95_low": low,
        "equivalence_wilson_95_high": high,
        "apparent_false_equivalence_fraction_valid": (
            hits / valid if status == "outside" and valid else None
        ),
        "apparent_equivalence_detection_fraction_valid": (
            hits / valid if status == "inside" and valid else None
        ),
    }


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
    if reference_n < 3 or trials < 2 or sample_n < 3 or bootstraps < 20 or seed < 0 or not 0 < coverage < 1:
        raise ValueError("Invalid calibration sizes")
    if (reference_n >= 10_000 or sample_n >= 10_000):
        raise ValueError("Role streams require fewer than 10,000 replicates")
    epsilons = sorted(set(float(v) for v in spec["epsilon_grid"]))
    if not epsilons or any(not np.isfinite(v) or v <= 0 for v in epsilons):
        raise ValueError("Invalid exploratory epsilon grid")
    result = []
    for ci, condition in enumerate(conditions):
        for gi, generator in enumerate(generators):
            cell = ci * len(generators) + gi
            block = stream_seed(seed, cell, 0, trials)
            reference, ref_failed = sample_stream(
                spec, condition, generator, block, reference_n
            )
            if len(reference) < 3:
                raise RuntimeError("Too few reference pairs for " + condition["id"])
            truth = float(reference.mean())
            reference_se = float(reference.std(ddof=1) / np.sqrt(len(reference)))
            reference_low = truth - 1.96 * reference_se
            reference_high = truth + 1.96 * reference_se
            counts = {m: [0, 0, 0.0, 0, 0, 0, []] for m in
                      ("normal", "percentile", "studentized")}
            eq_counts = {m: {e: 0 for e in epsilons} for m in counts}
            failures = 0
            for trial in range(trials):
                trial_seed = stream_seed(seed, cell, trial + 1, trials)
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
                    if np.isfinite(low) and np.isfinite(high) and low <= high:
                        counts[method][0] += int(low <= truth <= high)
                        counts[method][1] += 1
                        counts[method][2] += high - low
                        counts[method][3] += int(low > 0 or high < 0)
                        counts[method][4] += int(low <= reference_low and high >= reference_high)
                        counts[method][5] += int(low <= reference_high and high >= reference_low)
                        counts[method][6].append((high-low)/2)
                        for epsilon in epsilons:
                            eq_counts[method][epsilon] += int(-epsilon < low and high < epsilon)
            for method, (covered, eligible, width, excludes_zero, contains_ref, overlaps_ref, halfwidths) in counts.items():
                wilson_low, wilson_high = wilson(covered, eligible)
                median_halfwidth = float(np.median(halfwidths)) if eligible else None
                row = {
                    "condition": condition["id"], "generator": generator,
                    "method": method, "reference_n": len(reference),
                    "reference_failures": ref_failed, "reference_mean": truth,
                    "reference_mc_se": reference_se,
                    "requested_calibration_trials": trials,
                    "requested_pairs_per_trial": sample_n,
                    "failed_calibration_triads": failures,
                    "valid_intervals": eligible,
                    "invalid_or_insufficient_trials": trials - eligible,
                    "coverage_hits": covered,
                    "coverage_wilson_95_low": wilson_low,
                    "coverage_wilson_95_high": wilson_high,
                    "reference_95_normal_low": reference_low,
                    "reference_95_normal_high": reference_high,
                    "fraction_containing_reference_band": contains_ref / eligible if eligible else None,
                    "fraction_overlapping_reference_band": overlaps_ref / eligible if eligible else None,
                    "median_interval_halfwidth": median_halfwidth,
                    "reference_se_to_median_halfwidth": reference_se / median_halfwidth if median_halfwidth else None,
                    "coverage_against_estimated_reference": covered / eligible if eligible else None,
                    "mean_width": width / eligible if eligible else None,
                    "excluded_zero_fraction": excludes_zero / eligible if eligible else None,
                    "nominal_coverage": coverage,
                    "status": "exploratory_closed_loop_method_calibration",
                    "equivalence_diagnostics_json": json.dumps([
                        equivalence_diagnostics(eq_counts[method][epsilon], eligible,
                                                trials, reference_low, reference_high, epsilon)
                        for epsilon in epsilons
                    ], allow_nan=False, sort_keys=True),
                }
                result.append(row)
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
    args.output.mkdir(parents=True, exist_ok=False)
    path = args.output / "closed_loop_coverage.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    commit = subprocess.run(["git", "rev-parse", "HEAD"],
                            cwd=Path(__file__).resolve().parent,
                            capture_output=True, text=True, check=True).stdout.strip()
    (args.output / "metadata.json").write_text(json.dumps({
        "status": "exploratory_closed_loop_method_calibration",
        "source_commit": commit,
        "seed_allocation": "disjoint 10-million blocks per cell and reference/trial; v2",
        "numpy_version": np.__version__,
        "equivalence_rule": "strict interval containment; reference-band class is approximate; ambiguous references do not receive error-rate labels",
        "coverage_diagnostic": "Wilson intervals conditional on valid trials and fixed estimated reference; reference-band sensitivity is not a coverage correction",
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
