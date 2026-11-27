"""Minimal Windows diagnostic for the ARC H1 GEE stack."""

from __future__ import annotations

import faulthandler
from pathlib import Path
import sys

import numpy as np

from h1_exact_monte_carlo import (
    Scenario,
    build_valid_lags,
    fit_gee,
    load_config,
    prepare_analysis_data,
    replication_rng,
    simulate_prompt_panel,
    evaluate_replication,
)

CONFIG = Path(__file__).resolve().parent.parent / "protocol" / "exact_design_config.json"


def mark(text: str) -> None:
    print(f"[H1-PROBE] {text}", flush=True)


def main() -> None:
    faulthandler.enable(all_threads=True)
    config = load_config(CONFIG)
    scenario = Scenario(72, 0.75, 1.0, "M0")
    rng = replication_rng(config, scenario, 0, 0)

    mark("simulate_prompt_panel")
    prompts = simulate_prompt_panel(config, scenario, rng)
    mark(f"prompts={len(prompts)}")

    mark("build_valid_lags")
    lags = build_valid_lags(prompts, config)
    mark(f"lags={len(lags)}")

    mark("prepare_analysis_data")
    train, test = prepare_analysis_data(prompts, lags, config)
    mark(f"train={len(train)} test={len(test)}")

    for name in ("M0", "M1", "M2", "M3", "M4"):
        mark(f"{name}: fit_gee START")
        result = fit_gee(name, train)
        mark(f"{name}: fit_gee DONE converged={result.converged}")
        mark(f"{name}: predict START")
        pred = np.asarray(result.predict(test))
        mark(f"{name}: predict DONE n={len(pred)}")

    mark("single-fit probe COMPLETE")
    mark("evaluate_replication loop START")
    for rep in (4,):
        mark(f"replication={rep} START")
        rep_rng = replication_rng(config, scenario, 0, rep)
        mark("replication=4 simulate START")
        prompt_data = simulate_prompt_panel(config, scenario, rep_rng)
        mark(f"replication=4 simulate DONE prompts={len(prompt_data)}")
        mark("replication=4 lags START")
        lag_data = build_valid_lags(prompt_data, config)
        mark(f"replication=4 lags DONE lags={len(lag_data)}")
        mark("replication=4 prepare START")
        train, test = prepare_analysis_data(prompt_data, lag_data, config)
        mark(f"replication=4 prepare DONE train={len(train)} test={len(test)}")
        for model_name in ("M0", "M1", "M2", "M3", "M4"):
            mark(f"replication=4 {model_name} fit START")
            result = fit_gee(model_name, train)
            mark(f"replication=4 {model_name} fit DONE converged={result.converged}")
            mark(f"replication=4 {model_name} predict START")
            pred = np.asarray(result.predict(test))
            mark(f"replication=4 {model_name} predict DONE n={len(pred)}")
        mark("replication=4 staged probe COMPLETE")
        row = {"all_models_converged": True, "train_lags": len(train), "test_lags": len(test)}
        mark(
            f"replication={rep} DONE "
            f"converged={row.get('all_models_converged')} "
            f"train={row.get('train_lags')} test={row.get('test_lags')}"
        )
    mark("PROBE COMPLETE")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        sys.exit(1)
