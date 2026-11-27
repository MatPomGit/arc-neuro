# SPDX-License-Identifier: Apache-2.0
# Modified in ARC Neuro: update example commands and protocol paths.
"""Audit the superseded ARC H1 sequential RMSE decision rule.

This module is retained for historical Monte Carlo diagnostics only. The
primary post-Monte-Carlo H1 architecture is implemented in
h1_inference_analysis.py and does not use M1-first predictive gating.

Summarize ARC H1 Monte Carlo architectural decision errors.

Consumes merged h1_exact_replications.csv and writes:
- h1_decision_matrix.csv: truth x retained architecture frequencies;
- h1_margin_operating_characteristics.csv: error rates by design and margin;
- h1_design_ranking.csv: conservative N/margin screening across data-quality cells.

This utility does not choose a scientific margin automatically. It exposes the
trade-offs required by manuscripts/MSC-ATTACH-P01/protocol/decision_margins.md.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import pandas as pd

TRUTH_TO_DECISION = {
    "M0": "M0_no_state_increment",
    "M1": "M1_state_only",
    "M2": "M2_separate_components",
    "M3": "M3_signed_discrepancy",
    "M4": "M4_asymmetric",
}

COMPLEXITY = {
    "M0_no_state_increment": 0,
    "M1_state_only": 1,
    "M3_signed_discrepancy": 2,
    "M4_asymmetric": 3,
    "M2_separate_components": 3,
}


def margin_columns(frame: pd.DataFrame) -> list[str]:
    return sorted(c for c in frame.columns if c.startswith("representation_margin_"))


def long_decisions(
    frame: pd.DataFrame,
    config: dict[str, object] | None = None,
) -> pd.DataFrame:
    rows = []
    config = config or {}
    minimum_people = int(config.get("minimum_people_with_valid_lags", 100))
    minimum_prediction_couples = int(
        config.get("minimum_prediction_couples", 2)
    )
    for column in margin_columns(frame):
        margin = column.removeprefix("representation_margin_").replace("p", ".")
        for _, row in frame.iterrows():
            decision = row.get(column)
            truth = str(row["truth"])
            expected = TRUTH_TO_DECISION[truth]
            converged = bool(row.get("all_models_converged", False))
            sufficient = (
                float(row.get("people_with_minimum_lags", 0.0)) >= minimum_people
                and all(
                    int(row.get(f"delta_{pair}_n", 0)) >= minimum_prediction_couples
                    for pair in ("M1_M0", "M2_M1", "M3_M2", "M4_M3", "M4_M2")
                )
            )
            valid = converged and sufficient and pd.notna(decision)
            if not converged:
                decision = "inconclusive_model_failure"
            elif not sufficient:
                decision = "inconclusive_data_insufficient"
            elif not valid:
                decision = "inconclusive_other"
            elif str(decision).startswith("inconclusive_"):
                decision = str(decision)
            correct = decision == expected
            expected_complexity = COMPLEXITY[expected]
            observed_complexity = COMPLEXITY.get(str(decision))
            rows.append({
                "couples": int(row["couples"]),
                "compliance_target": float(row["compliance_target"]),
                "missingness_strength": float(row["missingness_strength"]),
                "truth": truth,
                "replication": int(row["replication"]),
                "margin": float(margin),
                "expected": expected,
                "decision": decision,
                "correct": correct,
                "inconclusive": str(decision).startswith("inconclusive_"),
                "false_simplification": (
                    observed_complexity is not None
                    and observed_complexity < expected_complexity
                ),
                "false_complexity": (
                    observed_complexity is not None
                    and observed_complexity > expected_complexity
                ),
                "people": int(row.get("people", int(row["couples"]) * 2)),
                "people_with_minimum_lags": float(row.get("people_with_minimum_lags", float("nan"))),
                "data_sufficient": (
                    float(row.get("people_with_minimum_lags", 0.0)) >= minimum_people
                    and all(
                        int(row.get(f"delta_{pair}_n", 0)) >= minimum_prediction_couples
                        for pair in ("M1_M0", "M2_M1", "M3_M2", "M4_M3", "M4_M2")
                    )
                ),
                "all_models_converged": bool(row.get("all_models_converged", False)),
            })
    return pd.DataFrame(rows)


def decision_matrix(long: pd.DataFrame) -> pd.DataFrame:
    keys = ["couples", "compliance_target", "missingness_strength", "margin", "truth"]
    counts = (
        long.groupby(keys + ["decision"], dropna=False)
        .size().rename("n").reset_index()
    )
    totals = counts.groupby(keys)["n"].transform("sum")
    counts["probability"] = counts["n"] / totals
    return counts


def binomial_precision(successes: int, n: int) -> tuple[float, float, float, float]:
    """Return probability, Monte Carlo SE, and a clipped 95% MC interval."""

    if n <= 0:
        nan = float("nan")
        return nan, nan, nan, nan
    probability = successes / n
    se = math.sqrt(probability * (1.0 - probability) / n)
    critical = 1.959963984540054
    return (
        probability,
        se,
        max(0.0, probability - critical * se),
        min(1.0, probability + critical * se),
    )


def operating_characteristics(long: pd.DataFrame) -> pd.DataFrame:
    keys = ["couples", "compliance_target", "missingness_strength", "margin", "truth"]
    rows = []
    binary = [
        ("correct", "correct_decision"),
        ("inconclusive", "inconclusive"),
        ("false_simplification", "false_simplification"),
        ("false_complexity", "false_complexity"),
        ("all_models_converged", "convergence"),
        ("data_sufficient", "data_sufficiency"),
    ]
    for values, group in long.groupby(keys, dropna=False):
        row = dict(zip(keys, values, strict=True))
        n = int(len(group))
        row["replications"] = n
        for source, label in binary:
            successes = int(group[source].astype(bool).sum())
            probability, se, low, high = binomial_precision(successes, n)
            row[f"{label}_rate"] = probability
            row[f"{label}_mcse"] = se
            row[f"{label}_mc95_low"] = low
            row[f"{label}_mc95_high"] = high
        row["mean_people_with_minimum_lags"] = float(
            pd.to_numeric(group["people_with_minimum_lags"], errors="coerce").mean()
        )
        rows.append(row)
    return pd.DataFrame(rows)


def design_ranking(oc: pd.DataFrame) -> pd.DataFrame:
    """Worst-cell screening; lower loss is preferable, not a final selection."""
    keys = ["couples", "margin"]
    rows = []
    for values, group in oc.groupby(keys, dropna=False):
        couples, margin = values
        rows.append({
            "couples": int(couples),
            "margin": float(margin),
            "worst_correct_decision_rate": float(group["correct_decision_rate"].min()),
            "worst_convergence_rate": float(group["convergence_rate"].min()),
            "worst_inconclusive_rate": float(group["inconclusive_rate"].max()),
            "worst_false_simplification_rate": float(group["false_simplification_rate"].max()),
            "worst_false_complexity_rate": float(group["false_complexity_rate"].max()),
            "minimum_mean_people_with_minimum_lags": float(group["mean_people_with_minimum_lags"].min()),
        })
    result = pd.DataFrame(rows)
    # Screening score is descriptive only and must not be used as an automatic
    # scientific choice of N or margin.
    result["screening_loss"] = (
        (1.0 - result["worst_correct_decision_rate"])
        + result["worst_inconclusive_rate"]
        + result["worst_false_simplification_rate"]
        + result["worst_false_complexity_rate"]
        + (1.0 - result["worst_convergence_rate"])
    )
    return result.sort_values(["screening_loss", "couples", "margin"])


def sesoi_operating_characteristics(
    frame: pd.DataFrame,
    sesoi_values: list[float],
) -> pd.DataFrame:
    """Evaluate whether the M2 symmetry contrast is practically equivalent."""

    required = {"M2_d_sym_ci_low", "M2_d_sym_ci_high"}
    if not required.issubset(frame.columns):
        return pd.DataFrame()
    rows = []
    keys = ["couples", "compliance_target", "missingness_strength", "truth"]
    for values, group in frame.groupby(keys, dropna=False):
        for sesoi in sesoi_values:
            low = pd.to_numeric(group["M2_d_sym_ci_low"], errors="coerce")
            high = pd.to_numeric(group["M2_d_sym_ci_high"], errors="coerce")
            valid = low.notna() & high.notna()
            equivalent = valid & (low >= -sesoi) & (high <= sesoi)
            excludes_equivalence = valid & ((low > sesoi) | (high < -sesoi))
            rows.append({
                **dict(zip(keys, values, strict=True)),
                "sesoi_beta": float(sesoi),
                "replications": int(len(group)),
                "valid_symmetry_intervals": int(valid.sum()),
                "symmetry_equivalence_rate": float(equivalent.mean()),
                "symmetry_exclusion_rate": float(excludes_equivalence.mean()),
                "symmetry_inconclusive_rate": float((valid & ~equivalent & ~excludes_equivalence).mean()),
            })
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    required = {
        "couples", "compliance_target", "missingness_strength",
        "truth", "replication", "all_models_converged",
    }
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"input missing required columns: {sorted(missing)}")
    if not margin_columns(frame):
        raise ValueError("input contains no representation_margin_* columns")

    long = long_decisions(frame, config)
    matrix = decision_matrix(long)
    oc = operating_characteristics(long)
    ranking = design_ranking(oc)
    sesoi = sesoi_operating_characteristics(
        frame,
        [float(v) for v in config.get("candidate_sesoi_beta", [])],
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    long.to_csv(args.output_dir / "h1_decisions_long.csv", index=False)
    matrix.to_csv(args.output_dir / "h1_decision_matrix.csv", index=False)
    oc.to_csv(args.output_dir / "h1_margin_operating_characteristics.csv", index=False)
    ranking.to_csv(args.output_dir / "h1_design_ranking.csv", index=False)
    if not sesoi.empty:
        sesoi.to_csv(
            args.output_dir / "h1_sesoi_operating_characteristics.csv",
            index=False,
        )

    print(f"Decision rows: {len(long)}")
    print(f"Design-margin candidates: {len(ranking)}")


if __name__ == "__main__":
    main()
