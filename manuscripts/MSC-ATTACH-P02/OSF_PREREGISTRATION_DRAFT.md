# M02: draft for a prospective OSF registration

Status: draft, not submitted, not registered, not a frozen confirmatory protocol.
Prepared 2026-10-08. This file does not establish registration or ethical approval.

## Study and disclosure

Working title: When the True Controller Is Not Recoverable: Observational Equivalence in Models of Relational Regulation.
Author: Mateusz Pomianek, Rzeszów University of Technology; ORCID 0000-0001-7769-8919.
This is synthetic computational research. No participants or human observations.

The author has inspected the legacy stress test, the 2026-10-01 split benchmark, the 2026-10-07 standardized targeted/factorial runs and the 2026-10-08 methodological robustness extension. All are development evidence and must be disclosed. The registration will concern a distinct future execution with new seed streams, not those already inspected records. Code/config hashes and registration timestamp must precede final execution.

## Questions and estimands

1. How does generating-family recovery depend on observation design and selector?
2. Can high nominal recovery coexist with mean predictive differences smaller than the chosen computational resolution?
3. Which observation conditions undermine usable estimation and test feasibility?

Primary unit: an independent seed triad, with separate fitting/validation/test trajectories. Model choice and coefficients freeze before final losses are accessed. Sampling histories stay within each trajectory. Failures remain unsuccessful recovery in attempted denominators; additionally report evaluable recovery and paired-loss counts. Different generators/conditions may share specified innovation streams for paired contrasts.

## Proposed design, requiring final freeze

- Reuse the eight standardized families and explicitly declare known versus estimated nonlinear parameters.
- Keep a computational interpretation of gains; no mapping to psychological traits.
- Candidate primary selector: validation RMSE; Gaussian working AIC/BIC are separate sensitivity selectors with their assumptions stated.
- Candidate observation grid: the existing six-factor grid; decide prospectively whether additional observation arms are sensitivity-only or primary. Do not add favorable subsets after outcomes.
- Proposed precision target: worst-case pointwise recovery interval half-width at most 0.025. For Wilson 95% intervals, 1,600 independent attempted triads per cell yield a maximum half-width about 0.0245. This addresses a pointwise proportion, not simultaneous comparisons or paired-loss precision.
- Check resources and paired-loss interval calibration before freezing the final replicate count. Failed sparse triads can greatly reduce paired-loss precision despite sufficient attempted counts.
- Practical tolerance must be justified in simulator units before execution. The development sensitivity grid is disclosed; it is not a search for a favorable final tolerance. A primary engineering-resolution tolerance and any normalized secondary loss must be defined separately.
- Use simulation-based calibration to choose and justify the final interval method. Percentile bootstrap alone does not establish coverage under rare heavy tails or small evaluable counts.
- Freeze primary contrast family and multiplicity control, tie-breaking, rank/conditioning decisions, numerical failures and effective-order thresholds. No full Bayesian comparison without priors/likelihood.


A reproducible **planning-only** Wilson/Bonferroni attempt-count calculator and a prospective coverage-calibration checklist are provided in [PRECISION_AND_INFERENCE_GATES.md](PRECISION_AND_INFERENCE_GATES.md). They do not finalize the comparison family, justify epsilon, establish paired-loss precision or authorize a confirmatory run.

## Current open decisions

| Required before submission/run | Current status |
|---|---|
| Exact primary grid, generators, initial conditions and observation transformations | Draft choices, not frozen |
| Replication count and compute-feasibility decision | Proposed 1,600 for pointwise recovery; loss precision/calibration open |
| Primary ε, loss units/normalization and substantive computational rationale | Open |
| Final interval method, calibration evidence, coverage and multiplicity | Open |
| Comparator selection, candidate order and practical degeneracy rule | Development implementation exists; final rule not frozen |
| Missingness/failure policies and common triad eligibility | Development implementation exists; final policy not frozen |
| New seed registry and untouched final-output procedure | Must be created and checksummed before execution |
| Exact source commit, dependency lock and independent reproduction | Must be attached and verified |

## Analysis and deviations

Report family recovery with pointwise/simultaneous uncertainty as specified at freeze; keep nominal and effective outcomes separate. Report fitted nominal-family versus prospectively selected competitor paired differences, near-tie frequency and interval-contained equivalence separately. Do not use nonsignificance as equivalence. Keep failures and contrary outcomes in the result bundle. Parameter intervals require a justified likelihood/coverage analysis and cannot be inferred from conditional working profiles.

Any change after freeze records its date, rationale, whether outputs were inspected and which claims become exploratory. Development evidence is neither pooled silently nor relabeled as confirmation.

## Registration package and release procedure

Complete open decisions; attach the frozen numerical configuration, exact source/config hashes, dependency lock, seed registry, analysis/output contract and disclosed development evidence list. Register a timestamped copy on OSF before executing the new final seeds. Preserve the registration URL/identifier in the repository only after actual submission succeeds. Then execute, audit, independently reproduce and report all prespecified outcomes.

Official guidance: https://www.cos.io/initiatives/prereg. This document is a reviewable draft; no external operation has been performed.
