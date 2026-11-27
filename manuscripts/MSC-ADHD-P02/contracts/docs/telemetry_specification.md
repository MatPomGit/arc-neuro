# ARC-ADHD core telemetry specification

Status: version 0.2 design contract.

The telemetry model is event based. It is designed to reconstruct the adaptive controller and the challenge-regulation-recovery sequence without retaining unnecessary raw sensor streams.

## Design principles

1. **Deterministic replay:** a researcher should be able to reconstruct why the controller changed difficulty, sensory load or regulation support.
2. **Separation of missingness and non-recovery:** missing telemetry is not right-censoring.
3. **Versioned intervention:** every record identifies the software/intervention version and schema version.
4. **Minimal raw data:** derived features are preferred when raw streams are not required by the research question.
5. **Monotonic session time:** within-session timing uses a monotonic clock to avoid wall-clock discontinuities.
6. **Pseudonymization:** no direct participant identifiers belong in the telemetry payload.

## Required event families

### session_started

Required fields:

- participant_pseudonym;
- study_arm;
- intervention_version;
- schema_version;
- session_id;
- session_index;
- device_capability_profile_id;
- app_generated_installation_id;
- device_qualification_rule_version;
- device_qualification_outcome;
- configuration_hash;
- monotonic_session_start.

### trial_completed

Required fields:

- session_id;
- task_id;
- trial_id;
- task rule;
- target class (GO/NO-GO);
- expected response;
- actual response;
- correctness;
- omission/commission status;
- cognitive difficulty vector;
- sensory configuration;
- response latency for valid responses;
- task-specific derived features;
- safety state.

The target class, expected response and actual response are retained so balanced rule success can be reconstructed from trial telemetry rather than trusted as an opaque derived value.

The immediate eligibility reference and target-rule recovery reference are different scientific objects. The former describes the preswitch current-rule state used for challenge scheduling. The latter is the mapping-matched `RULE_CALIBRATION` reference used to compute (B_{\mathrm{ref}}) and, when timing is eligible, the (S/V) timing baseline.

### challenge_started

Required fields:

- challenge_event_id;
- challenge_type;
- challenge eligibility rule version;
- challenge onset;
- immediate current-rule eligibility-reference bounds and composition;
- target-rule recovery-reference ID/version;
- target-rule recovery-reference rule and GO-stimulus identity;
- target-rule behavioral GO/NO-GO counts;
- core challenge eligibility snapshot hash;
- timing-feature eligibility flag and unavailability reasons;
- cognitive difficulty;
- sensory load;
- randomized cue assignment when applicable.

### regulation_action

Required fields:

- challenge_event_id;
- action type;
- action onset;
- whether selected by the child or suggested by the system;
- explicit child difficulty/overload input when provided;
- controller reason code.

### recovery_assessed

Required fields:

- challenge_event_id;
- recovery feature-model ID (`B`, `B+S`, `B+V`, or `B+S+V`);
- target-rule recovery-reference ID/version;
- current non-positive (q_e(t));
- non-negative component deficits for exactly the features in the selected model;
- recovery threshold delta;
- stability-window count (w) in consecutive score updates;
- recovery criterion state;
- recovery measurement context version/hash;
- active task rule;
- cognitive-difficulty state;
- sensory configuration;
- response-window timing;
- stimulus-distribution/content version;
- event-level cue assignment when applicable;
- whether the recovery measurement context remains unchanged;
- assessment timestamp.

### recovery_closed

Required fields:

- challenge_event_id;
- frozen recovery feature-model ID;
- final (q_e(t)) and component deficits when recovery data remain valid;
- recovery-monitoring onset timestamp;
- threshold-entry timestamp when observed;
- stability-confirmation timestamp when observed;
- pre-monitoring latency T_pre;
- recovery observed: yes/no;
- monitoring-anchored recovery latency T_rec when observed;
- total challenge-to-stable-return latency T_total when observed;
- right-censoring flag;
- censor limit;
- censor reason;
- recovery-data-valid flag;
- invalid reason when recovery data are scientifically invalid;
- recovery-measurement-context-unchanged flag;
- telemetry completeness flag;
- safety override flag.

For the Signal Gate candidate space, stored component values are deficits \(d_j\ge0\), and the stored score must satisfy \(q_e(t)=-\sum_j w_jd_j\le0\). A stored positive q is invalid, as is a component set that does not match the recorded model ID.

A complete telemetry record may still contain scientifically invalid recovery data. In particular, a score-relevant context change during `RECOVERY_MONITORING` is represented as `recovery_data_valid = false`, not as right-censoring and not as missing telemetry.

### session_ended

Required fields:

- planned versus actual duration;
- completion state;
- early-stop reason;
- overload events;
- adverse-event flag;
- telemetry completeness summary.

## BYOD device context

The core study uses private participant/caregiver Android phones.

Research telemetry should prefer coarse execution-context variables over unique hardware identifiers.

Permitted default device-context fields may include:

- Android major version;
- display refresh-rate bucket;
- logical screen-size bucket;
- benchmark/performance class;
- ordinary audio availability;
- optional haptic availability;
- background/resume capability result;
- qualification outcome/version;
- app-generated random installation identifier.

The default telemetry must not require IMEI, device serial, Android ID, advertising ID, MAC address, account identifiers, installed-app inventory or precise location.

A material device/profile change between sessions must be logged. Timing-sensitive reference variables should follow the prespecified reset/sensitivity rule rather than assuming direct comparability.

BYOD qualification and nonqualification reasons are feasibility data, distinct from clinical outcomes.

## Recovery time decomposition

Scientific recovery time uses three explicitly separated quantities:

- `T_pre = t_monitor - t_challenge`;
- `T_rec = t_threshold_entry - t_monitor`;
- `T_total = t_threshold_entry - t_challenge = T_pre + T_rec`.

The primary performance-recovery clock starts only when `RECOVERY_MONITORING` begins. The stability-confirmation timestamp is stored separately because the application can identify the beginning of a qualifying run only after the required future score updates confirm it.

Right-censoring is applied to the monitoring-anchored `T_rec` window. A longer pause/orient/strategy sequence therefore changes `T_pre` and `T_total`, but does not mechanically lengthen `T_rec`.

## Time semantics

All event times within a session should be expressed in milliseconds from a monotonic session clock.

Wall-clock timestamps, if retained for operational reasons, should be stored separately from the scientific event timing and minimized according to the data-protection plan.

## Missingness taxonomy

Use explicit missingness codes rather than null values alone.

Suggested codes:

- not_applicable;
- sensor_unavailable;
- tracking_failure;
- participant_skipped;
- safety_abort;
- software_error;
- session_terminated;
- unknown.

A recovery event with incomplete data is not automatically censored. Censoring describes failure to observe the recovery criterion within the prespecified observation window while the event remains otherwise analyzable.

## Controller reason codes

Every adaptive change should include a reason code from a controlled vocabulary, for example:

- task_too_easy;
- task_too_difficult;
- sensory_overload;
- participant_request;
- repeated_error;
- recovery_not_observed;
- recovery_stable;
- safety_override;
- scheduled_progression;
- research_randomization.

## Versioning

The following values must be immutable within a frozen study build:

- schema version;
- challenge eligibility rule version;
- target-rule recovery-reference construction/version;
- recovery-score feature set;
- recovery-score weights/signs;
- delta;
- stability window w;
- censor limit;
- controller rule version;
- task configuration version.

Any change creates a new intervention version and is recorded as a protocol deviation if it occurs after study lock.

## Reference implementation

The machine-readable contract is stored in:

schemas/recovery_event.schema.json

The JSON schema validates structure, not scientific validity. Scientific validity still depends on the preregistered definitions and controller implementation.
