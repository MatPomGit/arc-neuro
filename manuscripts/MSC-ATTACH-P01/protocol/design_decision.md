> Historical design record. The N=84 decision below was calibrated with the broader adjacent-lag definition. The current confirmatory analysis excludes prompt 1 -> 2, so final N is reopened only for the focused comparable-lag recalibration in `h1_comparable_lag_recalibration_plan.md`.

# H1 pilot design decision

## Status

The full exact-design Monte Carlo is complete.

Locked analysis target:

- 84 couples.

The completed grid contained 120,000 replications across 50, 60, 72, and 84 couples, compliance targets 0.65/0.75/0.85, two missingness-strength conditions, and M0-M4 truths.

## Locked design elements

- 84-couple analysis target;
- planning compliance target approximately 0.75 or higher;
- 14 consecutive days;
- 6 synchronized semi-random prompts per day;
- 84 planned prompts per participant;
- days 1-11 for model fitting and feature construction;
- days 12-14 as untouched temporal holdout;
- at least 100 people with at least 30 valid same-day lag pairs for confirmatory interpretation;
- Gaussian GEE, identity link, couple-level clustering, independence working correlation, bias-reduced sandwich covariance, statsmodels 0.15.0;
- two co-primary one-sided coefficient tests of H0: beta <= delta_beta with Holm family-wise alpha 0.05;
- delta_beta = 0.5;
- signed-discrepancy symmetry tolerance delta_sym = 1.0;
- M4 d_asym retained as secondary descriptive structural evidence without a confirmatory tolerance;
- participant RMSE as secondary predictive evidence.

## Why N=84

At nominal 75% compliance, N=84 was the smallest tested candidate that was robust to the current data-sufficiency criterion under the informative-missingness stress condition. N=72 remained materially vulnerable to data insufficiency in that condition.

At compliance near 65%, even N=84 was not robust under the current 100-person/30-lag rule. The study therefore requires active compliance management and should not treat 65% completion as an acceptable planning target.

## Recruitment ceiling

The exact-design simulation calibrated prompt compliance and lag availability, not couple-level attrition before or during the study. Therefore it supports an analysis target of 84 couples but does not by itself determine how many couples must be enrolled to obtain 84 analyzable couples.

A recruitment ceiling must be set separately before recruitment using an explicit retention assumption. No extension may depend on observed H1 effects, p values, model ranking, or holdout prediction.

## Inferential consequence of the Monte Carlo

The earlier M1-first sequential RMSE hierarchy is rejected as the primary decision rule. It produced false simplification under true M2-M4 data-generating processes despite good parameter recovery.

The final primary architecture is coefficient-first:

- H1-P1: M2 beta_r_star;
- H1-P2: M3 beta_e;
- Holm multiplicity control;
- SESOI requirement;
- structural M2/M4 contrasts reported separately;
- RMSE reported as secondary predictive evidence.

See:

- exact_design_config.json;
- h1_exact_design_results_report.md;
- analysis_plan.md;
- preregistration.md;
- decision_margins.md.
