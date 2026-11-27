# SPDX-License-Identifier: Apache-2.0
"""Summarize the configured synthetic parameter-recovery experiment.

The summary is descriptive across generated trajectories, not an estimate of
uncertainty or evidence about human behavior.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from statistics import mean, median


MODELS = {
    "context": "behavior_context_rmse",
    "previous_action": "behavior_ar_rmse",
    "P": "behavior_p_rmse",
    "PI": "behavior_pi_rmse",
    "PID": "behavior_pid_rmse",
}


def summarize(csv_path: Path, config_path: Path) -> dict:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("No trajectories in recovery CSV")

    def values(field: str) -> list[float]:
        return [float(row[field]) for row in rows]

    errors = {
        name: [float(row[f"{name}_est"]) - float(row[f"{name}_true"]) for row in rows]
        for name in ("kp", "ki", "kd")
    }
    rmse = {name: values(field) for name, field in MODELS.items()}
    return {
        "config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
        "trajectories": len(rows),
        "oracle_max_test_rmse": max(values("oracle_pid_test_rmse")),
        "oracle_max_absolute_parameter_error": {
            name: max(map(abs, error)) for name, error in errors.items()
        },
        "behavior_mean_test_rmse": {name: mean(v) for name, v in rmse.items()},
        "behavior_median_test_rmse": {name: median(v) for name, v in rmse.items()},
        "pi_better_than_p": sum(a < b for a, b in zip(rmse["PI"], rmse["P"])),
        "pid_better_than_pi": sum(a < b for a, b in zip(rmse["PID"], rmse["PI"])),
        "mean_pi_improvement_over_p": mean(b - a for a, b in zip(rmse["PI"], rmse["P"])),
        "mean_pid_improvement_over_pi": mean(b - a for a, b in zip(rmse["PID"], rmse["PI"])),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    summary = json.dumps(summarize(args.csv, args.config), indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(summary, encoding="utf-8")
    print(summary, end="")


if __name__ == "__main__":
    main()
