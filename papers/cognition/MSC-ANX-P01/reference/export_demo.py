"""Write a local demonstration schedule; no participant data or network."""
import argparse
import json
from pathlib import Path
from design import manifest

def demo_manifest(seed):
    if type(seed) is not int or not 0 <= seed <= 2**53-1:
        raise ValueError("seed must be a nonnegative JavaScript-safe integer")
    main = manifest(seed)
    practice = []
    for attempt in (1, 2):
        practice_seed = (seed + 16 * attempt) % 2**53
        rows = manifest(practice_seed)["switching"][48:72]
        practice.append([dict(row, practice=True, practice_attempt=attempt) for row in rows])
    return dict(main, mode="local-demo", demo_version="0.2.0", practice=practice,
                timing=dict(cue_ms=300, response_ms=2000, iti_ms=500))

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    parser.add_argument("--seed",type=int,default=42)
    a=parser.parse_args()
    with a.output.open("x",encoding="utf-8") as f:
        json.dump(demo_manifest(a.seed),f,ensure_ascii=False,indent=2,allow_nan=False)
        f.write("\n")
