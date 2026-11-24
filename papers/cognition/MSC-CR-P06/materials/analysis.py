"""Reference ANCOVA analysis for MSC-CR-P06, no third-party dependencies.

Complete-case sensitivity and pooling of independently generated multiple
imputations. Does not generate PMM imputations or fit the item-level GLMM.
Normal-reference HC3 and Rubin intervals are asymptotic, not exact small-N tests.
"""
from __future__ import annotations

import itertools
import math
from statistics import mean, NormalDist, variance

SEQUENCES = tuple("".join(s) for s in itertools.permutations("ABC"))
ENDPOINTS = {
    "H1": ("accuracy_T0", "accuracy_T1", 100),
    "H2": ("accuracy_T0", "accuracy_T2", 100),
    "H3": ("brier_T0", "brier_T1", 1),
    "H4": ("justification_T0", "justification_T1", 1),
}
SCORE_FIELDS = {v for a,b,_ in ENDPOINTS.values() for v in (a,b)}
Z = NormalDist()


def validate(rows):
    """Reject mixed identifiers, invalid ranges, and unplanned columns.

    Rows are participant-level pseudonymous summaries; no contact data.
    Return independent copies with omitted score fields normalized to None.
    """
    seen = set()
    out = []
    for row in rows:
        if set(row)-({"participant_id","arm","stratum","sequence"} | SCORE_FIELDS):
            raise ValueError("Unexpected field")
        pid = row.get("participant_id")
        if not isinstance(pid,str) or not pid or pid in seen:
            raise ValueError("Invalid or duplicate participant ID")
        seen.add(pid)
        if type(row.get("arm")) is not int or row["arm"] not in (0,1):
            raise ValueError("Invalid arm")
        if type(row.get("stratum")) is not int or row["stratum"] not in (0,1):
            raise ValueError("Invalid stratum")
        if row.get("sequence") not in SEQUENCES:
            raise ValueError("Invalid sequence")
        clean = dict(row)
        for field in SCORE_FIELDS:
            value = row.get(field)
            limit = 2 if field.startswith("justification") else 1
            if value is not None and (type(value) not in (int,float) or not math.isfinite(value) or not 0<=value<=limit):
                raise ValueError("Invalid endpoint: "+field)
            clean[field] = value
        out.append(clean)
    if not out or {r["arm"] for r in out}!={0,1}:
        raise ValueError("Both randomized arms required")
    return out


def _dot(a,b):
    return math.fsum(x*y for x,y in zip(a,b))


def _inverse(a):
    """Gauss-Jordan with partial pivoting; fail closed on singular design."""
    n = len(a)
    m = [list(row)+[float(i==j) for j in range(n)] for i,row in enumerate(a)]
    scale = max(abs(v) for row in a for v in row)
    for i in range(n):
        k = max(range(i,n),key=lambda j:abs(m[j][i]))
        if abs(m[k][i]) <= 1e-11*max(1,scale):
            raise ValueError("Rank-deficient ANCOVA design")
        m[i],m[k] = m[k],m[i]
        pivot = m[i][i]
        m[i] = [v/pivot for v in m[i]]
        for j in range(n):
            if j!=i:
                factor = m[j][i]
                m[j] = [v-factor*w for v,w in zip(m[j],m[i])]
    return [row[n:] for row in m]


def _wald(estimate, var, alpha=.05):
    if not math.isfinite(var) or var<=0:
        raise ValueError("Undefined or zero effect variance")
    se = math.sqrt(var)
    critical = Z.inv_cdf(1-alpha/2)
    # erfc is stable even for very small p-values.
    return {"estimate":estimate,"variance":var,"se":se,
            "ci":[estimate-critical*se,estimate+critical*se],
            "p":math.erfc(abs(estimate/se)/math.sqrt(2))}


def fit_endpoint(rows, hypothesis, *, complete_case=True):
    """Adjusted intervention minus control with HC3 covariance.

    Covariates: matching baseline, two-level experience stratum and
    five fixed sequence indicators (ABC reference). No variable selection.
    """
    rows = validate(rows)
    baseline, outcome, scale = ENDPOINTS[hypothesis]
    used = [r for r in rows if r[baseline] is not None and r[outcome] is not None]
    if not complete_case and len(used)!=len(rows):
        raise ValueError("Incomplete imputation")
    if {r["arm"] for r in used}!={0,1}:
        raise ValueError("Both arms required after missingness")
    center = mean(r[baseline] for r in used)
    x = [[1.,float(r["arm"]),r[baseline]-center,float(r["stratum"])]
         + [float(r["sequence"]==s) for s in SEQUENCES[1:]] for r in used]
    y = [r[outcome] for r in used]
    p = len(x[0])
    if len(x)<=p:
        raise ValueError("Insufficient residual degrees of freedom")
    cols = list(zip(*x))
    inv = _inverse([[_dot(a,b) for b in cols] for a in cols])
    beta = [_dot(row,[_dot(col,y) for col in cols]) for row in inv]
    v = 0.
    for row,yi in zip(x,y):
        q = [_dot(a,row) for a in inv]
        leverage = _dot(row,q)
        if not 0<=leverage<1-1e-10:
            raise ValueError("Invalid leverage")
        residual = yi-_dot(row,beta)
        v += (q[1]*residual/(1-leverage))**2
    result = _wald(beta[1]*scale,v*scale**2)
    result.update({"hypothesis":hypothesis,"unit":"percentage_points" if scale==100 else "raw_score",
                   "n_randomized":len(rows),"n_used":len(used),
                   "n_by_arm":{str(a):sum(r["arm"]==a for r in used) for a in (0,1)},
                   "reference":"asymptotic_normal_HC3"})
    return result


def holm(pvalues):
    """Holm step-down adjusted p-values, preserving hypothesis labels."""
    if not pvalues or any(type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1 for v in pvalues.values()):
        raise ValueError("Invalid p-values")
    order = sorted(pvalues,key=lambda k:pvalues[k])
    out = {}
    running = 0.
    for i,k in enumerate(order):
        running = max(running,min(1.,(len(order)-i)*pvalues[k]))
        out[k] = running
    return out


def rubin(estimates):
    """Scalar Rubin pooling; normal-reference interval, not finite-df t."""
    estimates = list(estimates)
    if len(estimates)<2:
        raise ValueError("At least two imputations required")
    q = [r["estimate"] for r in estimates]
    u = [r["variance"] for r in estimates]
    if any(not math.isfinite(x) for x in q+u) or min(u)<=0:
        raise ValueError("Invalid imputation estimates")
    m = len(q)
    within, between = mean(u), variance(q)
    total = within+(1+1/m)*between
    result = _wald(mean(q),total)
    result.update({"m":m,"within_variance":within,"between_variance":between,
                   "missing_information_fraction_asymptotic":(1+1/m)*between/total,
                   "reference":"asymptotic_normal_Rubin_HC3"})
    return result


def _align(original, completed):
    completed = validate(completed)
    by_id = {r["participant_id"]:r for r in completed}
    if set(by_id)!={r["participant_id"] for r in original}:
        raise ValueError("Imputations must preserve randomized population")
    ordered = []
    for row in original:
        new = by_id[row["participant_id"]]
        for key in ("arm","stratum","sequence"):
            if row[key]!=new[key]:
                raise ValueError("Imputation changed design")
        for key in SCORE_FIELDS:
            if new[key] is None or (row[key] is not None and row[key]!=new[key]):
                raise ValueError("Imputation incomplete or changed observed score")
        ordered.append(new)
    return ordered


def _adjust(results):
    adjusted = holm({h:results[h]["p"] for h in ("H2","H3","H4")})
    for h,r in results.items():
        r["p_adjusted"] = adjusted.get(h,r["p"])
    return results


def analyze_complete_cases(rows):
    return _adjust({h:fit_endpoint(rows,h) for h in ENDPOINTS})


def analyze_imputations(original, datasets, *, expected_m=50, delta=0., shifted_arm=None):
    """Pool supplied imputations; bounded MNAR shift only for missing H1 outcomes.

    delta is in raw proportion units; e.g. -0.05 means a five percentage
    point decrease. Shift is applied before fitting, never to observed values.
    This is a sensitivity scenario, not evidence of an MNAR mechanism.
    """
    original = validate(original)
    datasets = list(datasets)
    if type(expected_m) is not int or expected_m<2 or len(datasets)!=expected_m:
        raise ValueError("Unexpected number of imputations")
    if (type(delta) not in (int,float) or not math.isfinite(delta) or not -1<=delta<=1
            or (shifted_arm is not None and (type(shifted_arm) is not int or shifted_arm not in (0,1)))
            or (delta!=0 and shifted_arm is None)):
        raise ValueError("Invalid sensitivity scenario")
    fits = {h:[] for h in ENDPOINTS}
    for completed in datasets:
        aligned = _align(original,completed)
        for old,new in zip(original,aligned):
            if old["accuracy_T1"] is None and new["arm"]==shifted_arm:
                new["accuracy_T1"] = min(1.,max(0.,new["accuracy_T1"]+delta))
        for h in ENDPOINTS:
            fits[h].append(fit_endpoint(aligned,h,complete_case=False))
    out = {}
    for h,estimates in fits.items():
        out[h] = rubin(estimates)
        out[h].update({"hypothesis":h,"unit":estimates[0]["unit"],
                       "n_randomized":len(original),"n_used":len(original),
                       "delta_primary":delta,"shifted_arm":shifted_arm})
    return _adjust(out)


def missingness(rows):
    rows = validate(rows)
    return {str(a):{"n":sum(r["arm"]==a for r in rows),
                    "missing":{f:sum(r["arm"]==a and r[f] is None for r in rows)
                               for f in sorted(SCORE_FIELDS)}} for a in (0,1)}
