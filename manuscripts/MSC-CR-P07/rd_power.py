"""Monte Carlo evaluation of the primary trial-weighted RD, conditional on task bank."""
import argparse
import json
import numpy as np
from scipy.special import expit, logit
from scipy.optimize import brentq
from scipy.special import roots_hermitenorm
from scipy.stats import binomtest
from marginal_rd import estimate_rd


def scenario(n, tasks, rd, sd_person, sd_task, initial_correct, missing, replicates, seed):
    if n < 3 or tasks < 4 or tasks % 4 or replicates < 1:
        raise ValueError("Invalid sample design")
    if not (0 < initial_correct <= 1 and 0 <= missing < 1 and sd_person >= 0 and sd_task >= 0):
        raise ValueError("Invalid nuisance parameters")
    bank_seed, simulation_seed = np.random.SeedSequence(seed).spawn(2)
    bank = np.random.default_rng(bank_seed).normal(0, sd_task, tasks)
    nodes, weights = roots_hermitenorm(40)
    eta = logit(.2) + bank[:, None] + sd_person * nodes
    def risk(b):
        return float(np.mean(expit(eta+b) @ weights / np.sqrt(2*np.pi)))
    p0 = risk(0)
    if not -p0 < rd < 1-p0:
        raise ValueError("Infeasible marginal effect")
    beta = brentq(lambda b: risk(b)-p0-rd, -40, 40)
    person = np.repeat(np.arange(n), tasks)
    task = np.tile(np.arange(tasks), n)
    estimates, covered, rejected, positive, failed = [], 0, 0, 0, 0
    for child in simulation_seed.spawn(replicates):
        rng = np.random.default_rng(child)
        # Independent 2x2 assignments AFTER each initial response.
        tone = rng.integers(0, 2, n*tasks)
        wrong = rng.integers(0, 2, n*tasks)
        eligible = (rng.random(n*tasks) < initial_correct) & (wrong == 1)
        keep = eligible & (rng.random(n*tasks) >= missing)
        u = rng.normal(0, sd_person, n)
        y = rng.binomial(1, expit(logit(.2)+bank[task]+u[person]+beta*tone))
        fit = estimate_rd(person[keep], tone[keep], y[keep])
        if fit is None:
            failed += 1
            continue
        estimates.append(fit["rd"])
        covered += fit["lower"] <= rd <= fit["upper"]
        rejected += fit["lower"] > 0 or fit["upper"] < 0
        positive += fit["lower"] > 0
    ci = binomtest(rejected, replicates).proportion_ci()
    power_ci = binomtest(positive, replicates).proportion_ci()
    valid = len(estimates)
    cov_ci = binomtest(covered, valid).proportion_ci() if valid else None
    return dict(n=n, tasks=tasks, rd=rd, baseline_risk=p0, beta=beta,
                sd_person=sd_person, sd_task=sd_task, initial_correct=initial_correct,
                missing=missing, replicates=replicates, seed=seed, failed=failed,
                rejected=rejected, rate=rejected/replicates, lower95=ci.low, upper95=ci.high,
                positive=positive, directional_power=positive/replicates,
                power_lower95=power_ci.low, power_upper95=power_ci.high,
                covered=covered, coverage=covered/valid if valid else None,
                coverage_lower95=cov_ci.low if cov_ci else None,
                coverage_upper95=cov_ci.high if cov_ci else None,
                bias=float(np.mean(estimates)-rd) if valid else None)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--replicates", type=int, default=1000)
    p.add_argument("--seed", type=int, default=20261126)
    p.add_argument("--smoke", action="store_true")
    args = p.parse_args()
    from itertools import product
    grid = [(80, 0, .5, .3, .75, 0)] if args.smoke else product(
        (80, 160, 240), (0, .03, .05, .08), (.5, 1), (.3, .7), (.55, .75), (0, .1))
    print(json.dumps([scenario(n, 24, rd, sp, st, q, m, args.replicates, args.seed)
                      for n, rd, sp, st, q, m in grid], indent=2, allow_nan=False))
