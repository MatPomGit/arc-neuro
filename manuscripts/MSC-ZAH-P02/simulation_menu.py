"""Validated interactive launcher for the preliminary sensitivity model."""
import subprocess
import sys
from pathlib import Path

def main():
    try:
        n = [int(x) for x in input("Sample sizes (space separated): ").split()]
        reps = int(input("Replications per configuration: "))
        effect = float(input("Effect magnitude: "))
        sd = float(input("Stimulus SD: "))
        stimuli = int(input("Stimuli per cell: "))
        seed = int(input("Random seed: "))
        import math
        if not n or min(n)<2 or reps<1 or stimuli<1 or seed<0 or not all(math.isfinite(x) and x>=0 for x in (effect,sd)):
            raise ValueError("Invalid parameters")
    except (ValueError, EOFError) as exc:
        print(exc, file=sys.stderr)
        return 2
    print(f"Total replications: {4*len(n)*reps}", flush=True)
    return subprocess.call([sys.executable,str(Path(__file__).with_name("simulate_power.py")),"--n",*map(str,n),"--reps",str(reps),"--effect",str(effect),"--stimulus-sd",str(sd),"--stimuli",str(stimuli),"--seed",str(seed)])
if __name__=="__main__":
    sys.exit(main())
