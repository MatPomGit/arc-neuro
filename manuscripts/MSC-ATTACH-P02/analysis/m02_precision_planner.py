"""Prospective Monte Carlo precision planning for M02 (no simulation outcomes).

Uses a worst-case Wilson interval bound over p in [0,1]. Simultaneous
Bonferroni coverage is a conservative planning option, not a finalized
inferential choice or a correction for data-dependent contrasts.
"""
from __future__ import annotations

import argparse
import json
from math import ceil, sqrt
from statistics import NormalDist


def wilson_half_width(n: int, p: float, confidence: float) -> float:
    if n < 1 or not 0 <= p <= 1 or not 0 < confidence < 1:
        raise ValueError("Invalid n, proportion, or confidence")
    z = NormalDist().inv_cdf((1 + confidence) / 2)
    return z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (
        1 + z * z / n
    )


def required_attempts(target: float, confidence: float, comparisons: int = 1) -> int:
    """Minimum independent attempted triads for a worst-case Wilson half-width.

    The maximum half-width is attained at p=0.5. The comparison adjustment
    applies Bonferroni to interval coverage; it is not a power calculation.
    """
    if not 0 < target < 0.5 or not 0 < confidence < 1 or comparisons < 1:
        raise ValueError("Invalid target, confidence, or comparisons")
    adjusted = 1 - (1 - confidence) / comparisons
    low, high = 1, 2
    while wilson_half_width(high, 0.5, adjusted) > target:
        low, high = high, high * 2
    while low + 1 < high:
        mid = (low + high) // 2
        if wilson_half_width(mid, 0.5, adjusted) <= target:
            high = mid
        else:
            low = mid
    return high if wilson_half_width(low, 0.5, adjusted) > target else low


def plan(target: float, confidence: float, comparisons: int,
         generators: int, conditions: int, trajectories_per_attempt: int,
         evaluable_fraction: float) -> dict:
    if min(generators, conditions, trajectories_per_attempt) < 1:
        raise ValueError("Counts must be positive")
    if not 0 < evaluable_fraction <= 1:
        raise ValueError("Evaluable fraction must be in (0,1]")
    n = required_attempts(target, confidence, comparisons)
    cells = generators * conditions
    return {
        "status": "planning_only_not_preregistered",
        "target_wilson_half_width": target,
        "familywise_confidence": confidence,
        "bonferroni_comparisons": comparisons,
        "attempts_per_cell": n,
        "cells": cells,
        "total_attempted_triads": n * cells,
        "total_generated_trajectories": n * cells * trajectories_per_attempt,
        "assumed_evaluable_fraction_not_empirically_estimated": evaluable_fraction,
        "expected_evaluable_per_cell_not_guaranteed": n * evaluable_fraction,
        "approx_attempts_for_evaluable_target": ceil(n / evaluable_fraction),
        "caution": (
            "Wilson precision concerns attempted-triad recovery only. "
            "It does not ensure paired-loss equivalence precision, bootstrap "
            "coverage, parameter interval coverage, or computational feasibility."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--half-width", type=float, default=0.025)
    parser.add_argument("--confidence", type=float, default=0.95)
    parser.add_argument("--comparisons", type=int, default=1)
    parser.add_argument("--generators", type=int, default=8)
    parser.add_argument("--conditions", type=int, default=64)
    parser.add_argument("--trajectories-per-attempt", type=int, default=3)
    parser.add_argument("--evaluable-fraction", type=float, default=1.0)
    args = parser.parse_args()
    print(json.dumps(plan(args.half_width, args.confidence, args.comparisons,
                          args.generators, args.conditions,
                          args.trajectories_per_attempt,
                          args.evaluable_fraction), indent=2))


if __name__ == "__main__":
    main()
