# ARC-ADHD core statistical analysis plan

Status: pre-pilot framework. This is not yet a locked SAP because the external primary outcome and assessment schedule are not frozen.

## Analysis hierarchy

The programme separates:

1. feasibility estimands;
2. mechanistic recovery estimands;
3. independent near-transfer outcomes;
4. the future confirmatory far-transfer endpoint.

The pilot must not be reinterpreted as confirmatory because a nominal p value is small.

## Analysis populations

### Intention-to-treat

All randomized participants are analysed according to randomized allocation for external pilot outcomes, regardless of adherence.

### Safety population

All participants who start at least one assigned session contribute to safety summaries according to the intervention actually received.

### Mechanistic event population

All prespecified eligible challenge events contribute to recovery analysis when a valid recovery or censoring status can be determined. Events are not removed because recovery was slow or absent.

## Pilot clinical estimand

The provisional pilot estimand is the between-group difference at post-intervention on the selected external regulation/dysregulation outcome, conditional on baseline value and prespecified design factors.

The purpose is to estimate:

- direction and magnitude;
- confidence interval;
- variance;
- baseline-follow-up correlation;
- missingness;
- clustering/repeated-measure structure needed for the future confirmatory calculation.

No binary efficacy declaration is based on this pilot estimand.

## Longitudinal model

If baseline, post and follow-up measurements are available, a repeated-measures model can include:

- treatment group;
- time;
- treatment-by-time interaction;
- baseline stratification variables;
- participant-level repeated observations.

The exact covariance structure must be selected without outcome-driven fishing and documented before the pilot database is locked.

## Recovery estimand

For eligible challenge event e, define three ordered process times:

- `T_pre`: challenge onset to entry into `RECOVERY_MONITORING`;
- `T_rec`: recovery-monitoring onset to the first score update beginning a fully confirmed qualifying stability run;
- `T_total = T_pre + T_rec`: challenge onset to the same stable-return threshold entry.

The **primary mechanistic time-to-event quantity is T_rec**, because this isolates measurable post-regulation performance recovery from the duration of pause/orient/strategy execution. `T_pre` and `T_total` are secondary process variables and must be reported rather than silently folded into `T_rec`.

T_rec is right-censored when a complete qualifying stability run is not confirmed before the monitoring censor limit. The censor clock begins at `RECOVERY_MONITORING` onset, not challenge onset.

The event-level analysis should account for:

- repeated events within sessions;
- repeated sessions within participants;
- challenge type;
- session number;
- prespecified difficulty/sensory state;
- censoring.

Each recovery event also has a locked measurement context containing the active task rule, cognitive-difficulty state, sensory configuration, response-window timing, stimulus distribution and any prespecified event-level cue assignment. Ordinary adaptation is suspended while recovery is measured. A score-relevant context change invalidates the mechanistic event; it is not recoded as faster recovery or ordinary right-censoring. Scientific recovery validity is therefore modeled separately from telemetry completeness.

Candidate models include mixed-effects survival or accelerated-failure-time approaches. Model choice should be driven by the observed data-generating structure in feasibility work, then frozen before pilot inferential analysis.

## Recovery-score sensitivity analysis

The primary values of delta, stability-window count w (in consecutive score updates) and monitoring censor limit c_e are fixed before pilot outcome inspection.

Sensitivity analyses can examine a small preregistered grid around these values. They are robustness checks and cannot replace the primary definition if the primary analysis is inconvenient.

## Micro-randomized cue analysis

If cue events are randomized within participants, the proximal estimand is the average effect of the assigned cue condition on the prespecified immediate outcome among events eligible for randomization.

The analysis must include:

- eligibility rule;
- randomization probability;
- carryover window;
- proximal outcome window;
- repeated-event dependence;
- missing-event handling;
- prespecified moderators only.

This component is mechanistic and does not create additional clinical primary endpoints.

## Missing data

Missingness should be reported by arm, time point and reason.

For the future confirmatory outcome:

- complete-case analysis alone is insufficient if missingness is material;
- a prespecified multiple-imputation or likelihood-based approach should be used when assumptions are plausible;
- sensitivity analysis should examine departures from the primary missing-at-random assumption when dropout may depend on unobserved outcome severity.

Mechanistic event missingness is handled separately from right-censoring. A missing telemetry event is not equivalent to a participant who failed to recover. A complete telemetry record can also be scientifically invalid when the recovery measurement context changes before event closure; this third state must remain separate from both missingness and censoring.

## Multiplicity

The core programme has one future confirmatory primary clinical endpoint.

Secondary outcomes, recovery analyses and cue-level experiments are labelled accordingly. Companion papers on facial feedback, bilateral audio and embodied/AR interaction are independent research questions and do not become evidence for the core primary endpoint.

## Effect reporting

Report effect estimates with confidence intervals and clinically interpretable units.

Avoid:

- declaring equivalence from a nonsignificant superiority test;
- converting censored recovery times into maximum observed values;
- selecting favorable delta/w values after seeing results;
- subgroup claims based only on nominal interaction patterns;
- treating in-game improvement as a clinical endpoint.

## Pilot-to-confirmatory handoff

The pilot should provide the inputs needed to design the definitive trial:

- standard deviation or other scale parameter for the selected primary endpoint;
- baseline-post correlation;
- follow-up retention;
- expected adherence;
- active-control response;
- recruitment rate per site and month;
- expected missingness;
- plausible minimally important effect, justified clinically rather than chosen from the pilot point estimate alone.

The confirmatory trial should then be prospectively registered, described using SPIRIT 2025 and TIDieR, and reported using CONSORT 2025.

## BYOD device heterogeneity

The intervention is delivered on participant/caregiver private Android phones under a frozen compatibility/qualification policy.

Before the pilot analysis is locked, prespecify:

- the coarse capability/performance fields retained for analysis;
- how installation/device-profile changes are identified;
- whether timing-sensitive task features are reset, stratified or otherwise handled after a material profile change;
- sensitivity analyses for capability/performance class when reaction-time-derived variables materially contribute to a mechanistic outcome;
- reporting of qualification, fallback and nonqualification rates.

Exact manufacturer/model should not be introduced post hoc as an unrestricted moderator simply because it is available. Device-related analyses must be limited to prespecified research-relevant capability dimensions.

BYOD qualification outcome is a feasibility/process variable, not a clinical endpoint.
