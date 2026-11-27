"""Run exploratory M02 independent-trajectory and observation robustness.

Reuse the standardized plant unchanged. Fit, select and evaluate using either
three temporal blocks or three independent trajectories with matched scoring
sample sizes. Compare validation RMSE with Gaussian working AIC/BIC, bootstrap
paired replicate losses, and diagnose conditional-regression information.
Run with --config --output --source-commit and optional --existing-ledger.
This does not implement a full latent-state likelihood or human measurement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np

from controller_identifiability_split import split_indices
from controller_identifiability_suite import (
    CANDIDATES,
    csv_write,
    generate,
    matrices,
    observe,
    validate_spec,
    wilson,
)

CRITERIA = ("validation_rmse", "aic", "bic")
MODES = ("temporal", "independent")


def validate_robustness(spec: dict) -> None:
    """Validate all extra observation and bootstrap settings before execution.
    """
    validate_spec(spec)
    if not 2 <= spec["replications"] < 10_000:
        raise ValueError("replicate count must preserve distinct role seeds")
    if spec["action_noise_sd"] <= 0:
        raise ValueError("positive working noise SD required for information")
    if not isinstance(spec["bootstrap_resamples"], int):
        raise ValueError("bootstrap count must be an integer")
    if spec["bootstrap_resamples"] < 100:
        raise ValueError("at least 100 bootstrap draws required")
    eps = np.asarray(spec["epsilon_grid"], dtype=float)
    if not len(eps) or not np.all(np.isfinite(eps)) or np.any(eps <= 0):
        raise ValueError("positive finite tolerance grid required")
    for condition in spec["conditions"]:
        distribution = condition.get("noise_distribution", "gaussian")
        if distribution not in ("gaussian", "student_t"):
            raise ValueError("unknown observation-noise distribution")
        if distribution == "student_t" and condition.get("noise_df", 0) <= 2:
            raise ValueError("t-noise requires finite variance: df > 2")
        levels = condition.get("quantization_levels")
        if levels is not None:
            if not isinstance(levels, int) or levels < 2:
                raise ValueError("quantization levels must be integer >= 2")
            bound = condition.get("quantization_bound", 0)
            if not np.isfinite(bound) or bound <= 0:
                raise ValueError("positive finite quantization bound required")


def quantize(values: np.ndarray, levels: int, bound: float) -> np.ndarray:
    """Map to equally spaced bounded numeric categories in original units."""
    step = 2 * bound / (levels - 1)
    return (
        np.rint((np.clip(values, -bound, bound) + bound) / step) * step - bound
    )


def observe_extended(data: dict, condition: dict, seed: int) -> tuple:
    """Apply optional irregular sampling, variance-matched t-noise or bins.

    The unchanged default delegates to the archived observation function.
    Irregular retained indices are Bernoulli samples with mean stride; time
    zero is retained. Quantization affects both discrepancy and action.
    """
    custom = condition.get("irregular") or (
        condition.get("noise_distribution") == "student_t"
    )
    if not custom:
        error, action, dt = observe(data, condition, seed)
    else:
        n = len(data["error"])
        if condition.get("irregular"):
            draws = np.random.default_rng(seed + 5_000_000).random(n)
            indices = np.flatnonzero(draws < 1 / condition["stride"])
        else:
            indices = np.arange(0, n, condition["stride"])
        missing = np.random.default_rng(seed + 3_000_000).random(n)
        indices = np.unique(
            np.r_[0, indices[missing[indices] >= condition["missingness"]]]
        )
        rng = np.random.default_rng(seed + 4_000_000)
        if condition.get("noise_distribution") == "student_t":
            df = condition["noise_df"]
            noise = rng.standard_t(df, n) * np.sqrt((df - 2) / df)
        else:
            noise = rng.standard_normal(n)
        error = data["error"][indices] + condition["noise_sd"] * noise[indices]
        action = data["action"][indices]
        dt = np.r_[1.0, np.diff(indices).astype(float)]
    if "quantization_levels" in condition:
        args = (
            condition["quantization_levels"],
            condition["quantization_bound"],
        )
        error, action = quantize(error, *args), quantize(action, *args)
    return error, action, dt


def information_criteria(rss: float, n: int, columns: int) -> tuple:
    """Return working Gaussian AIC/BIC, counting coefficients and variance.

    Drop the common Gaussian likelihood constant. Nonpositive RSS has no
    finite variance MLE; return unavailable rather than imposing a floor.
    These scores do not become a correct latent likelihood under clipping,
    noisy covariates, coarse categories or residual dependence.
    """
    if not np.isfinite(rss) or rss <= 0 or n <= columns:
        return None, None
    deviance = n * np.log(rss / n)
    parameters = columns + 1
    return float(deviance + 2 * parameters), float(
        deviance + parameters * np.log(n)
    )


def bootstrap_interval(
    values: np.ndarray, draws: int, seed: int, coverage: float
) -> tuple:
    """Resample independent replicate-level paired differences as units.

    Return percentile intervals for the mean, retaining both models inside
    each difference. No time-point resampling or finite-sample coverage claim.
    """
    values = np.asarray(values, dtype=float)
    if len(values) < 2:
        return None, None
    if not np.all(np.isfinite(values)):
        raise ValueError("bootstrap differences must be finite")
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(values), (draws, len(values)))
    means = values[indices].mean(axis=1)
    alpha = (1 - coverage) / 2
    return tuple(float(x) for x in np.quantile(means, [alpha, 1 - alpha]))


def interval_label(
    low: float | None, high: float | None, epsilon: float
) -> str:
    """Classify only interval containment or beyond-band separation."""
    if low is None or high is None:
        return "insufficient_pairs"
    if low > -epsilon and high < epsilon:
        return "development_equivalent"
    if high < -epsilon:
        return "generator_predictively_better"
    if low > epsilon:
        return "competitor_predictively_better"
    return "inconclusive"


def conditional_information(
    X: np.ndarray, y: np.ndarray, sigma: float
) -> tuple[dict, list[dict]]:
    """Diagnose a fixed-design Gaussian regression, with intercept nuisance.

    Report the conditional slope information after projecting out intercept,
    normalized-feature conditioning and illustrative profiled RSS curves.
    Profile nuisance coefficients by constrained least squares with known
    working sigma. These are not latent closed-loop parameter likelihoods.
    """
    centered = X[:, 1:] - X[:, 1:].mean(axis=0)
    information = centered.T @ centered / sigma**2
    eigenvalues = np.linalg.eigvalsh(information)
    norm = np.linalg.norm(centered, axis=0)
    full_rank = np.linalg.matrix_rank(X) == X.shape[1]
    out = {
        "rank": int(np.linalg.matrix_rank(X)),
        "columns": X.shape[1],
        "information_min": float(eigenvalues[0]),
        "information_max": float(eigenvalues[-1]),
        "normalized_condition": None,
    }
    if np.all(norm > 0):
        normalized = centered / norm
        if np.linalg.matrix_rank(normalized) == normalized.shape[1]:
            out["normalized_condition"] = float(np.linalg.cond(normalized))
    if not full_rank:
        return out, []
    coefficients = np.linalg.lstsq(X, y, rcond=None)[0]
    covariance = sigma**2 * np.linalg.inv(X.T @ X)
    rss_min = float(np.sum((y - X @ coefficients) ** 2))
    profiles = []
    for index, parameter in enumerate(("kp", "ki", "kd"), start=1):
        scale = float(np.sqrt(covariance[index, index]))
        nuisance = np.delete(X, index, axis=1)
        for offset in np.linspace(-4, 4, 41):
            fixed = coefficients[index] + offset * scale
            adjusted = y - X[:, index] * fixed
            fitted = (
                nuisance @ np.linalg.lstsq(nuisance, adjusted, rcond=None)[0]
            )
            rss = float(np.sum((adjusted - fitted) ** 2))
            profiles.append(
                {
                    "parameter": parameter,
                    "fixed_value": fixed,
                    "estimate": coefficients[index],
                    "working_se": scale,
                    "profile_deviance": max(0.0, (rss - rss_min) / sigma**2),
                }
            )
    return out, profiles


def select(
    fits: dict, criterion: str, exclude: str | None = None
) -> str | None:
    """Freeze eligible model choice without reading final losses."""
    names = [
        name
        for name in CANDIDATES
        if name != exclude
        and fits[name]["status"] == "ok"
        and fits[name].get(criterion) is not None
    ]
    return (
        min(names, key=lambda name: fits[name][criterion]) if names else None
    )


def evaluate(
    spec: dict, condition: dict, generator: str, replicate: int
) -> tuple[list[dict], dict | None, list[dict]]:
    """Generate one seed triad; freeze all choices before final evaluation."""
    seeds = [spec["seed"] + replicate + role * 10_000 for role in range(3)]
    observations = [
        observe_extended(
            generate(spec, condition, generator, seed), condition, seed
        )
        for seed in seeds
    ]
    try:
        bounds = [
            split_indices(len(a), *spec["split"]) for _, a, _ in observations
        ]
    except ValueError:
        return (
            [
                {
                    "condition": condition["id"],
                    "generator": generator,
                    "replicate": replicate,
                    "seeds": seeds,
                    "failure": "insufficient_observations",
                    "scores": [],
                }
            ],
            None,
            [],
        )
    designs = [
        matrices(e, a, dt, spec["integral_leak"], spec["nonlinear_width"])
        for e, a, dt in observations
    ]
    fits = {}
    fit_n = bounds[0][0]
    for name in CANDIDATES:
        X = np.column_stack([np.ones(fit_n), designs[0][name][:fit_n]])
        y = observations[0][1][:fit_n]
        try:
            coefficients, _, rank, _ = np.linalg.lstsq(X, y, rcond=None)
            rss = float(np.sum((y - X @ coefficients) ** 2))
            aic, bic = information_criteria(rss, fit_n, X.shape[1])
            fits[name] = {
                "status": "ok" if rank == X.shape[1] else "rank_deficient",
                "coefficients": coefficients,
                "aic": aic,
                "bic": bic,
            }
        except np.linalg.LinAlgError:
            fits[name] = {"status": "numerical_failure"}
    scores = []
    for mode in MODES:
        role = 0 if mode == "temporal" else 1
        start, end = bounds[role]
        for name in CANDIDATES:
            if fits[name]["status"] == "ok":
                X = np.column_stack(
                    [np.ones(end - start), designs[role][name][start:end]]
                )
                residual = observations[role][1][start:end] - (
                    X @ fits[name]["coefficients"]
                )
                fits[name]["validation_rmse"] = float(
                    np.sqrt(np.mean(residual**2))
                )
        for criterion in CRITERIA:
            chosen = select(fits, criterion)
            competitor = select(fits, criterion, exclude=generator)
            scores.append(
                {
                    "mode": mode,
                    "criterion": criterion,
                    "selected": chosen,
                    "competitor": competitor,
                }
            )
    # All choices above are frozen before any final action is scored.
    for score in scores:
        role = 0 if score["mode"] == "temporal" else 2
        start = bounds[role][1]
        losses = {}
        for name in CANDIDATES:
            if fits[name]["status"] == "ok":
                a = observations[role][1][start:]
                X = np.column_stack(
                    [np.ones(len(a)), designs[role][name][start:]]
                )
                losses[name] = float(
                    np.sqrt(np.mean((a - X @ fits[name]["coefficients"]) ** 2))
                )
        competitor = score["competitor"]
        score["paired_delta"] = (
            losses[generator] - losses[competitor]
            if generator in losses and competitor in losses
            else None
        )
        score["final_rmse_selected"] = losses.get(score["selected"])
        score["final_n"] = len(observations[role][1]) - start
    info, profiles = None, []
    if generator == "pid":
        X = np.column_stack([np.ones(fit_n), designs[0]["pid"][:fit_n]])
        info, profiles = conditional_information(
            X, observations[0][1][:fit_n], spec["action_noise_sd"]
        )
        info.update(condition=condition["id"], replicate=replicate)
        if replicate != 0:
            profiles = []
        for profile in profiles:
            profile.update(condition=condition["id"], replicate=replicate)
    row = {
        "condition": condition["id"],
        "generator": generator,
        "replicate": replicate,
        "seeds": seeds,
        "failure": None,
        "fit_n": fit_n,
        "observed_n": [len(a) for _, a, _ in observations],
        "candidate_status": {
            name: fit["status"] for name, fit in fits.items()
        },
        "fitted_models": {
            name: {
                key: (
                    value.tolist() if isinstance(value, np.ndarray) else value
                )
                for key, value in fit.items()
            }
            for name, fit in fits.items()
        },
        "scores": scores,
    }
    return [row], info, profiles


def summarize(rows: list[dict], spec: dict) -> list[dict]:
    """Keep failed triads in recovery denominators and bootstrap paired loss.
    """
    summaries = []
    for condition in spec["conditions"]:
        for generator in spec["generators"]:
            group = [
                row
                for row in rows
                if row["condition"] == condition["id"]
                and row["generator"] == generator
            ]
            for mode in MODES:
                for criterion in CRITERIA:
                    scores = [
                        score
                        for row in group
                        for score in row["scores"]
                        if score["mode"] == mode
                        and score["criterion"] == criterion
                    ]
                    count = sum(
                        score["selected"] == generator for score in scores
                    )
                    low, high = wilson(count, len(group), spec["coverage"])
                    delta = np.array(
                        [
                            score["paired_delta"]
                            for score in scores
                            if score["paired_delta"] is not None
                        ]
                    )
                    ci = bootstrap_interval(
                        delta,
                        spec["bootstrap_resamples"],
                        spec["bootstrap_seed"] + len(summaries),
                        spec["coverage"],
                    )
                    summaries.append(
                        {
                            "condition": condition["id"],
                            "generator": generator,
                            "mode": mode,
                            "criterion": criterion,
                            "attempted": len(group),
                            "evaluable": sum(
                                s["selected"] is not None for s in scores
                            ),
                            "correct": count,
                            "recovery_low": low,
                            "recovery_high": high,
                            "paired_n": len(delta),
                            "paired_delta_mean": (
                                float(delta.mean()) if len(delta) else None
                            ),
                            "bootstrap_low": ci[0],
                            "bootstrap_high": ci[1],
                            "equivalence_status": interval_label(
                                *ci, spec["epsilon"]
                            ),
                        }
                    )
    return summaries


def reanalyze_ledger(path: Path, spec: dict) -> list[dict]:
    """Sensitivity-only reanalysis of an already inspected factorial ledger."""
    groups = {}
    with path.open() as handle:
        for line in handle:
            row = json.loads(line)
            key = (row["condition"], row["generator"])
            groups.setdefault(key, [])
            if row["paired_delta"] is not None:
                groups[key].append(row["paired_delta"])
    output = []
    for index, ((condition, generator), values) in enumerate(
        sorted(groups.items())
    ):
        low, high = bootstrap_interval(
            np.array(values),
            spec["bootstrap_resamples"],
            spec["bootstrap_seed"] + 10_000 + index,
            spec["coverage"],
        )
        for epsilon in spec["epsilon_grid"]:
            output.append(
                {
                    "condition": condition,
                    "generator": generator,
                    "paired_n": len(values),
                    "epsilon": epsilon,
                    "epsilon_over_action_noise": epsilon
                    / spec["action_noise_sd"],
                    "bootstrap_low": low,
                    "bootstrap_high": high,
                    "equivalence_status": interval_label(low, high, epsilon),
                }
            )
    return output


def run(
    spec: dict,
    output: Path,
    source_commit: str,
    existing_ledger: Path | None = None,
) -> list[dict]:
    """Execute and archive development outputs with source/environment hashes.
    """
    validate_robustness(spec)
    output.mkdir(parents=True, exist_ok=True)
    rows, information, profiles = [], [], []
    for condition in spec["conditions"]:
        for generator in spec["generators"]:
            for replicate in range(spec["replications"]):
                records, info, profile = evaluate(
                    spec, condition, generator, replicate
                )
                rows.extend(records)
                if info is not None:
                    information.append(info)
                profiles.extend(profile)
        print(f"Completed {condition['id']}", flush=True)
    with (output / "triads.jsonl").open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, allow_nan=False) + "\n")
    summary = summarize(rows, spec)
    csv_write(output / "summary.csv", summary)
    csv_write(output / "conditional_information.csv", information)
    csv_write(output / "conditional_profiles.csv", profiles)
    if existing_ledger is not None:
        csv_write(
            output / "factorial_bootstrap_sensitivity.csv",
            reanalyze_ledger(existing_ledger, spec),
        )
    (output / "config.json").write_text(json.dumps(spec, indent=2) + "\n")
    sources = [
        Path(__file__),
        Path(__file__).with_name("controller_identifiability_suite.py"),
        Path(__file__).with_name("controller_identifiability_split.py"),
        Path(__file__).with_name("fit_controller.py"),
    ]

    def checksum(path: Path) -> str:
        """Return the exact archived byte hash."""
        return hashlib.sha256(path.read_bytes()).hexdigest()

    metadata = {
        "evidence_id": spec["evidence_id"],
        "evidence_status": "development_only",
        "source_commit": source_commit,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "attempted_triads": len(rows),
        "generated_trajectories": 3 * len(rows),
        "failed_triads": sum(row["failure"] is not None for row in rows),
        "source_hashes": {p.name: checksum(p) for p in sources},
        "existing_ledger_sha256": (
            checksum(existing_ledger) if existing_ledger is not None else None
        ),
        "outputs_sha256": {
            p.name: checksum(p)
            for p in sorted(output.iterdir())
            if p.is_file() and p.name != "metadata.json"
        },
        "limitations": [
            "pointwise exploratory percentile bootstrap",
            "working Gaussian AIC/BIC, not Bayesian evidence",
            "conditional information, not full latent FIM",
            "fixed gains, within-design fresh innovations",
            "quantization is not a validated Likert observation",
        ],
    }
    (output / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )
    return summary


def main() -> None:
    """Run the configured development design and optional ledger reanalysis."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--existing-ledger", type=Path)
    args = parser.parse_args()
    run(
        json.loads(args.config.read_text()),
        args.output,
        args.source_commit,
        args.existing_ledger,
    )


if __name__ == "__main__":
    main()
