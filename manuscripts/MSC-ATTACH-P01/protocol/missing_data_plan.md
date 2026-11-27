# H1 missing-data plan

Status: primary handling locked; IPW truncation candidate remains to be selected before recruitment from targeted simulation.

## 1. Primary analysis

The confirmatory H1 analysis uses observed valid same-day lag pairs.

Missed prompts are not:

- reconstructed;
- backfilled;
- treated as if a momentary state had been measured;
- bridged to the next available prompt.

The primary GEE therefore estimates the locked marginal mean model on observed valid lags.

This analysis is not claimed to be automatically unbiased under informative missingness.

## 2. Prespecified IPW-GEE sensitivity

A history-based stabilized inverse-probability-of-observation weighted GEE is used as the main missing-data sensitivity analysis.

Weighted GEE is appropriate as an MAR sensitivity when response probabilities can be represented by observed history. It does not solve missing-not-at-random selection caused by the current unobserved state.

The weighted model uses exactly the same M0-M4 outcome mean models, couple clusters, and independence working correlation as the primary H1 model; the weighted sensitivity uses the ordinary robust sandwich covariance because the pinned statsmodels 0.15.0 bias-reduced covariance is not compatible with observation weights. Only observation weights are added.

## 3. Leakage safeguard

Both response-probability models are fitted using days 1-11 only.

The days 12-14 temporal holdout does not determine:

- response-model coefficients;
- predictor selection;
- probability floor;
- weight-truncation quantiles;
- weight normalization.

Training-derived response models and training-derived truncation bounds are then applied unchanged to holdout prompts/lags.

## 4. Response-probability models

Numerator model:

- prompt stratum;
- study day.

Denominator model:

- prompt stratum;
- study day;
- prior response rate;
- whether the immediately previous scheduled prompt was observed;
- indicator that no previous observed prompt exists;
- last observed negative affect;
- last observed absolute relational discrepancy;
- last observed absolute signed action.

All psychological predictors are historical observed values. The current prompt's state or action is never used to predict whether that same prompt is observed.

The initial prompt has explicit no-history coding rather than fabricated psychological history.

## 5. Stabilized lag weights

Each observed scheduled prompt receives a stabilized observation weight:

w_prompt = P(R=1 | time) / P(R=1 | time, observed history).

A valid t -> t+1 lag receives the product of the stabilized weights for the two prompts that are required to construct the lag.

Training lag weights determine the truncation bounds. The same numeric bounds are applied to the holdout.

After truncation, weights are normalized to mean 1 in the training data. This scaling is applied consistently to the confirmatory weighted fit.

## 6. Positivity and weight diagnostics

Report:

- minimum fitted denominator response probability;
- 1st percentile fitted denominator probability;
- raw and truncated weight distributions;
- maximum stabilized lag weight;
- fraction of weights affected by truncation;
- effective sample size:
  ESS = (sum w)^2 / sum(w^2);
- ESS as a fraction of the number of training lags.

Severe positivity problems or a very low ESS are reported as a limitation rather than hidden by stronger truncation.

## 7. Candidate truncation rules

The exact-design configuration evaluates:

- no truncation;
- 1st/99th percentile;
- 2.5th/97.5th percentile.

The current provisional implementation defaults to 1st/99th percentile solely for engineering tests.

FINAL BEFORE DATA:
select one truncation rule based on simulation operating characteristics and weight diagnostics. Do not choose it using human H1 effect estimates.

## 8. Monte Carlo interpretation

The exact generator contains two conceptually different missingness situations.

At missingness_strength = 0:
nonresponse varies because of person response propensity but does not additionally depend on the generated momentary state/action variables.

At missingness_strength = 1:
response probability additionally depends on contemporaneous negative affect, absolute discrepancy, and absolute action. If the current prompt is not observed, those values would also be unobserved in a real study. This is therefore an MNAR-like stress condition relative to the history-only IPW model.

Consequences:

- improved IPW performance under a history-compatible response process supports the implementation;
- incomplete correction under the contemporaneous stress condition is expected and must not be presented as IPW failure or as evidence that MAR holds;
- robustness of the primary conclusion across unweighted and IPW analyses is informative, but neither analysis identifies an MNAR mechanism without additional assumptions.

## 9. Decision reporting

For every M0-M4 model, report primary versus IPW:

- convergence;
- key within-person coefficients;
- participant-paired holdout RMSE;
- direction and magnitude of coefficient changes.

A sensitivity result is considered materially discordant when it changes whether H1-P1 or H1-P2 satisfies the preregistered directional, Holm-adjusted, and SESOI criteria, or when it moves a structural contrast across its locked equivalence/asymmetry boundary.

RMSE changes are reported as secondary predictive discordance and do not redefine the co-primary H1 result.

## 10. Software

Implementation:
`software/study_design/h1_ipw_sensitivity.py`

Primary references:

- Chen, Yi, and Cook (2010), weighted GEE for longitudinal response/covariate data missing at random.
- Cole and Hernán (2008), construction and diagnostics of inverse-probability weights.

The primary H1 estimator remains the unweighted GEE defined in `estimator_decision.md`.
