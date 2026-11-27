# H1 comparable-lag recalibration plan

Status: prespecified before rerunning the exact-design Monte Carlo.

## Reason for recalibration

The confirmatory autoregressive lag definition now excludes prompt 1 -> 2 because the source action at prompt 1 summarizes an overnight/first-of-day interval rather than the standardized preceding same-day ESM interval represented by later source prompts. The earlier 120,000-replication calibration therefore cannot be used unchanged to freeze the analysis target.

## Focused simulation grid

The recalibration uses:
- candidate couples: 72, 84, 96, 108, 120;
- compliance: 0.75;
- missingness_strength: 0 and 1;
- truths: M0-M4;
- 1000 deterministic replications per scenario;
- current coefficient-first H1 inference;
- the same 14-day, six-prompt schedule, 1-4 h response-to-response lag window, estimator, SESOI, multiplicity, and missing-data generator as the current protocol.

This is 50 scenarios and 50,000 replications, rather than rerunning the full 150,000-replication factorial grid.

## Prospective sample-size decision rule

The selection condition is compliance = 0.75 and missingness_strength = 1. Select the smallest candidate N satisfying every guardrail. To account for Monte Carlo sampling error, minimum-rate guardrails are evaluated against the lower 95% Wilson bound and maximum-rate guardrails against the upper 95% Wilson bound:

- minimum primary data-sufficiency rate across M0-M4 >= 0.99;
- H1-P1 support rate under M2 >= 0.90;
- H1-P2 support rate under M3 >= 0.90;
- H1-P1 false-positive rate under M0 <= 0.075;
- H1-P2 false-positive rate under M0 <= 0.075.

The missingness_strength = 0 condition is reported as a reference. It cannot rescue a candidate that fails the prespecified stress condition.

If a point estimate meets a threshold but its required Wilson bound does not, that criterion is treated as inconclusive rather than passed. If no candidate satisfies all guardrails, the recruitment target remains unfrozen and the design must be revised prospectively or additional prespecified simulation precision obtained.

## Execution

On the Windows research workstation run:

    software\study_design\H1_RECALIBRATE.bat

The runner:
1. uses the pinned Python 3.12 H1 environment;
2. executes isolated, resumable replications through the existing Windows scheduler;
3. writes results to `studies/pilot_h1/comparable_lag_recalibration/`, separate from historical `exact_results/`;
4. performs the standard strict merge and coefficient-first inference;
5. applies the prospective guardrails with `h1_recalibration_summary.py`;
6. writes `h1_recalibration_guardrails.csv`, `h1_recalibration_decision.json`, and `h1_recalibration_report.md`.

Raw chunks and the large merged replication table stay untracked. Compact decision artifacts can be reviewed and committed after completion.

## Interpretation

The recalibration decides the analysis target only. It does not change the psychological model, the H1 hypotheses, SESOI = 0.5, Holm FWER = 0.05, the GEE estimator, or the descriptive-only status of M4 asymmetry.
