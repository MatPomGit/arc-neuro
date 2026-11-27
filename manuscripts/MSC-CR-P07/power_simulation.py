"""Prospective Monte Carlo planning; no empirical data.

Crossed random-intercept logistic model, fitted with statsmodels mean-field variational Bayes.
Posterior normal screening is approximate; it is not a frequentist Wald test.
Null calibration is required before recruitment planning.
"""
import argparse
import itertools
import warnings

import numpy as np
import pandas as pd
from scipy.special import expit, logit
from scipy.stats import norm, binomtest
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM


def simulate_trials(rng, n, tasks, alpha, beta, sd_person, sd_task,
                    initial_correct, missing):
    if n < 2 or tasks < 4 or tasks % 4:
        raise ValueError("Require n >= 2 and tasks divisible by four")
    if not (0 < initial_correct <= 1 and 0 <= missing < 1
            and sd_person >= 0 and sd_task >= 0):
        raise ValueError("Invalid scenario")
    person = np.repeat(np.arange(n), tasks)
    task = np.tile(np.arange(tasks), n)
    condition = np.concatenate([
        rng.permutation(np.repeat(np.arange(4), tasks // 4))
        for _ in range(n)
    ])
    tone = condition % 2
    wrong = condition // 2
    initial = rng.binomial(1, initial_correct, n * tasks)
    u = rng.normal(0, sd_person, n)
    v = rng.normal(0, sd_task, tasks)
    y = rng.binomial(1, expit(alpha + beta * tone + u[person] + v[task]))
    keep = (wrong == 1) & (initial == 1) & (rng.random(n * tasks) >= missing)
    return pd.DataFrame(dict(person=person[keep], task=task[keep],
                             tone=tone[keep], y=y[keep]))


def fit_trial(d):
    if any(d[c].nunique() < 2 for c in ("person", "task", "tone", "y")):
        return None
    try:
        model = BinomialBayesMixedGLM.from_formula(
            "y ~ tone", {"person": "0 + C(person)", "task": "0 + C(task)"},
            d, vcp_p=0.5, fe_p=5)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            fit = model.fit_vb(fit_method="BFGS", minim_opts={"maxiter": 500})
        if caught or not fit.optim_retvals.success:
            return None
        b, se = fit.fe_mean[1], fit.fe_sd[1]
        if not np.isfinite(b) or not np.isfinite(se) or se <= 0:
            return None
        return float(b), float(se)
    except (ValueError, RuntimeError, ArithmeticError, np.linalg.LinAlgError):
        return None


def scenario(n, tasks, beta, sd_person, sd_task, initial_correct,
             missing, replicates, seed, alpha=logit(.2)):
    if replicates < 1:
        raise ValueError("replicates must be positive")
    outcomes = []
    for child in np.random.SeedSequence(seed).spawn(replicates):
        rng = np.random.default_rng(child)
        # statsmodels VB uses NumPy's legacy RNG for starting values.
        state = np.random.get_state()
        try:
            np.random.seed(int(child.generate_state(1)[0]))
            outcomes.append(fit_trial(simulate_trials(
                rng, n, tasks, alpha, beta, sd_person, sd_task,
                initial_correct, missing)))
        finally:
            np.random.set_state(state)
    valid = np.asarray([o for o in outcomes if o is not None], dtype=float).reshape(-1, 2)
    failed = replicates - len(valid)
    estimates, ses = valid.T
    rejected = int(np.sum(np.abs(estimates / ses) > norm.ppf(.975)))
    covered = int(np.sum(np.abs(estimates - beta) <= norm.ppf(.975) * ses))
    coverage_ci = binomtest(covered, len(valid)).proportion_ci(method="exact") if len(valid) else None
    ci = binomtest(rejected, replicates).proportion_ci(method="exact")
    return dict(n=n, tasks=tasks, alpha=alpha, beta=beta,
                sd_person=sd_person, sd_task=sd_task,
                initial_correct=initial_correct, missing=missing,
                replicates=replicates, seed=seed, rejected=rejected,
                failed=failed, rejection_rate=rejected / replicates,
                failure_rate=failed / replicates,
                mean_bias=float(np.mean(estimates - beta)) if len(valid) else None,
                rmse=float(np.sqrt(np.mean((estimates - beta)**2))) if len(valid) else None,
                coverage=covered / len(valid) if len(valid) else None,
                coverage_lower95=coverage_ci.low if coverage_ci else None,
                coverage_upper95=coverage_ci.high if coverage_ci else None,
                lower95=ci.low, upper95=ci.high,
                conditional_rate=(rejected / (replicates - failed)
                                  if failed < replicates else None))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20261126)
    parser.add_argument("--output", required=True)
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    grid = itertools.product((80, 160, 240), (0, np.log(1.3), np.log(1.6)),
                             (.5, 1), (.3, .7), (.55, .75), (0, .1))
    if args.smoke:
        grid = [(8, 0, .5, .3, .75, 0)]
    rows = [scenario(n, 8 if args.smoke else 24, b, sp, st, q, m,
                     args.replicates, args.seed)
            for n, b, sp, st, q, m in grid]
    pd.DataFrame(rows).to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
