# Measurement and telemetry plan

## 1. Measurement principle

ARC-ADHD must separate four levels of outcome:

1. performance inside the game;
2. proximal effects of sensory modality, movement and regulation cues;
3. performance on independent cognitive tasks;
4. clinically and functionally meaningful behavior outside the game.

Only level 4 can support a strong claim of generalized therapeutic benefit. Level 1 alone is evidence of task learning, while level 2 identifies potential active ingredients.

## 2. Outcome hierarchy

### 2.1 Primary external outcome

The first randomized trial should define one primary external measure of emotion regulation or emotion dysregulation.

Selection criteria:

- appropriate for ages 8-12;
- validated psychometric properties;
- available in Polish or suitable for validated translation;
- sensitive to change;
- feasible for repeated caregiver assessment;
- licensing compatible with the study.

The exact primary external instrument is intentionally unfrozen. Candidate evidence, Polish-language status and licensing are maintained in `docs/outcome_measure_audit.md`; the current measurement plan must not silently restore a deprioritized instrument as the default.

### 2.2 ADHD symptom outcomes

Use an established parent-rated ADHD symptom scale and, where feasible, an independent teacher-rated scale.

Possible options include SNAP-IV or an appropriately licensed alternative. The exact instrument should be fixed before recruitment.

### 2.3 Functional outcomes

Symptoms alone are insufficient. Include a measure of impairment in daily functioning, for example:

- homework and school-task completion;
- family conflict around routines;
- ability to resume activity after frustration;
- peer or classroom functioning;
- ability to use regulation strategies outside the game.

A standardized impairment scale is preferable to an ad hoc questionnaire for the confirmatory study.

### 2.4 Body-awareness/interoception outcomes

Interoception should be treated as a mechanistic construct, not automatically as a clinical endpoint.

Candidate domains:

- noticing bodily activation;
- ability to distinguish calm from activated states;
- confidence in body-state judgments;
- consistency between repeated subjective ratings;
- externally validated age-appropriate interoceptive measure where psychometrically justified.

Heartbeat-counting tasks should not be adopted uncritically, because measurement validity is debated and performance may be influenced by knowledge and estimation strategies.

## 3. Independent cognitive outcomes

The authoritative pre-freeze plan is maintained in `docs/near_transfer_and_functional_outcomes.md`.

The pilot should use a minimal battery rather than several correlated executive-function tasks.

### Inhibition

Preferred candidate:

- an independent Stop-Signal Task designed and scored according to the 2019 consensus recommendations.

Candidate variables:

- SSRT when task/race-model assumptions and BYOD timing validity are satisfied;
- probability of responding on stop trials;
- go omissions;
- go accuracy;
- go RT distribution as a process/quality variable.

The assessment must not reuse Signal Gate stimuli, reward logic, regulation prompts or trained rule-switch contingencies.

### Cognitive flexibility

One secondary flexibility task may be retained after Polish-language, licensing and psychometric review.

The official NIH Toolbox DCCS has strong psychometric support but is not adopted directly as the Polish Android-BYOD measure because its current official delivery pathway does not match this study context.

### Working memory

Working memory remains optional/exploratory unless the intervention explicitly trains the corresponding construct.

### Functional impairment

WFIRS-P is the leading ADHD-specific candidate, and IRS is a brief parent/teacher alternative. Both remain conditional on final Polish-language/licensing verification.

Polish SDQ total/impact information may provide broad corroboration but is not the preferred sole functional endpoint because published Polish work identified limitations in the original subscale structure.

The battery should remain short enough to avoid fatigue-driven measurement noise and unnecessary multiplicity.

## 4. Ecological measurement

A lightweight ecological momentary assessment component can measure generalization.

Suggested caregiver/child micro-items:

- strongest frustration since last prompt;
- whether the child noticed a bodily signal before acting;
- whether a regulation strategy was attempted;
- whether movement was used adaptively;
- approximate time to return to the interrupted goal.

EMA should be sampled sparsely to avoid becoming an intervention itself.

## 5. Telemetry event model

Every event should contain only the fields needed for a predefined analysis.

Core identifiers:

- pseudonymous participant ID;
- intervention version;
- session ID;
- timestamp;
- task/module ID.

BYOD capability fields:

- app-generated installation ID;
- capability-profile ID;
- qualification-rule version;
- qualification outcome;
- Android major version;
- display refresh-rate bucket;
- logical screen-size bucket;
- benchmark/performance class;
- optional audio/haptic availability;
- device/profile-change flag.

Do not store IMEI, serial number, Android ID, advertising ID, MAC address, account identifiers, installed-app inventory, precise location, contacts, call/SMS history, or unrelated media metadata in standard research telemetry.

Performance fields:

- difficulty vector;
- trial type;
- target/non-target;
- response;
- correctness;
- response time;
- rule state;
- distractor level.

Modality fields:

- visual cue enabled/type;
- auditory cue enabled/type;
- haptic cue enabled/pattern ID;
- active sensory-channel count;
- audio output route;
- headphone mode;
- AR/stationary mode;
- body-awareness prompt type;
- movement-task flag.

Regulation fields:

- challenge event type;
- self-rated state when collected;
- body-location/state selection when collected;
- strategy offered;
- strategy selected;
- strategy completed;
- pause duration;
- return-to-task latency.

Facial-feedback fields should contain derived data only:

- facial module enabled/disabled;
- front-camera tracking confidence;
- selected blendshape rolling means/slopes;
- coarse head-pose features;
- distance from personal facial baseline;
- post-error facial response amplitude;
- facial recovery time;
- missing/occluded state;
- adaptation decision contribution.

Do not store raw front-camera frames or reusable face embeddings in standard telemetry.

Movement fields should preferably store derived features rather than raw streams:

- movement block duration;
- number of anchor transitions;
- coarse displacement proxy;
- orientation-change summary;
- stop/start compliance;
- stationary versus moving time;
- angular velocity summary;
- target-angle error;
- movement smoothness;
- rhythm phase error;
- inter-movement interval variability;
- dual-task motor cost;
- hand used for selected tasks.

AR fields:

- tracking quality state;
- AR block start/stop;
- safety pause;
- target-anchor count;
- movement-area configuration class.

Bilateral-audio fields:

- condition code blinded in analysis export;
- alternation rate;
- duration;
- headphone channel check result;
- user stop/skip;
- subjective pre/post activation.

Safety fields:

- manual pause;
- early exit;
- repeated failure threshold;
- sensory-overload flag;
- automatic sensory simplification;
- automatic cognitive difficulty reduction;
- AR tracking loss;
- caregiver stop request.

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
