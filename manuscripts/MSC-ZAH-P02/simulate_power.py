"""Preliminary balanced continuous-outcome sensitivity analysis; not final ordinal power."""
import argparse
import csv
from pathlib import Path
import numpy as np
from scipy.stats import f

def surface(scenario, effect):
    a, b = np.meshgrid(np.linspace(-1, 1, 4), np.linspace(-1, 1, 4))
    if scenario == "null":
        return np.zeros((4, 4))
    if scenario == "additive":
        return effect * (a + b)
    if scenario == "interaction":
        return effect * a * b
    if scenario == "peak":
        return effect * np.exp(-((a-1/3)**2+(b+1/3)**2)/0.2)
    raise ValueError(scenario)

def interaction(x):
    return x-x.mean(axis=-1, keepdims=True)-x.mean(axis=-2, keepdims=True)+x.mean(axis=(-1,-2), keepdims=True)

def simulate(n, reps, effect, seed, scenario, stimulus_sd, stimuli):
    rng = np.random.default_rng(seed)
    rejected = 0
    for _ in range(reps):
        # Independent stimulus sets per participant: optimistic baseline.
        noise = rng.normal(size=(n,4,4))
        noise += rng.normal(scale=stimulus_sd / np.sqrt(stimuli), size=noise.shape)
        y = interaction(surface(scenario,effect)+noise)
        ss = n*np.sum(y.mean(axis=0)**2)
        err = np.sum((y-y.mean(axis=0))**2)
        statistic = (ss/9)/(err/(9*(n-1)))
        rejected += f.sf(statistic,9,9*(n-1)) < .05
    p = rejected/reps
    return p, np.sqrt(p*(1-p)/reps)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, nargs="+", default=[40,80,120,200])
    parser.add_argument("--reps", type=int, default=1000)
    parser.add_argument("--effect", type=float, default=.3)
    parser.add_argument("--seed", type=int, default=20261127)
    parser.add_argument("--stimulus-sd", type=float, default=.5)
    parser.add_argument("--stimuli", type=int, default=4)
    args = parser.parse_args()
    if min(args.n)<2 or args.reps<1 or args.stimuli<1 or args.stimulus_sd<0 or args.effect<0:
        parser.error("Invalid simulation parameters")
    out = Path(__file__).resolve().parent/"results"
    out.mkdir(exist_ok=True)
    rows=[]
    for i, scenario in enumerate(("null","additive","interaction","peak")):
        for j,n in enumerate(args.n):
            p,se=simulate(n,args.reps,args.effect,args.seed+i*10000+j,scenario,args.stimulus_sd,args.stimuli)
            rows.append((scenario,n,args.reps,args.effect,args.stimulus_sd,args.stimuli,args.seed+i*10000+j,p,se))
    with (out/"preliminary_power.csv").open("w",newline="",encoding="utf-8") as file:
        writer=csv.writer(file)
        writer.writerow(["scenario","n","replications","effect","stimulus_sd","stimuli","seed","rejection_rate","mcse"])
        writer.writerows(rows)
    import matplotlib.pyplot as plt
    for scenario in ("null","additive","interaction","peak"):
        subset=sorted((r for r in rows if r[0]==scenario),key=lambda r:r[1])
        plt.errorbar([r[1] for r in subset],[r[7] for r in subset],yerr=[1.96*r[8] for r in subset],marker="o",label=scenario)
    plt.axhline(.05,linestyle=":",label="alpha")
    plt.axhline(.8,linestyle="--",label="target power")
    plt.xlabel("Participants")
    plt.ylabel("Interaction rejection rate")
    plt.ylim(0,1.05)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out/"preliminary_power.png",dpi=180)
    plt.close()

if __name__=="__main__":
    main()
