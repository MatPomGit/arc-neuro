"""Planning sensitivity of rare-category counts under a hypothetical ordinal bank."""
import csv
from statistics import NormalDist
import sys

import numpy as np


def simulate(n, probabilities, seed, reps=2000, loading=0.65):
    rng = np.random.default_rng(seed)
    thresholds = [NormalDist().inv_cdf(p) for p in np.cumsum(probabilities)[:-1]]
    failures = 0
    for start in range(0, reps, 50):
        count = min(reps - start, 50)
        factors = rng.normal(size=(count, n, 3))
        residuals = rng.normal(size=(count, n, 12))
        latent = loading * np.repeat(factors, 4, axis=-1) + np.sqrt(1 - loading**2) * residuals
        categories = np.searchsorted(thresholds, latent)
        failures += np.any(
            np.stack([(categories == level).sum(axis=1) < 5 for level in range(5)]),
            axis=(0, 2),
        ).sum()
    return int(failures)


def main():
    distributions = {
        "balanced": (0.10, 0.20, 0.40, 0.20, 0.10),
        "skewed": (0.02, 0.06, 0.17, 0.30, 0.45),
        "strongly_skewed": (0.01, 0.04, 0.10, 0.25, 0.60),
    }
    seed = 27112026
    reps = 2000
    cases = [(n, name, p) for n in (150, 250, 400, 600) for name, p in distributions.items()]
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["seed", "case", "n", "distribution", "reps", "sparse_reps", "risk", "mcse"])
    for index, ((n, name, p), child) in enumerate(zip(cases, np.random.SeedSequence(seed).spawn(len(cases)))):
        failures = simulate(n, p, child, reps=reps)
        risk = failures / reps
        writer.writerow([seed, index, n, name, reps, failures, f"{risk:.4f}",
                         f"{np.sqrt(risk * (1-risk) / reps):.4f}"])


if __name__ == "__main__":
    main()
