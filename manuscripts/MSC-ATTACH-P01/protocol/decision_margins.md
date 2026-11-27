# H1 decision margins: locked inferential thresholds

Status: post-Monte-Carlo revision before recruitment.

## Purpose

The completed exact-design Monte Carlo showed that predictive RMSE margins should not serve as a sequential gate for the M0-M4 family. H1 therefore separates:

1. a primary coefficient-scale SESOI for the two co-primary H1 effects;
2. a structural equivalence tolerance for the signed-discrepancy restriction;
3. a still-to-be-calibrated M4 asymmetry tolerance;
4. secondary predictive RMSE differences reported continuously with confidence intervals.

## 1. Primary coefficient SESOI

Relational predictors are recorded on matched 0-100 scales and within-person coefficients are expressed as signed-action points per 10-point change.

The locked working SESOI is

    delta_beta = 0.5.

For H1-P1 and H1-P2, the confirmatory null is directly H0: beta <= +0.5 against H1: beta > +0.5. The two one-sided Wald p values for these SESOI nulls are controlled with Holm family-wise alpha = 0.05. Ordinary tests against zero and 95% confidence intervals remain descriptive.

The threshold may only be revisited before recruitment if cognitive/measurement piloting demonstrates that the signed-action instrument cannot resolve effects of this magnitude. It may not be changed using human H1 outcome data.

## 2. Signed-discrepancy symmetry tolerance

In M2 define

    d_sym = beta_r_star + beta_r_hat.

Exact signed-discrepancy symmetry implies d_sym = 0.

The locked tolerance is

    delta_sym = 1.0.

Prospective equivalence uses the 90% confidence interval:

- wholly inside [-1,+1]: practically compatible with symmetry;
- wholly outside the equivalence region on one side: practically incompatible;
- otherwise: inconclusive.

The value 1.0 is selected from the prespecified exact-design grid because, at N=84 and compliance around 0.75 or higher, the completed Monte Carlo provided useful discrimination between M3 truth and the unconstrained M2 truth. The historical Monte Carlo used 95% intervals for this diagnostic, making that screening conservative relative to the prospective 90% TOST-style interval.

## 3. M4 asymmetry tolerance

For M4 define

    d_asym = beta_positive + beta_negative,

where beta_negative multiplies max(-e,0). Symmetry implies d_asym = 0.

The exact-design full grid did not store the covariance needed to reconstruct d_asym after the fact, so a focused validation was run at the locked N=84 design. The independent grid used compliance 0.75/0.85, missingness-strength 0/1, M3/M4 truths, 1000 replications per cell, and candidate tolerances 0.25/0.5/0.75.

All three candidate tolerances failed the prespecified guardrails because precision was inadequate: the M3 symmetry-compatible rate was too low and the M4 material-asymmetry rate was far below the required 0.80. Therefore no delta_asym is locked. M4 asymmetry is reported descriptively using beta_positive, beta_negative, d_asym, and a 95% confidence interval.

## 4. Predictive RMSE

For models A and B define the paired holdout difference at the participant level and aggregate participant differences to the couple level for uncertainty.

RMSE comparisons are secondary evidence. Report:

- point estimate;
- t-based 95% CI across couples;
- direction;
- optional interpretation against prespecified sensitivity margins.

No RMSE comparison gates another model. No single predictive margin determines the primary H1 conclusion.

The earlier candidate grid 0, 0.1, 0.25, 0.5 remains archived as design-development information and may be shown in sensitivity analyses, but it is not a confirmatory model-selection rule.

## 5. Multiplicity safeguard

The co-primary family contains exactly:

- H1-P1: M2 beta_r_star > 0;
- H1-P2: M3 beta_e > 0.

Use one-sided Wald p values for H0: beta <= delta_beta and Holm adjustment at family-wise alpha = 0.05.

Structural equivalence/asymmetry tests and predictive RMSE comparisons are reported separately and cannot rescue failure of the co-primary family.

## 6. Interpretation safeguard

Statistical significance, practical relevance, structural compatibility, and predictive adequacy answer different questions.

A significant coefficient smaller than the SESOI is not treated as practically supported. A symmetry-compatible d_sym does not prove that people literally compute a difference score. A small RMSE difference does not establish mechanistic equality. Conversely, a predictive comparison cannot suppress a prespecified direct coefficient test.
