# Concept: event-locked wearable EEG during ARC-ADHD

## 1. Scientific role

This paper adds a neurophysiological **measurement layer** to ARC-ADHD without changing the core intervention.

The child performs the same Signal Gate challenge-regulation-recovery sequence while wearing Muse S Athena. EEG is synchronized with the application's event stream and analyzed offline.

The first study does not use EEG to:

- diagnose ADHD;
- label emotions;
- automatically change task difficulty;
- decide whether the child has recovered;
- provide neurofeedback;
- establish clinical efficacy.

Its role is to test whether the behavioral recovery process has a measurable and reproducible electrophysiological correlate.

## 2. Working title

**Event-Locked Wearable EEG During ARC-ADHD Regulation Training: A Muse S Athena Study of Challenge and Recovery Dynamics**

Alternative:

**Neurophysiological Signatures of Challenge and Recovery During ARC-ADHD Training: An Event-Locked Muse S Athena EEG Study**

## 3. Primary research question

Does event-locked wearable EEG provide reproducible within-child information about controlled challenge and post-regulation recovery beyond the behavioral telemetry already available from ARC-ADHD?

## 4. Core hypotheses

### H1: event-phase modulation

Prespecified EEG spectral features differ within child across stable task performance, controlled rule switch, regulation, recovery monitoring, and stable return.

This is an event-related within-person hypothesis, not a claim about a diagnostic ADHD EEG phenotype.

### H2: behavioral-neural recovery coupling

A separately defined neural recovery time is associated with the monitoring-anchored behavioral recovery latency (T_{rec}), while allowing substantial event-level heterogeneity.

Failure to observe reproducible coupling weakens the claim that the wearable EEG measure captures the same recovery process.

### H3: incremental information

Adding EEG features to a behavioral/context model improves participant-held-out prediction of a prespecified proximal recovery outcome compared with behavioral/context telemetry alone.

If EEG does not provide reproducible incremental out-of-sample value, the headband should not be retained as a necessary ARC-ADHD measurement channel.

## 5. Measurement periods

Each eligible rule-switch event is partitioned into explicit phases.

1. **Immediate prechallenge reference**: stable performance under the current rule. This is used to quantify challenge reactivity.
2. **Challenge response**: the initial interval after the explicit A↔B switch.
3. **Regulation interval**: pause, orient, strategy selection and strategy execution. EEG is retained, but movement-contaminated data may be unsuitable for primary spectral inference.
4. **Recovery monitoring**: begins at the same timestamp used by the core (T_{rec}) definition.
5. **Stable return**: windows after behavioral recovery has been confirmed.

In addition, the dedicated A/B rule-calibration block provides a **target-rule-matched EEG reference**. This is essential because the post-switch rule is not identical to the immediate prechallenge rule.

## 6. Candidate spectral feature family

The first analysis uses a deliberately small spectral family.

Candidate conventional frequency ranges:

- delta: 1–4 Hz;
- theta: 4–8 Hz;
- alpha: 8–13 Hz;
- beta: 13–30 Hz;
- low gamma: 30–45 Hz.

These boundaries are analysis conventions, not biological categories with one-to-one psychological meanings.

Primary emphasis should initially be placed on theta, alpha and beta because task-related work in ADHD has most often examined these ranges. Delta and low gamma should be secondary/exploratory, with low gamma subject to especially strict electromyographic-artifact controls.

Theta/beta ratio is not a privileged primary biomarker. If reported, it is secondary and cannot be interpreted diagnostically.

## 7. Spectral estimation

A candidate engineering pipeline is:

1. preserve the raw research EEG stream;
2. verify timestamps, packet order and acquisition gaps;
3. apply the frozen channel/montage specification obtained from Muse research documentation;
4. remove or flag gross artifacts using rules fixed independently of outcomes;
5. derive overlapping short-time spectral windows;
6. compute log absolute band power;
7. compute relative band power as a secondary representation;
8. retain channel-level features before any regional aggregation.

Exact filter cutoffs, window duration, overlap, line-noise handling and artifact thresholds must be frozen after technical signal-quality validation and before inferential participant analysis.

## 8. Challenge-reactivity EEG measure

For band (b) and channel (c), challenge reactivity can be expressed as

[
R_{bc}^{(e)}
=
log P_{bc,mathrm{challenge}}^{(e)}
-
log P_{bc,mathrm{prechallenge}}^{(e)}.
]

This quantity answers whether the controlled switch perturbs spectral activity relative to the immediately preceding state.

It is not used as the recovery reference because the post-switch rule differs from the preswitch rule.

## 9. Neural recovery measure

For recovery, use a target-rule-matched calibration reference.

For feature (j=(b,c)),

[
z_j(t)
=
rac{
log P_j(t)-operatorname{median}(log P_{j,mathrm{ref,target}})
}{
1.4826,operatorname{MAD}(log P_{j,mathrm{ref,target}})+epsilon_j
}.
]

A robust multifeature neural distance can be defined as

[
D_{mathrm{EEG}}(t)
=
operatorname{median}_{jin Q(t)}
|z_j(t)|,
]

where (Q(t)) contains only quality-passed EEG features at time (t).

A candidate neural recovery latency is

[
T_{mathrm{EEG}}^{(e)}
=
inf
left{
	au ge 0:
D_{mathrm{EEG}}(t)ledelta_{mathrm{EEG}}
	ext{ for } w_{mathrm{EEG}} 	ext{ consecutive windows}
ight},
]

with time origin equal to ARC-ADHD `RECOVERY_MONITORING` onset.

The threshold, minimum valid channels/features, stability count and censoring rule must be calibrated using signal/measurement properties only. They must not be chosen to maximize correlation with (T_{rec}), EDI or treatment response.

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
