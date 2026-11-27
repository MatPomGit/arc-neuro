"""Focused operating-characteristic analysis for the ARC H1 M4 asymmetry contrast.

This script consumes merged exact-design replication output generated with
h1_asymmetry_validation_config.json. It does not run Monte Carlo itself.

For M4, the fitted contrast is

    d_asym = beta_positive + beta_negative

because beta_negative multiplies max(-e, 0). Perfect signed-discrepancy
symmetry implies d_asym = 0.

Candidate tolerances are evaluated with a 90% Wald interval. This utility
reports operating characteristics and guardrail status, but deliberately does
not choose the scientific tolerance automatically.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import pandas as pd

CRIT90 = 1.6448536269514722


def classify_asymmetry_interval(
    low: float,
    high: float,
    tolerance: float,
) -> str:
    """Classify one 90% interval relative to a symmetric tolerance region."""

    if not (
        math.isfinite(low)
        and math.isfinite(high)
        and math.isfinite(tolerance)
        and tolerance > 0.0
    ):
        return "unavailable"
    if low >= -tolerance and high <= tolerance:
        return "symmetry_compatible"
    if low > tolerance or high < -tolerance:
        return "asymmetry_material"
    return "inconclusive"


def binomial_summary(successes: int, n: int) -> tuple[float, float, float, float]:
    """Return probability, MCSE, and clipped normal 95% Monte Carlo interval."""

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


def long_classifications(
    frame: pd.DataFrame,
    config: dict[str, Any],
) -> pd.DataFrame:
    """Expand each replication over prespecified candidate tolerances."""

    validation = dict(config["asymmetry_validation"])
    tolerances = [float(v) for v in validation["candidate_tolerances"]]
    minimum_people = int(config.get("minimum_people_with_valid_lags", 100))

    rows: list[dict[str, Any]] = []
    for _, source in frame.iterrows():
        estimate = float(source.get("M4_d_asym_estimate", float("nan")))
        se = float(source.get("M4_d_asym_se", float("nan")))
        converged = bool(source.get("M4_converged", False))
        sufficient = (
            float(source.get("people_with_minimum_lags", 0.0))
            >= minimum_people
        )

        if math.isfinite(estimate) and math.isfinite(se):
            low = estimate - CRIT90 * se
            high = estimate + CRIT90 * se
        else:
            low = high = float("nan")

        for tolerance in tolerances:
            if not sufficient:
                result = "inconclusive_data_insufficient"
            elif not converged:
                result = "inconclusive_model_failure"
            elif not (
                math.isfinite(estimate)
                and math.isfinite(se)
                and math.isfinite(low)
                and math.isfinite(high)
            ):
                result = "inconclusive_precision"
            else:
                result = classify_asymmetry_interval(low, high, tolerance)

            truth = str(source["truth"])
            expected = (
                "symmetry_compatible"
                if truth == "M3"
                else "asymmetry_material"
                if truth == "M4"
                else "not_target_truth"
            )
            rows.append(
                {
                    "couples": int(source["couples"]),
                    "compliance_target": float(source["compliance_target"]),
                    "missingness_strength": float(source["missingness_strength"]),
                    "truth": truth,
                    "replication": int(source["replication"]),
                    "tolerance": tolerance,
                    "d_asym_estimate": estimate,
                    "d_asym_se": se,
                    "d_asym_ci90_low": low,
                    "d_asym_ci90_high": high,
                    "data_sufficient": sufficient,
                    "M4_converged": converged,
                    "classification": result,
                    "expected_classification": expected,
                    "correct_classification": bool(result == expected),
                }
            )
    return pd.DataFrame(rows)


def operating_characteristics(long: pd.DataFrame) -> pd.DataFrame:
    """Summarize classification frequencies by design cell and tolerance."""

    keys = [
        "couples",
        "compliance_target",
        "missingness_strength",
        "truth",
        "tolerance",
    ]
    rows: list[dict[str, Any]] = []
    for values, group in long.groupby(keys, dropna=False):
        row = dict(zip(keys, values, strict=True))
        n = int(len(group))
        row["replications"] = n

        indicators = {
            "correct_classification": group["correct_classification"].astype(bool),
            "symmetry_compatible": group["classification"].eq("symmetry_compatible"),
            "asymmetry_material": group["classification"].eq("asymmetry_material"),
            "inconclusive": group["classification"].astype(str).str.startswith("inconclusive"),
            "data_sufficient": group["data_sufficient"].astype(bool),
            "M4_converged": group["M4_converged"].astype(bool),
        }
        for label, indicator in indicators.items():
            probability, mcse, low, high = binomial_summary(
                int(indicator.sum()),
                n,
            )
            row[f"{label}_rate"] = probability
            row[f"{label}_mcse"] = mcse
            row[f"{label}_mc95_low"] = low
            row[f"{label}_mc95_high"] = high

        row["mean_d_asym_estimate"] = float(
            pd.to_numeric(group["d_asym_estimate"], errors="coerce").mean()
        )
        row["mean_d_asym_se"] = float(
            pd.to_numeric(group["d_asym_se"], errors="coerce").mean()
        )
        rows.append(row)
    return pd.DataFrame(rows)


def candidate_guardrails(
    oc: pd.DataFrame,
    config: dict[str, Any],
) -> pd.DataFrame:
    """Evaluate prespecified cross-cell guardrails without selecting a winner."""

    validation = dict(config["asymmetry_validation"])
    guardrails = dict(
        validation["operating_characteristic_guardrails"]
    )
    rows: list[dict[str, Any]] = []

    for tolerance, group in oc.groupby("tolerance", dropna=False):
        m3 = group[group["truth"] == "M3"]
        m4 = group[group["truth"] == "M4"]

        if m3.empty or m4.empty:
            raise ValueError(
                "focused asymmetry validation requires both M3 and M4 truth"
            )

        worst_m3_symmetry = float(m3["symmetry_compatible_rate"].min())
        worst_m3_false_asymmetry = float(m3["asymmetry_material_rate"].max())
        worst_m4_material = float(m4["asymmetry_material_rate"].min())
        worst_m4_false_symmetry = float(m4["symmetry_compatible_rate"].max())
        worst_inconclusive = float(group["inconclusive_rate"].max())

        checks = {
            "M3_symmetry_compatibility": (
                worst_m3_symmetry
                >= float(
                    guardrails["minimum_M3_symmetry_compatibility_rate"]
                )
            ),
            "M3_false_asymmetry": (
                worst_m3_false_asymmetry
                <= float(guardrails["maximum_M3_false_asymmetry_rate"])
            ),
            "M4_material_asymmetry": (
                worst_m4_material
                >= float(
                    guardrails["minimum_M4_material_asymmetry_rate"]
                )
            ),
            "M4_false_symmetry": (
                worst_m4_false_symmetry
                <= float(guardrails["maximum_M4_false_symmetry_rate"])
            ),
        }

        rows.append(
            {
                "tolerance": float(tolerance),
                "worst_M3_symmetry_compatible_rate": worst_m3_symmetry,
                "worst_M3_false_asymmetry_rate": worst_m3_false_asymmetry,
                "worst_M4_material_asymmetry_rate": worst_m4_material,
                "worst_M4_false_symmetry_rate": worst_m4_false_symmetry,
                "worst_inconclusive_rate": worst_inconclusive,
                **{
                    f"passes_{name}": bool(value)
                    for name, value in checks.items()
                },
                "passes_all_guardrails": bool(all(checks.values())),
            }
        )

    return pd.DataFrame(rows).sort_values("tolerance")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    config = json.loads(args.config.read_text(encoding="utf-8"))

    required = {
        "couples",
        "compliance_target",
        "missingness_strength",
        "truth",
        "replication",
        "people_with_minimum_lags",
        "M4_converged",
        "M4_d_asym_estimate",
        "M4_d_asym_se",
    }
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(
            f"input missing asymmetry-validation columns: {sorted(missing)}"
        )

    truth_values = set(frame["truth"].astype(str))
    unexpected = truth_values - {"M3", "M4"}
    if unexpected:
        raise ValueError(
            f"unexpected truth scenarios in focused validation: {sorted(unexpected)}"
        )

    long = long_classifications(frame, config)
    oc = operating_characteristics(long)
    guardrails = candidate_guardrails(oc, config)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    long.to_csv(
        args.output_dir / "h1_asymmetry_decisions_long.csv",
        index=False,
    )
    oc.to_csv(
        args.output_dir / "h1_asymmetry_operating_characteristics.csv",
        index=False,
    )
    guardrails.to_csv(
        args.output_dir / "h1_asymmetry_candidate_guardrails.csv",
        index=False,
    )

    print(f"Asymmetry decision rows: {len(long)}")
    print(f"Candidate tolerances: {len(guardrails)}")
    print(
        "Passing all guardrails: "
        + ", ".join(
            str(value)
            for value in guardrails.loc[
                guardrails["passes_all_guardrails"],
                "tolerance",
            ].tolist()
        )
        if bool(guardrails["passes_all_guardrails"].any())
        else "Passing all guardrails: none"
    )


if __name__ == "__main__":
    main()
