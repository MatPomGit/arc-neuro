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
