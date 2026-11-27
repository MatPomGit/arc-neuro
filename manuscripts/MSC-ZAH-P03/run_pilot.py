"""Run a small synthetic pilot, not a sample-size decision."""
import argparse
from pathlib import Path
from simulate_power import run, generate

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--reps",type=int,default=5)
    p.add_argument("--seed",type=int,default=20261127)
    p.add_argument("--output",type=Path,default=Path(__file__).resolve().parent/"results"/"pilot.csv")
    a=p.parse_args()
    run([0,.5],generate,16,a.reps,a.seed,a.output,k=16)
