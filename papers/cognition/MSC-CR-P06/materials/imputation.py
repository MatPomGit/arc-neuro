"""Prospective P06 FCS predictive mean matching; synthetic verification only.

Type-1 PMM: fixed observed-donor predictions and stochastic recipient
predictions. Donors are observed outcomes in the same randomized arm.
No participant-level output is written to disk by this module.
"""
from __future__ import annotations
import math
import random
from statistics import mean
from analysis import SCORE_FIELDS, SEQUENCES, validate, _dot, _inverse

FIELDS = tuple(sorted(SCORE_FIELDS))


def _cholesky(a):
    n=len(a)
    l=[[0.]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            s=(a[i][j]+a[j][i])/2-_dot(l[i][:j],l[j][:j])
            if i==j:
                if s<=0:
                    raise ValueError("Non-positive posterior covariance")
                l[i][j]=math.sqrt(s)
            else:
                l[i][j]=s/l[j][j]
    return l


def _design(rows, field):
    x=[[float(r["arm"]),float(r["stratum"])]
       +[float(r["sequence"]==s) for s in SEQUENCES[1:]]
       +[r[f] for f in FIELDS if f!=field] for r in rows]
    # Standardize nonconstant columns; ridge excludes the intercept.
    columns=[]
    for col in zip(*x):
        center=mean(col)
        sd=math.sqrt(mean((v-center)**2 for v in col))
        if sd>1e-12:
            columns.append([(v-center)/sd for v in col])
    return [[1.]+[col[i] for col in columns] for i in range(len(rows))]


def _step(rows, original, field, missing, observed, rng, donors, ridge):
    x=_design(rows,field)
    p=len(x[0])
    n=len(observed)
    if n<=p+2:
        raise ValueError("Too few observed values for PMM: "+field)
    xo=[x[i] for i in observed]
    y=[original[i][field] for i in observed]
    cols=list(zip(*xo))
    gram=[[_dot(a,b) for b in cols] for a in cols]
    # Small ridge stabilizes near-collinear predictors; intercept unpenalized.
    for j in range(1,p):
        gram[j][j]+=ridge*max(gram[j][j],1.)
    inv=_inverse(gram)
    beta=[_dot(row,[_dot(col,y) for col in cols]) for row in inv]
    rss=sum((v-_dot(row,beta))**2 for row,v in zip(xo,y))
    if rss<=1e-14:
        raise ValueError("Degenerate PMM residual variance: "+field)
    # Approximate ridge posterior draw using conventional residual df.
    sigma2=rss/rng.gammavariate((n-p)/2,2.)
    l=_cholesky(inv)
    z=[rng.gauss(0,1) for _ in range(p)]
    draw=[b+math.sqrt(sigma2)*_dot(row,z) for b,row in zip(beta,l)]
    donor_pred={i:_dot(x[i],beta) for i in observed}
    for i in missing:
        pred=_dot(x[i],draw)
        eligible=[j for j in observed if original[j]["arm"]==original[i]["arm"]]
        # Randomize ties before distance sorting, then sample uniformly.
        rng.shuffle(eligible)
        eligible.sort(key=lambda j:abs(donor_pred[j]-pred))
        rows[i][field]=original[rng.choice(eligible[:donors])][field]


def generate_imputations(rows, *, m=50, iterations=20, donors=5, seed=20261124, ridge=1e-5):
    """Return independently initialized FCS chains and aggregate trace diagnostics.

    Imputation includes randomized arm, stratum, sequence and the other six
    summary measures. All donor values are observed, never imputed. Requires
    enough observed donors within each arm; fails closed for sparse designs.
    Ridge PMM is a prospective reference, not a validated clinical pipeline.
    """
    if any(type(v) is not int or v<minimum for v,minimum in ((m,2),(iterations,1),(donors,1))):
        raise ValueError("Invalid PMM settings")
    if type(seed) is not int or not isinstance(ridge,(int,float)) or not math.isfinite(ridge) or not 0<ridge<=.1:
        raise ValueError("Invalid seed or ridge")
    original=validate(rows)
    masks={f:[i for i,r in enumerate(original) if r[f] is None] for f in FIELDS}
    observed={f:[i for i,r in enumerate(original) if r[f] is not None] for f in FIELDS}
    targets=[f for f in FIELDS if masks[f]]
    for f in targets:
        for arm in (0,1):
            if any(original[i]["arm"]==arm for i in masks[f]) and sum(original[j]["arm"]==arm for j in observed[f])<donors:
                raise ValueError("Insufficient same-arm donors: "+f)
    master=random.Random(seed)
    datasets=[]
    traces=[]
    for _ in range(m):
        rng=random.Random(master.getrandbits(64))
        completed=[dict(r) for r in original]
        for f in targets:
            for i in masks[f]:
                pool=[j for j in observed[f] if original[j]["arm"]==original[i]["arm"]]
                completed[i][f]=original[rng.choice(pool)][f]
        chain=[]
        for iteration in range(iterations):
            for f in targets:
                _step(completed,original,f,masks[f],observed[f],rng,donors,ridge)
            chain.append({f:{"mean":mean(completed[i][f] for i in masks[f]),
                             "sd":math.sqrt(mean((completed[i][f]-mean(completed[j][f] for j in masks[f]))**2 for i in masks[f]))}
                          for f in targets})
        datasets.append(completed)
        traces.append(chain)
    return {"datasets":datasets,"traces":traces,"settings":{"m":m,"iterations":iterations,
            "donors":donors,"seed":seed,"ridge":ridge},"missing_counts":{f:len(masks[f]) for f in FIELDS},
            "status":"REFERENCE_PMM_NOT_EMPIRICALLY_VALIDATED"}
