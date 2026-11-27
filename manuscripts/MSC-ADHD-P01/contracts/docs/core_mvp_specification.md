# ARC-ADHD core MVP specification

Status: version 0.1 engineering boundary.

The core MVP is intentionally smaller than the complete ARC-ADHD research programme. Its purpose is to instantiate the challenge-regulation-recovery mechanism without requiring AR, facial sensing or bilateral audio.

## Required capabilities

### 1. Executive-control task

At least one reproducible task must support:

- a stable baseline rule;
- bounded manipulation of difficulty;
- identifiable eligible challenge events;
- objective response accuracy and latency;
- return to the same goal after regulation.

The first implementation can use selective attention/inhibition with rule switching because the task can generate controlled, recoverable perturbations without requiring a complex content library.

### 2. Session state machine

Minimum states:

1. readiness;
2. baseline task;
3. eligible challenge;
4. pause;
5. orient;
6. strategy selection;
7. strategy execution;
8. recovery monitoring;
9. resume goal;
10. reflection;
11. session complete;
12. safety stop.

Every transition must produce a telemetry event.

### 3. Minimum sensory set

**Visual:** required for ordinary task presentation and instructions.

**Auditory:** optional, short, non-bilateral cueing. The intervention must remain usable when audio is disabled.

**Haptic:** optional, one standardized pause/attention pattern. The intervention must remain usable when haptics are disabled.

Sensory channels must not be added merely to increase stimulation. Cognitive difficulty and sensory load remain separate controller variables.

### 4. Body orientation

The core MVP includes only low-burden orientation to current bodily state, for example:

- breathing;
- muscle tension;
- contact with the floor or chair;
- urge to move;
- posture.

This is a regulation-strategy component, not an embodied-training claim.

### 5. Regulation strategy library

Initial strategy families:

- paced breathing;
- brief muscle release;
- grounding/orienting;
- attentional redeployment;
- simple reappraisal;
- problem solving;
- controlled brief movement.

The MVP does not need every strategy to be equally emphasized. Strategy choice must be logged.

### 6. Adaptation hierarchy

Controller priority:

1. safety override;
2. explicit child stop or difficulty request;
3. sensory-overload rule;
4. task-performance rule;
5. recovery-state rule;
6. scheduled research randomization;
7. ordinary progression.

No passive sensor estimate may override an explicit stop request.

## Explicitly excluded from the core MVP

- front-camera facial adaptation;
- identity or categorical emotion recognition;
- augmented-reality missions;
- spatial anchors or home-environment mapping;
- embodied movement as a transfer manipulation;
- alternating bilateral auditory stimulation;
- outdoor location;
- raw continuous audio recording;
- raw continuous video recording.

## Core BYOD assumption

Phase 0 onward is designed for the participant/caregiver's private Android phone.

The study freezes a versioned compatibility/qualification policy rather than one hardware model. Each installation must establish a privacy-minimized capability profile and pass core qualification before participant-facing use.

Core qualification evaluates:

- compatible Android/runtime;
- display/layout compatibility;
- touch input;
- monotonic timing;
- app-local durable storage;
- offline operation;
- benchmark/performance class;
- background/resume behavior;
- optional audio/haptic capability and fallbacks.

Camera, microphone, precise location, AR and haptics are not mandatory for the core condition.

A material device/profile change requires requalification. Timing-sensitive reference measures must not be assumed directly comparable across different profiles without the prespecified reset/sensitivity rule.

The proportion of private devices that fail or require fallbacks is itself a feasibility outcome.

## Version lock

Before the pilot randomized trial, freeze:

- task version;
- challenge rules;
- strategy library;
- controller rules;
- sensory configuration;
- recovery definition;
- telemetry schema;
- active-control specification;
- participant-facing wording.

Any post-lock change is a new intervention version.
