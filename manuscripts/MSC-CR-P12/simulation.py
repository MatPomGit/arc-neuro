"""Synthetic planning, using a participant-level SDT approximation to ITT."""
import argparse
import csv
import sys

import numpy as np
from scipy.special import ndtr, ndtri
from scipy.stats import ttest_ind


def sdt(rejections, total):
    """Last axis is ordered as correct advice, incorrect advice."""
    z = ndtri((rejections + 0.5) / (total + 1))
    return z[..., 1] - z[..., 0], -z.mean(axis=-1)


def simulate(rng, n, effect, item_sd, loss, mnar=False, reps=1000):
    """Simulate baseline/day 14, two far domains, parallel forms, 16 trials per domain."""
    shape = (reps, 2, n // 2, 2, 2, 1, 1)
    group = np.arange(2).reshape(1, 2, 1, 1, 1, 1, 1)
    wave = np.arange(2).reshape(1, 1, 1, 2, 1, 1, 1)
    sign = np.array([-0.5, 0.5]).reshape(1, 1, 1, 1, 1, 2, 1)
    criterion = rng.normal(0, 0.55, (reps, 2, n // 2, 1, 1, 1, 1))
    sensitivity = rng.normal(0, 0.45, criterion.shape)
    knowledge = rng.normal(0, 0.70, (reps, 2, n // 2, 1, 2, 1, 1))
    session = rng.normal(0, 0.22, shape)
    items = rng.normal(0, item_sd, (reps, 1, 1, 2, 2, 2, 8))
    domain = np.array([0.10, -0.10]).reshape(1, 1, 1, 1, 2, 1, 1)
    eta = criterion + session + items + group * wave * 0.10
    eta = eta + sign * (0.95 + sensitivity + 0.20 * knowledge + domain + group * wave * effect)
    rejections = (rng.random(np.broadcast_shapes(eta.shape, shape)) < ndtr(eta)).sum(axis=-1)
    d, _ = sdt(rejections, 8)
    gains = (d[..., 1, :] - d[..., 0, :]).mean(axis=-1)
    # MCAR or stress test: post-baseline dropout depends on latent proficiency.
    propensity = np.full(gains.shape, loss)
    if mnar:
        propensity += 0.18 * np.tanh(-sensitivity.reshape(gains.shape) / 0.45)
        propensity = np.clip(propensity, 0.01, 0.95)
    gains[rng.random(gains.shape) < propensity] = np.nan
    result = ttest_ind(gains[:, 1], gains[:, 0], axis=1, equal_var=False, nan_policy="omit")
    decisions = (result.pvalue < 0.05) & (result.statistic > 0)
    estimate = decisions.mean()
    return (
        estimate,
        np.sqrt(estimate * (1 - estimate) / reps),
        np.isfinite(gains).sum(axis=(1, 2)).mean(),
        np.isfinite(result.pvalue).sum(),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=27112026)
    parser.add_argument("--reps", type=int, default=1200)
    args = parser.parse_args()
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["seed", "reps", "n", "delta_latent", "item_sd", "loss", "dropout",
                     "positive_decision_rate", "mcse", "retained_mean", "valid_reps"])
    scenarios = [
        (n, effect, difficulty, loss, mnar)
        for n in (160, 320, 480, 640)
        for effect in (0, 0.20, 0.35, 0.50)
        for difficulty, loss, mnar in ((0.30, 0.15, False), (0.65, 0.30, False), (0.65, 0.30, True))
    ]
    for scenario, seed in zip(scenarios, np.random.SeedSequence(args.seed).spawn(len(scenarios))):
        n, effect, difficulty, loss, mnar = scenario
        chunks = [min(100, args.reps - offset) for offset in range(0, args.reps, 100)]
        rng = np.random.default_rng(seed)
        values = [simulate(rng, n, effect, difficulty, loss, mnar, reps) for reps in chunks]
        rate = np.average([row[0] for row in values], weights=chunks)
        retained = np.average([row[2] for row in values], weights=chunks)
        valid = sum(row[3] for row in values)
        writer.writerow([args.seed, args.reps, n, effect, difficulty, loss, "MNAR" if mnar else "MCAR",
                         f"{rate:.4f}", f"{np.sqrt(rate * (1-rate) / args.reps):.4f}",
                         f"{retained:.2f}", valid])


if __name__ == "__main__":
    main()
