## 10. Synchronization contract

The application and EEG recorder must be synchronized at event level.

Preferred architecture:

- direct research SDK acquisition on the same Android device or a tightly coupled local acquisition service;
- ARC-ADHD writes scientific event markers and EEG samples against a shared monotonic time base where technically supported.

If separate clocks are unavoidable:

- emit repeated synchronization markers;
- estimate offset and drift with a documented affine clock transform;
- retain raw source timestamps and transformed timestamps;
- quantify residual synchronization error;
- reject event-level analyses when synchronization uncertainty exceeds the frozen tolerance.

A simple post hoc nearest-timestamp join without drift characterization is insufficient.

Required ARC markers include:

- session start;
- rule calibration start/end by rule;
- baseline/reference-window boundaries;
- challenge candidate;
- challenge onset and target rule;
- regulation-state transitions;
- recovery-monitoring onset;
- each recovery-score update;
- threshold-entry timestamp;
- stable-recovery confirmation;
- recovery censor/invalid closure;
- pause, stop, overload and technical interruption.

## 11. Artifact and signal-quality model

Wearable EEG during a game is especially vulnerable to:

- eye movements and blinks;
- facial and jaw EMG;
- head movement;
- band displacement;
- poor electrode contact;
- Bluetooth packet loss;
- device buffering;
- movement during regulation exercises.

The paper must report signal quality as an outcome, not hide it by analyzing only convenient segments.

Motion sensors should be retained as artifact/context channels when available from the research interface.

Primary EEG analyses should prespecify:

- minimum usable channels/features;
- maximum packet loss;
- amplitude/clipping rules;
- movement-contamination rules;
- minimum clean duration per phase;
- whether and how channels can be rejected;
- whether rejected windows can re-enter after quality recovery.

No source localization claim should be made from this sparse wearable montage.

## 12. Study sequence

### Stage E0: technical validation

Before child data:

- obtain Muse research access/license;
- verify Athena raw EEG acquisition;
- verify channel metadata and scale;
- benchmark Bluetooth stability;
- quantify app↔EEG clock offset/drift;
- verify event-marker reconstruction;
- determine movement/artifact behavior during representative ARC tasks.

These data are engineering validation, not evidence for the child mechanism.

### Stage E1: observational pediatric substudy

Children complete the frozen ARC-ADHD task while EEG is recorded.

Primary goals:

- acquisition feasibility;
- signal-quality distribution;
- event synchronization validity;
- within-child phase-related spectral dynamics;
- estimability of (T_{EEG});
- relation of (T_{EEG}) to behavioral (T_{rec}).

### Stage E2: incremental-value validation

Only if E1 succeeds:

- train models using behavioral/context features alone;
- compare with behavioral/context + EEG;
- use participant-level grouped cross-validation;
- freeze one incremental-value metric;
- test calibration and failure by device/signal-quality strata.

Only after a reproducible positive incremental-value gate should EEG-informed adaptation or neurofeedback be considered in a separate future study.

## 13. Statistical model

The core analyses are repeated-event, within-person models.

Candidate models include:

- mixed models for band-power change by event phase;
- functional or time-varying models for recovery trajectories;
- mixed-effects association between (T_{EEG}) and (T_{rec});
- participant-grouped predictive validation for incremental EEG value.

Random effects should represent repeated events within sessions and participants.

The paper should report effect sizes and uncertainty, not only nominal significance.

## 14. Key confounds

The analysis must explicitly model or control:

- current rule and switch direction;
- task difficulty;
- sensory load;
- response-window timing;
- strategy type;
- movement level;
- medication status if part of the study design;
- session number;
- time-on-task/fatigue;
- device/acquisition profile;
- EEG signal quality.

## 15. Falsification criteria

The EEG companion hypothesis is weakened when:

1. event synchronization is not sufficiently accurate for phase-level analysis;
2. usable EEG coverage is too low or systematically related to challenge severity;
3. spectral effects disappear after motion/EMG quality controls;
4. apparent effects are not reproducible within participants across sessions;
5. (T_{EEG}) is unstable to small prespecified preprocessing perturbations;
6. neural recovery does not relate reproducibly to behavioral recovery;
7. EEG adds no participant-held-out predictive or decision value beyond behavioral/context features.

A null EEG result does not invalidate ARC-ADHD's behavioral mechanism.

## 16. Scope exclusions

Not part of this first paper:

- real-time EEG-driven task adaptation;
- closed-loop neurofeedback;
- ADHD diagnosis from EEG;
- prediction of an individual child's clinical prognosis;
- source localization;
- claims that a frequency band directly represents a discrete emotion;
- fNIRS as a co-primary modality;
- sleep outcomes.

Athena fNIRS may support a later multimodal paper, but including it now would confound the specific value of EEG.

## 17. Data and privacy boundary

Raw EEG is more sensitive than ordinary game telemetry and requires explicit participant/caregiver information and study-specific governance.

The study should define:

- whether raw EEG is retained;
- encryption at rest and in transfer;
- pseudonymous linkage to ARC events;
- retention period;
- restricted access;
- withdrawal/deletion procedure;
- whether data can be shared publicly or only under controlled access.

The core application must remain usable without EEG.

## 18. Most important implementation dependency

The largest current external dependency is not the spectral algorithm. It is access to an Athena-specific research acquisition interface with documented raw EEG channels and reliable timestamp semantics.

The manufacturer currently directs academic/clinical researchers to its research partnership route. The acquisition pipeline should not be implemented by reverse engineering a consumer stream when an authorized research pathway is required.
