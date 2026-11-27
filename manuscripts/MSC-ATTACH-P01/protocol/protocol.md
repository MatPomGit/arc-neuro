# ARC H1 pilot protocol

## 1. Scientific objective

The purpose of this study is to test the minimum empirical hinge of ARC without protecting one mathematical representation in advance.

H1-P1 asks whether desired relational state contributes to subsequent signed regulation beyond perceived state, context, and action history in the unconstrained M2 model.

H1-P2 asks whether signed desired-minus-perceived discrepancy predicts subsequent signed regulation in the preregistered direction in M3.

M2, M3, and M4 are then structurally characterized using direct coefficient contrasts. Temporal-holdout RMSE supplies secondary predictive evidence but does not determine whether another prespecified model may be interpreted.

The study tests temporal association and representation, not a unique latent computational controller.

## 2. Design

The temporal design is a 14-day intensive longitudinal dyadic study. The sample-size target is temporarily reopened only because the confirmatory lag definition changed.

- analysis target: provisional; 84 couples was the previous calibrated target and the final target will be the smallest of 72/84/96/108/120 satisfying the prespecified comparable-lag recalibration guardrails;
- 6 synchronized prompts per day;
- 84 planned prompts per participant;
- planning prompt compliance: approximately 0.75 or higher.

N = 84 was selected by the completed historical exact-design Monte Carlo because it was the smallest tested candidate robust to the then-current data-sufficiency criterion at approximately 75% compliance under the informative-missingness stress condition. That run included prompt 1 -> 2; therefore the final N is not frozen until the focused comparable-lag recalibration is completed.

The enrollment ceiling must be set separately from an explicit retention assumption because couple-level attrition was not calibrated by the Monte Carlo. No sample-size adaptation may depend on observed H1 effects, p values, structural labels, or holdout performance.

## 3. Eligibility

Proposed inclusion criteria:

- age 18 years or older;
- current romantic relationship of at least 6 months;
- cohabiting with the enrolled partner during the 14-day sampling period;
- both partners consent independently;
- both partners use a compatible smartphone and can receive study prompts;
- sufficient language proficiency for the validated baseline measures and ESM items.

Proposed exclusion criteria:

- inability to provide informed consent;
- planned separation from the partner for most of the sampling period;
- participation by only one member of the couple after enrollment.

Relationship duration and cohabitation thresholds are design decisions and should be reviewed during ethics preparation.

## 4. Baseline session

Required:

- informed consent;
- age and basic demographic variables needed for sample description;
- relationship duration;
- cohabitation duration;
- ECR-R attachment anxiety and avoidance;
- participant and couple pseudonymous identifiers;
- usual waking interval for prompt scheduling.

Optional, secondary:

- a validated positive secure-base representation measure if a scoring workflow is ready before preregistration.

Mentalized affectivity, emotion-regulation flexibility, and disorganization measures are deliberately omitted from the minimum H1 protocol unless there is a specific secondary hypothesis and acceptable burden.

## 5. Prompt schedule

Each participant receives six prompts per day across the person's waking period. Both partners receive synchronized prompts.

The scheduler should:

- stratify prompts across the waking day;
- randomize prompt time within each stratum;
- maintain a minimum interval between prompts;
- store scheduled and actual response timestamps;
- expire prompts after a preregistered window;
- identify the first prompt of each day so that overnight lags can be excluded.

The exact operational schedule is now locked in `operational_rules.md`: one shared 14-hour waking window per couple, six equal 140-minute strata, minimum 90-minute scheduled separation, one reminder at 15 minutes, and expiry after 30 minutes. The complete schedule is generated before day 1.

## 6. Within-prompt sequence

At each prompt, item order should preserve the intended temporal interpretation as far as self-report permits.

Current-state block:

1. perceived closeness now;
2. desired closeness now;
3. current negative affect or attachment-relevant distress;
4. whether a salient relational stressor or conflict occurred since the prior prompt.

Interval block:
5. approach/proximity-seeking action since the prior prompt;
6. overt distancing/space-seeking action since the prior prompt;
7. internal suppression/disengagement since the prior prompt;
8. perceived partner responsiveness/availability since the prior prompt;
9. interaction context, including whether meaningful contact occurred.

At prompt t+1, the interval block refers to the period after prompt t. This permits the primary lag e(t) -> a(t+1).

## 7. Core variables

Perceived relational state:
r_hat(t) = current perceived closeness to partner, 0-100 VAS.

Desired relational state:
r*(t) = current desired closeness to partner, 0-100 VAS with identical anchors.

Relational discrepancy:
e(t) = r*(t) - r_hat(t), range -100 to +100.

Approach action:
intensity of behavior aimed at increasing closeness, support, reassurance, or contact since the previous prompt.

Distance action:
intensity of behavior aimed at increasing distance or space, withdrawal, or reduced engagement since the previous prompt. This observed action channel is not a direct measure of experienced autonomy, autonomy satisfaction, or attachment avoidance.

Primary signed action:
a_signed(t) = approach(t) - distance(t), range -100 to +100.

Internal regulation:
suppression, minimization, distraction, or cognitive disengagement without an overt interpersonal action. This is secondary because avoidant regulation may occur without visible partner-directed behavior.

## 8. Primary H1 estimands

The primary H1 estimands are direct within-person coefficients rather than a sequential predictive winner.

Co-primary:

- H1-P1: M2 within-person desired-state coefficient beta_r_star;
- H1-P2: M3 within-person discrepancy coefficient beta_e.

Both are expected to exceed the locked relevance threshold delta_beta = 0.5. Full H1 support requires Holm-adjusted one-sided Wald rejection of H0: beta <= delta_beta for both tests at family-wise alpha = 0.05.

Structural characterization is separate:

- M2 d_sym = beta_r_star + beta_r_hat tests compatibility with the signed-discrepancy equality restriction;
- M4 d_asym = beta_positive + beta_negative tests asymmetry because beta_negative multiplies max(-e,0).

Temporal-holdout participant RMSE remains the locked predictive metric but is secondary evidence and does not gate interpretation of M2, M3, or M4.

## 9. Same-day lag definition

A primary lag pair is valid only under the locked `operational_rules.md`: adjacent prompt numbers within one study day, both prompts inside their response windows, complete required H1 fields, no technical-invalid flag, and actual response-to-response elapsed time between 60 and 240 minutes inclusive.

Missed prompts break the lag. Overnight transitions and bridging across missed prompts are excluded.

## 10. Primary and secondary outcomes

Primary:
signed interpersonal action.

Mandatory sensitivity outcomes:

- approach action;
- distancing action.

Secondary:

- internal suppression/disengagement;
- perceived partner responsiveness;
- next-prompt perceived closeness;
- negative affect.

A cancellation of simultaneously high approach and distance in the signed score must be detectable through the two component analyses.

## 11. Data quality

The following are reported before hypothesis testing:

- response rate per participant;
- response rate by day and prompt stratum;
- response latency;
- number of valid same-day lag pairs;
- within-person SD for r_hat, r*, e, approach, distance, and signed action;
- floor/ceiling frequencies;
- missingness by baseline attachment dimensions and relationship characteristics.

For confirmatory dynamic interpretation, the current planning criterion is that at least 100 individuals provide at least 30 valid same-day lag pairs, and each confirmatory participant must also provide at least 3 valid holdout lags on days 12-14. If the aggregate criterion is not met, H1 analysis is reported as feasibility/exploratory rather than definitive.

## 11.1 Measurement-reactivity diagnostic

Repeated assessment of perceived and desired closeness may itself increase discrepancy salience, alter desired-state reports, or change regulation. Before confirmatory interpretation, report study-day trends in r_hat(t), r*(t), and e(t).

The reactivity diagnostic is prespecified as descriptive/sensitivity evidence, not a third confirmatory hypothesis:

- fit study day as a fixed linear trend after the locked time-of-day/context terms;
- inspect whether r_hat, r*, or e show material monotonic drift across the 14 days;
- refit the primary H1 models with study day and a study-day-by-discrepancy term as a sensitivity analysis;
- report whether H1-P1/H1-P2 conclusions materially change.

A day trend is not interpreted as proof that measurement caused the change, because genuine relationship change, habituation, burden, and selective missingness can generate the same pattern. The purpose is to detect sensitivity of the ARC conclusions to repeated-measurement drift.

## 12. Predictive holdout

The last three study days are reserved as a temporal holdout for the predictive comparison.

Training period:
days 1-11.

Test period:
days 12-14.

No transformation, lag rule, interaction, hyperparameter, or model-selection decision may be changed after viewing test-period performance.

Five locked models are compared:

- M0: context plus autoregressive action terms;
- M1: M0 plus perceived closeness;
- M2: M0 plus perceived and desired closeness as separate predictors;
- M3: M0 plus signed desired-minus-perceived discrepancy;
- M4: M0 plus separate positive and negative discrepancy components.

The five models are fitted as a locked family, but they are not evaluated through a sequential winner-takes-all gate. H1-P1 is tested directly in M2, H1-P2 directly in M3, and M2/M4 structural contrasts are interpreted separately.

Participant-level RMSE on days 12-14 is the locked predictive metric. Model differences are paired within participants, aggregated at the couple level for uncertainty, and reported as secondary predictive evidence. Pooled RMSE is descriptive only.

## 13. Statistical analysis

The confirmatory estimator is Gaussian GEE with identity link, couple-level clustering, independence working correlation, bias-reduced sandwich covariance, statsmodels 0.15.0, maximum 100 iterations, and convergence tolerance 1e-8.

The confirmatory context set is fixed as:

- current negative affect/distress;
- relational stressor available at t;
- meaningful partner interaction/contact available at t;
- prompt stratum/time of day;
- actual elapsed time.

Confirmatory autoregressive rows use only adjacent same-day transitions 2->3, 3->4, 4->5, and 5->6. Prompt 1 -> 2 is excluded because the source action at the first prompt summarizes the overnight/first-of-day interval rather than a standardized preceding same-day ESM interval.

Primary reporting:

- H1-P1 beta_r_star in M2 with estimate, SE, 95% CI, raw one-sided p value, Holm-adjusted p value, and SESOI classification;
- H1-P2 beta_e in M3 with the same quantities;
- M2 d_sym with prospective 90% equivalence interval relative to delta_sym = 1.0;
- M4 beta_positive, beta_negative, and d_asym;
- participant/couple-clustered holdout RMSE differences as secondary predictive evidence;
- raw and person-centered descriptive distributions;
- mandatory approach and distance component analyses.

The analysis uses actual elapsed time because semi-random sampling produces unequal intervals. No data-driven model or covariate selection is permitted.

## 14. Missing data

Missing ESM prompts are not retrospectively reconstructed.

The report distinguishes:

- intermittent nonresponse;
- missed full days;
- study withdrawal;
- technical failure.

The primary analysis uses observed valid lag pairs and does not reconstruct missed prompts. The mandatory sensitivity is stabilized inverse-probability weighted GEE using the locked history-based response model in `missing_data_plan.md`. Only the final truncation rule remains FINAL BEFORE DATA and must be selected from the prespecified candidates using targeted IPW operating-characteristic and positivity/ESS diagnostics.

## 15. H1 interpretation

Full H1 support requires both co-primary tests:

- H1-P1: Holm-adjusted one-sided Wald p < 0.05 for H0: beta_r_star <= delta_beta = 0.5;
- H1-P2: Holm-adjusted one-sided Wald p < 0.05 for H0: beta_e <= delta_beta = 0.5.

Exactly one supported co-primary test is partial support. Neither supported under adequate data quality is no confirmatory support. Insufficient data, nonconvergence, or inadequate precision yields an inconclusive result.

Representation is characterized separately. M2 signed-discrepancy symmetry is supported when the 90% CI for d_sym lies wholly inside [-1.0,+1.0]. A wholly external interval is evidence against that restriction; overlap is inconclusive.

M4 asymmetry is secondary structural evidence. The completed focused validation did not support any prespecified practical-equivalence tolerance at N=84, so d_asym is reported with a 95% confidence interval without a confirmatory symmetry/asymmetry threshold.

Holdout RMSE is secondary convergent/discordant evidence. It cannot block evaluation of a prespecified model and cannot rescue failure of the co-primary inferential family.

## 16. Ethics and participant burden

The ESM module should remain short enough for completion within roughly 60-90 seconds. Sensitive relationship items require:

- separate consent from each partner;
- no disclosure of one partner's answers to the other;
- clear withdrawal procedures;
- a protocol for distress and conflict escalation triggered by study participation;
- secure pseudonymous storage of couple linkage.

## 17. Progression rule

Proceed to the larger H2-H4 program only if:

- compliance and lag-pair criteria are met;
- r_hat and r_star show sufficient within-person variation;
- the locked GEE model family is estimable without severe convergence or identifiability problems;
- the co-primary H1 result is full or partial support with a scientifically interpretable structural profile.

A purely predictive RMSE advantage or a statistically significant secondary construct is not sufficient by itself to trigger progression.


