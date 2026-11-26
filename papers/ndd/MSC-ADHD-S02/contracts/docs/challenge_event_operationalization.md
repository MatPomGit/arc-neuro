# ARC-ADHD Phase 0 challenge-event operationalization

Status: pre-Phase 0 contract ready for preregistration. The event logic is specified; the remaining pacing and safety values must be ratified with the final Phase 0 session/safety configuration before recruitment.

Authoritative machine-readable rule:

`config/challenge_eligibility.phase0.example.json`

Executable evaluator:

`scripts/evaluate_challenge_eligibility.py`

Reference cases:

`examples/challenge_eligibility_cases.json`

## 1. Scope

The first Phase 0 challenge family is restricted to an explicit Signal Gate rule switch:

- A → B; or
- B → A.

Other conceptual challenge families, such as interruption or recoverable error, are deferred from the first recovery-measure stabilization round. They may be evaluated later only after showing that the same recovery construct and measurement assumptions remain interpretable.

A hidden rule switch is not permitted.

## 2. Why both rule mappings are calibrated first

A rule switch should test recovery from a changed control demand, not discovery of an unknown rule.

Before the first eligible challenge, the child is therefore exposed to both A and B mappings in the dedicated `RULE_CALIBRATION` state.

Calibration serves three purposes:

1. verify that both mappings can be understood;
2. provide behaviorally interpretable A↔B switching rather than first-time rule learning;
3. create the stable target-rule recovery reference for (B), and, when the private phone has a qualified timing profile, the matched correct-GO RT reference for (S) and (V).

Calibration trials do not create challenge IDs and do not enter the recovery-event sample.

## 3. Core event eligibility versus timing-feature eligibility

Eligibility is separated into two layers.

### 3.1 Core challenge-event eligibility

A challenge can open a core recovery event when the behavioral/task, pacing, integrity and safety requirements pass.

This event remains scientifically useful for the mandatory behavioral feature B even when the device does not support sufficiently reliable timing for S or V.

### 3.2 Timing-feature eligibility

Timing-enriched models require, in addition:

- a timing-qualified execution profile;
- a stored timing reference for the target post-switch rule;
- the timing reference rule ID to equal the target rule ID;
- the timing reference GO stimulus identity to equal the GO stimulus identity of the recovery window.

Failure of a timing-only requirement does not retrospectively make the behavioral challenge invalid. Instead, the event is recorded as unavailable for timing-enriched candidate models.

This distinction prevents hardware heterogeneity from being hidden through silent event exclusion.

## 4. Preconditions evaluated before opening the event

Eligibility is evaluated atomically while the application is in `CHALLENGE_PENDING`.

The event must satisfy all of the following before a `challenge_event_id` is created.

### Task and rule state

- task is Signal Gate;
- current state is `BASELINE_TASK`;
- current rule is A or B;
- target rule is the other rule;
- both rule mappings have completed calibration;
- the explicit switch cue is available;
- the challenge is not selected because an error has just been observed.

### Immediate eligibility reference

The current candidate eligibility-reference contract requires:

- at least 12 valid prechallenge observations;
- at least 4 GO trials;
- at least 4 NO-GO trials;
- all reference observations interpreted under the current preswitch rule;
- a reference rebuilt after a child pause;
- a fresh reference after the previous recovery event closes.

These are project-specific Phase 0 candidate values, not universal psychometric thresholds. This current-rule window determines readiness for challenge scheduling but is not used as (B_{\mathrm{ref}}) in the recovery score.

### Target-rule recovery reference

The recovery score uses the separate `RULE_CALIBRATION` reference for the target post-switch rule. The target-rule reference must match both the recovery rule ID and GO-stimulus identity. Its behavioral counts define (B_{\mathrm{ref}}); when timing is qualified, the same versioned reference also supplies the correct-GO RT distribution for (S) and (V).

In the first Phase 0 implementation the target-rule recovery reference is immutable within a session. A later design may study controlled updating, but it must not be introduced silently during Phase 0.

### Separation from the previous event

For a subsequent challenge:

- the previous recovery event must already be closed;
- at least 12 valid task trials must have occurred after its closure;
- the fresh reference requirement must be satisfied;
- at least 30 seconds must have elapsed since the previous challenge onset.

The trial-count requirement protects measurement independence from the immediately preceding recovery episode. The wall-clock interval is a separate pacing safeguard and remains subject to final Phase 0 ratification.

### Remaining event budget

The application must not open a challenge merely because the remaining session time exceeds the recovery censor limit.

Instead, a locked `required_event_time_ms` is supplied by the active study configuration and must include:

- the configured challenge/regulation sequence;
- the recovery censor window;
- transition/persistence margin.

Eligibility requires the remaining session time to cover the complete locked event budget.

The event budget must be at least as long as the configured recovery censor window.

### Integrity

The application requires:

- healthy required telemetry;
- no already-open recovery event;
- no active technical interruption.

### Safety and child agency

The challenge is suppressed when:

- sensory overload is active;
- a safety override is active;
- the child is still in the post-pause suppression state.

Safety and explicit child actions outrank scientific scheduling.

## 5. No conditioning on observed destabilization

Challenge eligibility is determined before the switch.

The application must not wait for a commission error, omission, slowing, or another unfavorable post-switch response and then decide that the event was a valid challenge only because performance worsened.

Such selection would condition the mechanistic sample on a post-challenge response.

An eligible challenge may therefore produce:

- clear behavioral destabilization;
- mild perturbation;
- no detectable perturbation.

The latter is a legitimate measurement outcome rather than a reason to erase the event.

## 6. Challenge limit

The current candidate pacing contract allows at most three challenges per session.

This value is an ARC-ADHD engineering candidate. It must be ratified with the final session duration, child burden, safety rules and strategy durations before participant recruitment.

Initial rule assignment or session-level counterbalancing should be specified separately if challenge-direction balance is required analytically. Challenge eligibility itself does not select a direction based on recent performance.

## 7. Atomic scheduling sequence

A challenge candidate follows this order:

1. `BASELINE_TASK` emits `challenge_candidate`;
2. enter `CHALLENGE_PENDING`;
3. snapshot all eligibility inputs;
4. evaluate the versioned eligibility rule;
5. if suppressed, record all suppression reasons and return to `BASELINE_TASK`;
6. if eligible, atomically assign the challenge metadata and event ID;
7. enter `CHALLENGE_ACTIVE`;
8. present the explicit new rule cue and switch;
9. proceed through regulation;
10. start recovery monitoring under the locked measurement context.

A suppressed candidate is not a failed recovery event and must not create a placeholder recovery record.

## 8. Required eligibility telemetry

For every challenge candidate, retain enough information to reconstruct the decision:

- eligibility-rule version;
- task/state;
- current and target rule;
- switch-cue availability;
- calibration status;
- reference counts and reference rule;
- freshness flags;
- prior-event status;
- trials and time since previous event;
- challenge count;
- remaining session time;
- locked required event budget;
- telemetry/integrity state;
- overload/safety/pause state;
- timing-profile qualification;
- target-rule recovery-reference ID/version, rule and GO-stimulus identity;
- behavioral counts in the target-rule recovery reference;
- correct-GO RT count and timing-profile reference when timing is qualified;
- core eligibility result;
- all core suppression reasons;
- timing-feature eligibility result;
- all timing-unavailability reasons.

## 9. Core suppression reason vocabulary

The current contract recognizes:

- `task_id_ineligible`;
- `task_state_ineligible`;
- `target_rule_not_distinct`;
- `switch_cue_unavailable`;
- `rule_mappings_not_calibrated`;
- `insufficient_reference_observations`;
- `insufficient_reference_go_trials`;
- `insufficient_reference_nogo_trials`;
- `reference_rule_mismatch`;
- `reference_not_fresh_after_pause`;
- `reference_not_fresh_after_recovery`;
- `minimum_interchallenge_interval`;
- `insufficient_trials_since_recovery_close`;
- `challenge_limit_reached`;
- `event_budget_not_locked_or_too_short`;
- `insufficient_remaining_session_time`;
- `telemetry_unhealthy`;
- `recovery_event_already_open`;
- `technical_interrupt`;
- `sensory_overload`;
- `safety_override`;
- `recent_pause`.

Multiple reasons are preserved rather than collapsed into one code.

## 10. Timing-unavailability reason vocabulary

Timing-enriched candidates separately use:

- `core_event_ineligible`;
- `timing_profile_unqualified`;
- `target_rule_timing_reference_unavailable`;
- `timing_reference_rule_mismatch`;
- `timing_reference_go_stimulus_mismatch`.

## 11. Phase 0 analysis implications

Phase 0 should report:

- total challenge candidates;
- core-eligible challenge count and proportion;
- suppression reasons;
- eligible events by A→B and B→A direction;
- timing-feature-eligible proportion among core-eligible events;
- timing-unavailability reasons;
- valid, censored and scientifically invalid recovery outcomes among core-eligible events.

For comparisons among B/S/V feature candidates, timing-enriched models should be evaluated on the prespecified timing-eligible subset, while B should additionally be reported on the complete core-eligible event population. The denominator difference must remain visible.

## 12. Remaining pre-recruitment freeze items

The logical eligibility contract is now explicit.

Before participant recruitment the study must still ratify and version-lock:

- 30 s interchallenge pacing value;
- maximum of three challenges per session;
- complete event-time budget generated from the final regulation strategy durations and censor limit;
- final safety/overload/post-pause configuration;
- final Signal Gate timing/difficulty values;
- BYOD timing qualification thresholds.

Changing those values after participant data become visible requires a documented protocol deviation or a new iterative Phase 0 version.
