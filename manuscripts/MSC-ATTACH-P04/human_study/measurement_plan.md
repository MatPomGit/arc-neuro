# M04: ecological measurement and bridge protocol

Status: candidate plan; no human observations and no new validated instrument. This document describes measurement, not controller diagnosis. It does not change the authoritative H1 instrument.

## Construct-to-observation mapping

| Construct | Candidate source / scale | Timing and interpretation |
|---|---|---|
| Perceived closeness r_hat | H1 A1, 0–100, no closeness/bond to very strong closeness/bond | Current state; self-report, not objective partner behavior |
| Desired closeness r_star | H1 A2, same 0–100 anchors | Current wish, not ideal relationship; keep separately from A1 |
| Discrepancy e | r_star − r_hat, −100 to 100 | Derived value; retain both components and their measurement error |
| Approach | H1 C1, 0–100 | Actions since preceding prompt; not a trait or PID gain |
| Distancing | H1 C2, 0–100 | Separate from autonomy satisfaction and trait avoidance |
| Internal regulation | H1 C3, 0–100 | Suppression/disengagement; separate from overt distancing |
| Signed action | C1 − C2, −100 to 100 | Secondary summary; simultaneous high actions can cancel |
| Negative affect | H1 A3, 0–100 | Momentary distress; not a clinical symptom diagnosis |
| Stressor and impact | H1 B1 yes/no; B1a 0–100 if yes | Context; no identifying narrative of the event |
| Meaningful contact | H1 B2 yes/no | In-person or remote; not message content or contact monitoring |
| Perceived responsiveness | H1 D1, 0–100 if contact occurred | Participant's perception; not verified partner intent |
| Attachment anxiety L / avoidance U | Candidate ECR-R, authorized language version pending | Baseline contextual dimensions; comparator for M04, not generator ground truth |
| Observation process | Scheduled/delivered/opened/submitted timestamps, timezone, item timing and missingness reason when available | Distinguish actual elapsed time, skipped item, nonresponse and technical failure |

Full item wording and conditional logic: [H1 Polish candidate](../../../studies/pilot_h1/survey_items_pl.md). Avoid duplicating or silently changing that instrument. A1 precedes A2; C1/C2 can both be high. Daily first prompts have a different reference period. The M04 design must prespecify admissible lags and overnight handling; do not transfer H1 exclusions without checking the actual schedule.

## Existing questionnaire versus experimental items

The original ECR-R has two 18-item subscales, anxiety and avoidance. Follow the documented original response format, reverse coding and subscale means; do not score a global controller or security index. Its original documentation does not establish the validity, rights or scoring details of any particular Polish translation. Before deployment, name the exact adaptation, primary validation source, permission/license, reference relationship, item order, response anchors, scoring key and missing-item rule. Do not improvise a shortened translation or reproduce protected item banks in Git.

ECR-R is a possible comparator for incremental prediction, never a label for P/PI/PID. Momentary H1 items remain experimental; single items have no internal-consistency coefficient. For multi-item trait scales report sample-specific reliability and its uncertainty, and avoid treating a high coefficient as discriminant validity. Do not add S/M/F, dominance or disorganization batteries without an independently justified question and burden budget.

## Measurement quality and burden

Interview participants about the meaning of desired versus perceived closeness, internal regulation versus distancing, and simultaneous approach/distance. Record item-specific misunderstanding categories and decisions. Feasibility reporting includes completion time median/IQR/90th percentile, item skipping, prompt completion, floor/ceiling proportions, within-person variance and notification failures. These are observed quality outcomes, not selection filters designed to favor a model.

Perceived and desired scores share response method and can have correlated errors. Difference scores can amplify or conceal error. The simulator's analyst-noise SD 0.04 must not be described as questionnaire reliability. Temporal aggregates and estimated derivatives/integrals depend on elapsed time, missingness and smoothing. Fit preprocessing on development data only, then freeze it. Distinguish within-person change from between-person mean differences.

Missingness is not zero action. Conditional nonadministration is not nonresponse. No forward filling or interpolation is assumed; any such processing requires a prospective justification, maximum gap and a sensitivity analysis. Participant reports of partner behavior do not establish dyadic causality. Do not request EEG, video, audio, location, message logs or wearable data in this proposed observational package.

## Verified sources and unresolved details

- Original ECR-R documentation: https://labs.psychology.illinois.edu/~rcfraley/measures/ecrr.htm (checked 2026-10-07). This supports the original instrument structure only; Polish adaptation remains unresolved.
- ARC definitions: `model/specification.json`, version 0.9.0. No model semantic revision is introduced here.
- H1 candidate instrument: `studies/pilot_h1/survey_items_pl.md`, version 0.2-pl-cognitive. Its preparation does not establish validity in humans.


## M04-specific prospective question and endpoints

The baseline predictor is the frozen M03 score/subscale definition, with a fixed version and validation status. The primary planned endpoint is prospectively recorded initiation of a relational action at a later prompt, distinguishing opportunity and context. This is a candidate endpoint requiring final wording, scale and analysis freeze; it is not H1's discrepancy coefficient. Self-reported daily action remains subject to shared-method bias. Private partner reports, if adopted, supplement rather than replace this endpoint and require separate consent; partner agreement is not objective mechanistic ground truth.

The main association is between-person incremental predictive value of baseline propensity, beyond authorized adjacent-trait measures and prespecified context/opportunity terms. Within-person state-to-action associations are separately labeled secondary and cannot be read as effects of a stable person-level score. Define lag windows, overnight gaps, reverse temporal checks, missingness, dependence and a model-appropriate primary metric prospectively. No causal interpretation follows from observational prediction.

Validation: reserve entire unseen people/couples for generalization, keeping all dyad members together; additionally distinguish later-time performance in known people. Freeze scoring, preprocessing, comparator set and tuning on development only. Simulation-calibrate participants, repeated observations, missingness and effect/precision assumptions; prompts are not independent participants. Retain skipped items as missing, not zero actions.

Any relationship of scale scores to fitted dynamic parameters is a separate secondary question, contingent on identifiability under observation conditions. Report parameter uncertainty and predictive ambiguity; an apparent gain correlation does not validate a P/PI/PID psychological type. If M03 does not yield defensible distinct scores, pause confirmation or prospectively revise M04 around an established trait with a new protocol/version. Do not recover the candidate construct by changing M04's final-test scoring.

No M03 EFA/CFA is repeated as a primary M04 result; no ARC H1/H2/H3 test is duplicated as a primary bridge result. Exact duration, prompts, sample N, burden, compensation and any dyadic module remain pending; do not adopt the H1 14 × 6 schedule without calibration.
