"""Planning-only H1 power via Fisher approximation and Monte Carlo.

Independent attrition and Gaussian Fisher-z sampling are assumptions,
not empirical estimates or a full trial-level simulation.
"""
from math import atanh, ceil, sqrt, isfinite
from statistics import NormalDist
from random import Random
import argparse
import json

NORM = NormalDist()


def complete_n(r, k=8, alpha=.05, power=.8):
    if not (0 < abs(r) < 1 and type(k) is int and k >= 0 and 0 < alpha < 1 and .5 < power < 1):
        raise ValueError("invalid design parameters")
    return ceil(k+3+((NORM.inv_cdf(1-alpha/2)+NORM.inv_cdf(power))/atanh(abs(r)))**2)


def approximate_power(n, r, k=8, alpha=.05):
    if not (type(n) is int and type(k) is int and k >= 0 and n > k+3 and abs(r) < 1 and 0 < alpha < 1):
        raise ValueError("invalid design parameters")
    mu = atanh(r)*sqrt(n-k-3)
    z = NORM.inv_cdf(1-alpha/2)
    return NORM.cdf(-z-mu) + 1-NORM.cdf(z-mu)


def simulate(recruited, r, k=8, attrition=.2, alpha=.05, repetitions=5000, seed=42):
    if not (type(recruited) is int and type(k) is int and k >= 0 and recruited > k+3 and
            abs(r) < 1 and 0 <= attrition < 1 and 0 < alpha < 1 and type(repetitions) is int and repetitions > 0):
        raise ValueError("invalid design parameters")
    rng = Random(seed)
    threshold = NORM.inv_cdf(1-alpha/2)
    success = total = insufficient = 0
    for _ in range(repetitions):
        n = sum(rng.random() >= attrition for _ in range(recruited))
        total += n
        if n <= k+3:
            insufficient += 1
            continue
        z = rng.gauss(atanh(r)*sqrt(n-k-3), 1)
        success += abs(z) > threshold
    p = success/repetitions
    return dict(model="Fisher-z; independent attrition", recruited=recruited, r=r, k=k,
                alpha=alpha, attrition=attrition, repetitions=repetitions, seed=seed,
                mean_complete=total/repetitions, power=p, mc_se=sqrt(p*(1-p)/repetitions),
                insufficient=insufficient)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recruited", type=int, default=444)
    parser.add_argument("--r", type=float, default=.15)
    parser.add_argument("--k", type=int, default=8)
    parser.add_argument("--attrition", type=float, default=.2)
    parser.add_argument("--repetitions", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    a = parser.parse_args()
    print(json.dumps(simulate(a.recruited, a.r, a.k, a.attrition, repetitions=a.repetitions, seed=a.seed), indent=2))
