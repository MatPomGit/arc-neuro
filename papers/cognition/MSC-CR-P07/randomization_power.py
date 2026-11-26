"""Conditional randomization test for the sharp null of no tone effect.
Requires exchangeable randomized tone conditional on participant-specific counts
among eligible wrong-advice trials, and eligibility/missingness unaffected by tone. Not a weak-null RD CI.
"""
import argparse
import json
import numpy as np
from scipy.special import expit, logit
from scipy.stats import hypergeom, binomtest


def conditional_test(person, tone, y):
    person, tone, y = map(np.asarray, (person, tone, y))
    if any(a.ndim != 1 for a in (person, tone, y)) or not (len(person) == len(tone) == len(y)):
        raise ValueError('Expected aligned vectors')
    if not np.isin(tone, [0, 1]).all() or not np.isin(y, [0, 1]).all():
        raise ValueError('Expected binary tone and outcome')
    if not len(y) or len(np.unique(tone)) < 2:
        return None
    pmf = np.array([1.0]); offset = 0; expected = 0.; observed = 0; informative = 0
    for p in np.unique(person):
        idx = person == p
        m, k, s = int(idx.sum()), int(tone[idx].sum()), int(y[idx].sum())
        lo, hi = max(0, k+s-m), min(k,s)
        pmf = np.convolve(pmf, hypergeom.pmf(np.arange(lo, hi+1), m, s, k))
        offset += lo; expected += k*s/m
        observed += int(np.dot(tone[idx], y[idx])); informative += int(hi > lo)
    if not informative:
        return None
    support = np.arange(len(pmf)) + offset
    extreme = np.abs(support-expected) >= abs(observed-expected)-1e-10
    return float(np.clip(pmf[extreme].sum()/pmf.sum(), 0, 1))


def simulate(rng, n, tasks, beta, sd_person=.5, sd_task=.3, initial_correct=.75, missing=0, balanced=False):
    person = np.repeat(np.arange(n), tasks)
    task = np.tile(np.arange(tasks), n)
    condition = (np.concatenate([rng.permutation(np.repeat(np.arange(4), tasks//4)) for _ in range(n)])
                 if balanced else rng.integers(0, 4, n*tasks))
    tone = condition % 2
    initial = rng.binomial(1, initial_correct, n*tasks)
    u = rng.normal(0,sd_person,n); v = rng.normal(0,sd_task,tasks)
    y = rng.binomial(1, expit(logit(.2)+beta*tone+u[person]+v[task]))
    keep = (condition//2 == 1) & (initial == 1) & (rng.random(n*tasks) >= missing)
    return person[keep], tone[keep], y[keep]


def scenario(n, tasks, beta, replicates, seed, sd_person=.5, sd_task=.3, initial_correct=.75, missing=0):
    if n < 2 or tasks < 4 or tasks % 4 or replicates < 1 or not (0 < initial_correct <= 1 and 0 <= missing < 1 and sd_person >= 0 and sd_task >= 0):
        raise ValueError('Invalid design')
    rng = np.random.default_rng(seed)
    values = [conditional_test(*simulate(rng,n,tasks,beta,sd_person,sd_task,initial_correct,missing)) for _ in range(replicates)]
    rejects = sum(p is not None and p <= .05 for p in values)
    failures = sum(p is None for p in values)
    ci = binomtest(rejects,replicates).proportion_ci()
    return dict(n=n,tasks=tasks,beta=beta,sd_person=sd_person,sd_task=sd_task,initial_correct=initial_correct,missing=missing,replicates=replicates,seed=seed,rejects=rejects,failures=failures,rate=rejects/replicates,lower95=ci.low,upper95=ci.high)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replicates',type=int,default=200)
    parser.add_argument('--seed',type=int,default=20261126)
    parser.add_argument('--grid',action='store_true')
    parser.add_argument('--output')
    args=parser.parse_args()
    ns = (80,120,160,200,240) if args.grid else (80,)
    ors = (1,1.2,1.4,1.6,1.8) if args.grid else (1,1.6)
    rows = [scenario(n,24,np.log(o),args.replicates,args.seed)
            for n in ns for o in ors]
    for row, o in zip(rows, (o for n in ns for o in ors)):
        row['odds_ratio'] = o
    result = json.dumps(rows,indent=2)
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(result+'\n',encoding='utf-8')
    else:
        print(result)
