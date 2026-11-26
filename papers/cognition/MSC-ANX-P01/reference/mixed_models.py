"""Synthetic-only mixed models; explicit numerical identification gates."""
import argparse
import json
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from numpy.polynomial.hermite import hermgauss
from scipy.optimize import minimize
from scipy.special import expit, logsumexp
from scipy.stats import norm
from statsmodels.stats.multitest import multipletests

from statistical import (NUMERIC, CATEGORICAL, matrix, participant_rows,
                         choice_frame, effect, finite, ModelUnavailable)
from synthetic import synthetic


def _quadrature(x, y, groups, nodes):
    z, w = hermgauss(nodes)
    z = np.sqrt(2) * z
    logw = np.log(w) - .5*np.log(np.pi)
    # Padded cluster arrays allow vectorized integration, including unequal sizes.
    labels, inverse = np.unique(groups, return_inverse=True)
    lengths = np.bincount(inverse)
    xx = np.zeros((len(labels), max(lengths), x.shape[1]))
    yy = np.zeros(xx.shape[:2])
    mask = np.zeros_like(yy)
    pos = np.zeros(len(labels), dtype=int)
    for i, g in enumerate(inverse):
        j = pos[g]
        xx[g,j], yy[g,j], mask[g,j] = x[i], y[i], 1
        pos[g] += 1

    def objective(theta):
        beta, sigma = theta[:-1], np.exp(theta[-1])
        eta = (xx @ beta)[...,None] + sigma*z
        loglik = np.sum(mask[...,None]*(yy[...,None]*eta-np.logaddexp(0,eta)), axis=1)
        logjoint = loglik + logw
        logm = logsumexp(logjoint, axis=1)
        posterior = np.exp(logjoint-logm[:,None])
        residual = mask[...,None]*(yy[...,None]-expit(eta))
        score_beta = np.einsum("gtp,gtq,gq->p", xx, residual, posterior)
        score_sd = np.einsum("gtq,q,gq->", residual, sigma*z, posterior)
        return -float(logm.sum()), -np.r_[score_beta, score_sd]
    return objective


def _hessian(gradient, theta):
    columns = []
    for j in range(len(theta)):
        step = 1e-4*max(1., abs(theta[j]))
        delta = np.zeros_like(theta)
        delta[j] = step
        columns.append((gradient(theta+delta)-gradient(theta-delta))/(2*step))
    h = np.column_stack(columns)
    return (h+h.T)/2


def logistic_ri(y, x, groups, term):
    """Frequentist random-intercept logit, ML by Gaussian quadrature."""
    y = np.asarray(y, dtype=float)
    raw = x.to_numpy(dtype=float)
    groups = np.asarray(groups)
    if (len(y) != len(raw) or len(groups) != len(y) or len(np.unique(groups)) < 30
            or set(np.unique(y)) != {0.,1.} or not np.isfinite(raw).all()
            or np.linalg.matrix_rank(raw) != raw.shape[1] or term not in x
            or x.columns[0] != "intercept" or not np.all(raw[:,0]==1)):
        raise ModelUnavailable("invalid or unidentified random-intercept model")
    means = raw[:,1:].mean(axis=0)
    scales = raw[:,1:].std(axis=0)
    if np.any(scales <= 0):
        raise ModelUnavailable("constant predictor")
    a = raw.copy()
    a[:,1:] = (raw[:,1:]-means)/scales
    start = np.r_[np.zeros(a.shape[1]), -.3]
    bounds = [(None,None)]*a.shape[1]+[(-5.,2.)]
    coarse = _quadrature(a,y,groups,32)
    fine = _quadrature(a,y,groups,64)
    def fit(obj, initial):
        result = minimize(obj, initial, jac=True, method="L-BFGS-B", bounds=bounds,
                          options={"ftol":1e-12,"gtol":1e-6,"maxiter":500})
        if not result.success or not np.isfinite(result.fun):
            raise ModelUnavailable("random-intercept optimizer failed")
        return result
    initial = fit(coarse,start)
    result = fit(fine,initial.x)
    theta = result.x
    if not -4.95 < theta[-1] < 1.95:
        raise ModelUnavailable("random-effect variance on numerical boundary")
    if np.max(np.abs(fine(theta)[1])) > .02:
        raise ModelUnavailable("score not near zero")
    # Compare integration resolutions before using the observed information.
    check = _quadrature(a,y,groups,96)
    if abs(check(theta)[0]-result.fun) > .01 or np.max(np.abs(check(theta)[1])) > .05:
        raise ModelUnavailable("quadrature resolution inadequate")
    info = _hessian(lambda t: fine(t)[1], theta)
    if np.min(np.linalg.eigvalsh(info)) <= 1e-6:
        raise ModelUnavailable("nonpositive or singular observed information")
    cov = np.linalg.inv(info)
    transform = np.eye(len(theta))
    transform[0,1:-1] = -means/scales
    transform[1:-1,1:-1] = np.diag(1/scales)
    beta = transform @ theta
    var = transform @ cov @ transform.T
    i = list(x.columns).index(term)
    se = float(np.sqrt(var[i,i]))
    estimate = float(beta[i])
    lo, hi = estimate-1.959963984540054*se, estimate+1.959963984540054*se
    return dict(model="binomial logit random intercept; marginal ML; conditional coefficient",
                n_trials=len(y), n_participants=len(np.unique(groups)),
                random_intercept_sd=float(np.exp(theta[-1])),
                log_likelihood=-float(result.fun), quadrature_nodes=64,
                quadrature_check_nodes=96, gad_effect=dict(estimate=estimate,se=se,ci95=[lo,hi],
                p=float(2*norm.sf(abs(estimate/se))),odds_ratio=float(np.exp(estimate)),
                or_ci95=[float(np.exp(lo)),float(np.exp(hi))]))


def fit_choice_glmm(records, task):
    frame,x,omitted,refs,excluded = choice_frame(records, task)
    out = logistic_ri(frame["chosen"],x,frame["participant_id"],"gad5")
    return dict(out, task=task, omitted_constant=omitted,reference_levels=refs,excluded=excluded)


def switching_frame(records, accuracy=False):
    base, excluded = participant_rows(records, require_switch=False)
    participants = base.set_index("participant_id").to_dict("index")
    rows = []
    for rec in records:
        pid = rec["participant_id"]
        if pid not in participants:
            continue
        seen = set()
        for trial in rec["switching"]:
            key = trial["block"],trial["trial_index"]
            if key in seen or trial.get("participant_id") != pid:
                raise ValueError("invalid switching identity")
            seen.add(key)
            if not trial["mixed"] or trial["transition"] == "undefined":
                continue
            if trial["transition"] not in ("switch","repeat"):
                raise ValueError("invalid transition")
            if trial["focus_lost"] or trial["technical_error"]:
                continue
            rt = trial["rt_ms"]
            if not trial["timeout"] and (not finite(rt) or not 150 <= rt <= 2000):
                continue
            correct = not trial["timeout"] and trial["correct"]
            if not accuracy and not correct:
                continue
            sw = int(trial["transition"] == "switch")
            person = participants[pid]
            rows.append(dict(participant_id=pid, **person, switch=sw,
                             interaction=sw*person["gad5"], outcome=int(correct) if accuracy else np.log(rt)))
    frame = pd.DataFrame(rows)
    if frame.empty or frame["participant_id"].nunique()<30:
        raise ModelUnavailable("insufficient switching clusters")
    x,omitted,refs = matrix(frame,["gad5","switch","interaction",*NUMERIC],CATEGORICAL)
    if "switch" not in x or "interaction" not in x:
        raise ValueError("unidentified switch interaction")
    return frame,x,omitted,refs,excluded


def fit_rt_mixed(records, *, random_slope=True):
    frame,x,omitted,refs,excluded = switching_frame(records)
    return rt_mixed(frame,x,random_slope=random_slope) | dict(
        omitted_constant=omitted,reference_levels=refs,excluded=excluded)


def rt_mixed(frame,x,*,random_slope):
    re = x[["intercept","switch"]] if random_slope else x[["intercept"]]
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        model = sm.MixedLM(frame["outcome"],x,groups=frame["participant_id"],exog_re=re)
        fit = model.fit(reml=False,method="lbfgs",maxiter=300,disp=False)
    if not fit.converged or np.min(np.linalg.eigvalsh(fit.cov_re))<=1e-8:
        raise ModelUnavailable("RT mixed model failed convergence or singular covariance")
    return dict(model="ML Gaussian mixed model; log RT", random_slope=random_slope,
                n_trials=len(frame),n_participants=int(frame["participant_id"].nunique()),
                interaction=effect(fit,"interaction"),
                warnings=[str(w.message) for w in caught])


def fit_accuracy_glmm(records):
    frame,x,omitted,refs,excluded = switching_frame(records,accuracy=True)
    out = logistic_ri(frame["outcome"],x,frame["participant_id"],"interaction")
    out["interaction"] = out.pop("gad_effect")
    return dict(out,omitted_constant=omitted,reference_levels=refs,excluded=excluded)


def analyze_mixed(records,random_slope=True):
    records=list(records)
    h2,h3=choice_family(records)
    return dict(data_origin="synthetic", H2=h2,H3=h3,
                RT=optional_fit(lambda:fit_rt_mixed(records,random_slope=random_slope)),
                accuracy=optional_fit(lambda:fit_accuracy_glmm(records)))


def optional_fit(call):
    try:
        return dict(call(),status="estimated")
    except (ModelUnavailable,np.linalg.LinAlgError,FloatingPointError) as exc:
        return dict(status="not_estimated",reason=str(exc))


def choice_family(records, *, fitter=fit_choice_glmm):
    models=[optional_fit(lambda t=t:fitter(records,t)) for t in ("risk","ambiguity")]
    pvalues=[m["gad_effect"]["p"] if m["status"]=="estimated" else 1. for m in models]
    adjusted=multipletests(pvalues,method="holm")[1]
    for model,p in zip(models,adjusted):
        if model["status"]=="estimated":
            model["gad_effect"]["p_holm"]=float(p)
    return models


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n",type=int,default=150)
    parser.add_argument("--seed",type=int,default=42)
    parser.add_argument("--intercept-only",action="store_true")
    args=parser.parse_args()
    print(json.dumps(analyze_mixed(synthetic(args.seed,args.n),not args.intercept_only),indent=2,allow_nan=False))
