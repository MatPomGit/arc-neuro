# ARC-ADHD Phase 0 protocol

Status: pre-recruitment design document. This is not evidence of ethics approval, registration or participant recruitment.

## Purpose

Phase 0 is a co-design and construct-validation stage. Its purpose is to determine whether the core ARC-ADHD challenge-regulation-recovery sequence can be understood, tolerated, measured and reproduced before a feasibility study.

Phase 0 is **not** designed to estimate clinical efficacy.

## Core questions

1. Can children aged 8–12 years understand the sequence: challenge → pause → orient → select strategy → regulate → recover → resume goal?
2. Can controlled challenge events be delivered without unacceptable distress or overload?
3. Can recovery be represented by a stable behavioral score and explicit right-censoring rule?
4. Can the required telemetry be captured with sufficiently low missingness?
5. Are the regulation prompts, sensory cues and session pacing acceptable?
6. Which design elements require revision before Phase 1?

## Planned participants

Provisional target: approximately 12–20 child-caregiver dyads across iterative rounds.

The exact number is not an efficacy sample-size target. Iteration should continue until predefined design coverage is reached and no new critical comprehension or safety problem emerges across consecutive rounds.

Before recruitment, the study documentation must freeze:

- target diagnostic confirmation procedure;
- inclusion and exclusion criteria;
- medication policy;
- common comorbidity handling;
- accessibility adaptations;
- recruitment source;
- caregiver role;
- stopping and escalation rules.

## Required study roles

Before participant-facing work, the project should assign explicit responsibility for:

- clinical/developmental interpretation;
- trial/statistical methodology;
- intervention implementation;
- safety monitoring;
- data protection;
- participant/caregiver communication.

These are functional responsibilities. The detailed role matrix, separation-of-duties rules and named-assignment gate are maintained in `docs/study_roles_and_responsibilities.md`. Authorship remains based on actual scholarly contribution.

## BYOD device policy

Phase 0 uses the participant/caregiver's private Android phone.

The study therefore freezes a device-qualification policy rather than one phone model.

Before the first participant-facing session on an installation, and after a material device/OS/application change, the application should run the versioned BYOD qualification procedure defined in `docs/device_profile_specification.md`.

The qualification profile should capture only research-relevant coarse capabilities, including:

- Android/application version;
- display refresh-rate bucket;
- logical screen-size bucket;
- touch availability;
- ordinary audio availability;
- optional haptic availability;
- local-storage test;
- offline-session test;
- background/resume test;
- benchmark/performance class;
- relevant thermal/power warnings when available;
- qualification rule/version.

The default scientific telemetry must not require IMEI, device serial, Android ID, advertising ID, account identifiers, precise location, contact data, installed-app inventory, or unrelated personal media.

Qualification outcomes are:

- qualified_core;
- qualified_with_fallbacks;
- not_qualified.

BYOD qualification itself is a feasibility outcome. Phase 0 should report the proportion of screened private phones that qualify, qualify with fallbacks, or fail qualification, together with coarse reasons for failure.

If a participant changes phone or the execution profile changes materially between sessions, the device must be requalified. Timing-sensitive variables must not be assumed directly comparable across materially different device profiles without the prespecified reset/sensitivity rule.

## Session structure

A target Phase 0 session contains:

1. onboarding and assent check;
2. device and sensory-preference check;
3. tutorial when required;
4. mandatory A/B rule calibration;
5. baseline executive-control task;
6. one or more eligible controlled rule-switch challenge events;
7. pause and orientation prompt;
8. strategy selection;
9. regulation action;
10. recovery monitoring;
11. return to the interrupted goal;
12. brief structured feedback;
13. caregiver feedback where relevant;
14. session close and adverse-event check.

The number of challenge events per session must remain bounded and is frozen before each iterative round.

## Controlled challenge

The first Phase 0 recovery-measure stabilization round uses **one challenge family only: an explicit Signal Gate rule switch A→B or B→A**.

Recoverable errors, temporary interruptions and other non-threatening changes remain conceptual later extensions. They are not pooled into the first Phase 0 recovery event sample.

Both rule mappings are calibrated before the first challenge. This prevents first-time rule discovery from being confused with recovery from a changed control demand. Calibration trials are not recovery events.

Core challenge eligibility requires, among other prespecified conditions:

- `BASELINE_TASK` state and Signal Gate task identity;
- distinct current and target rules;
- explicit switch cue available;
- both rule mappings calibrated;
- at least 12 valid immediate eligibility-reference observations under the current rule;
- at least 4 GO and 4 NO-GO eligibility-reference trials;
- a stable target-rule recovery reference from `RULE_CALIBRATION` for the post-switch rule and GO-stimulus mapping;
- a fresh reference after a pause and after the previous recovery event;
- no already-open recovery event;
- healthy required telemetry;
- no technical interruption, active overload or safety override;
- sufficient trial/time separation from the previous event;
- remaining session time covering the complete locked event budget.

The immediate eligibility reference is not the (q_e(t)) baseline. Recovery normalization uses the separate target-rule calibration reference, which avoids comparing post-switch performance under one mapping with baseline performance under the opposite mapping.

Challenge eligibility is determined **before** the switch. An event is not retrospectively accepted because the child made an error, slowed, or otherwise showed visible destabilization.

Timing-feature eligibility is tracked separately. A core behavioral event may remain valid for (B) when the phone timing profile is unqualified. (S) and (V) additionally require a target-rule timing reference matched to the post-switch rule and GO-stimulus identity.

The authoritative contract is `docs/challenge_event_operationalization.md` and the executable rule is `config/challenge_eligibility.phase0.example.json`.

The current 30 s interchallenge interval and maximum of three challenges per session are project-specific candidate pacing values. They require final ratification with the Phase 0 safety/session configuration before recruitment.

## Regulation strategies

The initial strategy library may include:

- paced breathing;
- brief muscle release;
- grounding/orienting;
- attentional redeployment;
- simple reappraisal;
- problem solving;
- controlled brief movement.

The study does not assume that one strategy is universally optimal.

The following should be recorded:

- strategy offered;
- strategy selected;
- whether selection was child-initiated or prompted;
- strategy completion;
- explicit child difficulty/overload input;
- reason for any intervention change.

## Sensory channels

Visual presentation is required.

Audio and haptics are optional. The session must remain usable when either is disabled.

Cognitive difficulty and sensory load are separate variables. A child who reports sensory overload should not automatically be treated as unable to perform the cognitive task.

## Recovery measurement

Phase 0 is the calibration stage for the recovery measure.

For every eligible challenge event, the system records sufficient data to determine:

- the pre-challenge reference state;
- the core-versus-timing feature eligibility status;
- candidate B/S/V feature deficits;
- candidate recovery score;
- whether the recovery criterion is met;
- recovery latency when observed;
- right-censoring when recovery is not observed before the event window closes;
- technical missingness separately from non-recovery.

Parameter calibration follows `docs/recovery_metric_calibration_plan.md`.

No external clinical outcome may be used to choose the recovery definition during Phase 0.

## Outcomes

### Primary Phase 0 outcomes

- sequence comprehension;
- task/challenge comprehension;
- valid recovery-record proportion;
- recovery censoring proportion;
- telemetry completeness;
- BYOD qualification and fallback rate;
- device/profile-change rate and technical interruption burden;
- overload/stop events;
- critical usability or safety failures.

### Secondary descriptive outcomes

- strategy selection distribution;
- challenge-type completion;
- session duration;
- child-rated difficulty/comfort;
- caregiver-reported acceptability;
- optional qualitative usability comments.

Clinical symptom change is not a Phase 0 endpoint.

## Iterative rounds

Each round should freeze:

- application version;
- challenge rules;
- strategy wording;
- sensory configuration;
- recovery candidate definition;
- telemetry schema;
- session procedure.

After a round, changes may be made based on predefined design objectives.

Every change must record:

- problem observed;
- evidence supporting the change;
- affected construct;
- new version;
- whether the change alters interpretation of data collected previously.

Data from materially different versions should not be pooled without explicit justification.

## Provisional progression criteria

The authoritative criteria are maintained in `docs/progression_criteria.md`.

Key Phase 0 targets currently include:

- at least 85% sequence completion after onboarding with no more than one neutral prompt;
- at least 90% of eligible challenge events yielding a valid recovery time or explicit right-censoring status;
- at least 95% completeness of required telemetry fields;
- no unresolved critical safety/comprehension failure across two consecutive iterative rounds.

These are ARC-ADHD design targets, not universal literature thresholds.

## Safety and stopping

The child can stop or pause at any time without penalty.

A challenge is stopped or suppressed when any prespecified condition occurs, including:

- explicit stop request;
- clear distress;
- sensory overload;
- repeated failure beyond the permitted challenge envelope;
- technical condition that compromises safe continuation.

An intervention-related serious adverse event or recurrent unmitigated safety pattern stops progression pending formal assessment.

## Data protection

Phase 0 uses pseudonymous research identifiers.

The core study does not require:

- front-camera facial sensing;
- raw continuous video;
- raw continuous audio;
- AR spatial mapping;
- outdoor geolocation.

Data handling must be documented before recruitment, including lawful basis, access, retention, deletion/withdrawal procedure and controller/processor responsibilities where applicable.

## Analysis

Phase 0 analysis is descriptive and measurement-focused.

Report:

- numerator and denominator for each progression criterion;
- confidence intervals where informative;
- missingness by reason;
- recovery censoring by challenge type;
- telemetry failure modes;
- distribution of candidate recovery features;
- within-person event counts;
- qualitative usability themes where collected.

Do not perform or interpret a clinical efficacy test.

## Phase 0 output package

Before progression, archive:

- protocol version;
- intervention manifest;
- application build hash;
- challenge-rule version;
- recovery calibration report;
- telemetry schema version;
- progression-criteria decision;
- deviations;
- adverse-event summary;
- list of unresolved design issues.

The Phase 1 build is a new frozen version and must not be inferred automatically from Phase 0 code.
