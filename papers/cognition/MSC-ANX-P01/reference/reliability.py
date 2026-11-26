"""Synthetic-only reliability and H1 attenuation sensitivity analysis."""
import argparse
import json
import math
from collections import Counter
import numpy as np
from design import VERSION, STIMULUS_VERSION
from synthetic import synthetic, summarize
from power import approximate_power, complete_n


def split_trials(rows, seed=0):
    """Split scheduled trials within block/transition, before outcome filtering."""
    rng = np.random.default_rng(seed)
    cells, seen = {}, set()
    for trial in rows:
        key = (trial["block"], trial["trial_index"])
        if key in seen:
            raise ValueError("duplicate trial")
        seen.add(key)
        if not trial["mixed"] or trial["transition"] == "undefined":
            continue
        if trial["transition"] not in ("switch", "repeat"):
            raise ValueError("invalid transition")
        cells.setdefault((trial["block"], trial["transition"]), []).append(trial)
    halves = [[], []]
    counts = Counter()
    for (block, condition), trials in sorted(cells.items()):
        trials = sorted(trials, key=lambda x:x["trial_index"])
        order = rng.permutation(len(trials))
        extra = 0 if counts[0,condition] < counts[1,condition] else 1 if counts[1,condition] < counts[0,condition] else int(rng.integers(2))
        n0 = len(trials)//2 + int(len(trials)%2 and extra==0)
        for half, indices in enumerate((order[:n0],order[n0:])):
            halves[half].extend(trials[i] for i in indices)
            counts[half,condition] += len(indices)
    return halves


def half_cost(rows, minimum=25):
    groups={"switch":[],"repeat":[]}
    for t in rows:
        rt=t["rt_ms"]
        if (t["focus_lost"] or t["technical_error"] or t["timeout"]
                or not t["correct"] or rt is None or not math.isfinite(rt) or not 150<=rt<=2000):
            continue
        groups[t["transition"]].append(rt)
    if min(map(len,groups.values()))<minimum:
        return None
    return float(np.median(groups["switch"])-np.median(groups["repeat"]))


def paired_costs(records, split_seed=42, minimum=25):
    if type(minimum) is not int or minimum<1:
        raise ValueError("invalid minimum")
    pairs, exclusions, seen = [], Counter(), set()
    for rec in records:
        pid=rec.get("participant_id")
        if rec.get("data_origin")!="synthetic" or not isinstance(pid,str) or not pid.startswith("SYN-"):
            raise ValueError("synthetic provenance required")
        if pid in seen:
            raise ValueError("duplicate participant")
        seen.add(pid)
        if (rec.get("protocol_version"),rec.get("stimulus_version"))!=(VERSION,STIMULUS_VERSION):
            raise ValueError("mixed or unsupported versions")
        trials=rec["switching"]
        if any(t.get("participant_id")!=pid for t in trials):
            raise ValueError("mismatched trial identity")
        halves=split_trials(trials,split_seed)
        if not summarize(trials)["eligible"]:
            exclusions["primary_ineligible"]+=1
            continue
        costs=[half_cost(half,minimum) for half in halves]
        if None in costs:
            exclusions["insufficient_half_trials"]+=1
            continue
        pairs.append(costs)
    return np.asarray(pairs,dtype=float).reshape(-1,2),dict(exclusions)


def correlation(pairs):
    a=np.asarray(pairs,dtype=float)
    if a.ndim!=2 or a.shape[1]!=2 or len(a)<3 or not np.isfinite(a).all():
        return None
    if np.any(np.ptp(a,axis=0)==0):
        return None
    return float(np.clip(np.corrcoef(a.T)[0,1],-1,1))


def spearman_brown(r):
    # Negative split correlations indicate an unreliable score. Preserve the
    # raw r; do not turn an inadmissible corrected coefficient into zero.
    if r is None or r<=-1 or r>1:
        return None
    return 2*r/(1+r)


def reliability(pairs, bootstrap=2000, seed=43):
    a=np.asarray(pairs,dtype=float)
    if type(bootstrap) is not int or bootstrap<1:
        raise ValueError("invalid bootstrap count")
    r=correlation(a)
    if r is None:
        raise ValueError("insufficient or constant paired scores")
    sb=spearman_brown(r)
    rng=np.random.default_rng(seed)
    raw,corrected=[],[]
    for _ in range(bootstrap):
        b=a[rng.integers(0,len(a),len(a))]
        q=correlation(b)
        if q is None:
            continue
        raw.append(q)
        c=spearman_brown(q)
        if c is not None and math.isfinite(c):
            corrected.append(c)
    def ci(values):
        return [float(v) for v in np.quantile(values,[.025,.975])] if values else None
    return dict(n=len(a),split_r=r,spearman_brown=sb,
                admissible_reliability=sb is not None and 0<=sb<=1,
                split_r_ci95=ci(raw),spearman_brown_ci95=ci(corrected),
                bootstrap=bootstrap,valid_raw=len(raw),valid_corrected=len(corrected),
                mean_difference_ms=float(np.mean(a[:,0]-a[:,1])),
                sd_difference_ms=float(np.std(a[:,0]-a[:,1],ddof=1)),
                ci_method="paired participant percentile bootstrap; fixed split")


def attenuation(latent_r, reliability_x, reliability_y, n=355, k=8):
    """Classical independent error approximation on residualized variables."""
    if not (0<abs(latent_r)<1 and 0<reliability_x<=1 and 0<reliability_y<=1):
        raise ValueError("invalid attenuation parameters")
    observed=latent_r*math.sqrt(reliability_x*reliability_y)
    return dict(latent_partial_r=latent_r,reliability_x=reliability_x,
                reliability_y=reliability_y,observed_partial_r=observed,
                n_complete=n,power=approximate_power(n,observed,k),
                complete_n_80=complete_n(observed,k))


def analyze(records, split_seed=42, bootstrap=2000, bootstrap_seed=43):
    pairs,excluded=paired_costs(records,split_seed)
    result=reliability(pairs,bootstrap,bootstrap_seed)
    return dict(data_origin="synthetic",split_seed=split_seed,bootstrap_seed=bootstrap_seed,
                exclusions=excluded,reliability=result,
                attenuation_scenarios=[attenuation(.15,.85,y) for y in (.3,.5,.7,.9,1.)])


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n",type=int,default=80)
    p.add_argument("--seed",type=int,default=42)
    p.add_argument("--bootstrap",type=int,default=2000)
    a=p.parse_args()
    print(json.dumps(analyze(synthetic(a.seed,a.n),bootstrap=a.bootstrap),indent=2,allow_nan=False))
