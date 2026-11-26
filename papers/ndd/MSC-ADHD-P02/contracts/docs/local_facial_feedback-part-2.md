## 10. Adaptation architecture

Recommended hierarchy:

1. safety rules;
2. explicit child input;
3. objective task performance;
4. sensorimotor performance;
5. facial-behavior signal;
6. historical personalization.

Facial feedback should therefore modify confidence in an adaptation decision rather than independently control the game.

Example:

difficulty_decrease_score =
    w_p * performance_deterioration +
    w_m * motor_deterioration +
    w_f * facial_deviation +
    w_s * subjective_difficulty

with:

w_f < w_p

in the first research build.

Weights should be fixed and preregistered before efficacy analysis.

## 11. Temporal hysteresis

The controller should not react to transient expressions.

Require:

- minimum persistence time;
- repeated-window confirmation;
- cooldown after an adaptation;
- maximum number of difficulty changes per minute;
- no adaptation during a single isolated facial movement.

This reduces oscillation and overreaction.

## 12. Local processing and privacy

Default architecture:

1. front-camera frame enters the on-device pipeline;
2. landmarks/blendshapes are extracted locally;
3. the image frame is immediately discarded;
4. only prespecified derived features are retained;
5. no raw video is uploaded;
6. no face image is stored in standard telemetry;
7. no identity embedding is created.

Prefer storing aggregated windows such as:

- mean selected blendshape coefficient;
- slope;
- variability;
- baseline-distance index;
- tracking confidence;
- recovery metrics.

This follows the project's data-minimization principle.

## 13. Front versus rear camera

The project already uses the rear camera for AR and environmental search.

The first MVP should avoid requiring simultaneous front and rear camera analysis because mobile support and performance vary across devices.

Recommended sequencing:

- stationary screen task: front camera may provide optional facial feedback;
- AR/environment search: rear camera is active and facial feedback is suspended;
- after AR block: optional front-camera check-in can resume.

The camera state should be logged.

## 14. Affective adaptation examples

The system can adapt:

### Difficulty

- event rate;
- distractor density;
- memory load;
- rule-switch frequency;
- motor tempo.

### Sensory complexity

- reduce simultaneous modalities;
- reduce animation;
- simplify audio;
- temporarily remove haptics if overload is suspected.

### Regulation support

- offer pause;
- prompt body check-in;
- switch to a brief movement strategy;
- provide slower haptic breathing guidance;
- move from screen-centered task to environmental grounding.

### Instruction format

- repeat instruction in audio;
- present one rule at a time;
- temporarily display a rule reminder.

The system should not reward or punish a child for a facial pattern.

## 15. Scientific hypotheses

**H14.** Within-person facial-behavior deviations will provide incremental information about excessive task demand beyond task-performance measures alone.

**H15.** A multimodal controller using behavioral + sensorimotor + facial information will reduce periods of sustained overload compared with a controller based only on accuracy.

**H16.** Post-error facial recovery dynamics will correlate with behavioral recovery dynamics within participants, but this association will show substantial between-person heterogeneity.

**H17.** Personalized within-child facial baselines will outperform population-level categorical emotion labels for predicting self-reported task difficulty.

## 16. Experimental validation

### Study A: facial signal validity

During stationary tasks collect:

- facial derived features;
- objective task difficulty;
- errors and RT variability;
- child-reported difficulty;
- optional caregiver/observer ratings.

Test whether facial features add predictive value after behavioral variables are included.

### Study B: adaptive-controller ablation

Compare:

A. performance-only adaptation;
B. performance + sensorimotor adaptation;
C. performance + sensorimotor + facial adaptation.

Primary proximal outcomes:

- time spent in prespecified overload state;
- task completion;
- error bursts;
- self-reported excessive difficulty;
- unnecessary difficulty reductions.

### Study C: recovery analysis

Induce only ethically acceptable challenge events already present in the protocol.

Measure:

- facial response trajectory;
- task performance trajectory;
- motor trajectory;
- subjective recovery.

Test temporal coupling without assigning emotion categories.

## 17. Fairness and robustness

Facial analysis must be evaluated across:

- lighting conditions;
- skin tones;
- glasses;
- hair occlusion;
- facial morphology;
- camera angles;
- device quality;
- age;
- neurodevelopmental comorbidities where represented.

Low confidence should produce **no facial inference**, not a forced estimate.

## 18. Regulatory and ethical boundary

The module processes data from a child's face in a health-oriented research context and can influence intervention behavior.

Therefore it requires:

- explicit protocol-level justification;
- caregiver consent and age-appropriate child assent;
- ability to use the intervention without facial analysis where study design permits;
- data-protection impact assessment as appropriate;
- clear separation from biometric identification;
- legal review of applicable AI and medical-device requirements before deployment.

If the software is used in an educational institution, EU AI Act restrictions on emotion-recognition systems require specific legal review. The project should not assume that a medical or safety exception automatically applies merely because the research concerns ADHD.

## 19. Design principle

The child should never receive messages such as:

"the camera sees that you are angry."

Preferred interaction:

"That part looked difficult from your recent game signals. Would you like to slow it down, take a short pause, or continue?"

The system adapts to **difficulty and regulation needs**, not to a claimed hidden emotional truth.
