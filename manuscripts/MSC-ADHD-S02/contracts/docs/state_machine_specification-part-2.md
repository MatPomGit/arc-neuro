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
