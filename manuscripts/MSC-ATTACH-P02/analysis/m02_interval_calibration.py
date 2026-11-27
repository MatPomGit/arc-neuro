"""Illustrative calibration of paired mean confidence interval coverage.

Synthetic controlled distributions, NOT the M02 closed-loop model, and NOT
preregistered confirmatory evidence. Fresh independent calibration draws.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
from statistics import NormalDist
import numpy as np

SCENARIOS = ("normal", "skewed", "heavy_tail", "contaminated")


def draw(rng, scenario, trials, n):
    if scenario == "normal":
        return rng.normal(0, 1, (trials, n))
    if scenario == "skewed":
        return rng.exponential(1, (trials, n)) - 1.0
    if scenario == "heavy_tail":
        return rng.standard_t(3, (trials, n)) / np.sqrt(3)
    if scenario == "contaminated":
        x = rng.normal(0, 1, (trials, n))
        return x + rng.normal(0, 8, (trials, n)) * (
            rng.random((trials, n)) < 0.02
        )
    raise ValueError(f"Unknown scenario: {scenario}")


def intervals(sample, confidence, bootstraps, rng):
    """Resample whole paired differences, never times or two losses separately."""
    n = len(sample)
    if n < 3 or bootstraps < 20 or not np.all(np.isfinite(sample)):
        raise ValueError("Need >=3 finite pairs and >=20 bootstrap samples")
    mean = float(sample.mean())
    se = float(sample.std(ddof=1) / np.sqrt(n))
    z = NormalDist().inv_cdf((1 + confidence) / 2)
    alpha = (1 - confidence) / 2
    draws = sample[rng.integers(0, n, (bootstraps, n))]
    bootmeans = draws.mean(axis=1)
    percentile = np.quantile(bootmeans, [alpha, 1 - alpha])
    bootse = draws.std(axis=1, ddof=1) / np.sqrt(n)
    ok = bootse > 0
    if ok.mean() < 0.95 or se <= 0:
        studentized = (float("nan"), float("nan"))
    else:
        pivot = (bootmeans[ok] - mean) / bootse[ok]
        qlo, qhi = np.quantile(pivot, [alpha, 1 - alpha])
        studentized = (float(mean - qhi * se), float(mean - qlo * se))
    return {"normal": (mean - z * se, mean + z * se),
            "percentile": tuple(map(float, percentile)),
            "studentized": studentized}


def calibrate(seed=20261008, trials=300, n_values=(20, 80),
              bootstraps=399, confidence=0.95):
    if trials < 20 or bootstraps < 20 or any(n < 3 for n in n_values) or not 0 < confidence < 1:
        raise ValueError("Invalid calibration settings")
    results = []
    for si, scenario in enumerate(SCENARIOS):
        for ni, n in enumerate(n_values):
            rng = np.random.default_rng(np.random.SeedSequence([seed, si, ni]))
            stats = {key: [0, 0, 0.] for key in ("normal", "percentile", "studentized")}
            for sample in draw(rng, scenario, trials, n):
                for method, (lo, hi) in intervals(sample, confidence, bootstraps, rng).items():
                    if np.isfinite(lo) and np.isfinite(hi) and lo <= hi:
                        stats[method][0] += int(lo <= 0 <= hi)
                        stats[method][1] += 1
                        stats[method][2] += hi - lo
            for method, (hits, valid, widths) in stats.items():
                coverage = hits / valid if valid else None
                results.append({
                    "scenario": scenario, "n": n, "method": method,
                    "trials": trials, "valid_intervals": valid,
                    "empirical_coverage": coverage,
                    "coverage_mc_se": (
                        float(np.sqrt(coverage * (1 - coverage) / valid)) if valid else None
                    ),
                    "mean_interval_width": widths / valid if valid else None,
                    "nominal_confidence": confidence, "truth_mean": 0.0,
                    "seed": seed, "evidence_status": "method_calibration_only",
                })
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--seed", type=int, default=20261008)
    p.add_argument("--trials", type=int, default=300)
    p.add_argument("--sample-sizes", type=int, nargs="+", default=[20, 80])
    p.add_argument("--bootstraps", type=int, default=399)
    p.add_argument("--confidence", type=float, default=0.95)
    args = p.parse_args()
    rows = calibrate(args.seed, args.trials, tuple(args.sample_sizes),
                     args.bootstraps, args.confidence)
    args.output.mkdir(parents=True, exist_ok=True)
    path = args.output / "calibration.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    metadata = {
        "evidence_status": "method_calibration_only", "seed": args.seed,
        "trials": args.trials, "sample_sizes": args.sample_sizes,
        "bootstraps": args.bootstraps, "confidence": args.confidence,
        "scenarios": list(SCENARIOS),
        "csv_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "warning": "Distribution-only calibration, NOT M02 closed-loop coverage.",
    }
    (args.output / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    for row in rows:
        print(f"{row['scenario']:13} n={row['n']:3} {row['method']:11} "
              f"coverage={row['empirical_coverage']:.3f} "
              f"MC_SE={row['coverage_mc_se']:.3f}")


if __name__ == "__main__":
    main()
