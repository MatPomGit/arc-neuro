"""Coefficient-first ARC H1 inference analysis.

This module supersedes the sequential M1-first RMSE gate as the primary H1
decision architecture. It consumes the merged exact-design replication table
and writes compact operating-characteristic summaries for:

- H1-P1: positive M2 within-person desired-state coefficient;
- H1-P2: positive M3 within-person signed-discrepancy coefficient;
- Holm family-wise error control across one-sided SESOI tests for H1-P1/H1-P2;
- coefficient SESOI classification;
- M2 signed-discrepancy symmetry contrast;
- secondary descriptive M4 asymmetry contrast when available;
- secondary temporal-holdout RMSE summaries.

The legacy h1_decision_analysis.py is retained only to audit the failed
sequential predictive rule documented by the completed Monte Carlo.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import norm

CRIT95 = 1.959963984540054
CRIT90 = 1.6448536269514722


def one_sided_positive_p(estimate: float, two_sided_p: float) -> float:
    """Convert a symmetric two-sided Wald p value to H1: beta > 0."""

    if not (math.isfinite(estimate) and math.isfinite(two_sided_p)):
        return float("nan")
    half = min(max(two_sided_p, 0.0), 1.0) / 2.0
    return half if estimate >= 0.0 else 1.0 - half


def sesoi_one_sided_p(
    estimate: float,
    se: float,
    sesoi: float,
) -> float:
    """Test H0: beta <= SESOI against H1: beta > SESOI."""

    if not (
        math.isfinite(estimate)
        and math.isfinite(se)
        and se > 0.0
        and math.isfinite(sesoi)
    ):
        return float("nan")
    z_value = (estimate - sesoi) / se
    return float(norm.sf(z_value))


def holm_adjust(pvalues: dict[str, float]) -> dict[str, float]:
    """Return Holm-adjusted p values while preserving input labels."""

    valid = [
        (name, float(value))
        for name, value in pvalues.items()
        if math.isfinite(float(value))
    ]
    adjusted = {name: float("nan") for name in pvalues}
    if not valid:
        return adjusted

    ordered = sorted(valid, key=lambda item: item[1])
    m = len(ordered)
    running = 0.0
    for rank, (name, value) in enumerate(ordered):
        candidate = min(1.0, (m - rank) * value)
        running = max(running, candidate)
        adjusted[name] = min(1.0, running)
    return adjusted


def estimate_is_positive(value: object) -> bool:
    """Return True only for a finite positive coefficient."""

    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(numeric) and numeric > 0.0


def interval_classification(
    low: float,
    high: float,
    tolerance: float,
    *,
    compatible: str,
    incompatible: str,
) -> str:
    """Three-state equivalence classification around zero."""

    if not (
        math.isfinite(low)
        and math.isfinite(high)
        and math.isfinite(tolerance)
        and tolerance > 0
    ):
        return "unavailable"
    if low >= -tolerance and high <= tolerance:
        return compatible
    if low > tolerance or high < -tolerance:
        return incompatible
    return "inconclusive"


def row_data_sufficient(row: pd.Series, config: dict[str, Any]) -> bool:
    """Apply the locked primary coefficient-data sufficiency criterion."""

    minimum_people = int(config.get("minimum_people_with_valid_lags", 100))
    return float(row.get("people_with_minimum_lags", 0.0)) >= minimum_people


def classify_replication(
    row: pd.Series,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Classify one exact-design replication under revised H1 inference."""

    final = dict(config.get("final_design", {}))
    alpha = float(final.get("familywise_alpha", 0.05))
    sesoi = float(final.get("primary_sesoi_beta", 0.5))
    sym_tol = float(
        final.get("signed_discrepancy_symmetry_tolerance", 1.0)
    )
    asymmetry_role = str(
        final.get(
            "asymmetry_role",
            "secondary descriptive structural evidence only",
        )
    )

    out: dict[str, Any] = {
        "couples": int(row["couples"]),
        "compliance_target": float(row["compliance_target"]),
        "missingness_strength": float(row["missingness_strength"]),
        "truth": str(row.get("truth", "")),
        "replication": int(row.get("replication", -1)),
        "people": int(row.get("people", int(row["couples"]) * 2)),
        "people_with_minimum_lags": float(
            row.get("people_with_minimum_lags", float("nan"))
        ),
        "primary_data_sufficient": row_data_sufficient(row, config),
    }

    specs = {
        "H1_P1": (
            "M2",
            "M2_r_star_wp10_estimate",
            "M2_r_star_wp10_se",
            "M2_r_star_wp10_pvalue",
        ),
        "H1_P2": (
            "M3",
            "M3_e_wp10_estimate",
            "M3_e_wp10_se",
            "M3_e_wp10_pvalue",
        ),
    }

    raw_p: dict[str, float] = {}
    for label, (model, est_col, se_col, p_col) in specs.items():
        estimate = float(row.get(est_col, float("nan")))
        se = float(row.get(se_col, float("nan")))
        p2 = float(row.get(p_col, float("nan")))
        converged = bool(row.get(f"{model}_converged", False))
        low95 = (
            estimate - CRIT95 * se
            if math.isfinite(estimate) and math.isfinite(se)
            else float("nan")
        )
        p1 = one_sided_positive_p(estimate, p2)
        p_sesoi = sesoi_one_sided_p(estimate, se, sesoi)
        raw_p[label] = p_sesoi
        out[f"{label}_estimate"] = estimate
        out[f"{label}_se"] = se
        out[f"{label}_ci95_low"] = low95
        out[f"{label}_p_one_sided_zero"] = p1
        out[f"{label}_p_one_sided_sesoi"] = p_sesoi
        out[f"{label}_model_converged"] = converged
        out[f"{label}_ci95_above_sesoi"] = bool(
            math.isfinite(low95) and low95 > sesoi
        )

    adjusted = holm_adjust(raw_p)
    for label in specs:
        out[f"{label}_p_holm"] = adjusted[label]
        out[f"{label}_supported"] = bool(
            out["primary_data_sufficient"]
            and out[f"{label}_model_converged"]
            and math.isfinite(adjusted[label])
            and adjusted[label] < alpha
            and estimate_is_positive(out[f"{label}_estimate"])
        )

    if not out["primary_data_sufficient"]:
        primary = "inconclusive_data_insufficient"
    elif not (
        out["H1_P1_model_converged"]
        and out["H1_P2_model_converged"]
    ):
        primary = "inconclusive_model_failure"
    elif not all(
        math.isfinite(float(out[f"{label}_estimate"]))
        and math.isfinite(float(out[f"{label}_se"]))
        and math.isfinite(float(out[f"{label}_p_holm"]))
        for label in specs
    ):
        primary = "inconclusive_precision"
    else:
        supported = int(out["H1_P1_supported"]) + int(
            out["H1_P2_supported"]
        )
        primary = (
            "full_support"
            if supported == 2
            else "partial_support"
            if supported == 1
            else "no_confirmatory_support"
        )
    out["H1_primary_result"] = primary

    # M2 symmetry: use prospective 90% equivalence interval from stored SE.
    d_sym = float(row.get("M2_d_sym_estimate", float("nan")))
    d_sym_se = float(row.get("M2_d_sym_se", float("nan")))
    if math.isfinite(d_sym) and math.isfinite(d_sym_se):
        sym_low = d_sym - CRIT90 * d_sym_se
        sym_high = d_sym + CRIT90 * d_sym_se
    else:
        sym_low = sym_high = float("nan")
    out["M2_d_sym_estimate"] = d_sym
    out["M2_d_sym_ci90_low"] = sym_low
    out["M2_d_sym_ci90_high"] = sym_high
    out["M2_symmetry_result"] = interval_classification(
        sym_low,
        sym_high,
        sym_tol,
        compatible="symmetry_compatible",
        incompatible="symmetry_incompatible",
    )

    # M4 asymmetry is available only for simulations/fits produced after the
    # post-Monte-Carlo revision.
    d_asym = float(row.get("M4_d_asym_estimate", float("nan")))
    d_asym_se = float(row.get("M4_d_asym_se", float("nan")))
    if math.isfinite(d_asym) and math.isfinite(d_asym_se):
        asym_low = d_asym - CRIT90 * d_asym_se
        asym_high = d_asym + CRIT90 * d_asym_se
    else:
        asym_low = asym_high = float("nan")
    out["M4_d_asym_estimate"] = d_asym
    out["M4_d_asym_ci90_low"] = asym_low
    out["M4_d_asym_ci90_high"] = asym_high
    out["M4_asymmetry_result"] = "secondary_descriptive_only"
    out["M4_asymmetry_role"] = asymmetry_role

    for name in (
        "delta_M1_M0",
        "delta_M2_M1",
        "delta_M3_M2",
        "delta_M4_M3",
        "delta_M4_M2",
    ):
        out[name] = float(row.get(name, float("nan")))
        out[f"{name}_ci_low"] = float(
            row.get(f"{name}_ci_low", float("nan"))
        )
        out[f"{name}_ci_high"] = float(
            row.get(f"{name}_ci_high", float("nan"))
        )
        out[f"{name}_n"] = int(row.get(f"{name}_n", 0))

    return out


def build_inference_table(
    frame: pd.DataFrame,
    config: dict[str, Any],
) -> pd.DataFrame:
    """Classify all rows using the revised coefficient-first architecture."""

    return pd.DataFrame(
        [classify_replication(row, config) for _, row in frame.iterrows()]
    )


def probability_table(
    inference: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """Return scenario-specific frequencies for a categorical result."""

    keys = [
        "couples",
        "compliance_target",
        "missingness_strength",
        "truth",
    ]
    counts = (
        inference.groupby(keys + [column], dropna=False)
        .size()
        .rename("n")
        .reset_index()
    )
    totals = counts.groupby(keys)["n"].transform("sum")
    counts["probability"] = counts["n"] / totals
    return counts


def primary_operating_characteristics(
    inference: pd.DataFrame,
) -> pd.DataFrame:
    """Summarize support, sufficiency, and co-primary power by scenario."""

    keys = [
        "couples",
        "compliance_target",
        "missingness_strength",
        "truth",
    ]
    rows: list[dict[str, Any]] = []
    for values, group in inference.groupby(keys, dropna=False):
        row = dict(zip(keys, values, strict=True))
        row["replications"] = int(len(group))
        for col in (
            "primary_data_sufficient",
            "H1_P1_supported",
            "H1_P2_supported",
        ):
            row[f"{col}_rate"] = float(group[col].astype(bool).mean())
        row["full_support_rate"] = float(
            (group["H1_primary_result"] == "full_support").mean()
        )
        row["partial_support_rate"] = float(
            (group["H1_primary_result"] == "partial_support").mean()
        )
        row["no_confirmatory_support_rate"] = float(
            (
                group["H1_primary_result"]
                == "no_confirmatory_support"
            ).mean()
        )
        row["inconclusive_rate"] = float(
            group["H1_primary_result"]
            .astype(str)
            .str.startswith("inconclusive_")
            .mean()
        )
        rows.append(row)
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
        "couples",
        "compliance_target",
        "missingness_strength",
        "truth",
        "replication",
        "people_with_minimum_lags",
        "M2_converged",
        "M3_converged",
        "M2_r_star_wp10_estimate",
        "M2_r_star_wp10_se",
        "M2_r_star_wp10_pvalue",
        "M3_e_wp10_estimate",
        "M3_e_wp10_se",
        "M3_e_wp10_pvalue",
        "M2_d_sym_estimate",
        "M2_d_sym_se",
    }
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(
            f"input missing revised H1 inference columns: {sorted(missing)}"
        )

    inference = build_inference_table(frame, config)
    primary_oc = primary_operating_characteristics(inference)
    primary_matrix = probability_table(
        inference, "H1_primary_result"
    )
    symmetry_matrix = probability_table(
        inference, "M2_symmetry_result"
    )
    asymmetry_matrix = probability_table(
        inference, "M4_asymmetry_result"
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    inference.to_csv(
        args.output_dir / "h1_inference_long.csv",
        index=False,
    )
    primary_oc.to_csv(
        args.output_dir / "h1_primary_operating_characteristics.csv",
        index=False,
    )
    primary_matrix.to_csv(
        args.output_dir / "h1_primary_result_matrix.csv",
        index=False,
    )
    symmetry_matrix.to_csv(
        args.output_dir / "h1_symmetry_result_matrix.csv",
        index=False,
    )
    asymmetry_matrix.to_csv(
        args.output_dir / "h1_asymmetry_result_matrix.csv",
        index=False,
    )

    print(f"Revised H1 inference rows: {len(inference)}")
    print(
        "Primary scenarios: "
        f"{len(primary_oc)}"
    )


if __name__ == "__main__":
    main()
