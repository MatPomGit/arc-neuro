"""Synthetic crossed ordinal model; Bayesian interval decision, not a CLMM LRT."""
import argparse
import csv
from pathlib import Path
import numpy as np
import pymc as pm
import arviz as az

def fit(y, X, groups, seed, *, draws=500, tune=500, chains=4, diagnostic=True):
    with pm.Model():
        b=pm.Normal("beta",0,1.5,shape=X.shape[1])
        eta=pm.math.dot(X,b)
        for name, ids in groups.items():
            sd=pm.HalfNormal(name+"_sd",1)
            z=pm.Normal(name+"_z",0,1,shape=int(ids.max())+1)
            eta=eta+sd*z[ids]
        for name in ("observer","source"):
            ids=groups[name]
            sd=pm.HalfNormal(name+"_slope_sd",.5)
            z=pm.Normal(name+"_slope_z",0,1,shape=int(ids.max())+1)
            eta=eta+sd*z[ids]*X[:,1]
        cuts=pm.Normal("cuts",0,2,shape=4,transform=pm.distributions.transforms.ordered,initval=[-1.5,-.5,.5,1.5])
        pm.OrderedLogistic("y",eta=eta,cutpoints=cuts,observed=y)
        trace=pm.sample(draws,tune=tune,chains=chains,cores=1,random_seed=seed,target_accept=.95,progressbar=False)
    if not diagnostic:
        return trace.posterior.beta.values.reshape(-1,X.shape[1])
    summary=az.summary(trace,var_names=["beta","cuts"]+[k+"_sd" for k in groups]+["observer_slope_sd","source_slope_sd"])
    if int(trace.sample_stats.diverging.sum()) or not np.isfinite(summary[["r_hat","ess_bulk","ess_tail"]]).all().all() or summary.r_hat.max()>1.01 or min(summary.ess_bulk.min(),summary.ess_tail.min())<400:
        return None
    return trace.posterior.beta.values.reshape(-1,X.shape[1])


def generate(rng, observers, sources, clips_per_source, effect, measurement_sd=.2):
    if min(observers,sources)<6 or observers%3 or clips_per_source<2 or measurement_sd<0:
        raise ValueError("Require observers divisible by three, at least six observers and sources, and two clips per source")
    k=sources*clips_per_source
    observer=np.repeat(np.arange(observers),k)
    clip=np.tile(np.arange(k),observers)
    source=clip//clips_per_source
    # Each observer sees each clip once; each clip has balanced realism.
    level=(observer+clip)%3
    r=np.array([-.5,0,.5])[level]
    mid=(level==1).astype(float)
    avatar=(observer//3+clip)%4
    context=clip%clips_per_source%2
    true_x=rng.normal(size=sources)[source]+rng.normal(0,.5,k)[clip]
    true_x=(true_x-true_x.mean())/true_x.std()
    measured=true_x+rng.normal(0,measurement_sd,k)[clip]
    measured=(measured-measured.mean())/measured.std()
    X=np.column_stack([measured,r,measured*r,mid,measured*mid,context])
    eta=.3*true_x+.2*r+effect*true_x*r+.2*context
    for ids,sd in [(observer,.7),(source,.5),(clip,.3),(avatar,.4)]:
        eta+=rng.normal(0,sd,int(ids.max())+1)[ids]
    eta+=r*(rng.normal(0,.35,observers)[observer]+rng.normal(0,.25,sources)[source])
    y=np.digitize(eta+rng.logistic(size=len(eta)),[-1.5,-.5,.5,1.5])
    return y,X,dict(observer=observer,source=source,clip=clip,avatar=avatar)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--observers",type=int,default=60)
    p.add_argument("--sources",type=int,default=24)
    p.add_argument("--clips-per-source",type=int,default=2)
    p.add_argument("--measurement-sd",type=float,default=.2)
    p.add_argument("--reps",type=int,default=5)
    p.add_argument("--seed",type=int,default=20261127)
    p.add_argument("--output",type=Path,default=Path("results/pilot.csv"))
    a=p.parse_args()
    if a.reps<1 or a.output.exists():
        p.error("Positive repetitions and new output required")
    rng=np.random.default_rng(a.seed)
    rows=[]
    for effect in (0,.25,.5):
        valid=hits=0
        for _ in range(a.reps):
            y,X,groups=generate(rng,a.observers,a.sources,a.clips_per_source,effect,a.measurement_sd)
            try:
                draws=fit(y,X,groups,int(rng.integers(1,2**30)))
            except (ValueError,FloatingPointError,np.linalg.LinAlgError,pm.exceptions.SamplingError):
                continue
            if draws is None:
                continue
            valid+=1
            lo,hi=np.quantile(draws[:,2],[.025,.975])
            hits+=int(lo>0 or hi<0)
        rate=hits/valid if valid else float("nan")
        rows.append(dict(effect=effect,observers=a.observers,sources=a.sources,clips_per_source=a.clips_per_source,measurement_sd=a.measurement_sd,seed=a.seed,reps=a.reps,valid=valid,hits=hits,rate=rate,mcse=np.sqrt(rate*(1-rate)/valid) if valid else float("nan"),lower=hits/a.reps,upper=(hits+a.reps-valid)/a.reps))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("x",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

if __name__=="__main__":
    main()
