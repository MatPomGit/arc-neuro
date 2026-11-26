# ARC-ADHD first core task specification

Status: candidate implementation specification, version 0.1. The task is not yet frozen for Phase 0.

## 1. Purpose

The first core task should be simple enough to implement and explain, yet rich enough to support:

- sustained/selective attention;
- response inhibition;
- simple rule maintenance;
- controlled rule switching;
- participant-specific pre-challenge reference behavior;
- objective post-challenge recovery measurement.

It is not intended to measure every executive function in one task.

## 2. Candidate task

Working name: **Signal Gate**.

Narrative:

The child helps an exploratory robot pass through a sequence of signal gates. Each signal contains a simple visual attribute. The current rule determines whether to respond or withhold.

The narrative is optional presentation. The scientific task logic remains independent of artwork.

## 3. Basic trial structure

Each trial contains:

1. fixation/readiness interval if enabled;
2. stimulus presentation;
3. response window;
4. neutral feedback when configured;
5. inter-trial interval.

Response mode:

- one large tap area for GO;
- no response for NO-GO.

The task should not require precise drag gestures or multi-touch in the first version.

## 4. Stimulus dimensions

The initial implementation should use simple, easily discriminable visual features.

Candidate examples:

- color;
- shape;
- symbol category.

Avoid:

- emotionally loaded faces;
- reading-dependent words;
- culturally specific semantic knowledge;
- photographic distractors;
- rapid visual effects.

A study build should use one predefined stimulus set and log its content version.

## 5. Rule structure

Example rule A:

- GO for blue signal;
- NO-GO for orange signal.

Example rule B:

- GO for orange signal;
- NO-GO for blue signal.

The exact colors/symbols are implementation content and may be changed for accessibility before freeze.

The rule should be visually explained during tutorial and represented by a simple persistent cue during early Phase 0 if required.

## 6a. Rule calibration

Before the first eligible challenge, both A and B rule mappings are exposed in a dedicated calibration state.

The current candidate contract requires per rule:

- at least 12 valid calibration trials;
- at least 4 GO trials;
- at least 4 NO-GO trials.

Calibration provides the target-rule recovery reference used by (B) for both mappings. On timing-qualified profiles, the same reference also provides the correct-GO RT distribution required by (S) and (V). Calibration observations are never labeled as recovery events.

This calibration precedes the immediate prechallenge eligibility window. The two references serve different purposes: the target-rule calibration reference defines the mapping-specific level to which post-switch behavior is compared, whereas the immediate current-rule window only establishes readiness and challenge eligibility.

## 6. Baseline block

Purpose:

- establish stable current-rule task behavior;
- produce the immediate prechallenge eligibility reference;
- ensure the child is currently able to follow the active rule.

Baseline must contain enough valid observations for the configured challenge-eligibility rule.

The current candidate configuration uses a minimum of 12 reference observations, but this value remains unfrozen.

## 7. Controlled challenge hook

The first Phase 0 controlled challenge is an **explicit rule switch**. Other challenge families are deferred from the initial recovery-measure stabilization sample.

At an eligible event:

1. the current rule changes from A to B or B to A;
2. the application clearly presents the new rule according to the configured challenge condition;
3. the challenge onset is timestamped;
4. ordinary performance is observed;
5. the application transitions into the regulation sequence according to the study logic.

The challenge is not designed to trick the child through hidden rule changes.

The scientific manipulation is adaptation to a changed rule, not deception.

Challenge eligibility is fixed before observing the child's post-switch response. An error, omission or slowing after the switch is an outcome of the event and cannot be used retrospectively to decide that the challenge was eligible.

The complete eligibility contract is defined in `docs/challenge_event_operationalization.md`.

## 8. Trial outcomes

Required per-trial observables:

- stimulus ID;
- rule ID;
- target class;
- expected response;
- actual response;
- correctness;
- omission;
- commission error;
- response latency for valid responses;
- trial start;
- response-window close;
- current cognitive-difficulty state;
- current sensory state;
- current challenge-event ID if applicable.

## 9. Candidate recovery features

The pre-Phase 0 candidate space is deliberately restricted to three primitive features:

- **B: balanced rule success**, combining GO hit probability and NO-GO correct-rejection probability with equal conditional weight;
- **S: correct-GO slowing**, a one-sided increase in median correct GO reaction time relative to the participant-specific reference;
- **V: correct-GO variability increase**, a one-sided increase in robust reaction-time dispersion.

The allowed candidate models are exactly:

- `B`;
- `B+S`;
- `B+V`;
- `B+S+V`.

There is no timing-only recovery model. Accuracy, rule-error rate, omission rate and commission-error rate are not entered as separate equally weighted components because they partially recode the same Signal Gate response events.

The authoritative definitions, weights, minimum trial counts, hard Phase 0 gates and model-selection rule are in:

`docs/recovery_feature_operationalization.md`

and

`config/recovery_feature_candidates.phase0.json`.

The Phase 0 decision must select the smallest construct-sufficient model using measurement properties only. External clinical outcomes and treatment-group differences are prohibited model-selection signals.

For `S` and `V`, the timing reference must match the target post-switch rule and GO-stimulus identity. The immediate pre-switch RT must not be used as the timing baseline because the switch reverses the response mapping.


[Continue to part 2](core_task_specification-part-2.md)
