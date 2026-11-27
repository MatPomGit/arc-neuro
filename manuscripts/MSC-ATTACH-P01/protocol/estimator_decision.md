# H1 confirmatory estimator decision

Date: 27 September 2026

Status: locked before human outcome data.

## Decision

The primary H1 estimator is a Gaussian generalized estimating equation (GEE) with:

- identity link;
- couple-level clustering using `couple_id`;
- independence working correlation;
- bias-reduced sandwich covariance;
- explicit within-person and between-person decomposition;
- `statsmodels==0.15.0`;
- maximum 100 iterations;
- convergence tolerance `1e-8`.

There are no Bayesian priors and no required random-effects distribution in the primary H1 estimator.

## Why GEE rather than making DSEM mandatory?

H1 is currently an architecture and representation test. It asks whether average within-person state/target information improves prediction of subsequent action and whether M2, M3, or M4 is the justified representation.

The first H1 test does not require identification of a person-specific latent controller or estimation of the distribution of individual dynamic slopes.

GEE is therefore a better primary match because it:

1. directly estimates population-average regression parameters;
2. allows all repeated observations from both partners to remain clustered at the couple level;
3. separates mean-model specification from the exact working covariance model;
4. permits a simple locked covariance structure rather than data-driven covariance selection;
5. supports robust sandwich inference;
6. can be evaluated directly under the exact M0-M4 predictive hierarchy.

The bias-reduced sandwich covariance is used because ordinary robust covariance can have poor finite-cluster behavior. The design currently considers roughly 50-84 couples, so finite-cluster performance is relevant.

## Why independence working correlation?

The independence structure is deliberate rather than an assumption that observations are actually independent.

All observations from a couple remain in one GEE cluster. The independence structure only avoids estimating a working correlation parameter from the confirmatory data. Robust covariance is used for misspecification.

This keeps the H1 estimator stable, auditable, and identical across M0-M4.

## Heterogeneity is not ignored

The exact Monte Carlo generator contains:

- couple random action intercepts;
- participant random action intercepts;
- participant-specific relational slope heterogeneity;
- couple-level state differences;
- participant-level state/target differences;
- shared dyadic stressors.

The primary GEE does not parameterize these random effects explicitly. Instead, the design simulation asks whether the simpler marginal estimator retains acceptable bias, interval coverage, type-I error, convergence, and model-selection behavior when such heterogeneity exists.

If it does not, the estimator decision must be revised before data collection.

## Dyadic clustering

The robust cluster is the couple, not the individual.

This choice allows:

- repeated observations within a participant;
- dependence between partners;
- shared couple-level shocks

to remain inside the same robust covariance cluster.

## Leakage safeguard

Within/between decomposition uses participant means calculated only from observed days 1-11 prompts.

Days 12-14 never contribute to:

- person means;
- centering;
- feature engineering;
- model specification;
- model selection.

This preserves the temporal holdout.

## Prediction

Primary prediction is population-average prediction from the locked GEE.

Primary metric:
participant-paired RMSE on days 12-14.

This study asks whether the relational architecture improves prediction for later observations in participants already observed during training. Generalization to entirely new participants is a separate and stronger validation target.

## Sensitivity analyses

The mandatory missing-data sensitivity is history-based stabilized IPW-GEE. It retains the locked M0-M4 mean models, couple cluster, identity link, and independence working correlation. The primary unweighted GEE uses the bias-reduced sandwich covariance; the weighted sensitivity uses the ordinary robust sandwich covariance because the pinned statsmodels 0.15.0 implementation fails when observation weights are combined with its bias-reduced covariance calculation. Weighted finite-cluster coverage is evaluated explicitly in targeted Monte Carlo rather than assumed.

DSEM and mixed-effects models may be used as additional prespecified sensitivity analyses after the primary specification is locked.

They are not alternate primary estimators that can be selected after inspecting outcomes.

H2 is a separate problem. Its central question is random-slope/cross-level moderation, so the H2 estimator should be selected and powered separately.

## Reproducibility

Pinned dependencies are stored in:

`software/study_design/requirements-lock.txt`

Exact-design configuration:

`studies/pilot_h1/exact_design_config.json`

Implementation:

`software/study_design/h1_exact_monte_carlo.py`

Ordinary CI runs only a deterministic smoke test. The full factorial Monte Carlo is intentionally not a commit-time workflow.
