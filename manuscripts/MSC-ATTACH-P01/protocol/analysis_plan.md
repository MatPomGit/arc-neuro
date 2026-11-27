# H1 pilot analysis plan

## 1. Confirmatory objective

The pilot tests whether momentary relational target/state information predicts subsequent signed interpersonal regulation beyond context and behavioral persistence, and whether that relation is adequately represented by a signed discrepancy or requires a less constrained representation.

The completed exact-design Monte Carlo showed that the earlier sequential RMSE gate was not a valid primary decision rule: true M2-M4 processes could be incorrectly stopped at M0/M1 despite accurate coefficient recovery. H1 therefore uses direct model-specific inferential tests as primary evidence. Temporal-holdout RMSE is retained as secondary predictive evidence and never gates access to another confirmatory model.

## 2. Locked model family

All models use the same preregistered context set and prior signed action.

M0:
context + prior signed action.

M1:
M0 + perceived closeness r_hat(t).

M2:
M0 + perceived closeness r_hat(t) + desired closeness r_star(t), entered separately.

M3:
M0 + signed discrepancy e(t) = r_star(t) - r_hat(t).

M4:
M0 + positive discrepancy max(e, 0) + negative discrepancy magnitude max(-e, 0).

M2 is the least constrained target-aware model. M3 is the parsimonious signed-discrepancy model. M4 allows different slopes for closeness deficit and closeness surfeit. No model outside M0-M4 enters the confirmatory analysis.

## 3. Co-primary H1 tests

The co-primary inferential family contains two directional within-person tests.

### H1-P1: desired-state contribution

In M2, the within-person desired-state coefficient beta_r_star is expected to be positive after adjustment for perceived state, context, and prior action.

Evidence for H1-P1 requires:

- the estimate to be positive;
- the Holm-adjusted one-sided Wald p value for H0: beta_r_star <= delta_beta to be below family alpha = 0.05.

This directly tests whether target information contributes beyond perceived state without requiring M1 to outperform M0 first.

### H1-P2: discrepancy-action coupling

In M3, beta_e is expected to be positive.

Evidence for H1-P2 requires:

- the estimate to be positive;
- the Holm-adjusted one-sided Wald p value for H0: beta_e <= delta_beta to be below family alpha = 0.05.

Full confirmatory support for the core H1 discrepancy claim requires both H1-P1 and H1-P2. If only one is supported, the result is reported as partial rather than forced into a winning model label.

The working coefficient SESOI is delta_beta = 0.5 signed-action points per 10-point within-person change. This value is selected from the prespecified simulation grid as a conservative relevance floor for the primary effects; it remains subject only to pre-recruitment measurement-calibration review if cognitive piloting shows that the signed-action scale cannot resolve effects of this magnitude.

## 4. Multiplicity

H1-P1 and H1-P2 form one confirmatory family.

Each co-primary test uses the one-sided Wald null H0: beta <= delta_beta. These two SESOI-based p values are adjusted with the Holm procedure at family-wise alpha = 0.05. Ordinary tests against zero and 95% confidence intervals are reported descriptively. All other coefficient tests are secondary confirmatory or descriptive and do not rescue failure of a co-primary test.

## 5. Structural representation tests

Structural characterization is performed irrespective of whether M1 improves prediction over M0.

### 5.1 Signed-discrepancy restriction

In M2 define

d_sym = beta_r_star + beta_r_hat.

Exact signed-discrepancy symmetry implies d_sym = 0 because beta_r_hat = -beta_r_star.

Prospective equivalence testing uses a prespecified symmetry tolerance

delta_sym = 1.0

on the coefficient-per-10-point scale. The primary structural classification uses a 90% confidence interval, corresponding to two one-sided equivalence tests at alpha = 0.05:

- interval wholly inside [-delta_sym, +delta_sym]: compatible with the signed-discrepancy restriction;
- interval wholly outside the equivalence region on one side: evidence against the restriction;
- otherwise: inconclusive.

The full exact-design Monte Carlo supported delta_sym = 1.0 as a usable discrimination tolerance at N = 84: under M3 truth, equivalence was commonly recovered at compliance >= 0.75, whereas false equivalence under the unconstrained M2 truth was rare. The earlier 95% interval Monte Carlo check was conservative relative to the prospective 90% equivalence interval.

### 5.2 Asymmetry contrast

In M4 define

d_asym = beta_positive + beta_negative,

where beta_negative multiplies the nonnegative magnitude max(-e, 0). Under a perfectly symmetric signed-discrepancy relation, beta_negative = -beta_positive and d_asym = 0.

The completed focused N=84 validation showed that no prespecified practical-equivalence tolerance (0.25, 0.50, 0.75) achieved acceptable operating characteristics. M4 therefore remains a prespecified secondary structural model, but d_asym is reported descriptively with its estimate and 95% confidence interval. No confirmatory symmetry/asymmetry threshold is used in this pilot. A future study making asymmetry a confirmatory claim requires separate prospective design work.

### 5.3 No forced winner

M2, M3, and M4 are not collapsed into a single mandatory winner. The confirmatory report gives a structural evidence profile:

- target contribution supported or not;
- signed-discrepancy coupling supported or not;
- M2 symmetry restriction compatible, incompatible, or inconclusive;
- M4 slopes and d_asym estimate with its 95% confidence interval, without a confirmatory symmetry/asymmetry classification.

This prevents a failure in one nested approximation from blocking evaluation of another prespecified representation.

## 6. Temporal-holdout prediction

Days 1-11 are used for model fitting and feature construction. Days 12-14 form the untouched temporal holdout.

Participant-level holdout RMSE remains the primary predictive metric, but prediction is secondary to the co-primary inferential tests for the scientific H1 claim.

For participant i and model m:

RMSE_i,m = sqrt(mean((a_signed_observed - a_signed_predicted)^2)).

Paired model differences are aggregated to couple-level means before uncertainty is calculated. Confidence intervals use the t distribution across couples.

Report the prespecified comparisons:

- M1 - M0;
- M2 - M1;
- M3 - M2;
- M4 - M3;
- M4 - M2.

RMSE is reported as a continuous difference with confidence interval. No sequential predictive gate determines whether a later model may be interpreted. Material-improvement/non-inferiority margins may be shown as secondary sensitivity thresholds, but no single RMSE margin defines the primary H1 conclusion.

## 6.1 Comparable within-day lag rule

Confirmatory autoregressive rows use only adjacent same-day transitions 2->3, 3->4, 4->5, and 5->6. Prompt 1 -> 2 is excluded prospectively because the source action at prompt 1 summarizes the overnight/first-of-day interval and is not comparable to the standardized preceding same-day ESM intervals represented by later source prompts.

All other locked lag-validity rules remain unchanged: both adjacent prompts must be valid and observed, the pair must not cross a missed prompt or day boundary, and the actual response-to-response interval must be 1-4 hours.

## 7. Within-person and between-person decomposition

Every time-varying relational predictor used confirmatorily is decomposed into:

- participant mean X_between(i);
- within-person deviation X_within(i,t).

H1 concerns within-person effects.

For prediction on days 12-14, participant means are estimated using observed days 1-11 prompts only. Holdout prompts do not contribute to centering, feature engineering, or between-person summaries.

## 8. Primary outcome

a_signed = approach - distance.

Mandatory component analyses:

- approach;
- distance.

Simultaneously high approach and high distance can cancel in the signed score, so the component analyses are required for interpretation. Internal suppression/disengagement remains secondary in H1.

## 9. Locked confirmatory context set

Use:

- negative_affect(t);
- relational_stressor available at t;
- meaningful_interaction/contact available at t;
- prompt stratum/time of day;
- actual elapsed_hours between t and t+1.

No data-driven stepwise covariate selection is allowed.

## 10. Confirmatory estimator and dyadic dependence

The primary H1 estimator is locked as:

- Gaussian GEE;
- identity link;
- clustering by couple_id;
- independence working correlation;
- bias-reduced sandwich covariance;
- statsmodels 0.15.0;
- maximum 100 iterations;
- convergence tolerance 1e-8.

Both partners and all repeated observations therefore belong to the same robust cluster. The analysis is marginal/population-average.

DSEM and mixed-effects models remain prespecified sensitivity or later-stage approaches rather than alternate primary estimators selected after seeing outcomes.

A fit that does not report convergence is an estimator failure. The primary estimator or covariance structure is not changed post hoc to rescue it.

## 11. Data sufficiency and sample size

The exact-design Monte Carlo completed 120,000 replications.

The previous analysis target is 84 couples. It was the smallest prespecified candidate robust to the earlier sufficiency criterion under approximately 75% compliance and the prespecified informative-missingness stress condition. That calibration included the prompt 1 -> 2 transition. After adopting the comparable-lag rule, N=84 is provisional and the operating characteristics must be recalibrated before recruitment is frozen.

The confirmatory planning criterion remains:

- at least 100 individuals with at least 30 valid same-day lag pairs;
- adequate holdout data for the paired predictive comparisons.

At N = 84 and compliance = 0.75, this criterion was met in essentially all non-informative-missingness replications and approximately 99.9% of the informative-missingness stress replications. At compliance = 0.65, none of the tested candidate sizes was robust.

If the empirical dataset fails the locked sufficiency criterion, H1 is reported as inconclusive for confirmatory purposes; a null estimate is not interpreted as falsification.

The enrollment ceiling must be determined separately from expected couple-level attrition because couple dropout was not explicitly calibrated by the exact-design Monte Carlo.

## 12. Missingness

Primary analysis uses observed valid same-day lag pairs without retrospective imputation.

Mandatory sensitivity is history-based stabilized IPW-GEE with the same mean models, couple clusters, and independence working correlation. Response models are trained on days 1-11 only, and training-derived models and truncation bounds are applied unchanged to days 12-14.

The IPW sensitivity is an MAR analysis conditional on observed history. It is not interpreted as correction for the contemporaneous unobserved-state stress mechanism.

Discordance is evaluated against the direct co-primary coefficient conclusions and structural contrasts, not against the superseded sequential RMSE tree.

## 13. Exact-design Monte Carlo result and consequence

The completed exact-design Monte Carlo established:

- full model convergence in the evaluated summary cells;
- approximately nominal type-I error under M0;
- small coefficient bias;
- strong power for the main M1-M4 relational effects at N = 84;
- robust data sufficiency at N = 84 when compliance is approximately 0.75 or higher;
- failure of the earlier M1-first sequential RMSE rule to identify true M2-M4 processes reliably.

The completed 120,000-replication grid rejects the old primary decision tree and remains historical evidence about estimator behavior. Its N = 84 sample-size conclusion is not final because that grid included prompt 1 -> 2. Final N is selected only by the prospectively specified comparable-lag recalibration.

The focused M4 asymmetry validation has been completed. It showed insufficient precision for a confirmatory asymmetry/equivalence classification at N=84, so no delta_asym is locked.

## 14. Robustness analyses

Mandatory:

- approach outcome separately;
- distance outcome separately;
- exclude intervals with no meaningful partner interaction;
- include actual elapsed time;
- inspect predictor distributions and within-person variation;
- compare primary unweighted GEE with the prespecified IPW-GEE sensitivity.

No robustness analysis is allowed to replace a failed co-primary test post hoc.

## 14.1 Measurement-reactivity sensitivity

Repeated measurement of perceived and desired closeness may alter discrepancy salience or desired-state reporting. The analysis therefore includes a prespecified non-confirmatory reactivity diagnostic:

- estimate study-day trends in r_hat, r_star, and e after the locked context/time-of-day terms;
- report standardized change across the 14-day window with uncertainty;
- refit M2 and M3 with study day and study-day-by-primary-relational-predictor terms;
- compare the direction, magnitude, and confirmatory classification of H1-P1/H1-P2 with the primary specification.

These analyses diagnose temporal drift but do not identify its cause. A trend may reflect measurement reactivity, genuine relationship change, habituation, burden, or differential missingness. Therefore it is used to qualify interpretation rather than to replace the primary preregistered model.

## 15. Interpretation states

Full H1 support:
both H1-P1 and H1-P2 reject their SESOI nulls H0: beta <= delta_beta after Holm adjustment.

Partial support:
exactly one co-primary test meets both criteria.

No confirmatory support:
neither co-primary test meets both criteria under adequate data quality.

Inconclusive:
data sufficiency, convergence, or precision does not permit a confirmatory conclusion.

Structural representation is reported separately as signed-discrepancy-compatible, symmetry-incompatible, asymmetric, or inconclusive according to the prespecified contrasts. These structural labels do not override the co-primary H1 result.

Predictive RMSE results are reported as convergent, discordant, or inconclusive secondary evidence and do not gate the confirmatory coefficient tests.

