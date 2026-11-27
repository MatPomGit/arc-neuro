"""Summarize focused H1 comparable-lag sample-size recalibration."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import pandas as pd


def _rate(
    frame: pd.DataFrame,
    *,
    truth: str,
    column: str,
) -> float:
    row = frame[frame["truth"] == truth]
    if len(row) != 1:
        raise ValueError(f"expected one row for truth={truth}, got {len(row)}")
    return float(row.iloc[0][column])


def wilson_interval(successes: float, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Wilson score interval for a Monte Carlo probability."""

    if n <= 0:
        return float("nan"), float("nan")
    p = float(successes) / float(n)
    denominator = 1.0 + z * z / n
    centre = (p + z * z / (2.0 * n)) / denominator
    half = (
        z
        * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n))
        / denominator
    )
    return max(0.0, centre - half), min(1.0, centre + half)


def rate_interval(rate: float, n: int) -> tuple[float, float]:
    """Recover an integer event count from a Monte Carlo rate and bound it."""

    successes = int(round(float(rate) * int(n)))
    return wilson_interval(successes, int(n))


def summarize(
    primary_oc: pd.DataFrame,
    config: dict,
) -> tuple[pd.DataFrame, dict]:
    """Return per-N guardrail table and a machine-readable decision."""

    guard = config["recalibration_guardrails"]
    candidates = [int(v) for v in config["candidate_couples"]]
    rows = []

    for n in candidates:
        stress = primary_oc[
            (primary_oc["couples"] == n)
            & (primary_oc["compliance_target"] == 0.75)
            & (primary_oc["missingness_strength"] == 1.0)
        ].copy()
        reference = primary_oc[
            (primary_oc["couples"] == n)
            & (primary_oc["compliance_target"] == 0.75)
            & (primary_oc["missingness_strength"] == 0.0)
        ].copy()

        required_truths = {"M0", "M1", "M2", "M3", "M4"}
        if set(stress["truth"]) != required_truths:
            raise ValueError(
                f"N={n} stress condition missing truths: "
                f"{sorted(required_truths - set(stress['truth']))}"
            )
        if set(reference["truth"]) != required_truths:
            raise ValueError(
                f"N={n} reference condition missing truths: "
                f"{sorted(required_truths - set(reference['truth']))}"
            )

        stress_min_row = stress.loc[
            stress["primary_data_sufficient_rate"].idxmin()
        ]
        stress_min_suff = float(
            stress_min_row["primary_data_sufficient_rate"]
        )
        reference_min_suff = float(
            reference["primary_data_sufficient_rate"].min()
        )
        p1_power = _rate(
            stress, truth="M2", column="H1_P1_supported_rate"
        )
        p2_power = _rate(
            stress, truth="M3", column="H1_P2_supported_rate"
        )
        p1_fp = _rate(
            stress, truth="M0", column="H1_P1_supported_rate"
        )
        p2_fp = _rate(
            stress, truth="M0", column="H1_P2_supported_rate"
        )

        reps = int(stress_min_row["replications"])
        if not (stress["replications"].astype(int) == reps).all():
            raise ValueError(f"N={n} stress rows have unequal replication counts")
        suff_low, suff_high = rate_interval(stress_min_suff, reps)
        p1_power_low, p1_power_high = rate_interval(p1_power, reps)
        p2_power_low, p2_power_high = rate_interval(p2_power, reps)
        p1_fp_low, p1_fp_high = rate_interval(p1_fp, reps)
        p2_fp_low, p2_fp_high = rate_interval(p2_fp, reps)

        passes = {
            "data_sufficiency": suff_low
            >= float(guard["minimum_primary_data_sufficiency_rate"]),
            "H1_P1_power": p1_power_low
            >= float(guard["minimum_H1_P1_power_under_M2"]),
            "H1_P2_power": p2_power_low
            >= float(guard["minimum_H1_P2_power_under_M3"]),
            "H1_P1_type_I": p1_fp_high
            <= float(guard["maximum_H1_P1_false_positive_rate_under_M0"]),
            "H1_P2_type_I": p2_fp_high
            <= float(guard["maximum_H1_P2_false_positive_rate_under_M0"]),
        }
        rows.append(
            {
                "couples": n,
                "replications_per_stress_scenario": reps,
                "stress_min_data_sufficiency_rate": stress_min_suff,
                "stress_min_data_sufficiency_wilson_low": suff_low,
                "stress_min_data_sufficiency_wilson_high": suff_high,
                "reference_min_data_sufficiency_rate": reference_min_suff,
                "H1_P1_power_under_M2": p1_power,
                "H1_P1_power_wilson_low": p1_power_low,
                "H1_P1_power_wilson_high": p1_power_high,
                "H1_P2_power_under_M3": p2_power,
                "H1_P2_power_wilson_low": p2_power_low,
                "H1_P2_power_wilson_high": p2_power_high,
                "H1_P1_false_positive_under_M0": p1_fp,
                "H1_P1_false_positive_wilson_low": p1_fp_low,
                "H1_P1_false_positive_wilson_high": p1_fp_high,
                "H1_P2_false_positive_under_M0": p2_fp,
                "H1_P2_false_positive_wilson_low": p2_fp_low,
                "H1_P2_false_positive_wilson_high": p2_fp_high,
                **{f"pass_{k}": v for k, v in passes.items()},
                "passes_all_guardrails": all(passes.values()),
            }
        )

    table = pd.DataFrame(rows).sort_values("couples")
    passing = table[table["passes_all_guardrails"]]
    selected = (
        int(passing.iloc[0]["couples"]) if not passing.empty else None
    )
    decision = {
        "selected_analysis_target_couples": selected,
        "selection_status": (
            "selected"
            if selected is not None
            else "no_candidate_satisfies_all_guardrails"
        ),
        "candidate_couples": candidates,
        "guardrails": guard,
        "selection_rule_applied_prospectively": True,
    }
    return table, decision


def write_report(
    output_dir: Path,
    table: pd.DataFrame,
    decision: dict,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    table.to_csv(output_dir / "h1_recalibration_guardrails.csv", index=False)
    (output_dir / "h1_recalibration_decision.json").write_text(
        json.dumps(decision, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    selected = decision["selected_analysis_target_couples"]
    lines = [
        "# H1 comparable-lag recalibration decision",
        "",
        f"Status: **{decision['selection_status']}**.",
        "",
    ]
    if selected is not None:
        lines.append(
            f"Selected analysis target: **{selected} couples**, the smallest "
            "candidate satisfying every prespecified guardrail."
        )
    else:
        lines.append(
            "No candidate sample size satisfies every prespecified guardrail; "
            "the recruitment target must remain unfrozen."
        )
    lines += [
        "",
        "## Guardrail table",
        "",
        "See `h1_recalibration_guardrails.csv` for the complete machine-readable table.",
        "",
        "The selection condition is compliance = 0.75 with "
        "missingness_strength = 1. Guardrails are evaluated conservatively "
        "using 95% Wilson Monte Carlo confidence bounds: lower bounds for "
        "minimum-rate criteria and upper bounds for maximum-rate criteria. "
        "The missingness_strength = 0 condition is reported as a reference "
        "and does not override failure under the prespecified stress condition.",
        "",
    ]
    (output_dir / "h1_recalibration_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary-oc", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    primary_oc = pd.read_csv(args.primary_oc)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    table, decision = summarize(primary_oc, config)
    write_report(args.output_dir, table, decision)
    print(json.dumps(decision, ensure_ascii=False))


if __name__ == "__main__":
    main()
