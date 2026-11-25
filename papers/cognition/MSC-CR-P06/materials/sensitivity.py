"""Synthetic bounded-outcome Monte Carlo; no study data or observed effects."""
from __future__ import annotations
import argparse
import json
import math
import random
from statistics import mean, stdev
from analysis import SEQUENCES, fit_endpoint, rubin
from imputation import generate_imputations

MECHANISMS=("MCAR","MAR","MNAR")


def logistic(x):
    return 1/(1+math.exp(-x))


def generate(n_per_arm, effect, dropout, mechanism, seed, *, missing_scope="accuracy"):
    """24-item scores; balanced randomization cells, known additive risk effect.
    
    The accuracy scope masks only accuracy_T1; session scope also masks
    brier_T1 and justification_T1. All auxiliary scores are synthetic.
    dropout is the reference probability, not a fixed realized fraction.
    """
    if type(n_per_arm) is not int or n_per_arm<24 or n_per_arm%12:
        raise ValueError("n_per_arm must be a multiple of 12, at least 24")
    if mechanism not in MECHANISMS or not 0<=dropout<1 or not -.10<=effect<=.10:
        raise ValueError("Invalid simulation scenario")
    if missing_scope not in ("accuracy", "session"):
        raise ValueError("Invalid missing scope")
    rng=random.Random(seed)
    mask_rng=random.Random(seed ^ 0x5A17C0DE)
    full=[]
    masked=[]
    for arm in (0,1):
        for stratum in (0,1):
            for seq in SEQUENCES:
                for _ in range(n_per_arm//12):
                    ability=rng.uniform(.25,.85)
                    baseline=sum(rng.random()<ability for _ in range(24))/24
                    # Bounded for all possible pretest values and allowed effects.
                    p=.23+.48*baseline+.04*stratum+effect*arm
                    post=sum(rng.random()<p for _ in range(24))/24
                    delayed=sum(rng.random()<(.25+.43*baseline+.04*stratum+effect*arm/2) for _ in range(24))/24
                    row=dict(participant_id=f"synthetic-{len(full)}",arm=arm,stratum=stratum,sequence=seq,
                             accuracy_T0=baseline,accuracy_T1=post,accuracy_T2=delayed,
                             brier_T0=.10+.25*(1-baseline)+rng.uniform(0,.08),
                             brier_T1=.12+.20*(1-post)+rng.uniform(0,.12),
                             justification_T0=.3+baseline+rng.uniform(0,.3),
                             justification_T1=.3+post+rng.uniform(0,.3))
                    full.append(row)
                    copy=dict(row)
                    shift=0.
                    if mechanism in ("MAR","MNAR"):
                        shift=2*(.55-baseline)+.5*arm
                    if mechanism=="MNAR":
                        shift+=4*(p-post)
                    probability=logistic(math.log(dropout/(1-dropout))+shift) if dropout else 0.
                    if mask_rng.random()<probability:
                        copy["accuracy_T1"]=None
                        if missing_scope == "session":
                            copy["brier_T1"]=None
                            copy["justification_T1"]=None
                    masked.append(copy)
    return full,masked


def summarize(fits, truth, repetitions):
    n=len(fits)
    if not n:
        return {"successful":0,"failed":repetitions,"bias":None,"rmse":None,
                "coverage":None,"coverage_mcse":None,"rejection_rate":None,
                "rejection_mcse":None,"bias_mcse":None}
    errors=[r["estimate"]-truth for r in fits]
    coverage=mean(r["ci"][0]<=truth<=r["ci"][1] for r in fits)
    rejection=mean(r["p"]<.05 for r in fits)
    return {"successful":n,"failed":repetitions-n,"bias":mean(errors),
            "rmse":math.sqrt(mean(e*e for e in errors)),
            "coverage":coverage,"coverage_mcse":math.sqrt(coverage*(1-coverage)/n),
            "rejection_rate":rejection,"rejection_mcse":math.sqrt(rejection*(1-rejection)/n),
            "bias_mcse":stdev(errors)/math.sqrt(n) if n>1 else None}


def simulate(*, n_per_arm=144,effect=.08,dropout=.15,mechanism="MAR",
             repetitions=200,m=50,iterations=20,seed=20261124,missing_scope="accuracy"):
    """Full-data oracle, complete case, PMM and adverse delta scenarios.
    
    Failures are counted per method and not replaced. Coverage and rejection
    are conditional on successful fits; compare failure counts separately.
    """
    if type(repetitions) is not int or repetitions<1:
        raise ValueError("Invalid repetitions")
    if type(m) is not int or m<2 or type(iterations) is not int or iterations<1:
        raise ValueError("Invalid imputation settings")
    rng=random.Random(seed)
    imputation_rng=random.Random(seed ^ 0x1A2B3C4D)
    labels=("full","complete_case","pmm","pmm_delta_intervention","pmm_delta_control",
            "pmm_delta10_intervention","pmm_delta10_control")
    estimates={k:[] for k in labels}
    failure_reasons={k:{} for k in labels}
    missing=[]
    for _ in range(repetitions):
        full,masked=generate(n_per_arm,effect,dropout,mechanism,rng.getrandbits(64),missing_scope=missing_scope)
        missing.append(mean(r["accuracy_T1"] is None for r in masked))
        def attempt(label,fn):
            try:
                estimates[label].append(fn())
            except (ValueError,ArithmeticError) as exc:
                msg=str(exc)
                failure_reasons[label][msg]=failure_reasons[label].get(msg,0)+1
        attempt("full",lambda:fit_endpoint(full,"H1"))
        attempt("complete_case",lambda:fit_endpoint(masked,"H1"))
        imputation_seed=imputation_rng.getrandbits(64)
        try:
            datasets=generate_imputations(masked,m=m,iterations=iterations,
                                            seed=imputation_seed)["datasets"]
        except (ValueError,ArithmeticError) as exc:
            for k in labels[2:]:
                msg=str(exc)
                failure_reasons[k][msg]=failure_reasons[k].get(msg,0)+1
            continue
        def pool(shift_arm, delta=.05):
            results=[]
            for ds in datasets:
                adjusted=[dict(r) for r in ds]
                if shift_arm is not None:
                    for old,new in zip(masked,adjusted):
                        if old["accuracy_T1"] is None and old["arm"]==shift_arm:
                            new["accuracy_T1"]=max(0.,new["accuracy_T1"]-delta)
                results.append(fit_endpoint(adjusted,"H1",complete_case=False))
            return rubin(results)
        attempt("pmm",lambda:pool(None))
        attempt("pmm_delta_intervention",lambda:pool(1))
        attempt("pmm_delta_control",lambda:pool(0))
        attempt("pmm_delta10_intervention",lambda:pool(1,.10))
        attempt("pmm_delta10_control",lambda:pool(0,.10))
    return {"source":"SYNTHETIC_MONTE_CARLO_ONLY","truth_pp":100*effect,
            "settings":dict(n_per_arm=n_per_arm,effect=effect,dropout=dropout,
                            mechanism=mechanism,repetitions=repetitions,m=m,
                            iterations=iterations,seed=seed,missing_scope=missing_scope),
            "realized_missing_fraction":mean(missing),
            "methods":{k:{**summarize(v,100*effect,repetitions),"failure_reasons":failure_reasons[k]}
                       for k,v in estimates.items()}}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mechanism",choices=MECHANISMS,default="MAR")
    parser.add_argument("--n-per-arm",type=int,default=144)
    parser.add_argument("--effect",type=float,default=.08)
    parser.add_argument("--dropout",type=float,default=.15)
    parser.add_argument("--repetitions",type=int,default=200)
    parser.add_argument("--m",type=int,default=50)
    parser.add_argument("--iterations",type=int,default=20)
    parser.add_argument("--seed",type=int,default=20261124)
    parser.add_argument("--missing-scope",choices=("accuracy","session"),default="accuracy")
    print(json.dumps(simulate(**vars(parser.parse_args())),indent=2,allow_nan=False))
