"""Classical test theory and planning scenarios for P06; standard library only."""
from __future__ import annotations

import itertools
import math
import random
from statistics import NormalDist, mean, stdev, variance

Z = NormalDist()


def _correlation(x, y):
    if len(x) < 3:
        return None
    mx, my = mean(x), mean(y)
    xx = sum((v-mx)**2 for v in x)
    yy = sum((v-my)**2 for v in y)
    if not xx or not yy:
        return None
    return sum((a-mx)*(b-my) for a,b in zip(x,y)) / math.sqrt(xx*yy)


def wilson(successes, n, alpha=0.05):
    """Wilson interval for a binomial proportion; no responses means undefined."""
    if not (type(n) is int and type(successes) is int and 0 <= successes <= n and 0 < alpha < 1):
        raise ValueError("Invalid binomial parameters")
    if n == 0:
        return None
    z = Z.inv_cdf(1-alpha/2)
    p = successes/n
    denom = 1+z*z/n
    center = (p+z*z/(2*n))/denom
    half = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/denom
    return [max(0.0, center-half), min(1.0, center+half)]


def _kr20(matrix):
    """Binary-item alpha (KR-20), using consistent sample variances."""
    if len(matrix) < 2 or len(matrix[0]) < 2:
        return None
    k = len(matrix[0])
    total_var = variance([sum(row) for row in matrix])
    if total_var == 0:
        return None
    return k/(k-1)*(1-sum(variance(col) for col in zip(*matrix))/total_var)


def _percentile(values, q):
    ordered = sorted(values)
    i = q*(len(ordered)-1)
    lo, hi = math.floor(i), math.ceil(i)
    return ordered[lo]+(i-lo)*(ordered[hi]-ordered[lo])


def analyze_form(item_ids, rows, *, bootstrap=1000, seed=20261124):
    """One row per distinct participant for a single form (0/1/None per item).
    
    Item difficulty uses available responses; corrected item-total and KR-20
    use complete rows to keep the denominator and test length consistent.
    No imputation or automatic item deletion. Bootstrap resamples participants.
    """
    ids = tuple(item_ids)
    if len(ids) < 2 or len(set(ids)) != len(ids):
        raise ValueError("Need distinct item IDs")
    if type(bootstrap) is not int or bootstrap < 0:
        raise ValueError("Invalid bootstrap count")
    matrix = []
    for row in rows:
        if set(row)-set(ids):
            raise ValueError("Unknown item")
        vals = [row.get(i) for i in ids]
        if any(v is not None and (type(v) is not int or v not in (0,1)) for v in vals):
            raise ValueError("Expected binary scores or None")
        matrix.append(vals)
    complete = [r for r in matrix if None not in r]
    total = [sum(r) for r in complete]
    stats = {}
    for j, iid in enumerate(ids):
        observed = [r[j] for r in matrix if r[j] is not None]
        n = len(observed)
        p = mean(observed) if n else None
        rit = _correlation([r[j] for r in complete], [t-r[j] for t,r in zip(total,complete)])
        flags = []
        if p is not None and not 0.25 <= p <= 0.90:
            flags.append("review_difficulty")
        if rit is not None and rit <= 0:
            flags.append("review_discrimination")
        if rit is None:
            flags.append("discrimination_undefined")
        stats[iid] = {"n":n,"missing":len(matrix)-n,"p_correct":p,
                      "wilson_95":wilson(sum(observed),n),"corrected_item_total":rit,
                      "n_discrimination":len(complete),"flags":flags}
    reliability = _kr20(complete)
    draws = []
    rng = random.Random(seed)
    if reliability is not None:
        for _ in range(bootstrap):
            val = _kr20(rng.choices(complete,k=len(complete)))
            if val is not None:
                draws.append(val)
    # Fail closed when too many replicates are degenerate.
    ci = [_percentile(draws,.025),_percentile(draws,.975)] if len(draws)>=100 and len(draws)>=.9*bootstrap else None
    return {"n_rows":len(matrix),"n_complete":len(complete),"items":stats,
            "kr20":reliability,"kr20_bootstrap_95":ci,"bootstrap_valid":len(draws),
            "bootstrap_requested":bootstrap,"seed":seed,
            "floor_complete":sum(t==0 for t in total)/len(total) if total else None,
            "ceiling_complete":sum(t==len(ids) for t in total)/len(total) if total else None}


def compare_forms(rows):
    """Descriptive within-person comparisons of A/B/C scores in a pilot.

    Each row has unique participant_id, sequence (one permutation of ABC),
    and scores A/B/C in [0,1] or None. Pair differences use matched people;
    report order strata separately. This does not test measurement equivalence.
    """
    rows = list(rows)
    sequences = ["".join(s) for s in itertools.permutations("ABC")]
    counts = dict.fromkeys(sequences,0)
    seen = set()
    for row in rows:
        pid, seq = row["participant_id"],row["sequence"]
        if not isinstance(pid,str) or not pid or pid in seen or seq not in counts:
            raise ValueError("Invalid participant or sequence")
        seen.add(pid)
        counts[seq] += 1
        for f in "ABC":
            v = row.get(f)
            if v is not None and (type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1):
                raise ValueError("Invalid form score")
    def describe(data,a,b):
        pairs = [(r[a],r[b]) for r in data if r.get(a) is not None and r.get(b) is not None]
        diffs = [x-y for x,y in pairs]
        return {"n":len(diffs),"mean_difference":mean(diffs) if diffs else None,
                "sd_difference":stdev(diffs) if len(diffs)>=2 else None,
                "correlation":_correlation([x for x,y in pairs],[y for x,y in pairs])}
    pairs = {}
    for a,b in itertools.combinations("ABC",2):
        pairs[a+b] = {"overall":describe(rows,a,b),
                      "by_sequence":{s:describe([r for r in rows if r["sequence"]==s],a,b) for s in sequences}}
    return {"n":len(rows),"sequence_counts":counts,"pairs":pairs,
            "status":"DESCRIPTIVE_NOT_EQUIVALENCE_TEST"}


def sample_size(d, rho, *, power=.8, alpha=.05, attrition=.15):
    """Balanced ANCOVA normal approximation, d on marginal posttest SD scale.

    Assumes common slope, residual variance 1-rho**2, equal allocation and
    noninformative attrition. Rounds per arm up twice. Not final sample size.
    """
    if not (math.isfinite(d) and d>0 and 0<=rho<1 and .5<power<1 and 0<alpha<1 and 0<=attrition<1):
        raise ValueError("Invalid planning assumptions")
    n = math.ceil(2*(Z.inv_cdf(1-alpha/2)+Z.inv_cdf(power))**2*(1-rho*rho)/d**2)
    recruit = math.ceil(n/(1-attrition))
    return {"analyzable_per_arm":n,"recruit_per_arm":recruit,"recruit_total":2*recruit}


def simulate_ancova(n, d, rho, *, repetitions=2000, alpha=.05, seed=20261124):
    """Monte Carlo of Gaussian posttest ANCOVA with observed pretest.

    n complete cases per arm. Common slope and normal critical value;
    no missingness, bounds, item effects or estimated pilot parameters.
    Returns rejection fraction and Monte Carlo standard error.
    """
    if type(n) is not int or n<3 or type(repetitions) is not int or repetitions<1:
        raise ValueError("Invalid simulation size")
    if not (math.isfinite(d) and 0<=rho<1 and 0<alpha<1):
        raise ValueError("Invalid simulation assumptions")
    rng = random.Random(seed)
    residual_sd = math.sqrt(1-rho*rho)
    critical = Z.inv_cdf(1-alpha/2)
    rejected = 0
    for _ in range(repetitions):
        groups = []
        for arm in (0,1):
            x = [rng.gauss(0,1) for _ in range(n)]
            y = [d*arm+rho*v+residual_sd*rng.gauss(0,1) for v in x]
            mx,my = mean(x),mean(y)
            groups.append((mx,my,[v-mx for v in x],[v-my for v in y]))
        sxx = sum(v*v for _,_,x,_ in groups for v in x)
        slope = sum(a*b for _,_,x,y in groups for a,b in zip(x,y))/sxx
        delta_x = groups[1][0]-groups[0][0]
        effect = groups[1][1]-groups[0][1]-slope*delta_x
        mse = sum((b-slope*a)**2 for _,_,x,y in groups for a,b in zip(x,y))/(2*n-3)
        se = math.sqrt(mse*(2/n+delta_x**2/sxx))
        rejected += abs(effect/se)>critical
    rate = rejected/repetitions
    return {"rejection_rate":rate,"mc_se":math.sqrt(rate*(1-rate)/repetitions),
            "repetitions":repetitions,"seed":seed,"status":"SYNTHETIC_PLANNING_ONLY"}
