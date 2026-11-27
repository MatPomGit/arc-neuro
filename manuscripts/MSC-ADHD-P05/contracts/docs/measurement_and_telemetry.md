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


[Continue to part 2](measurement_and_telemetry-part-2.md)
