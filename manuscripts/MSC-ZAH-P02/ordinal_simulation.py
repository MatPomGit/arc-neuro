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
    output=Path(output)
    if output.exists():
        raise FileExistsError(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(seed)
    rows=[]
    for scenario in scenarios:
        valid=hits=0
        for _ in range(reps):
            y,X,groups,indices=generate(rng,n,k,scenario)
            try:
                draws=fit(y,X,groups,int(rng.integers(1,2**30)))
            except (ValueError, FloatingPointError, np.linalg.LinAlgError, pm.exceptions.SamplingError) as exc:
                print(f"Fit failed: {type(exc).__name__}: {exc}", flush=True)
                continue
            if draws is None:
                continue
            valid+=1
            # Bonferroni posterior intervals; frequentist calibration required.
            lo,hi=np.quantile(draws[:,indices],[.025/len(indices),1-.025/len(indices)],axis=0)
            hits+=int(np.any((lo>0)|(hi<0)))
        rate=hits/valid if valid else float("nan")
        rows.append(dict(scenario=scenario,n=n,clips=k,reps=reps,valid=valid,rejected=hits,rate=rate,mcse=np.sqrt(rate*(1-rate)/valid) if valid else float("nan"),lower=hits/reps,upper=(hits+reps-valid)/reps))
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
    person=np.repeat(np.arange(n),16)
    a=np.tile(np.repeat(np.arange(4),4),n)
    b=np.tile(np.arange(4),4*n)
    source=np.concatenate([rng.choice(max(k,16),16,replace=False) for _ in range(n)])
    avatar=rng.integers(0,8,len(a))
    A=np.eye(4)[a,1:]; B=np.eye(4)[b,1:]
    X=np.column_stack([A,B,(A[:,:,None]*B[:,None,:]).reshape(-1,9)])
    u=(a-1.5)/1.5; v=(b-1.5)/1.5
    mu={"null":np.zeros(len(a)),"additive":.5*(u+v),"interaction":.5*u*v,"peak":.5*np.exp(-((u-1/3)**2+(v+1/3)**2)/.2)}[scenario]
    eta=mu+rng.normal(0,.7,n)[person]+rng.normal(0,.5,max(k,16))[source]+rng.normal(0,.4,8)[avatar]+rng.logistic(size=len(a))
    return np.digitize(eta,[-1.5,-.5,.5,1.5]),X,dict(person=person,source=source,avatar=avatar),list(range(6,15))

if __name__=="__main__":
    cli(["null","additive","interaction","peak"],generate,"results/ordinal_power.csv")
