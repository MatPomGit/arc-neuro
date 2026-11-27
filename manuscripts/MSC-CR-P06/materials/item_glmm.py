"""Bayesian logistic crossed-intercept sensitivity model for P06.

Optional dependencies: numpy, scipy, statsmodels. Mean-field variational
posterior and Gaussian quadrature; not a frequentist maximum-likelihood fit.
"""
from __future__ import annotations
from analysis import validate, SEQUENCES


def prepare(participants, item_rows):
    """Use posttest positions of participants with observed baseline accuracy."""
    participants=validate(participants)
    by_id={r["participant_id"]:r for r in participants}
    target=[r for r in participants if r["accuracy_T0"] is not None]
    center=sum(r["accuracy_T0"] for r in target)/len(target) if target else 0.
    def features(r,arm):
        return [1.,float(arm),r["accuracy_T0"]-center,float(r["stratum"])]+[
            float(r["sequence"]==s) for s in SEQUENCES[1:]]
    observations=[]
    seen=set()
    for item in item_rows:
        if set(item)!={"participant_id","item_id","correct"}:
            raise ValueError("Unexpected item fields")
        pid,iid,y=item["participant_id"],item["item_id"],item["correct"]
        if pid not in by_id:
            raise ValueError("Unknown participant")
        r=by_id[pid]
        if (not isinstance(iid,str) or len(iid)!=3 or iid[0]!=r["sequence"][1]
                or iid[1:] not in {f"{j:02d}" for j in range(1,25)}):
            raise ValueError("Item outside assigned posttest form")
        if (pid,iid) in seen:
            raise ValueError("Duplicate participant-item pair")
        seen.add((pid,iid))
        if y is not None and (type(y) is not int or y not in (0,1)):
            raise ValueError("Expected 0/1/None")
        if y is not None and r["accuracy_T0"] is not None:
            observations.append((pid,iid,y,features(r,r["arm"])))
    if not observations or {row[2] for row in observations}!={0,1}:
        raise ValueError("Both binary outcomes required")
    if {by_id[row[0]]["arm"] for row in observations}!={0,1}:
        raise ValueError("Both arms must have observed items")
    return {"observations":observations,"x0":[features(r,0) for r in target],
            "x1":[features(r,1) for r in target],"n_randomized":len(participants),
            "n_standardized":len(target),"n_with_items":len({o[0] for o in observations})}


def fit_glmm(participants,item_rows,*,draws=2000,seed=20261124):
    """Fit crossed random intercepts and marginalize both over new draws.

    Standardizes over baseline-known randomized participants; no imputation
    of items. Relies on conditional ignorability; not a replacement for ITT.
    Intervals are approximate variational posterior credible intervals.
    """
    import numpy as np
    from scipy.sparse import coo_matrix
    from scipy.special import expit
    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

    if type(draws) is not int or draws<100 or type(seed) is not int:
        raise ValueError("Invalid posterior draw settings")
    prep=prepare(participants,item_rows)
    obs=prep["observations"]
    x=np.asarray([r[3] for r in obs])
    y=np.asarray([r[2] for r in obs])
    if np.linalg.matrix_rank(x)!=x.shape[1]:
        raise ValueError("Rank-deficient GLMM design")
    people={v:i for i,v in enumerate(sorted({r[0] for r in obs}))}
    items={v:i for i,v in enumerate(sorted({r[1] for r in obs}))}
    n=len(obs)
    if len(people)<2 or len(items)<2:
        raise ValueError("Insufficient random-effect levels")
    cols=[people[r[0]] for r in obs]+[len(people)+items[r[1]] for r in obs]
    z=coo_matrix((np.ones(2*n),(list(range(n))*2,cols)),
                 shape=(n,len(people)+len(items))).tocsr()
    ident=np.array([0]*len(people)+[1]*len(items),dtype=int)
    model=BinomialBayesMixedGLM(y,x,z,ident,vcp_p=.5,fe_p=2.)
    # Statsmodels' VB initialization uses NumPy's global RNG unless supplied.
    start=np.zeros(model.k_fep+model.k_vcp+model.k_vc)
    fit=model.fit_vb(mean=start,sd=np.full_like(start,.5),minim_opts={"maxiter":1000})
    if not fit.optim_retvals.get("success",False):
        raise ValueError("GLMM variational optimization did not converge")
    if not all(np.all(np.isfinite(v)) for v in (fit.fe_mean,fit.fe_sd,fit.vcp_mean,fit.vcp_sd)):
        raise ValueError("Nonfinite posterior parameters")
    rng=np.random.default_rng(seed)
    nodes,weights=np.polynomial.hermite.hermgauss(20)
    weights=weights/np.sqrt(np.pi)
    x0,x1=np.asarray(prep["x0"]),np.asarray(prep["x1"])
    effects=[]
    for _ in range(draws):
        beta=rng.normal(fit.fe_mean,fit.fe_sd)
        log_sd=rng.normal(fit.vcp_mean,fit.vcp_sd)
        sd=np.sqrt(np.sum(np.exp(2*log_sd)))
        if not np.isfinite(sd):
            raise ValueError("Nonfinite random-effect SD draw")
        offset=np.sqrt(2)*sd*nodes
        p0=expit((x0@beta)[:,None]+offset)@weights
        p1=expit((x1@beta)[:,None]+offset)@weights
        effects.append(100*np.mean(p1-p0))
    return {"estimate_pp":float(np.mean(effects)),
            "credible_interval_95_pp":np.quantile(effects,[.025,.975]).tolist(),
            "n_randomized":prep["n_randomized"],"n_standardized":prep["n_standardized"],
            "n_with_items":prep["n_with_items"],"n_observed_items":n,
            "random_effect_levels":{"participant":len(people),"item":len(items)},
            "log_sd_posterior_mean":fit.vcp_mean.tolist(),
            "draws":draws,"seed":seed,
            "reference":"BAYESIAN_VB_SENSITIVITY_NOT_PRIMARY"}
