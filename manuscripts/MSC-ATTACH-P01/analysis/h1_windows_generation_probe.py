"""Isolate repeated H1 data generation from statsmodels/GEE."""

from __future__ import annotations

import faulthandler
from pathlib import Path

from h1_exact_monte_carlo import (
    Scenario,
    build_valid_lags,
    load_config,
    prepare_analysis_data,
    replication_rng,
    simulate_prompt_panel,
)

CONFIG = Path(__file__).resolve().parent.parent / "protocol" / "exact_design_config.json"


def main() -> None:
    faulthandler.enable(all_threads=True)
    config = load_config(CONFIG)
    scenario = Scenario(72, 0.75, 1.0, "M0")
    for rep in range(100):
        print(f"[GEN-PROBE] replication={rep} START", flush=True)
        rng = replication_rng(config, scenario, 0, rep)
        prompts = simulate_prompt_panel(config, scenario, rng)
        lags = build_valid_lags(prompts, config)
        train, test = prepare_analysis_data(prompts, lags, config)
        print(
            f"[GEN-PROBE] replication={rep} DONE "
            f"prompts={len(prompts)} lags={len(lags)} "
            f"train={len(train)} test={len(test)}",
            flush=True,
        )
    print("[GEN-PROBE] COMPLETE", flush=True)


if __name__ == "__main__":
    main()
