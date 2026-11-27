# Draft preregistration: ARC H1 pilot

Status: draft for registration. The primary H1 inferential architecture is locked before recruitment. The final sample-size target is temporarily reopened only for the prospectively specified comparable-lag recalibration after exclusion of prompt 1 -> 2. Remaining items explicitly marked FINAL BEFORE DATA concern measurement calibration or sensitivity settings and must be resolved before recruitment or before any investigator sees human outcome data.

## 1. Confirmatory H1 structure

The pilot tests two co-primary claims and a separate structural representation question. The earlier sequential predictive hierarchy is superseded by the completed 120,000-replication exact-design Monte Carlo because it could stop at M0/M1 when M2-M4 generated the data despite accurate coefficient recovery.

### H1-P1: desired-state contribution

In M2, the within-person desired-closeness coefficient beta_r_star is expected to be positive after adjustment for perceived closeness, context, and prior signed action.

Support requires all of the following:

- positive estimate;
- Holm-adjusted one-sided Wald p < 0.05 for H0: beta_r_star <= delta_beta, where delta_beta = 0.5 signed-action points per 10-point within-person change.

### H1-P2: discrepancy-action coupling

In M3, beta_e is expected to be positive.

Support requires:

- positive estimate;
- Holm-adjusted one-sided Wald p < 0.05 for H0: beta_e <= delta_beta = 0.5.

Full confirmatory support for H1 requires both H1-P1 and H1-P2. Support for only one is reported as partial support. Neither test is gated by M1 versus M0 predictive performance.

### Structural representation

M2, M3, and M4 are characterized directly rather than forced into a single sequential winner.

For M2:

d_sym = beta_r_star + beta_r_hat.

Exact signed-discrepancy symmetry implies d_sym = 0. Prospective equivalence uses a 90% confidence interval and tolerance delta_sym = 1.0:

- interval wholly inside [-1.0, +1.0]: compatible with signed-discrepancy symmetry;
- interval wholly outside the equivalence region on one side: evidence against the restriction;
- otherwise: inconclusive.

For M4:

d_asym = beta_positive + beta_negative,

where beta_negative multiplies max(-e, 0). Symmetry implies d_asym = 0. The completed focused N=84 validation showed that the prespecified candidate tolerances 0.25, 0.50, and 0.75 all failed the operating-characteristic guardrails. Consequently, no confirmatory delta_asym is used in this pilot. Report d_asym and its 95% confidence interval as secondary structural evidence only.

Structural conclusions do not override failure of a co-primary H1 test.

## 2. Confirmatory status

H1-P1 and H1-P2 are the only co-primary confirmatory ARC tests in this pilot. The M2 symmetry and M4 asymmetry contrasts are prespecified structural characterization tests.

H2:
attachment anxiety/avoidance moderation is exploratory unless separately powered and preregistered.

H3:
secure-base recovery is not a confirmatory test in this pilot. H3 requires a dedicated recovery design and is the promotion test for candidate core construct S.

H4 and H5:
not tested confirmatorily in this pilot.

## 3. Sample

Analysis target status:
84 couples is the previous calibrated target. Final N is not frozen until the prespecified comparable-lag recalibration selects the smallest qualifying candidate among 72/84/96/108/120 couples.

The exact-design Monte Carlo compared 50, 60, 72, and 84 couples. At approximately 75% prompt compliance, N = 84 was the smallest tested candidate that was robust to the current confirmatory sufficiency criterion under the prespecified informative-missingness stress condition. At N = 72 and the same compliance, informative missingness caused frequent insufficiency.

Planning therefore assumes prompt compliance of approximately 0.75 or higher. If sustained compliance near 0.65 is plausible, none of the tested candidate sample sizes is robust under the current lag-sufficiency rule.

The recruitment ceiling for couple-level attrition is not inferred from this Monte Carlo because couple dropout was not explicitly calibrated. It must be set separately before recruitment from operational retention assumptions.

No optional stopping based on H1 coefficients, p values, model ranking, holdout RMSE, or apparent ARC support is allowed.

## 4. Sampling schedule

The operational schedule is locked in `operational_rules.md`:

- 14 consecutive days;
- one shared 14-hour waking window per couple, fixed before day 1;
- 6 synchronized semi-random prompts per day;
- six equal 140-minute strata;
- minimum 90-minute scheduled separation;
- 30-minute response window with one reminder at 15 minutes;
- actual response-to-response lag must be 60-240 minutes inclusive;
- no overnight or missed-prompt bridging.

The full 14-day schedule is generated before day 1 and is not adapted to study outcomes.

## 5. Relational predictors

Perceived relational state:

r_hat_it = current perceived closeness to partner, 0-100.

Desired relational state:

r_star_it = current desired closeness to partner, 0-100 with identical anchors.

Signed discrepancy:

e_it = r_star_it - r_hat_it.

Positive discrepancy:

e_positive_it = max(e_it, 0).

Negative discrepancy magnitude:

e_negative_it = max(-e_it, 0).

Every time-varying relational predictor used confirmatorily is decomposed into a participant mean and a within-person deviation. H1 concerns the within-person component; between-person means enter separately so within-person dynamics are not conflated with stable between-person differences.

Participant means used for both training and holdout predictors are calculated exclusively from observed days 1-11 prompts. Days 12-14 never contribute to centering or feature construction.

## 6. Primary outcome

a_signed_i,t+1 = approach_i,t+1 - distance_i,t+1.

Range:
-100 to +100 before any transformation.

Mandatory component outcomes:

- approach action;
- distance action.

Internal suppression/disengagement is secondary.

The signed outcome is retained for H1 parsimony, but simultaneous high approach and high distance must remain visible in the component analyses.

## 7. Valid lag pair

The exact lag and technical-validity rules are locked in `operational_rules.md`.

A confirmatory lag requires consecutive prompt numbers within one day, both prompts submitted inside their response windows, all variables required by the selected model, a valid signed action outcome at t+1, and an actual response-to-response interval of 60-240 minutes inclusive.

A missed or expired prompt breaks the lag. Overnight transitions and bridging across missed prompts are excluded.

## 8. Locked model family

All models contain the same preregistered context terms and prior signed action.

M0:
context + autoregressive action.

M1:
M0 + perceived closeness r_hat(t).

M2:
M0 + perceived closeness r_hat(t) + desired closeness r_star(t), entered as separate unconstrained predictors.

M3:
M0 + signed discrepancy e(t) = r_star(t) - r_hat(t).

M4:
M0 + e_positive(t) + e_negative(t), allowing asymmetric regulation of closeness deficit and closeness surfeit.

M2 is the least constrained target-aware model.
M3 is the primary parsimonious ARC discrepancy candidate.
M4 is the prespecified asymmetric alternative.

No model may be added to the confirmatory M0-M4 set after outcome data are inspected.

## 9. Locked confirmatory context set

The confirmatory context set is fixed as:

- current negative affect/distress at t;
- relational stressor indicator available at t;
- meaningful partner interaction/contact indicator available at t;
- prompt stratum/time of day;
- actual elapsed time between t and t+1.

No stepwise or data-driven covariate selection is allowed.

Additional contextual variables may be reported descriptively or in clearly labeled sensitivity/exploratory analyses, but they cannot replace this confirmatory set after data inspection.

## 10. Confirmatory estimator

The confirmatory estimator is locked as a Gaussian generalized estimating equation (GEE) with:

- identity link;
- couple_id as the clustering unit, so both partners and all repeated observations from a couple belong to one robust cluster;
- independence working correlation;
- bias-reduced sandwich covariance;
- statsmodels 0.15.0;
- maximum 100 iterations;
- convergence tolerance 1e-8.

The mean model contains explicit within-person deviations and participant means for time-varying relational predictors and the locked context set.

No Bayesian priors are used.

No random-effects distribution is required by the primary estimator. Person and couple random intercepts and person-specific relational-slope heterogeneity are instead included in the exact Monte Carlo generator to test whether the marginal GEE retains acceptable operating characteristics under richer data-generating heterogeneity.

A replication or empirical fit is considered converged only when the estimator reports converged = true. Nonconvergence is reported as estimator failure and is not repaired by switching covariance structures or estimators after outcome inspection.

DSEM or mixed-effects models may be reported as prespecified sensitivity analyses, but they do not replace the locked primary H1 estimator.

## 11. Data sufficiency

For confirmatory dynamic interpretation, require:

- at least 100 individuals with at least 30 valid same-day lag pairs each;
- adequate days 12-14 holdout data for the prespecified paired predictive summaries.

The completed historical exact-design Monte Carlo showed that N = 84 satisfied this criterion in essentially all scenarios at compliance 0.75 without the informative stress mechanism and in approximately 99.9% under the prespecified informative-missingness stress condition. That run used the broader adjacent-lag definition; the comparable-lag recalibration supersedes it for the final sample-size freeze.

If the empirical dataset does not meet the locked sufficiency criterion:

- report compliance and feasibility;
- report H1 estimates but label the confirmatory conclusion inconclusive;
- do not interpret a null result as falsification of ARC.

## 12. Temporal holdout

Training/model-locking period:
days 1-11.

Final temporal test:
days 12-14.

The holdout cannot be used for:

- choosing transformations;
- adding or removing predictors;
- adding interactions;
- changing lag definitions;
- changing context terms;
- tuning hyperparameters;
- selecting the estimator;
- changing the model set;
- choosing the predictive metric or comparison margin.

The final test block is opened only after all model specifications are locked.

## 13. Secondary predictive metric

The locked predictive metric is participant-level RMSE on the signed-action scale over valid days 12-14 holdout observations.

Paired model differences are aggregated to couple-level means before uncertainty is calculated, with t-based confidence intervals across couples.

Report:

- M1 - M0;
- M2 - M1;
- M3 - M2;
- M4 - M3;
- M4 - M2.

Prediction is secondary evidence for H1. It does not gate H1-P1, H1-P2, or structural interpretation. The failed sequential RMSE selection tree from the design-development phase is retained only as a documented simulation diagnostic.

No single RMSE margin defines the primary confirmatory conclusion. Prespecified material-improvement/non-inferiority margins may be reported as secondary sensitivity interpretations, alongside the continuous paired difference and confidence interval.

## 14. Confirmatory interpretation

The confirmatory result is no longer a sequential model-selection hierarchy.

### Co-primary result

Full H1 support:
H1-P1 and H1-P2 both reject H0: beta <= delta_beta after Holm adjustment.

Partial H1 support:
exactly one co-primary test satisfies both criteria.

No confirmatory H1 support:
neither test satisfies both criteria under adequate data quality.

Inconclusive:
data sufficiency, convergence, or precision precludes a confirmatory decision.

### Structural result

Independently report whether:

- the M2 equality restriction is compatible with signed-discrepancy symmetry, incompatible, or inconclusive;
- M4 slopes and d_asym estimate with its 95% confidence interval, without a confirmatory practical-symmetry/asymmetry classification (as specified in Sections 1 and 15).

### Predictive result

RMSE comparisons are reported as secondary convergent, discordant, or inconclusive evidence. A predictive result cannot suppress or rescue a co-primary inferential result.

## 15. Inferential parameters

Primary confirmatory parameters:

- M2 within-person beta_r_star;
- M3 within-person beta_e.

These two one-sided SESOI tests form one family and use Holm family-wise error control at alpha = 0.05. Ordinary p values against zero and 95% confidence intervals are reported descriptively.

Primary effect-size relevance threshold:

delta_beta = 0.5 signed-action points per 10-point within-person relational change.

Secondary structural parameters:

- M2 beta_r_hat;
- M2 d_sym = beta_r_star + beta_r_hat;
- M4 beta_positive;
- M4 beta_negative;
- M4 d_asym = beta_positive + beta_negative.

The signed-discrepancy symmetry tolerance is locked at delta_sym = 1.0. No M4 asymmetry tolerance is locked because the completed focused validation showed inadequate precision at N=84; M4 asymmetry is secondary/descriptive.

Also report autoregressive action parameters and between-person relational predictor means. These are not additional primary H1 tests.

## 16. Exclusions

Technical-invalid-record rules and non-exclusion rules are locked in `operational_rules.md`.

Confirmatory autoregressive analyses exclude the prompt 1 -> 2 transition. Only adjacent same-day transitions 2->3, 3->4, 4->5, and 5->6 are eligible, because the action reported at the first prompt refers to the overnight/first-of-day interval rather than a standardized preceding same-day ESM interval. All existing 1-4 hour, response-validity, adjacency, and no-bridging rules still apply.

Confirmatory participant-level inclusion currently requires:

- at least 30 valid same-day lag pairs across the study;
- at least 3 valid lag pairs in days 12-14.

These thresholds are locked for this preregistration. Any pre-recruitment change would require a timestamped protocol amendment with independent methodological justification and must not use human H1 outcome data.

Failure of one partner to meet the threshold does not automatically exclude the other partner. All enrolled participants remain in recruitment, compliance, and missingness reporting.

## 17. Missing data

No retrospective filling of missed ESM prompts.

Report missingness as a function of participant, day, prompt stratum, previous relational state/target/discrepancy, previous action, previous negative affect, and baseline attachment dimensions.

Primary analysis uses observed valid lag pairs without retrospective imputation.

Mandatory sensitivity is stabilized inverse-probability-of-observation weighted GEE. The numerator contains prompt stratum and study day. The denominator additionally contains prior response rate, previous scheduled-prompt response status, a no-history indicator, and last observed negative affect, absolute discrepancy, and absolute signed action. Response models are estimated on days 1-11 only and applied unchanged to the holdout.

The sensitivity is interpreted under a history-based MAR assumption and is not claimed to correct dependence on contemporaneous unobserved state/action.

Sensitivity discordance is evaluated against H1-P1/H1-P2 and the structural contrasts, not against the superseded sequential RMSE architecture.

FINAL BEFORE DATA:
select one prespecified weight-truncation rule from the candidates in exact_design_config.json using targeted simulation operating characteristics and positivity/ESS diagnostics.

## 18. Secondary and robustness analyses

Mandatory:

- approach outcome separately;
- distance outcome separately;
- exclude intervals with no meaningful partner interaction;
- include actual elapsed time;
- inspect raw and person-centered predictor distributions;
- compare participant-level and dyadic dependence specifications where appropriate;
- estimate study-day trends in r_hat, r_star, and e after the locked context/time-of-day terms;
- refit M2/M3 with study day and study-day-by-primary-relational-predictor terms to assess sensitivity to repeated-measurement drift.

Study-day trends are interpreted as measurement-reactivity diagnostics, not causal proof of reactivity, because genuine relationship change, habituation, burden, or selective missingness may generate the same pattern. Internal suppression/disengagement, partner responsiveness, H2 moderation, and other extensions remain secondary/exploratory in this pilot.

## 19. Deviations

All departures from this preregistration are timestamped and labeled:

- correction of implementation error;
- unavoidable data-quality response;
- exploratory modification.

A deviation is never silently incorporated into the confirmatory result.



## Sample-size freeze status after comparable-lag correction

The previously calibrated analysis target of 84 couples was obtained under the broader adjacent-lag definition that included prompt 1 -> 2. Because the confirmatory lag rule now excludes that transition, the target of 84 couples is provisional. Before recruitment is frozen, the exact-design Monte Carlo must be rerun on the current code using the expanded candidate grid 72, 84, 96, 108, and 120 couples. The final analysis target is selected prospectively from those operating characteristics without reference to human H1 outcomes.
