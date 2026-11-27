"""Synthetic Monte Carlo for the preregistered conditional log-odds contrasts."""
import argparse
import csv
from itertools import product
from pathlib import Path
import platform

import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.special import expit, log_expit, logsumexp, roots_hermitenorm
from scipy.stats import norm

CELLS = np.array(list(product([-.5, .5], repeat=3)))
C, V, B = CELLS.T
DESIGN = np.column_stack((np.ones(8), C, V, B, C*V, C*B, V*B, C*V*B))
H1 = 2 * DESIGN[:, 4]
SCENARIOS = {
    "null": (0., .7, .0, .0),
    "small": (.25, .7, .10, .0),
    "moderate": (.40, .7, .10, .0),
    "large": (.60, .7, .10, .0),
    "heterogeneous": (.40, 1.1, .20, .45),
}
SIZES = (160, 320, 480, 640, 960, 1280)
SEED = 20261126


def fit_choice(successes, trials, nodes=25):
    """Maximum marginal likelihood with a normal participant intercept."""
    available = trials.sum(axis=1) > 0
    successes, trials = successes[available], trials[available]
    n = len(trials)
    if n == 0 or (trials.sum(axis=0) == 0).any():
        raise ValueError("Every cell needs observations")
    q, weights = roots_hermitenorm(nodes)
    log_weights = np.log(weights / np.sqrt(2*np.pi))
    failures = trials - successes
    def objective(params):
        shift = np.exp(params[-1]) * q
        eta = params[:8] + shift[:, None]
        prob = expit(eta)
        ll = successes @ log_expit(eta).T + failures @ log_expit(-eta).T + log_weights
        marginal = logsumexp(ll, axis=1, keepdims=True)
        posterior = np.exp(ll - marginal)
        residual = successes * (posterior @ (1-prob)) - failures * (posterior @ prob)
        latent_score = successes @ (1-prob).T - failures @ prob.T
        return -marginal.sum(), -np.r_[residual.sum(axis=0), np.sum(posterior * latent_score * shift)]

    start = np.zeros(9)
    start[-1] = -.4
    result = minimize(objective, start, jac=True, method="L-BFGS-B",
                      bounds=[(None, None)]*8 + [(-5., 1.5)],
                      options={"ftol": 1e-12, "gtol": 1e-5})
    if not result.success or not -4.999 < result.x[-1] < 1.499:
        raise ValueError("Fit failed or hit the variance bound")
    step = np.eye(9) * 1e-4
    hessian = np.column_stack([(objective(result.x + d)[1] - objective(result.x - d)[1])/2e-4 for d in step])
    hessian = (hessian + hessian.T)/2
    np.linalg.cholesky(hessian)
    return result.x[:8], np.linalg.inv(hessian)[:8, :8]


def generate(rng, n, scenario):
    interaction, sd, dropout, slope_sd = SCENARIOS[scenario]
    coefficients = [0., -.8, .2, .6, interaction, 0., 0., 0.]
    logits = DESIGN @ coefficients + rng.normal(0., sd, (n, 1))
    logits += rng.normal(0., slope_sd, (n, 1)) * C
    observed = rng.random(n) >= dropout
    trials = np.broadcast_to(3*observed[:, None], (n, 8))
    return rng.binomial(trials, expit(logits)), trials


def wilson(hits, total):
    z = norm.ppf(.975)
    p = hits/total
    center = (p + z*z/(2*total))/(1 + z*z/total)
    radius = z*np.sqrt(p*(1-p)/total + z*z/(4*total**2))/(1 + z*z/total)
    return max(0., center-radius), min(1., center+radius)


def evaluate(scenario, n, repetitions):
    # Independent, deterministic streams for all sample size/scenario combinations.
    rng = np.random.default_rng(np.random.SeedSequence([SEED, list(SCENARIOS).index(scenario), n]))
    hits = failures = covered = tested = 0
    for _ in range(repetitions):
        successes, trials = generate(rng, n, scenario)
        try:
            estimate, covariance = fit_choice(successes, trials)
        except (ValueError, np.linalg.LinAlgError):
            failures += 1
            continue
        effect = H1 @ estimate
        error = np.sqrt(H1 @ covariance @ H1)
        hits += effect/error > norm.ppf(.975)
        covered += abs(effect-SCENARIOS[scenario][0]) <= norm.ppf(.975)*error
        tested += 1
    low, high = wilson(hits, repetitions)
    return [scenario, n, repetitions, hits, failures, hits/repetitions, low, high,
            covered/tested if tested else "", SEED, platform.python_version(), np.__version__, scipy.__version__]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repetitions", type=int, default=300)
    parser.add_argument("--scenario", choices=SCENARIOS, action="append")
    parser.add_argument("--size", type=int, action="append")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.repetitions < 1 or any(n < 1 for n in args.size or []):
        parser.error("Sample size and repetitions must be positive")
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["synthetic_scenario", "randomized_n", "replicates", "positive_rejections",
                         "fit_failures", "power", "mc_low", "mc_high", "coverage_among_fits",
                         "seed", "python", "numpy", "scipy"])
        for scenario, n in product(args.scenario or SCENARIOS, args.size or SIZES):
            writer.writerow(evaluate(scenario, n, args.repetitions))
            stream.flush()


if __name__ == "__main__":
    main()
