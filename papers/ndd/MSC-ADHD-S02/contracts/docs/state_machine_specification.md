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


[Continue to part 2](state_machine_specification-part-2.md)
