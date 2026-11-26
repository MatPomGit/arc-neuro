# ARC-ADHD core session state-machine specification

Status: implementation specification, version 0.1.

This document defines the minimum state machine for the core ARC-ADHD research application. It is intended to map cleanly to a Unity/C# implementation while remaining independent of Unity-specific APIs.

## 1. Design principles

The state machine must:

- make challenge, regulation, recovery and return-to-goal distinct states;
- preserve a global safety/stop path;
- never infer successful recovery from task progression alone;
- separate technical failure from right-censoring;
- remain deterministic for the same configuration, inputs and random seed;
- emit a transition event for every state change;
- reject transitions not present in the active configuration.

## 2. Core states

### BOOT

Purpose:

- initialize application runtime;
- load version/build metadata;
- initialize local durable storage.

Allowed next states:

- RESEARCH_SETUP;
- FATAL_ERROR.

### RESEARCH_SETUP

Purpose:

- load pseudonymous participant/session context;
- load study configuration;
- verify configuration hash and schema versions.

Allowed next states:

- DEVICE_QUALIFICATION;
- SAFE_STOP;
- FATAL_ERROR.

### DEVICE_QUALIFICATION

Purpose:

- run or verify the versioned BYOD qualification procedure;
- inspect mandatory core checks and optional capabilities;
- establish allowed fallbacks;
- persist the privacy-minimized capability/qualification profile;
- reject a private phone that cannot safely or validly run the configured core study.

Allowed next states:

- CAREGIVER_ONBOARDING after qualified_core;
- CAREGIVER_ONBOARDING after qualified_with_fallbacks;
- PROTOCOL_ABORT after not_qualified;
- SAFE_STOP;
- FATAL_ERROR.

### CAREGIVER_ONBOARDING

Purpose:

- present safety and logistics information;
- confirm permitted caregiver controls.

Allowed next states:

- CHILD_READINESS;
- SAFE_STOP.

### CHILD_READINESS

Purpose:

- confirm readiness;
- expose pause/stop;
- collect protocol-defined sensory preference state.

Allowed next states:

- TUTORIAL;
- RULE_CALIBRATION when tutorial is not required;
- PAUSED_BY_CHILD;
- SAFE_STOP.

### TUTORIAL

Purpose:

- teach the active task rule;
- run bounded practice;
- verify minimum comprehension if required.

Allowed next states:

- RULE_CALIBRATION;
- PAUSED_BY_CHILD;
- SAFE_STOP;
- PROTOCOL_ABORT.

### RULE_CALIBRATION

Purpose:

- expose both Signal Gate rule mappings before eligible rule-switch events;
- verify rule-specific comprehension;
- collect the target-rule/mapping-matched correct-GO timing reference when timing qualification permits;
- keep calibration observations outside the challenge/recovery event sample.

Allowed next states:

- BASELINE_TASK after calibration completion;
- PAUSED_BY_CHILD;
- SAFE_STOP;
- TECHNICAL_INTERRUPT;
- PROTOCOL_ABORT if required calibration cannot be completed.

### BASELINE_TASK

Purpose:

- perform the executive-control task;
- gather valid reference observations;
- update bounded controller state.

Allowed next states:

- CHALLENGE_PENDING;
- PAUSED_BY_CHILD;
- SAFE_STOP;
- SESSION_REFLECTION;
- TECHNICAL_INTERRUPT.

### CHALLENGE_PENDING

Purpose:

- evaluate challenge eligibility;
- select a configured challenge type;
- atomically commit challenge scheduling metadata.

Allowed next states:

- CHALLENGE_ACTIVE when eligible;
- BASELINE_TASK when suppressed;
- PAUSED_BY_CHILD;
- SAFE_STOP;
- TECHNICAL_INTERRUPT.

### CHALLENGE_ACTIVE

Purpose:

- deliver one bounded controlled challenge;
- record challenge onset;
- stop ordinary progression into new challenge events.

Allowed next states:

- REGULATION_PAUSE;
- PAUSED_BY_CHILD;
- SAFE_STOP;
- TECHNICAL_INTERRUPT.

### REGULATION_PAUSE

Purpose:

- simplify stimulation;
- establish a brief pause after the challenge.

Allowed next states:

- ORIENT;
- PAUSED_BY_CHILD;
- SAFE_STOP;
- TECHNICAL_INTERRUPT.

### ORIENT

Purpose:

- present one or more configured body/context orientation prompts.

Allowed next states:

- STRATEGY_SELECTION;
- PAUSED_BY_CHILD;
- SAFE_STOP;
- TECHNICAL_INTERRUPT.

### STRATEGY_SELECTION

Purpose:

- present the configured strategy subset;
- record selected/suggested strategy.

Allowed next states:

- STRATEGY_EXECUTION;
- PAUSED_BY_CHILD;
- SAFE_STOP;
- PROTOCOL_ABORT;
- TECHNICAL_INTERRUPT.

### STRATEGY_EXECUTION

Purpose:

- execute the selected bounded regulation strategy.

Allowed next states:

- RECOVERY_MONITORING;
- PAUSED_BY_CHILD;
- SAFE_STOP;
- TECHNICAL_INTERRUPT.

### RECOVERY_MONITORING

Purpose:

- instantiate and persist the versioned recovery measurement context;
- resume measurable task behavior under the locked task rule, cognitive difficulty, sensory configuration, timing, stimulus distribution and event-level cue assignment;
- suspend ordinary performance adaptation while the event remains open;
- compute the configured recovery score;
- track stability-window state;
- maintain censoring timer;
- invalidate the mechanistic event if a score-relevant measurement condition changes before closure.

Allowed next states:

- RECOVERY_OBSERVED;
- RECOVERY_CENSORED;
- RECOVERY_DATA_INVALID;
- PAUSED_BY_CHILD;
- SAFE_STOP;
- TECHNICAL_INTERRUPT.

### RECOVERY_OBSERVED

Purpose:

- close the recovery event as observed;
- persist recovery latency and criterion metadata.

Allowed next states:

- RESUME_GOAL;
- SAFE_STOP;
- FATAL_ERROR if durable persistence fails.

### RECOVERY_CENSORED

Purpose:

- close an otherwise analyzable event when the recovery criterion was not observed before the censor limit.

Allowed next states:

- RESUME_GOAL;
- SAFE_STOP;
- FATAL_ERROR if durable persistence fails.

### RECOVERY_DATA_INVALID

Purpose:

- close the mechanistic event as technically invalid rather than censored;
- record explicit missingness/error reasons.

Allowed next states:

- RESUME_GOAL when protocol allows continuation;
- SAFE_STOP;
- PROTOCOL_ABORT.

### RESUME_GOAL

Purpose:

- restore the interrupted task goal and ordinary task context.

Allowed next states:

- BASELINE_TASK;
- SESSION_REFLECTION;
- PAUSED_BY_CHILD;
- SAFE_STOP;
- TECHNICAL_INTERRUPT.

### PAUSED_BY_CHILD

Purpose:

- honor an explicit child pause without penalty;
- suppress new challenge events.

Allowed next states:

- previous resumable state, using explicit resume metadata;
- SAFE_STOP.

The implementation should not infer a resume target from UI history alone. The resumable source state must be stored explicitly.

### TECHNICAL_INTERRUPT

Purpose:

- handle backgrounding, temporary capability failure or recoverable runtime interruption.

Allowed next states:

- previous resumable state when validity criteria remain satisfied;
- RECOVERY_DATA_INVALID when recovery measurement is compromised;
- SAFE_STOP;
- FATAL_ERROR.

### SESSION_REFLECTION

Purpose:

- present bounded reflection or implementation-intention prompt.

Allowed next states:

- SESSION_COMPLETE;
- SAFE_STOP.

### SESSION_COMPLETE

Purpose:

- close session telemetry;
- persist upload batch;
- enter non-participant upload/summary flow.

Terminal for the child-facing session.

### SAFE_STOP

Purpose:

- stop active challenge and optional cues;
- preserve telemetry;
- end participant-facing activity safely.

Terminal for the child-facing session.

### PROTOCOL_ABORT

Purpose:

- end the research procedure because required protocol conditions cannot be satisfied, without implying a safety event.

Examples:

- tutorial comprehension criterion not reached;
- locked condition unavailable;
- required study input missing.

Terminal for the child-facing session.

### FATAL_ERROR

Purpose:

- fail closed when application integrity or durable event storage cannot be guaranteed.

Terminal.

## 3. Global transition priority

Before applying a normal transition, evaluate in order:

1. fatal integrity condition;
2. safety stop;
3. explicit child stop;
4. explicit child pause;
5. protocol abort;
6. technical interruption;
7. state-specific scientific transition;
8. ordinary progression.

A lower-priority transition cannot override a higher-priority one.

## 4. Recovery terminal-state rule

Exactly one scientific recovery terminal state may close an analyzable challenge event:

- RECOVERY_OBSERVED;
- RECOVERY_CENSORED;
- RECOVERY_DATA_INVALID.

Interpretation:

- observed = criterion satisfied for full stability window under an unchanged recovery measurement context;
- censored = criterion not observed before limit, but required telemetry and measurement context remained valid;
- invalid = scientific outcome cannot be evaluated because required data/integrity failed or because a score-relevant recovery measurement condition changed before closure.

A participant/safety action may invalidate a recovery event without implying telemetry failure. Scientific validity and telemetry completeness are separate fields.

## 5. Challenge suppression

CHALLENGE_PENDING must return to BASELINE_TASK with a suppression reason when any configured condition fails.

The authoritative suppression vocabulary is synchronized with `config/challenge_eligibility.phase0.example.json`. It includes task/rule/calibration failures, insufficient or stale references, inter-event pacing failures, insufficient locked event budget, telemetry/integrity failures, overload/safety state, recent pause and the per-session challenge limit.

Timing-only unavailability is recorded separately from core challenge suppression. In particular, an unqualified timing profile may make (S) and (V) unavailable while leaving an otherwise valid behavioral (B) event intact.

Suppression is not a failed challenge event and must not create a fake recovery record.

## 6. State entry/exit contract

Each state should implement the conceptual interface:

```
Enter(context)
Handle(input/event)
Exit(reason)
```

Study-critical state logic must not be embedded only in animation callbacks.

Animations and presentation effects may report completion to the state logic, but scientific transitions are controlled by explicit state rules.

## 7. Transition telemetry

Every state transition should record:

- session_id;
- monotonic sequence;
- monotonic timestamp;
- from_state;
- to_state;
- transition reason;
- configuration version/hash;
- active challenge_event_id if applicable;
- safety/overload state;
- controller reason code when applicable.

## 8. Unity implementation mapping

Recommended C# boundaries:

- `SessionStateMachine`: owns current state and transition validation;
- `ISessionState`: state interface;
- `SessionContext`: immutable/versioned study context plus current runtime values;
- `SafetyService`: highest-priority stop/safety signals;
- `ChallengeManager`: eligibility and challenge lifecycle;
- `RegulationManager`: strategy lifecycle;
- `RecoveryMonitor`: score/stability/censoring state;
- `TelemetryService`: durable event writes;
- `TaskController`: executive task state;
- `SensoryService`: visual/audio/haptic presentation;
- `StudyConfiguration`: locked configuration.

Do not create a separate Unity scene for every scientific state unless there is a concrete UI reason. Scene loading is not a substitute for an explicit scientific state machine.

## 9. Determinism

Deterministic replay requires the transition logic to depend only on:

- frozen configuration;
- ordered input events;
- explicit current state;
- versioned controller state;
- recorded random seed/assignments.

Wall-clock time, network responses, frame rate and unlogged global state must not alter study-critical decisions.

## 10. Acceptance cases

The state-machine implementation must test at least:

1. baseline → challenge → regulation → observed recovery → resume;
2. baseline → challenge → regulation → censored recovery → resume;
3. recovery telemetry failure → RECOVERY_DATA_INVALID;
4. child pause from baseline;
5. child pause during strategy execution;
6. child stop during challenge;
7. safety stop during recovery;
8. challenge suppression because of insufficient reference data;
9. challenge suppression after recent pause;
10. active-control configuration never entering regulation-training states;
11. temporary background interruption with valid resume;
12. interruption that invalidates recovery data;
13. fatal durable-storage failure;
14. normal session completion without any eligible challenge.

## 11. Machine-readable definition

The companion file:

`config/core_session_state_machine.example.json`

contains the current machine-readable state/transition graph for validation and future Unity translation.

It is an implementation contract, not evidence of human efficacy.
