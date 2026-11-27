"""Generate M02 robustness tables and a compact report from archived CSVs.

Run with --results and --manuscript. No simulation or model choice is performed.
The report preserves exploratory status and references immutable source outputs.
"""

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path


def read_rows(path: Path) -> list[dict]:
    """Read machine-readable rows without changing any scientific setting."""
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def report(results: Path, manuscript: Path) -> None:
    """Generate two tables, outcome summaries and report-input checksums."""
    rows = read_rows(results / "summary.csv")
    sensitivity = read_rows(results / "factorial_bootstrap_sensitivity.csv")
    lookup = {
        (r["condition"], r["generator"], r["mode"], r["criterion"]): r
        for r in rows
    }
    tables = manuscript / "tables"
    tables.mkdir(parents=True, exist_ok=True)
    selection = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Exploratory nominal recovery under selection rules}",
        r"\label{tab:m02-robustness-selection}",
        r"\begin{tabular}{llrrrr}",
        r"\toprule",
        r"Arm & Generator & Temporal & Independent & AIC & BIC \\",
        r"\midrule",
    ]
    for condition, arm in (
        ("reference", "Reference"),
        ("analyst_noise", "Noise"),
    ):
        for generator in ("p", "pid"):
            values = [
                lookup[condition, generator, mode, criterion]
                for mode, criterion in (
                    ("temporal", "validation_rmse"),
                    ("independent", "validation_rmse"),
                    ("independent", "aic"),
                    ("independent", "bic"),
                )
            ]
            counts = [f"{r['correct']}/{r['attempted']}" for r in values]
            selection.append(
                f"{arm} & {generator.upper()} & " + " & ".join(counts) + r" \\"
            )
    selection += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    selection_path = tables / "m02_robustness_selection.tex"
    selection_path.write_text("\n".join(selection) + "\n")
    threshold = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Factorial sensitivity: pointwise bootstrap labels}",
        r"\label{tab:m02-robustness-epsilon}",
        r"\begin{tabular}{rrrrr}",
        r"\toprule",
        r"$\epsilon$ & Equivalent & Inconclusive & Generator & Competitor \\",
        r"\midrule",
    ]
    for epsilon in ("0.001", "0.0025", "0.005", "0.01"):
        counts = Counter(
            r["equivalence_status"]
            for r in sensitivity
            if r["epsilon"] == epsilon
        )
        values = [
            counts[name]
            for name in (
                "development_equivalent",
                "inconclusive",
                "generator_predictively_better",
                "competitor_predictively_better",
            )
        ]
        threshold.append(
            epsilon + " & " + " & ".join(map(str, values)) + r" \\"
        )
    threshold += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    threshold_path = tables / "m02_robustness_epsilon.tex"
    threshold_path.write_text("\n".join(threshold) + "\n")
    statuses = Counter()
    unavailable_variance = 0
    unavailable_choices = 0
    with (results / "triads.jsonl").open() as handle:
        for line in handle:
            row = json.loads(line)
            statuses.update(row.get("candidate_status", {}).values())
            unavailable_variance += sum(
                fit["status"] == "ok" and fit.get("aic") is None
                for fit in row.get("fitted_models", {}).values()
            )
            unavailable_choices += sum(
                score["selected"] is None for score in row["scores"]
            )
    diagnostics = {
        "candidate_fit_status": dict(statuses),
        "full_rank_fits_without_finite_variance_MLE": unavailable_variance,
        "mode_criterion_records_without_selection": unavailable_choices,
        "units": "Fits and mode/criterion records are not extra failed triads.",
    }
    diagnostic_path = results / "execution_diagnostics.json"
    diagnostic_path.write_text(json.dumps(diagnostics, indent=2) + "\n")
    metadata = json.loads((results / "metadata.json").read_text())
    notes = [
        "# M02 exploratory robustness",
        "",
        f"Evidence: {metadata['evidence_id']}; development only.",
        f"Source commit: {metadata['source_commit']}.",
        "",
        f"{metadata['attempted_triads']} attempted triads; "
        f"{metadata['generated_trajectories']} generated trajectories; "
        f"{metadata['failed_triads']} common split-feasibility failures.",
        "",
        f"Candidate rank failures: {statuses['rank_deficient']}; "
        f"full-rank fits without finite variance MLE: {unavailable_variance}; "
        f"mode/criterion records without choice: {unavailable_choices}.",
        "## Independent validation-RMSE PID recovery",
        "",
    ]
    for condition in json.loads((results / "config.json").read_text())[
        "conditions"
    ]:
        r = lookup[condition["id"], "pid", "independent", "validation_rmse"]
        notes.append(
            f"- {condition['id']}: {r['correct']}/{r['attempted']}; "
            f"evaluable {r['evaluable']}; paired mean "
            f"{float(r['paired_delta_mean']):.8f}."
        )
    notes += [
        "",
        "AIC/BIC use fitting data, so their recovery counts are "
        "identical across validation modes by construction. Comparisons "
        "of validation-RMSE modes share fitted coefficients and seed "
        "triads. No multiplicity-controlled or human inference.",
        "",
        "Conditional information/profiles hold observed predictors "
        "fixed; they are not a full latent-state FIM or likelihood. "
        "Percentile bootstrap coverage is not established here.",
        "",
    ]
    (results / "development_report.md").write_text("\n".join(notes))
    paths = [
        diagnostic_path,
        results / "summary.csv",
        results / "factorial_bootstrap_sensitivity.csv",
        selection_path,
        threshold_path,
    ]
    hashes = {
        str(p.name): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths
    }
    record = {
        "source_hash": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "artifacts_sha256": hashes,
    }
    (results / "report_metadata.json").write_text(
        json.dumps(record, indent=2) + "\n"
    )


def main() -> None:
    """Generate source-derived manuscript tables and development notes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--manuscript", type=Path, required=True)
    args = parser.parse_args()
    report(args.results, args.manuscript)


if __name__ == "__main__":
    main()
