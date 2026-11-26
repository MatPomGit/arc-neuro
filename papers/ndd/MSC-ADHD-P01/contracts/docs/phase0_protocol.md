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


[Continue to part 2](phase0_protocol-part-2.md)
