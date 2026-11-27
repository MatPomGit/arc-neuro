# M02: computational analysis specification

Status: development specification, 2026-10-08. This is not a frozen confirmatory configuration or a new result.

## What the code currently does

`software/simulator/controller_identifiability_split.py` generates P/PI/PID trajectories and compares intercept-only (`context` in code), autoregressive, P, PI and PID regressions. The `context` label currently denotes an intercept, not a measured-context regression. Coefficients are estimated with ordinary least squares on the first block. Choice minimizes validation RMSE; exact ties favor the earlier candidate in the fixed order. The last block evaluates the frozen choice. Development fractions are 0.60/0.20/0.20. Observed lagged action in AR and observed discrepancy features make this conditional one-step prediction, not a recursive closed-loop rollout. Candidate regressions are not complete fitted copies of the nonlinear simulator.

## Required distinctions

| Quantity | Definition | Limitation |
|---|---|---|
| Nominal recovery | Validation-selected family equals synthetic label | Zero gains can make nominal labels functionally indistinguishable |
| Effective-order recovery | Agreement with prospectively defined reduced family | Rules and numerical tolerance remain to be frozen |
| Prediction | RMSE on last block for frozen coefficients/choice | Conditions on observed inputs; new-trajectory performance requires separate evaluation |
| Near tie | Absolute paired loss difference below frozen epsilon | Frequency is not a statistical equivalence conclusion |
| Equivalence | Prespecified interval for mean paired difference wholly within the band | Applies to loss, condition and candidates; not structural identifiability |
| Separation | Interval wholly above +epsilon or below -epsilon | Predictive separation, not proof of human mechanism |
| Inconclusive | Interval crosses a band boundary | Neither equivalence nor practical separation established |

## Before a separate confirmatory run

1. Freeze the final generator set, numerical factor grid, loss scale, tolerance, comparison family, multiplicity, interval method and effective-order thresholds. Choose replication counts from Monte Carlo precision and compute feasibility, not favorable recovery.
2. Evaluate interval calibration and unstable candidate extrapolation. Implement parameter intervals before reporting coverage; the completed suite currently reports bias and dispersion.
3. Preserve the implemented observation timing, causal histories, rank checks, validation-only competitor selection and deferred final scoring. Record any change explicitly and verify leakage tests.
4. Define any new scope (unknown nonlinear parameters, alternative missingness, recursive forecasting or independent-trajectory evaluation) prospectively. Those features are not implied by the completed conditional-prediction benchmark.
5. Reproduce in a clean, locked environment and archive source/config/output hashes. Retain failed attempts, candidate failures and separate attempted/evaluable denominators.

The old stress test and development benchmark remain development evidence. They must not be pooled silently into the expanded confirmatory run. New standardized results are recorded in the executed development archives described below.


## Implemented standardized benchmark (2026-10-07)

`controller_identifiability_suite.py` supplements the historical ARC-agent pipeline with a dimensionless feedback plant and eight generating/candidate families: intercept, AR, P, PI, PID, ARX, fixed-width tanh and sign-dependent switching slopes. Unlike the historical `context` label, `intercept` is explicit. This suite does not change `arc_model.py` or ARC 0.9.0 semantics.

The targeted config contains nine arms and exact PID reduction; the full development config crosses six two-level factors (64 conditions). Both use 80 seed blocks/cell, separate base seeds, fixed regular gains and 60/20/20 observed-time blocks. They retain candidate rank/conditioning, selection failures, nominal/effective labels, paired validation-selected competitors, near ties, pointwise Wilson recovery and normal mean-loss intervals, and parameter bias/dispersion. Parameter coverage is unavailable. Final loss calculation is explicitly deferred until choice is frozen in this suite; historical calculations remain separately identified.

Known nonlinear width and switching threshold, fixed gains, MCAR omissions, conditional prediction and the simplified plant limit generalization. An epsilon of 0.005 was a pre-run computational development choice, not a human-scale resolution or the final confirmatory threshold. Final confirmatory calibration, unknown nonlinear parameters, parameter intervals, recursive rollouts and independent-trajectory generalization remain open. The completed full development grid does not silently become preregistered confirmation.

## Executed methodological robustness extension (2026-10-08)

`controller_identifiability_robustness.py` reuses the archived plant unchanged. It generated 8,960 fresh-seed triads (26,880 trajectories), comparing temporal blocks with independent fitting/validation/final role trajectories. It adds Gaussian working AIC/BIC, t(3) variance-matched observation noise, irregular sampling, bounded seven-category error/action observations, pointwise percentile bootstrap (2,000 resamples), and conditional PID information/profile diagnostics. The common three-trajectory feasibility gate retains 968 failed triads in all recovery denominators. AIC/BIC select from fitting data and therefore have identical family choices across evaluation modes; final losses still differ.

The prior full factorial ledger was reanalyzed at four disclosed ε values without replacing its original normal intervals. This is sensitivity analysis after outcomes were inspected. Conditional information holds observed features fixed and is not the latent closed-loop FIM; Gaussian criteria are not full Bayesian evidence; quantization is not a validated human instrument. See `METHODOLOGICAL_REVIEW.md` and the archived output report. Independent-trajectory generalization now exists for fresh innovations at the same fixed gains/schedule, while independent-parameter generalization, recursive rollout and a full latent likelihood remain open.
