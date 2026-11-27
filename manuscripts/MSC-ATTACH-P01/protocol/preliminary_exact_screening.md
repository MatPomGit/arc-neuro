> Superseded timing layer: these engineering runs used exact-design configuration v1.0 before the operational sampling rules were locked. Configuration v1.1 now simulates six equal 140-minute strata, at least 90 minutes scheduled separation, response latency within a 30-minute response window, and valid response-to-response lags of 1-4 hours. The qualitative conclusions below remain useful for engineering provenance, but all sample-size and margin decisions must use fresh v1.1 results.

# Preliminary exact-design screening

Date: 27 September 2026

Status: engineering results only. These runs are not the final Monte Carlo, do not lock the sample size, and are not human empirical evidence.

## Purpose

The goal was to verify that the new M0-M4 GEE simulation runs, that all five estimators converge in representative scenarios, and that the older 60-couple planning target is not accepted without checking the richer missingness and dyadic generator.

The full design requires 1000 replications per scenario. The runs below used only 5-10 replications per truth scenario and therefore have high Monte Carlo uncertainty.

## Local engineering environment

The preliminary local runs used:

- Python 3.13;
- NumPy 2.3.5;
- pandas 2.2.3;
- SciPy 1.17.0;
- statsmodels 0.14.6.

The locked reproducibility environment for the repository is newer and uses statsmodels 0.15.0. CI is responsible for validating the smoke workflow under the pinned environment before merge.

## 75% target compliance

The generator includes person-level response propensity, so realized prompt response rates are lower than or vary around the nominal compliance parameter. The informative-missingness scenario additionally reduces response probability as a function of negative affect, discrepancy magnitude, and action magnitude.

### 60 couples

Non-informative missingness mechanism, 10 replications per truth:

- realized prompt response rate: approximately 0.74;
- median valid same-day lag pairs per person: approximately 39-40;
- mean number of people reaching at least 30 valid lags: approximately 93-97 of 120;
- all five GEE models converged in all engineering replications.

Informative missingness mechanism, 5 replications per truth:

- realized prompt response rate: approximately 0.71;
- median valid lags: approximately 36-37;
- mean number of people reaching at least 30 valid lags: approximately 80-87 of 120;
- all five GEE models converged.

This is insufficient for the current planning requirement of at least 100 people with at least 30 valid lag pairs.

### 72 couples

Non-informative missingness mechanism, 10 replications per truth:

- realized prompt response rate: approximately 0.74;
- median valid lags: approximately 39-40;
- mean number of people reaching at least 30 valid lags: approximately 110-114 of 144;
- all models converged.

Informative missingness mechanism, 10 replications per truth:

- realized prompt response rate: approximately 0.71;
- median valid lags: approximately 36-37;
- mean number of people reaching at least 30 valid lags: approximately 100-103 of 144;
- all models converged.

This makes 72 couples plausible but potentially borderline under the current informative-missingness mechanism.

### 84 couples

Informative missingness mechanism, 5 replications per truth:

- realized prompt response rate: approximately 0.71;
- median valid lags: approximately 36;
- mean number of people reaching at least 30 valid lags: approximately 117-124 of 168;
- all models converged.

This provides a visibly larger data-sufficiency buffer in the engineering run.

## Prediction behavior

The preliminary runs show the expected qualitative pattern:

- under M0 truth, adding relational terms produces RMSE differences near zero;
- under M1 truth, M1 improves over M0 while M2 adds little;
- under M2 truth, M2 improves over M1;
- under M3 truth, M2 and M3 have similar predictive performance;
- under M4 truth, M4 tends to improve over M3.

These are deliberately generated truth scenarios. They demonstrate that the pipeline can express the intended decisions; they are not evidence that any ARC model is true in humans.

## Current consequence

Do not lock 60 couples.

Keep 60, 72, and 84 couples in the full Monte Carlo comparison, with 50 couples retained as a deliberately lower design point.

The full run must quantify:

- probability of satisfying the valid-lag threshold;
- bias and 95% interval coverage;
- false-positive rates;
- convergence;
- probability of the correct H1-A/H1-B decision;
- sensitivity to RMSE margins;
- sensitivity to informative missingness.

Only after that run should the recruitment target and ceiling be fixed.
