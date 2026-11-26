"""Synthetic-only statistical reference. Never use as a frozen analysis plan."""
import argparse
import json
import math
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

from design import VERSION, STIMULUS_VERSION
from synthetic import summarize, synthetic

NUMERIC = ("age_years", "sleep_hours", "depression_total")
CATEGORICAL = ("os_family", "browser_family", "task_order")


def finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def participant_rows(records, require_switch=True):
    """Complete-case selection; separate eligibility for switching and decisions."""
    rows, excluded, seen = [], {}, set()
    for rec in records:
        pid = rec.get("participant_id")
        if rec.get("data_origin") != "synthetic" or not isinstance(pid, str) or not pid.startswith("SYN-"):
            raise ValueError("synthetic provenance required")
        if pid in seen:
            raise ValueError("duplicate participant")
        seen.add(pid)
        if (rec.get("protocol_version"), rec.get("stimulus_version")) != (VERSION, STIMULUS_VERSION):
            raise ValueError("mixed or unsupported versions")
        gad = rec.get("gad7_total")
        if not finite(gad) or not 0 <= gad <= 21 or int(gad) != gad:
            excluded[pid] = "invalid_gad7"
            continue
        if not all(finite(rec.get(k)) for k in NUMERIC):
            excluded[pid] = "missing_numeric_covariate"
            continue
        order = rec.get("task_order")
        if (order not in (["switching", "decision"], ["decision", "switching"])
                or not all(isinstance(rec.get(k), str) and rec[k] for k in CATEGORICAL[:2])):
            excluded[pid] = "invalid_categorical_covariate"
            continue
        row = dict(participant_id=pid, gad5=gad/5, task_order=order[0],
                   **{k: rec[k] for k in NUMERIC+CATEGORICAL[:2]})
        if require_switch:
            q = summarize(rec["switching"])
            if not q["eligible"]:
                excluded[pid] = "switching_ineligible"
                continue
            row.update(baseline_rt_ms=q["baseline_rt_ms"], switch_cost_ms=q["switch_cost_ms"])
        rows.append(row)
    if not rows:
        raise ValueError("no eligible complete cases")
    return pd.DataFrame(rows), excluded


def matrix(frame, numeric, categorical):
    """Treatment coding, deterministic level order, explicit constant controls."""
    data = {"intercept": np.ones(len(frame))}
    omitted, references = [], {}
    for name in numeric:
        values = frame[name].to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise ValueError(f"nonfinite predictor: {name}")
        if np.ptp(values) == 0:
            if name == "gad5" or name in ("ev_difference", "variance_difference", "nominal_payoff_contrast", "ambiguity_width"):
                raise ValueError(f"constant estimand predictor: {name}")
            omitted.append(name)
        else:
            data[name] = values
    for name in categorical:
        levels = sorted(frame[name].unique())
        references[name] = levels[0]
        if len(levels) == 1:
            omitted.append(name)
        for level in levels[1:]:
            data[f"{name}={level}"] = (frame[name] == level).astype(float).to_numpy()
    x = pd.DataFrame(data, index=frame.index)
    if len(x) <= x.shape[1] or np.linalg.matrix_rank(x.to_numpy()) != x.shape[1]:
        raise ValueError("insufficient observations or rank-deficient design")
    return x, omitted, references


def effect(fit, name, odds=False):
    lo, hi = fit.conf_int().loc[name]
    values = dict(estimate=float(fit.params[name]), se=float(fit.bse[name]),
                  ci95=[float(lo), float(hi)], p=float(fit.pvalues[name]))
    if not np.isfinite([values["estimate"], values["se"], *values["ci95"], values["p"]]).all():
        raise ValueError("nonfinite inference")
    if odds:
        values["odds_ratio"] = math.exp(values["estimate"])
        values["or_ci95"] = [math.exp(v) for v in values["ci95"]]
    return values


def fit_h1(records, *, baseline=True, depression=True):
    frame, excluded = participant_rows(records)
    covariates = [k for k in NUMERIC if depression or k != "depression_total"]
    if baseline:
        covariates.append("baseline_rt_ms")
    x, omitted, refs = matrix(frame, ["gad5", *covariates], CATEGORICAL)
    y = frame["switch_cost_ms"].to_numpy()
    if not np.isfinite(y).all() or np.ptp(y) == 0:
        raise ValueError("constant or invalid outcome")
    model = sm.OLS(y, x)
    if np.max(model.fit().get_influence().hat_matrix_diag) >= 1-1e-10:
        raise ValueError("HC3 undefined at unit leverage")
    fit = model.fit(cov_type="HC3", use_t=True)
    return dict(model="OLS HC3; t inference", n=len(frame), df_resid=int(fit.df_resid),
                gad5=effect(fit, "gad5"), coefficients={k: effect(fit, k) for k in x.columns},
                omitted_constant=omitted, reference_levels=refs, excluded=excluded,
                baseline=baseline, depression=depression)


def choice_frame(records, task):
    """Validate decision identities and build a task-specific complete-case frame."""
    contrasts = {"risk": ("ev_difference", "variance_difference"),
                 "ambiguity": ("nominal_payoff_contrast", "ambiguity_width")}
    if task not in contrasts:
        raise ValueError("invalid task")
    covariates, excluded = participant_rows(records, require_switch=False)
    participants = covariates.set_index("participant_id").to_dict("index")
    rows = []
    for rec in records:
        pid = rec["participant_id"]
        if pid not in participants:
            continue
        trials = [t for t in rec["decisions"] if t["task"] == task]
        keys = set()
        for trial in trials:
            key = trial["trial_index"]
            if key in keys or trial.get("participant_id") != pid:
                raise ValueError("invalid decision identity")
            keys.add(key)
            if type(trial.get("target_chosen")) is not bool or not all(finite(trial.get(k)) for k in contrasts[task]):
                raise ValueError("invalid synthetic decision trial")
            rows.append(dict(participant_id=pid, **participants[pid],
                             chosen=int(trial["target_chosen"]), **{k: trial[k] for k in contrasts[task]}))
        if not trials:
            excluded[pid] = "no_decision_trials"
    frame = pd.DataFrame(rows)
    if frame.empty or frame["participant_id"].nunique() < 30:
        raise ValueError("at least 30 clusters required for reference GEE")
    if frame["chosen"].nunique() != 2:
        raise ValueError("constant choice outcome")
    x, omitted, refs = matrix(frame, ["gad5", *contrasts[task], *NUMERIC], CATEGORICAL)
    return frame, x, omitted, refs, excluded


def fit_choice_gee(records, task):
    """Population-averaged sensitivity model, not the preregistered GLMM."""
    frame, x, omitted, refs, excluded = choice_frame(records, task)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        fit = sm.GEE(frame["chosen"], x, groups=frame["participant_id"],
                     family=sm.families.Binomial(),
                     cov_struct=sm.cov_struct.Independence()).fit(cov_type="robust")
    if not fit.converged or caught:
        raise ValueError("GEE failed convergence or issued warnings: " + "; ".join(str(w.message) for w in caught))
    return dict(model="GEE binomial logit; participant-cluster robust; sensitivity",
                task=task, n_participants=int(frame["participant_id"].nunique()), n_trials=len(frame),
                gad5=effect(fit, "gad5", odds=True), omitted_constant=omitted,
                reference_levels=refs, excluded=excluded)


def analyze(records):
    records = list(records)
    h1 = fit_h1(records)
    h2 = fit_choice_gee(records, "risk")
    h3 = fit_choice_gee(records, "ambiguity")
    adjusted = multipletests([h2["gad5"]["p"], h3["gad5"]["p"]], method="holm")[1]
    for model, p in zip((h2, h3), adjusted):
        model["gad5"]["p_holm_sensitivity"] = float(p)
    return dict(data_origin="synthetic", protocol_version=VERSION, stimulus_version=STIMULUS_VERSION,
                H1=h1, H1_without_baseline=fit_h1(records, baseline=False),
                H1_without_depression=fit_h1(records, depression=False),
                H2_GEE_sensitivity=h2, H3_GEE_sensitivity=h3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=80)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    print(json.dumps(analyze(synthetic(args.seed, args.n)), indent=2, allow_nan=False))
