> Historical exact-design report. Its N=84 conclusion was calibrated under the broader adjacent-lag definition. Final H1 sample size is reopened only for the prospectively specified comparable-lag recalibration after excluding prompt 1 -> 2.

# H1 exact-design Monte Carlo: results and design decisions

Status: completed exact-design Monte Carlo, 2026-09-29.

## 1. Simulation completeness

The final merge manifest contains 120 exact-design scenarios:
4 candidate sample sizes (50, 60, 72, 84 couples) ×
3 compliance targets (0.65, 0.75, 0.85) ×
2 missingness-strength conditions (0, 1) ×
5 truth scenarios (M0-M4).

Every scenario contains exactly 1000 replications with replication IDs 0-999.
There are no missing or unexpected replication IDs. Total completed replications:
120,000.

The full per-replication table is retained as a local compute artifact.
Compact summaries, decisions, manifest, and workstation metadata are retained
in the repository.

## 2. Estimator behaviour

Across the candidate sample sizes used for substantive evaluation, all five
GEE models converged in all summarized replications.

Under M0 truth, nominal 0.05 tests remain close to the nominal level.
For N=84, mean false-positive rates across compliance/missingness conditions
were approximately:

- M1 r_hat: 0.055
- M2 r_hat: 0.057
- M2 r_star: 0.052
- M3 e: 0.055
- M4 positive discrepancy: 0.054
- M4 negative discrepancy: 0.054

For N=72 the corresponding rates were approximately 0.050-0.056.

Coefficient recovery is strong. At N=84:

- M1 r_hat truth -1.5 is recovered with very small bias and power ~1.00.
- M2 r_star truth 2.0 has power ~1.00.
- M2 r_hat truth -0.75 has power approximately 0.93-1.00 depending on
  compliance/missingness.
- M3 discrepancy truth 1.5 has power ~1.00.
- M4 positive discrepancy truth 2.0 has power ~1.00.
- M4 negative discrepancy truth -1.2 has power approximately 0.83-0.98,
  with power above 0.92 in the N=84, compliance=0.75 conditions.

Bias of the main relational coefficients is small relative to the simulated
effect sizes.

Conclusion: the primary problem identified by the Monte Carlo is not GEE
estimation or coefficient recovery.

## 3. Data-sufficiency results

The current sufficiency rule requires at least 100 individuals with at least
30 valid same-day lag pairs and adequate prediction-holdout coverage.

### N = 50 couples

This design is effectively insufficient under the current rule because the
maximum sample contains exactly 100 individuals. Any participant failing the
lag criterion causes the design-level threshold to fail.

### N = 60 couples

At compliance 0.75, data insufficiency remains very frequent.
At compliance 0.85, sufficiency is generally achieved.

### N = 72 couples

At compliance 0.75:

- missingness_strength=0: only about 1.3% of replications fail sufficiency;
- missingness_strength=1: about 45% of replications fail sufficiency.

At compliance 0.85, sufficiency is essentially complete.

### N = 84 couples

At compliance 0.75:

- missingness_strength=0: effectively 100% sufficient;
- missingness_strength=1: approximately 99.9% sufficient.

At compliance 0.85, sufficiency is effectively complete.

At compliance 0.65, even N=84 does not satisfy the current 100-person/30-lag
criterion reliably.

### Sample-size implication

Among the prespecified candidate sizes, 84 couples is the robust choice if the
study is designed to maintain approximately 75% or higher prompt compliance.
If sustained compliance near 65% is considered plausible, none of the current
candidate sample sizes provides robust sufficiency under the locked lag
criterion; the design would require either a larger sample, higher compliance,
or a separately justified revision of the lag-sufficiency criterion.

## 4. Failure of the current hierarchical representation-selection rule

The Monte Carlo falsifies the current sequential RMSE-gating rule as a primary
model-selection procedure.

The current rule begins by requiring evidence that M1 improves over M0 before
proceeding to M2-M4. This is not valid for the simulated model family because
a true M2, M3, or M4 process need not make the restricted M1 state-only model
materially better than M0.

A clear example is N=84, compliance=0.85, missingness_strength=0,
RMSE margin 0.1:

- M0 truth -> M0_no_state_increment: 1.000
- M1 truth -> M1_state_only: 0.016, inconclusive_M1_M0: 0.939
- M2 truth -> M0_no_state_increment: 1.000
- M3 truth -> M0_no_state_increment: 0.257 and inconclusive_M1_M0: 0.743
- M4 truth -> M0_no_state_increment: 0.076 and inconclusive_M1_M0: 0.919

This failure coexists with excellent coefficient recovery and high power.
Therefore it is a decision-rule architecture problem, not a failure of the
simulated effects to be estimable.

## 5. Consequence for preregistration

The sequential RMSE decision tree must not be frozen as the primary H1
inference rule.

Recommended H1 inferential architecture:

1. Keep the prespecified M0-M4 model family.
2. Treat coefficient estimates, confidence intervals, and prespecified
   structural contrasts as primary inferential evidence.
3. Use temporal-holdout RMSE as secondary predictive evidence rather than as a
   mandatory sequential gate.
4. Report inconclusive results explicitly rather than forcing a single winning
   representation.
5. If a formal predictive model-comparison rule is still required, redesign it
   so M2, M3, and M4 can be compared against an appropriate baseline directly;
   the current M1-first gate is invalid.
6. Any redesigned selection rule requires a focused validation simulation
   before preregistration. The later comparable-lag correction changes lag availability, so the historical N=84 sample-size conclusion must be recalibrated prospectively.

## 6. Implemented design decision

Design decision locked from the completed Monte Carlo:

- analysis target: 84 couples;
- planning assumption: prompt compliance >= 0.75;
- retain 14 days and 6 synchronized prompts/day;
- retain same-day 60-240 minute valid-lag definition;
- retain Gaussian identity-link GEE with couple-level clustering;
- retain M0-M4 as a prespecified model family;
- do not retain the current hierarchical RMSE model-selection tree as the
  primary inferential procedure.

The N=84 decision should be described as robust to the prespecified
missingness stress test at 75% compliance, but not as robust to 65% compliance.

## 7. Remaining pre-recruitment tasks

The primary H1 inferential redesign has been implemented. Remaining tasks are now narrower:

- coefficient-first reanalysis of the completed 120,000-replication table is complete and archived in compact form;
- the independent 8,000-replication M4 asymmetry validation is complete; no delta_asym is locked because all prespecified candidates failed the operating-characteristic guardrails;
- select and lock the IPW truncation rule from the prespecified candidates using targeted weighted-GEE operating characteristics, positivity, and effective-sample-size diagnostics;
- set the enrollment ceiling from an explicit couple-retention assumption, separate from the locked analysis target of 84 couples;
- complete ESM cognitive interviews and burden/notification feasibility checks before freezing the human instrument.

The completed 120,000-replication exact-design grid is not rerun for these tasks.


## 8. Post-Monte-Carlo inference revision

The recommendation in Section 5 has now been implemented before human outcome
data collection.

The revised co-primary family is:

- H1-P1: one-sided Wald test of H0: M2 beta_r_star <= 0.5 versus
  beta_r_star > 0.5;
- H1-P2: one-sided Wald test of H0: M3 beta_e <= 0.5 versus
  beta_e > 0.5.

The two SESOI-based p values use Holm family-wise control at alpha = 0.05.

Structural representation is reported separately:

- M2 d_sym = beta_r_star + beta_r_hat, with prospective 90% equivalence
  interval and locked tolerance delta_sym = 1.0;
- M4 d_asym = beta_positive + beta_negative is retained as secondary descriptive structural evidence. The completed focused N=84 validation rejected all prespecified confirmatory tolerance candidates because precision was inadequate.

Temporal-holdout RMSE remains secondary predictive evidence and is not used as
a sequential gate.

The existing 120,000-replication table can be reclassified under H1-P1/H1-P2
without rerunning the Monte Carlo because it already contains the required M2
and M3 coefficient estimates, robust standard errors, and the M2 symmetry
contrast. The old table cannot reconstruct d_asym because the M4 cross-
coefficient covariance was not stored; that is why only the M4 asymmetry
tolerance requires a focused new validation simulation.


## 9. Focused M4 asymmetry validation closure

The independent 8,000-replication focused validation has now been completed.

None of delta_asym = 0.25, 0.50, or 0.75 passed the prespecified guardrails.
The dominant failure mode was insufficient precision rather than estimator bias:
mean d_asym estimates were close to 0 under M3 truth and close to 0.8 under M4
truth, but mean standard errors were approximately 0.42-0.49.

Consequently, M4 remains useful for estimating separate positive- and
negative-discrepancy slopes, but no confirmatory symmetry/asymmetry threshold
is used in the N=84 H1 pilot. See h1_asymmetry_validation_results.md.
