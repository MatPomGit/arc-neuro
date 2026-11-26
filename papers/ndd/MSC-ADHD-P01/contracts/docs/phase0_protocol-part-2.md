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
