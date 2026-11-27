"""Trial-level H1 planning simulation using the actual HC3 pipeline.

beta_ms is the generating shift per five observed GAD points, before QA
and truncation; coverage against that nominal shift is diagnostic only.
"""
import argparse
from dataclasses import dataclass,asdict
import json
from collections import Counter
import math
import numpy as np
from design import manifest
from statistical import fit_h1
from choice_power import interval


@dataclass(frozen=True)
class Scenario:
    recruited:int=444
    beta_ms:float=10.
    between_sd:float=35.
    trial_sd:float=90.
    heteroskedasticity:float=.15
    attrition:float=.2
    invalid_probability:float=.03
    error_probability:float=.06
    gad_reliability:float=1.
    alpha:float=.05

    def validate(self):
        if type(self.recruited) is not int or self.recruited<30 or not all(math.isfinite(v) for v in asdict(self).values()):
            raise ValueError("invalid scenario")
        if not (self.between_sd>=0 and self.trial_sd>0 and self.heteroskedasticity>=0 and
                0<=self.attrition<1 and 0<=self.invalid_probability<1 and 0<=self.error_probability<1 and
                0<self.gad_reliability<=1 and 0<self.alpha<1):
            raise ValueError("invalid scenario parameters")
        return self


def generate(s,rng,schedules):
    """Balanced schedule allocation independent of participant characteristics."""
    s.validate()
    order=rng.permutation(np.arange(s.recruited)%len(schedules))
    for i,slot in enumerate(order):
        if rng.random()<s.attrition:
            continue
        m=schedules[slot]
        pid=f"SYN-{i+1:06d}"
        latent=rng.normal()
        measured=np.sqrt(s.gad_reliability)*latent+np.sqrt(1-s.gad_reliability)*rng.normal()
        gad=int(np.clip(np.rint(7+5*measured),0,21))
        dep=int(np.clip(np.rint(.6*gad+rng.normal(3,3)),0,27))
        age=int(rng.integers(18,71))
        sleep=float(np.clip(rng.normal(7,1),2,12))
        os=["A","B"][int(rng.random()<.35)]
        browser=["X","Y"][int(rng.random()<.4)]
        base=600+2*(age-40)-5*(sleep-7)+rng.normal(0,55)
        # When reliability is 1, use observed GAD directly; otherwise a
        # latent proxy drives the shift, and nominal beta is not observed beta.
        exposure=gad/5 if s.gad_reliability==1 else 7/5+latent
        cost=75+s.beta_ms*exposure+1.5*dep+rng.normal(0,s.between_sd*(1+s.heteroskedasticity*gad/5))
        rows=m["switching"]
        noise=rng.normal(0,s.trial_sd*(1+s.heteroskedasticity*gad/5),len(rows))
        invalid=rng.random(len(rows))<s.invalid_probability
        errors=rng.random(len(rows))<s.error_probability
        trials=[]
        for j,t in enumerate(rows):
            rt=float(base+(cost if t["mixed"] and t["transition"]=="switch" else 0)+noise[j])
            timeout=rt>2000
            trials.append(dict(t,participant_id=pid,rt_ms=None if timeout else rt,timeout=timeout,
                               correct=not timeout and not bool(errors[j]),focus_lost=bool(invalid[j]),
                               technical_error=False))
        yield dict(data_origin="synthetic",participant_id=pid,protocol_version=m["protocol_version"],
                   stimulus_version=m["stimulus_version"],seed=m["seed"],task_order=m["task_order"],
                   decision_order=m["decision_order"],gad7_total=gad,depression_total=dep,
                   age_years=age,sleep_hours=sleep,os_family=os,browser_family=browser,switching=trials)


def simulate(s,repetitions=100,seed=42):
    s.validate()
    if type(repetitions) is not int or repetitions<1 or type(seed) is not int or seed<0:
        raise ValueError("invalid simulation parameters")
    rng=np.random.default_rng(seed)
    schedules=[manifest(i) for i in range(32)]
    counts=Counter()
    failures=Counter()
    estimates=[]
    ns=[]
    for _ in range(repetitions):
        rows=list(generate(s,rng,schedules))
        try:
            fit=fit_h1(rows)
        except (ValueError,np.linalg.LinAlgError,FloatingPointError) as exc:
            failures[str(exc)]+=1
            continue
        e=fit["gad5"]
        estimates.append(e["estimate"])
        ns.append(fit["n"])
        counts["fit"]+=1
        counts["reject"]+=e["p"]<=s.alpha
        counts["directional"]+=e["p"]<=s.alpha and e["estimate"]*s.beta_ms>0
        counts["nominal_coverage"]+=e["ci95"][0]<=s.beta_ms<=e["ci95"][1]
    return dict(data_origin="synthetic",scenario=asdict(s),repetitions=repetitions,seed=seed,
                fit=interval(counts["fit"],repetitions),reject=interval(counts["reject"],repetitions),
                directional_power=interval(counts["directional"],repetitions) if s.beta_ms else None,
                nominal_coverage_given_fit=interval(counts["nominal_coverage"],counts["fit"]),
                mean_estimate_given_fit=float(np.mean(estimates)) if estimates else None,
                mean_eligible_given_fit=float(np.mean(ns)) if ns else None,failures=dict(failures),
                note="Nominal shift is not necessarily the post-QA observed estimand.")


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--recruited",type=int,default=444)
    p.add_argument("--beta-ms",type=float,default=10.)
    p.add_argument("--repetitions",type=int,default=100)
    p.add_argument("--seed",type=int,default=42)
    a=p.parse_args()
    print(json.dumps(simulate(Scenario(recruited=a.recruited,beta_ms=a.beta_ms),a.repetitions,a.seed),
                     indent=2,allow_nan=False))
