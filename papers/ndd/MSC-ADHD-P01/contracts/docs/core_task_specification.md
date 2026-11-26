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

## 10. Difficulty dimensions

Cognitive difficulty must be explicit and separable.

Candidate dimensions:

### D1: target/non-target probability

Changes how frequently inhibition is required.

### D2: distractor similarity

Changes perceptual discrimination without changing the response rule.

### D3: rule-switch frequency

Changes flexibility demand.

### D4: response-window duration

May alter time pressure, but should be used conservatively because mobile timing variation and motor speed can confound interpretation.

The first controller should modify at most one cognitive dimension per adaptation transition.

## 11. Sensory dimensions

Sensory complexity is not part of cognitive difficulty.

Candidate sensory controls:

- decorative animation level;
- ordinary functional audio cue on/off;
- haptic pause cue on/off;
- spoken instruction on/off.

Reducing sensory complexity must not silently alter rule difficulty.

## 12. Feedback

Allowed:

- neutral correct/continue feedback;
- neutral error indication when required by the protocol;
- non-punitive progress feedback.

Avoid:

- loss of accumulated progress;
- negative character reactions;
- countdown pressure unrelated to the scientific task;
- loud error sounds;
- public score comparison;
- performance streak pressure.

## 13. Tutorial

Tutorial/calibration should teach:

1. GO action;
2. NO-GO withholding;
3. both rule mappings used by the first rule-switch challenge;
4. the explicit rule-change cue;
5. pause/stop control.

If timing-enriched recovery candidates are being evaluated, calibration must also provide a stable correct-GO timing reference for each target rule/GO-stimulus mapping before that mapping can be used in an eligible recovery event. The first exposure to Rule B must not simultaneously serve as both rule learning and timing-based recovery measurement.

Practice trials are not analyzed as primary mechanistic events.

If comprehension remains insufficient after the configured tutorial limit, the state machine should move to protocol abort rather than repeatedly increasing pressure.

## 14. Timing

Exact trial timing remains a Phase 0 configuration decision.

Requirements:

- all timing values versioned;
- monotonic clock used for scientific event timing;
- response window long enough for the target age group;
- no assumption that mobile millisecond timing is a clinical endpoint;
- BYOD capability/qualification profile logged.

## 15. Challenge eligibility

A challenge candidate may be evaluated only during `BASELINE_TASK`.

The current executable candidate rule is:

`config/challenge_eligibility.phase0.example.json`.

The task must expose the inputs needed by that rule.

## 16. Recovery return

After regulation, the application returns to the same task family and active goal.

The child should not receive an unrelated easy minigame as a substitute for recovery.

### Recovery measurement lock

On entry to `RECOVERY_MONITORING`, create and persist one recovery measurement context containing at minimum:

- active rule ID;
- cognitive-difficulty state;
- sensory configuration;
- response-window timing;
- stimulus-distribution/content version;
- assigned cue condition when applicable;
- a deterministic context hash.

Ordinary performance adaptation is suspended until the recovery event reaches `RECOVERY_OBSERVED`, `RECOVERY_CENSORED`, or `RECOVERY_DATA_INVALID`.

If safety, an explicit child request, a technical interruption, or another higher-priority rule requires a score-relevant context change, perform the required action but mark the recovery event scientifically invalid. Do not count performance under an easier or otherwise changed context as recovery.

A cue manipulation can remain analyzable only when its assignment is defined prospectively as part of the event-level measurement context and is not adaptively changed in response to emerging recovery performance.

## 17. Safety and overload

Challenge scheduling is suppressed when:

- safety override active;
- sensory overload active;
- recent child pause;
- telemetry unhealthy;
- insufficient reference observations;
- insufficient remaining observation time;
- minimum inter-challenge interval not satisfied;
- challenge count limit reached.

The task itself must never block the global child stop control.

## 18. Active-control boundary

The active-control arm may reuse the application shell and simple visual-search/pattern mechanics.

It must not reproduce the full:

challenge → regulation → recovery → resume-goal

sequence.

If the same Signal Gate task is used in the active control, challenge-regulation functionality must be disabled and the comparison must remain scientifically interpretable.

## 19. Phase 0 acceptance criteria

The task is ready for Phase 0 only when:

- tutorial can be completed using child-facing wording;
- GO/NO-GO events are logged deterministically;
- rule switches are reproducible from configuration;
- challenge eligibility is testable;
- trial timing is monotonic and ordered;
- telemetry supports candidate recovery features;
- sensory settings do not alter cognitive rule semantics;
- child pause/stop works during every task state;
- deterministic replay reproduces controller decisions;
- application interruption does not silently generate valid-looking trials.

## 20. Deferred task extensions

Not required for first Phase 0 build:

- working-memory sequence task;
- n-back;
- delay discounting;
- auditory-only task;
- cross-modal conflict task;
- sensorimotor rhythm;
- fine-motor tracing;
- AR stop-and-go;
- environmental camera search.

These can be added only when they answer a specific research question or later intervention need.
