"""Generate M02 development tables and figures from archived summary records.

Use --input for the suite output directory and --manuscript for the M02 source
directory. This reports development evidence only; it changes no thresholds.
Requires NumPy and Matplotlib; public artifacts contain synthetic aggregates.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def build_report(input_dir: Path, manuscript: Path) -> None:
    """Create aggregate figures/tables and record their derivation hashes."""
    with (input_dir / "summary.csv").open() as handle:
        rows = list(csv.DictReader(handle))
    config = json.loads((input_dir / "config.json").read_text())
    metadata = json.loads((input_dir / "metadata.json").read_text())
    lookup = {(r["condition"], r["generator"]): r for r in rows}
    generators = config["generators"]
    conditions = config.get(
        "display_conditions", [c["id"] for c in config["conditions"]]
    )
    figures = manuscript / "figures"
    tables = manuscript / "tables"
    figures.mkdir(exist_ok=True)
    tables.mkdir(exist_ok=True)
    values = np.array([
        [float(lookup[(c, g)]["recovery_attempted"]) for c in conditions]
        for g in generators
    ])
    fig, ax = plt.subplots(figsize=(10, 5.5), constrained_layout=True)
    mesh = ax.imshow(values, vmin=0, vmax=1, cmap="viridis", aspect="auto")
    ax.set_xticks(range(len(conditions)), [c.replace("_", " ") for c in conditions],
                  rotation=40, ha="right")
    ax.set_yticks(range(len(generators)), generators)
    ax.set_xlabel("Development observation condition")
    ax.set_ylabel("Nominal synthetic generator")
    for i, g in enumerate(generators):
        for j, c in enumerate(conditions):
            record = lookup[(c, g)]
            text = f'{record["nominal_correct"]}/{record["attempted"]}'
            ax.text(j, i, text, ha="center", va="center", fontsize=8,
                    color="white" if values[i, j] < 0.55 else "black")
    fig.colorbar(mesh, ax=ax, label="Validation-selected family recovery")
    fig.savefig(figures / "m02_development_recovery.pdf")
    fig.savefig(input_dir / "recovery_preview.png", dpi=140)
    plt.close(fig)

    chosen = ["reference", "analyst_noise", "combined"]
    fig, ax = plt.subplots(figsize=(8, 6), constrained_layout=True)
    colors = ["#325f8a", "#b46322", "#637d3c"]
    for arm, color, offset in zip(chosen, colors, (-0.18, 0, 0.18)):
        records = [lookup[(arm, g)] for g in generators]
        means = np.array([float(r["paired_delta_mean"]) for r in records])
        low = np.array([float(r["paired_delta_low"]) for r in records])
        high = np.array([float(r["paired_delta_high"]) for r in records])
        ax.errorbar(means, np.arange(len(generators)) + offset,
                    xerr=np.stack([means - low, high - means]),
                    fmt="o", markersize=4, color=color,
                    label=arm.replace("_", " "), capsize=2)
    epsilon = config["epsilon"]
    ax.axvspan(-epsilon, epsilon, color="#dddddd", alpha=0.55)
    ax.axvline(0, color="#555555", linewidth=0.8)
    ax.set_xscale("symlog", linthresh=epsilon)
    ax.set_xticks([-1, -0.1, -0.01, 0, 0.01, 0.1, 1])
    ax.set_xticklabels(["-1", "-0.1", "-0.01", "0", "0.01", "0.1", "1"])
    ax.set_yticks(range(len(generators)), generators)
    ax.set_xlabel("Final-test RMSE: nominal family minus validation competitor")
    ax.set_ylabel("Synthetic generator")
    ax.legend(loc="best", fontsize=8)
    fig.savefig(figures / "m02_development_paired_loss.pdf")
    fig.savefig(input_dir / "paired_loss_preview.png", dpi=140)
    plt.close(fig)

    n = config["replications"]
    lines = [r"\begin{table}[htbp]", r"\centering",
             r"\caption{Standardized development benchmark: nominal recovery}",
             r"\label{tab:m02-standardized-development}",
             r"\begin{tabular}{lrrr}", r"\toprule",
             r"Generator & Reference & Analyst noise & Combined \\",
             r"\midrule"]
    for g in generators:
        counts = [lookup[(c, g)]["nominal_correct"] for c in chosen]
        lines.append(g + " & " + " & ".join(f"{x}/{n}" for x in counts) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}"])
    table = tables / "m02_standardized_development.tex"
    table.write_text("\n".join(lines) + "\n")

    def value(condition: str, generator: str, field: str) -> str:
        return lookup[(condition, generator)][field]

    failures = sum(int(r["selection_failures"]) for r in rows)
    candidate_failures = sum(int(r["candidate_failures"]) for r in rows)
    n_conditions = len(config["conditions"])
    report = ["# M02 standardized development benchmark", "",
              "Evidence: `" + config["evidence_id"] + "`. Development only.",
              "Source commit: `" + metadata["source_commit"] + "`.", "",
              f"Executed {metadata['attempted_trajectories']} trajectories: "
              f"{len(generators)} generators × {n_conditions} conditions × {n} seeds.",
              f"Selection failures: {failures}; "
              f"candidate fit failures: {candidate_failures}.",
              "Candidate failures include rank deficiency "
              "and do not imply failed trajectories.",
              "", "| Generator | Reference | Analyst noise | Combined |",
              "|---|---:|---:|---:|"]
    for g in generators:
        counts = [value(c, g, "nominal_correct") for c in chosen]
        report.append(f"| {g} | " + " | ".join(f"{x}/{n}" for x in counts) + " |")
    if ("pid_reduced", "pid") in lookup:
        nominal = value("pid_reduced", "pid", "nominal_correct")
        effective = value("pid_reduced", "pid", "effective_correct")
        report.extend([
            "", "The PID reduction arm sets ki=kd=0. For nominal PID, "
            f"nominal recovery is {nominal}/{n}; "
            f"effective P recovery is {effective}/{n}.",
        ])
    design = ("full two-level factorial" if config.get("design_type")
              else "targeted rather than full factorial")
    report.extend([
        "", "The interval/equivalence summaries are pointwise "
        "developmental descriptions. "
        f"The computational epsilon was {epsilon}, fixed before this run; "
        "it is not calibrated to a human instrument and is not the "
        "confirmatory tolerance. Correct family recovery need not imply "
        "a practically material prediction advantage.",
        "", f"Design: {design}. Limitations: fixed gains, "
        "a standardized feedback plant rather than the full ARC agent, "
        "known nonlinear width and switching threshold, conditional action "
        "prediction, MCAR gaps, and no parameter interval coverage. "
        "Sampling reconstructs histories from retained observations; "
        "AR/ARX lags become previous observed rather than previous latent "
        "actions after gaps.",
        "", "The complete trajectory ledger is regenerated by the documented "
        "command instead of committed to Git. Its exact byte checksum and "
        "source/config hashes remain in metadata.json. Public results retain "
        "summary, confusion and parameter CSV files. Same-byte reproduction "
        "requires the recorded environment.",
    ])
    (input_dir / "development_report.md").write_text("\n".join(report) + "\n")
    paths = [table, figures / "m02_development_recovery.pdf",
             figures / "m02_development_paired_loss.pdf"]
    report_metadata = {
        "report_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "summary_sha256": hashlib.sha256(
            (input_dir / "summary.csv").read_bytes()
        ).hexdigest(),
        "matplotlib": matplotlib.__version__,
        "generated_sha256": {str(p.relative_to(manuscript)):
                             hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    }
    (input_dir / "report_metadata.json").write_text(
        json.dumps(report_metadata, indent=2) + "\n"
    )


def main() -> None:
    """Generate the M02 aggregate report without rerunning simulations."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--manuscript", type=Path, required=True)
    args = parser.parse_args()
    build_report(args.input, args.manuscript)


if __name__ == "__main__":
    main()
