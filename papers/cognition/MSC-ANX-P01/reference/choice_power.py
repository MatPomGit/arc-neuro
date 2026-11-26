"""Prospective paired H2/H3 power and calibration using the reference GLMM.

No observed data. Failed fits are counted, never silently replaced or dropped
from unconditional rejection probabilities.
"""
import argparse
from dataclasses import asdict, dataclass
import json
import math
from collections import Counter
import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import norm
from statsmodels.stats.multitest import multipletests
from mixed_models import logistic_ri


@dataclass(frozen=True)
class Scenario:
    recruited: int = 444
    repeats: int = 4
    beta_risk: float = -.15
    beta_ambiguity: float = -.20
    sd_risk: float = .65
    sd_ambiguity: float = .65
    rho: float = .4
    attrition: float = .2
    trial_missing: float = .02
    alpha: float = .05

    def validate(self):
        if type(self.recruited) is not int or self.recruited < 30:
            raise ValueError("recruited must be >=30")
        if type(self.repeats) is not int or self.repeats < 1:
            raise ValueError("repeats must be positive")
        if not all(math.isfinite(v) for v in asdict(self).values()):
            raise ValueError("nonfinite scenario")
        if not (0 < self.sd_risk <= 2 and 0 < self.sd_ambiguity <= 2 and
                -1 <= self.rho <= 1 and 0 <= self.attrition < 1 and
                0 <= self.trial_missing < 1 and 0 < self.alpha < 1):
            raise ValueError("invalid scenario probabilities or random effects")
        return self


def generate(s, rng):
    """Same participant covariates and correlated latent intercepts in both tasks."""
    s.validate()
    n = s.recruited
    gad = np.clip(np.rint(rng.normal(7, 5, n)), 0, 21)
    dep = np.clip(np.rint(.6*gad+rng.normal(3,3,n)),0,27)
    age = rng.integers(18,71,n)
    sleep = np.clip(rng.normal(7,1,n),2,12)
    order = rng.permutation(np.arange(n)%2)
    os = rng.binomial(1,.35,n)
    browser = rng.binomial(1,.4,n)
    u = rng.normal(size=(n,2))
    u[:,1] = s.rho*u[:,0]+np.sqrt(1-s.rho**2)*u[:,1]
    u *= [s.sd_risk,s.sd_ambiguity]
    retained = np.flatnonzero(rng.random(n)>=s.attrition)
    # Twelve unique factorial cells; default 4 repetitions yields 48 trials/task.
    d = np.repeat(np.repeat([-2.,0.,2.],4),s.repeats)
    level = np.repeat(np.tile(np.arange(4),3),s.repeats)
    t = len(d)
    ids = np.repeat(retained,t)
    shared = dict(intercept=np.ones(len(ids)),gad5=gad[ids]/5,
                  age_years=age[ids],sleep_hours=sleep[ids],
                  depression_total=dep[ids],task_order=order[ids],
                  os_family=os[ids],browser_family=browser[ids])
    results = {}
    for j,task in enumerate(("risk","ambiguity")):
        x = pd.DataFrame(shared)
        x["contrast"] = np.tile(d,len(retained))
        x["level"] = np.tile((level+3)**2-4 if j==0 else .2*(level+1),len(retained))
        beta = (s.beta_risk,s.beta_ambiguity)[j]
        eta = (-.1 + beta*x["gad5"]+.15*x["contrast"]
               +(-.02 if j==0 else -.5)*x["level"]
               +.005*(x["age_years"]-40)+.04*(x["sleep_hours"]-7)
               -.015*(x["depression_total"]-7)+.08*x["task_order"]
               +.05*x["os_family"]-.05*x["browser_family"]+u[ids,j])
        y = rng.binomial(1,expit(eta))
        valid = rng.random(len(ids))>=s.trial_missing
        xx = x.loc[valid].reset_index(drop=True)
        for k in ("age_years","sleep_hours","depression_total","task_order","os_family","browser_family"):
            if xx[k].nunique()<=1:
                xx=xx.drop(columns=k)
        results[task]=(y[valid],xx,ids[valid])
    return len(retained),results


def interval(k,n):
    """Wilson 95% Monte Carlo interval on a binomial probability."""
    if not n:
        return None
    z=norm.ppf(.975)
    p=k/n
    center=(p+z*z/(2*n))/(1+z*z/n)
    width=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return dict(count=k,denominator=n,rate=p,mc_ci95=[max(0.,center-width),min(1.,center+width)])


def simulate(s, repetitions, seed, *, fitter=logistic_ri):
    s.validate()
    if type(repetitions) is not int or repetitions<1 or type(seed) is not int or seed<0:
        raise ValueError("invalid repetitions or seed")
    rng=np.random.default_rng(seed)
    tasks=("risk","ambiguity")
    truth=dict(zip(tasks,(s.beta_risk,s.beta_ambiguity)))
    nulls=[t for t in tasks if truth[t]==0]
    alternatives=[t for t in tasks if truth[t]!=0]
    metrics={t:Counter() for t in tasks}
    estimates={t:[] for t in tasks}
    failures={t:Counter() for t in tasks}
    family=Counter()
    n_complete=[]
    for _ in range(repetitions):
        retained, data=generate(s,rng)
        n_complete.append(retained)
        pvalues=[]
        success={}
        for t in tasks:
            try:
                y,x,groups=data[t]
                e=fitter(y,x,groups,"gad5")["gad_effect"]
                if not (math.isfinite(e["p"]) and 0<=e["p"]<=1 and
                        math.isfinite(e["estimate"]) and all(map(math.isfinite,e["ci95"]))):
                    raise ValueError("invalid inference")
                success[t]=e
                metrics[t]["fit"]+=1
                estimates[t].append(e["estimate"])
                metrics[t]["covered"]+=e["ci95"][0]<=truth[t]<=e["ci95"][1]
                metrics[t]["raw_reject"]+=e["p"]<=s.alpha
                pvalues.append(e["p"])
            except (ValueError,np.linalg.LinAlgError,FloatingPointError) as exc:
                failures[t][str(exc)]+=1
                pvalues.append(1.)
        # Keep the prespecified family size even when one fit fails.
        adjusted=multipletests(pvalues,alpha=s.alpha,method="holm")[1]
        rejected={t for t,p in zip(tasks,adjusted) if t in success and p<=s.alpha}
        correct={t for t in rejected if truth[t]!=0 and success[t]["estimate"]*truth[t]>0}
        for t in tasks:
            metrics[t]["holm_reject"]+=t in rejected
            metrics[t]["directional_reject"]+=t in correct
        family["both_fit"]+=len(success)==2
        family["any_false_positive"]+=any(t in rejected for t in nulls)
        family["any_directional"]+=bool(correct)
        family["all_directional"]+=bool(alternatives) and set(alternatives)<=correct
    out={}
    for t in tasks:
        m=metrics[t]
        out[t]=dict(truth=truth[t],fit=interval(m["fit"],repetitions),
                    raw_reject=interval(m["raw_reject"],repetitions),
                    holm_reject=interval(m["holm_reject"],repetitions),
                    directional_power=interval(m["directional_reject"],repetitions) if truth[t]!=0 else None,
                    coverage_given_fit=interval(m["covered"],m["fit"]),
                    unconditional_coverage=interval(m["covered"],repetitions),
                    bias_given_fit=float(np.mean(estimates[t])-truth[t]) if estimates[t] else None,
                    failures=dict(failures[t]))
    return dict(data_origin="synthetic",scenario=asdict(s),repetitions=repetitions,seed=seed,
                mean_retained=float(np.mean(n_complete)),tasks=out,
                both_fit=interval(family["both_fit"],repetitions),
                fwer=interval(family["any_false_positive"],repetitions) if nulls else None,
                any_directional_power=interval(family["any_directional"],repetitions) if alternatives else None,
                all_directional_power=interval(family["all_directional"],repetitions) if alternatives else None)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--recruited",type=int,default=444)
    p.add_argument("--repeats",type=int,default=4)
    p.add_argument("--beta-risk",type=float,default=-.15)
    p.add_argument("--beta-ambiguity",type=float,default=-.20)
    p.add_argument("--sd-risk",type=float,default=.65)
    p.add_argument("--sd-ambiguity",type=float,default=.65)
    p.add_argument("--rho",type=float,default=.4)
    p.add_argument("--attrition",type=float,default=.2)
    p.add_argument("--trial-missing",type=float,default=.02)
    p.add_argument("--alpha",type=float,default=.05)
    p.add_argument("--repetitions",type=int,default=100)
    p.add_argument("--seed",type=int,default=42)
    a=vars(p.parse_args())
    repetitions=a.pop("repetitions")
    seed=a.pop("seed")
    print(json.dumps(simulate(Scenario(**a),repetitions,seed),indent=2,allow_nan=False))
