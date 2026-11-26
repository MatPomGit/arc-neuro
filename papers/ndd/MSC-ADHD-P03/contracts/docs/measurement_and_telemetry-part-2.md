## 6. Derived variables

Derived variables should be specified before outcome unblinding.

### Attention sensitivity

Use signal-detection measures where the task structure supports them:

d' = Z(hit rate) - Z(false alarm rate)

Extreme hit and false-alarm rates require a prespecified correction.

### Reaction-time variability

Use robust within-person measures rather than raw standard deviation alone when distributions are strongly skewed.

Candidate:

CV_RT = SD(RT) / mean(RT)

### Recovery latency

Define:

T_pre = t_monitor - t_challenge

T_rec = t_stable_entry - t_monitor

T_total = t_stable_entry - t_challenge = T_pre + T_rec

where `t_monitor` is entry into recovery monitoring and `t_stable_entry` is the first score update beginning a fully confirmed prespecified stable run. The confirmation timestamp is stored separately. This decomposition prevents regulation-strategy duration from being conflated with post-regulation performance recovery.

### Post-error disruption

Possible index:

PED = performance_pre_error - performance_post_error

with fixed windows around the challenge event.

### Cross-modal cue benefit

For a proximal outcome P:

CMB = P_multisensory - P_visual_only

Estimate separately for audiovisual and audiovisual+haptic conditions and model participant-level heterogeneity.

### Sensory-overload rate

SOR = overload_or_safety_events / eligible_multisensory_events

This should be analyzed jointly with performance. A small performance gain accompanied by a substantial overload increase should not be interpreted as a favorable effect.

### AR movement engagement

Possible features:

- proportion of session spent in safe movement;
- completed anchor transitions per minute;
- adherence to stop cues while moving.

These are process measures, not clinical outcomes.

### AR performance difference

For matched task content:

Delta_AR = P_AR - P_stationary

This helps distinguish movement/AR effects from task-learning effects.

### Body-state identification change

A within-person index can quantify change in:

- number of bodily signals recognized;
- response consistency;
- confidence;
- association with subsequent strategy selection.

It should remain exploratory until validated.

### Haptic-motor synchronization

For haptic beat time h_k and detected movement peak m_k:

e_k = m_k - h_k

Candidate measures:

MAE_sync = mean(|e_k|)

SD_sync = SD(e_k)

Bias_sync = mean(e_k)

These distinguish systematic anticipation, lag and unstable timing.

### Motor smoothness

Candidate IMU-derived measures:

- angular velocity RMS;
- angular jerk;
- overshoot count;
- direction-reversal count;
- spectral power around the target rhythm.

These are process variables, not clinical biomarkers.

### Real-world search efficiency

For camera/audio-guided search:

- target acquisition time;
- false candidate count;
- proportion of search time with screen guidance visible;
- camera orientation path length;
- number of rule errors.

Color and shape detections should be stored as derived events rather than raw images.

### Facial baseline deviation

For selected normalized facial features z_phi,i(t):

D_phi(t) = sqrt(sum_i w_i * z_phi,i(t)^2)

After a challenge event, define facial recovery as the first time D_phi remains below a preregistered threshold for a specified duration.

Derived variables:

- facial response amplitude;
- T_face_rec;
- T_task_rec;
- Delta_rec = T_face_rec - T_task_rec;
- proportion of windows with insufficient tracking confidence.

These variables are behavioral proxies, not emotion labels or clinical biomarkers.

### Incremental facial-information value

Compare predictive models of excessive task demand:

A. task performance only;
B. task + sensorimotor;
C. task + sensorimotor + facial behavior;
D. task + sensorimotor + facial behavior + child report.

Report incremental predictive performance and calibration rather than only classification accuracy.

### Bilateral-specific effect

For a prespecified proximal variable R:

BSE = R_alternating - R_matched_nonalternating

A clinically meaningful interpretation requires replication and cannot be inferred from a single short-term effect.

### BYOD qualification rate

For screened private phones report:

BYOD_core = qualified_core / screened_devices

BYOD_fallback = qualified_with_fallbacks / screened_devices

BYOD_fail = not_qualified / screened_devices

Always report the corresponding counts and reasons rather than only percentages.

These are implementation/feasibility variables, not treatment outcomes.

### Device-profile change rate

Track:

- number/proportion of participants changing phone or materially changing capability profile;
- timing-sensitive sessions before and after the change;
- reference resets or exclusions required by the preregistered rule.

A device/profile change must not be silently absorbed into longitudinal reaction-time trends.

### Strategy transfer index

An exploratory index can summarize whether strategies practiced in the game are later reported in daily life. It must remain exploratory until externally validated.

## 7. Adaptation audit variables

For every difficulty or sensory-load change store:

- previous cognitive difficulty state;
- previous sensory-load state;
- rolling performance estimate;
- target performance band;
- controller output;
- applied cognitive difficulty state;
- applied modality state;
- reason for clipping or safety override.

This permits exact reconstruction of the intervention delivered to each participant.

## 8. Missingness

Differentiate:

- session not started;
- session interrupted;
- sensory modality disabled by preference;
- AR unavailable because the environment was unsafe;
- Bluetooth/headphone failure;
- telemetry upload failure;
- outcome assessment missed;
- participant withdrawal.

Do not treat all missing observations as equivalent.

## 9. Telemetry validation

Before using telemetry as a mechanistic marker:

1. test event completeness;
2. verify clock ordering;
3. verify deterministic reconstruction;
4. test device-performance effects on reaction-time variables;
5. test vibration support across devices;
6. test audio route and stereo-channel correctness;
7. quantify Bluetooth timing variability;
8. validate AR tracking and movement-feature extraction;
9. compare telemetry-derived metrics with external cognitive tasks;
10. assess test-retest reliability where applicable.

Smartphone hardware variation can influence millisecond-level reaction-time estimates. Hardware and OS metadata should therefore be recorded in a privacy-preserving form sufficient for sensitivity analysis.

Bluetooth timing also prevents claims that software-scheduled left/right alternation corresponds exactly to neural stimulation timing without hardware validation.

## 10. Privacy-preserving sensor handling

Default principles:

- camera frames used by AR are processed locally and not uploaded;
- no face recognition;
- no continuous audio recording;
- microphone access is not required for the core design;
- raw accelerometer/gyroscope streams should be reduced locally to predefined features where possible;
- no exact geolocation is needed;
- environmental imagery is not a research endpoint.

## 11. Success criteria for the research program

Evidence should become progressively stronger:

### Feasibility

Children can use the intervention safely and complete the intended dose.

### Sensory tolerability

Audio, haptic and AR modes can be used without unacceptable overload or avoidance.

### Engagement

Children remain engaged without coercive reward mechanisms.

### Component evidence

Specific modalities produce measurable proximal effects beyond matched alternatives.

### Near transfer

Independent tasks closely related to trained constructs improve.

### Far transfer

External symptom, regulation or functioning measures improve relative to active control.

### Mechanistic support

Changes in the prespecified regulation-recovery process covary with external improvements and replicate in an independent sample.
