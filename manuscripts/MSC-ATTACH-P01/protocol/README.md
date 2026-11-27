# ARC H1 pilot

Status: protocol development before preregistration and data collection. The full exact-design Monte Carlo is complete.

## Primary questions

H1 uses two co-primary within-person tests:

- H1-P1: does desired relational closeness contribute to subsequent signed regulation beyond perceived closeness, context, and prior action in M2?
- H1-P2: does signed desired-minus-perceived discrepancy predict subsequent signed regulation in the preregistered direction in M3?

The temporal sequence remains:

r_hat(t), r*(t) -> representation of their relation -> a(t+1).

For confirmatory autoregressive rows, prompt 1 -> 2 is excluded because the source action at the first prompt summarizes a non-comparable overnight/first-of-day interval. Eligible within-day transitions are therefore 2->3, 3->4, 4->5, and 5->6, subject to the locked response-time and technical-validity rules.

Structural characterization then asks whether the M2 coefficients are compatible with the equal-and-opposite signed-discrepancy restriction and whether M4 requires asymmetric positive/negative discrepancy slopes.

## Current planning design

- population: adult cohabiting romantic couples;
- previous calibrated analysis target: 84 couples; this target is now provisional pending Monte Carlo recalibration under the comparable-lag rule that excludes prompt 1 -> 2;
- planning prompt compliance: approximately 0.75 or higher;
- duration: 14 consecutive days;
- schedule: 6 synchronized semi-random prompts per day;
- planned observations: 84 per participant;
- primary coordinate: current closeness, measured as perceived and desired closeness on the same scale;
- primary outcome: signed interpersonal regulatory action, approach intensity minus distancing intensity;
- co-primary inferential family: M2 beta_r_star and M3 beta_e;
- multiplicity: Holm family-wise alpha 0.05;
- coefficient SESOI: delta_beta = 0.5;
- signed-discrepancy symmetry tolerance: delta_sym = 1.0;
- predictive metric: participant RMSE on days 12-14, used as secondary evidence rather than a model-selection gate;
- primary estimator: Gaussian GEE with couple-level clustering and bias-reduced sandwich covariance.

The completed 120,000-replication exact-design Monte Carlo showed that the earlier M1-first RMSE hierarchy produced false simplification under true M2-M4 processes despite good coefficient recovery. That sequential rule is retained only as a historical diagnostic. Because that calibration used the broader adjacent-lag definition, N=84 and the associated data-sufficiency rates must be revalidated before recruitment is frozen under the new comparable-lag rule.

## Files

- protocol.md: study design and operational decisions;
- preregistration.md: confirmatory decisions to lock before recruitment;
- analysis_plan.md: coefficient-first H1 inference and structural tests;
- decision_margins.md: SESOI/equivalence thresholds and predictive-evidence role;
- ../results/historical_exact_design/h1_exact_design_results_report.md: historical completed Monte Carlo results under the broader adjacent-lag definition;
- h1_comparable_lag_recalibration_plan.md: prospective 50,000-replication recalibration plan after excluding prompt 1 -> 2;
- h1_comparable_lag_recalibration_config.json: focused sample-size recalibration grid, guardrails, and Monte Carlo uncertainty rule;
- survey_items.md: English draft baseline and ESM item wording;
- survey_items_pl.md: canonical Polish H1 ESM candidate (v0.2-pl-cognitive);
- cognitive_interview_plan.md: two-round cognitive-interview and usability micro-pilot protocol before instrument freeze;
- data_dictionary.csv: planned variables and derivations;
- operational_rules.md: locked sampling, lag-validity, and technical exclusion rules;
- exact_design_config.json: exact-design and post-Monte-Carlo inference settings;
- missing_data_plan.md: primary missing-data handling and IPW-GEE sensitivity;
- ../analysis/h1_inference_analysis.py: revised coefficient-first inference;
- h1_asymmetry_validation_config.json: frozen focused independent M3/M4 validation grid for the M4 d_asym contrast;
- ../results/historical_exact_design/h1_asymmetry_validation_results.md: completed focused validation results; no confirmatory delta_asym retained because all candidate tolerances failed guardrails;
- ../analysis/h1_asymmetry_operating_characteristics.py: audit candidate asymmetry tolerances against preregistered guardrails; completed results support descriptive-only M4 asymmetry inference;

## Scope

H1 is the only confirmatory theoretical test in this pilot. H2 and H3 require separate progression logic. A failure to achieve adequate compliance or enough valid lag pairs is a feasibility/data-sufficiency failure, not evidence against H1.


Migration: original README at source revision `9ddb0708dfcd380bcdc5a33f3a52d3b3c8df4b62`; removed historical Windows launcher references not yet migrated and adjusted result/code paths. Scientific owner: Mateusz Pomianek. CC-BY-4.0 ([license](../LICENSE-CC-BY-4.0.txt)). Recruitment remains blocked pending recalibration and ethics.
