import argparse
import subprocess
import sys
from pathlib import Path
from itertools import product

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--reps",type=int,default=100)
    a=p.parse_args()
    if a.reps<1:
        p.error("reps must be positive")
    root=Path(__file__).resolve().parent
    for n,k in product([40,80,120,200],[16,24,40]):
        out=root/"results"/f"power_n{n}_k{k}_b{a.reps}.csv"
        subprocess.run([sys.executable,str(root/"simulate_power.py"),"--n",str(n),"--clips",str(k),"--reps",str(a.reps),"--output",str(out)],check=True,cwd=root)
