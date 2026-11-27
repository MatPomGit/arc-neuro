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
