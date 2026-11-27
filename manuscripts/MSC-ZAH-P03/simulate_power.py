"""Synthetic crossed ordinal model; Bayesian interval decision, not a CLMM LRT."""
import argparse
import csv
from pathlib import Path
import numpy as np
import pymc as pm
import arviz as az

def fit(y, X, groups, seed):
    with pm.Model():
        b=pm.Normal("beta",0,1.5,shape=X.shape[1])
        eta=pm.math.dot(X,b)
        for name, ids in groups.items():
            sd=pm.HalfNormal(name+"_sd",1)
            z=pm.Normal(name+"_z",0,1,shape=int(ids.max())+1)
            eta=eta+sd*z[ids]
        cuts=pm.Normal("cuts",0,2,shape=4,transform=pm.distributions.transforms.ordered,initval=[-1.5,-.5,.5,1.5])
        pm.OrderedLogistic("y",eta=eta,cutpoints=cuts,observed=y)
        trace=pm.sample(500,tune=500,chains=4,cores=1,random_seed=seed,target_accept=.95,progressbar=False)
    summary=az.summary(trace,var_names=["beta","cuts"]+[k+"_sd" for k in groups])
    if int(trace.sample_stats.diverging.sum()) or not np.isfinite(summary[["r_hat","ess_bulk","ess_tail"]]).all().all() or summary.r_hat.max()>1.01 or min(summary.ess_bulk.min(),summary.ess_tail.min())<400:
        return None
    return trace.posterior.beta.values.reshape(-1,X.shape[1])

def run(scenarios, generate, n, reps, seed, output, k=24):
    if n<16 or reps<1 or k<8 or k%4:
        raise ValueError("Invalid design")
    rng=np.random.default_rng(seed)
    rows=[]
    for scenario in scenarios:
        valid=hits=0
        for _ in range(reps):
            y,X,groups,indices=generate(rng,n,k,scenario)
            draws=fit(y,X,groups,int(rng.integers(1,2**30)))
            if draws is None:
                continue
            valid+=1
            # Bonferroni posterior intervals; frequentist calibration required.
            lo,hi=np.quantile(draws[:,indices],[.025/len(indices),1-.025/len(indices)],axis=0)
            hits+=int(np.any((lo>0)|(hi<0)))
        rate=hits/valid if valid else float("nan")
        rows.append(dict(scenario=scenario,n=n,clips=k,reps=reps,valid=valid,rejected=hits,rate=rate,mcse=np.sqrt(rate*(1-rate)/valid) if valid else float("nan"),lower=hits/reps,upper=(hits+reps-valid)/reps))
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("x",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def cli(scenarios,generate,default):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n",type=int,default=80)
    p.add_argument("--clips",type=int,default=24)
    p.add_argument("--reps",type=int,default=100)
    p.add_argument("--seed",type=int,default=20261127)
    p.add_argument("--output",default=default)
    a=p.parse_args()
    run(scenarios,generate,a.n,a.reps,a.seed,a.output,a.clips)

def generate(rng,n,k,scenario):
    person=np.repeat(np.arange(n),k)
    clip=np.tile(np.arange(k),n)
    direction=(clip>=k//2).astype(int)
    violation=(clip+person)%2
    avatar=clip%4
    X=np.column_stack([direction,violation,direction*violation])
    eta=.3*direction+.3*violation+scenario*direction*violation+rng.normal(0,.7,n)[person]+rng.normal(0,.5,k)[clip]+rng.normal(0,.4,4)[avatar]+rng.logistic(size=len(clip))
    keep=rng.random(len(clip))>=.05
    return np.digitize(eta[keep],[-1.5,-.5,.5,1.5]),X[keep],dict(person=person[keep],clip=clip[keep],avatar=avatar[keep]),[2]

if __name__=="__main__":
    cli([0,.25,.5,.75],generate,"results/ordinal_power.csv")
