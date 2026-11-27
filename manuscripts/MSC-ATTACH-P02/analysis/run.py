# SPDX-License-Identifier: Apache-2.0
"""Command-line runner for one ARC simulation."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from arc_model import ARCConfig, ARCTraits, impulse, simulate

HERE = Path(__file__).resolve().parent


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run one ARC attachment simulation.")
    for name, default in {
        "L": 0.20,
        "U": 0.20,
        "C": 0.30,
        "S": 0.80,
        "M": 0.80,
        "F": 0.80,
    }.items():
        p.add_argument(f"--{name}", type=float, default=default)
    p.add_argument("--steps", type=int, default=200)
    p.add_argument("--responsiveness", type=float, default=0.80)
    p.add_argument("--controller-mode", choices=("p", "pi", "pid"), default="pid")
    p.add_argument("--shock-step", type=int, default=60)
    p.add_argument("--shock", type=float, default=-0.30)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--csv", type=Path, default=HERE.parents[2] / "build/MSC-ATTACH-P02/experiments/trajectory.csv")
    return p


def main() -> None:
    args = parser().parse_args()
    traits = ARCTraits(
        L=args.L,
        U=args.U,
        C=args.C,
        S=args.S,
        M=args.M,
        F=args.F,
    )
    config = ARCConfig(
        steps=args.steps,
        responsiveness=args.responsiveness,
        controller_mode=args.controller_mode,
    )
    perturbation = impulse(config, args.shock_step, args.shock)
    result = simulate(
        traits=traits,
        config=config,
        perturbation=perturbation,
        seed=args.seed,
    )
    result.to_csv(args.csv)

    print(
        json.dumps(
            {
                "traits": asdict(traits),
                "controller_mode": config.controller_mode,
                "gains": asdict(result.gains),
                "target_state_initial": float(result.target_state[0]),
                "regime": result.regime,
                "metrics": result.metrics,
                "trajectory_csv": str(args.csv),
            },
            indent=2,
            allow_nan=True,
        )
    )


if __name__ == "__main__":
    main()
