# Local facial-feedback and affective adaptation

## 1. Rationale

ARC-ADHD can use the front camera as an optional, local feedback channel for estimating how task demand is affecting the child during selected stationary game segments.

The module should not be framed as a system that "reads emotions from the face". A safer and scientifically stronger formulation is:

**local analysis of facial behavior and facial reactivity used as a probabilistic auxiliary signal for adaptive task regulation.**

The facial signal should be interpreted only together with behavioral, sensorimotor and self-report information.

## 2. Technical approach

A suitable first implementation is an on-device face-landmark pipeline such as MediaPipe Face Landmarker.

The module can extract:

- facial landmarks;
- facial transformation matrix / coarse head pose;
- blendshape coefficients;
- eye-blink-related coefficients;
- mouth press/stretch/open coefficients;
- brow movement coefficients;
- cheek/squint coefficients;
- tracking confidence.

No face identity recognition is required.

The system should never create a reusable face template for identifying the child.

## 3. Personal baseline rather than population emotion classifier

Facial behavior differs substantially between children.

ARC-ADHD should therefore use a brief within-person calibration period and model deviations from the child's own baseline rather than map a facial pattern directly to a universal emotion category.

Let:

phi_t = [b_t, h_t, q_t]

where:

- b_t = vector of selected facial blendshape coefficients;
- h_t = coarse head-pose/orientation features;
- q_t = tracking-quality/confidence variables.

Estimate a personal neutral/task-engaged baseline:

mu_phi, sigma_phi

from short low-demand calibration periods.

Then compute normalized within-person deviations:

z_phi(t) = (phi_t - mu_phi) / (sigma_phi + epsilon)

The system should analyze temporal patterns and change relative to baseline, not a single video frame.

## 4. What the system may estimate

The module may estimate operational states such as:

- increased facial motor activity;
- sustained facial tension proxy;
- reduced facial movement;
- repeated gaze/head diversion;
- increased blink-rate proxy;
- strong post-error facial reaction;
- slow return to personal baseline after challenge;
- prolonged loss of frontal-face tracking.

These states should be named descriptively.

Avoid directly labeling them as:

- anger;
- anxiety;
- sadness;
- frustration;
- boredom;
- deception;
- motivation.

Such labels require separate validation and can easily overstate what facial behavior can support.

## 5. Multimodal state fusion

Facial behavior should be a low-weight auxiliary signal in a multimodal model.

Define:

r_t = [P_t, M_t, F_t, S_t]

where:

- P_t = task-performance evidence, such as errors, omissions and reaction-time variability;
- M_t = motor/sensorimotor evidence from IMU and touch;
- F_t = facial-behavior evidence;
- S_t = subjective signal from the child's check-in when available.

The adaptive controller estimates a latent challenge state C_t:

C_t = g(P_t, M_t, F_t, S_t, history)

The controller should react only when evidence is sufficiently convergent and persistent.

A facial signal alone must never trigger a clinical conclusion.

## 6. Example adaptive rules

### Case A: likely excessive task demand

Observed jointly:

- repeated errors;
- increasing response-time variability;
- persistent facial-tension deviation from baseline;
- reduced movement precision.

Possible response:

1. reduce one cognitive difficulty dimension;
2. reduce sensory load if high;
3. offer a brief regulation pause;
4. reassess after a fixed window.

### Case B: facial change without behavioral deterioration

Observed:

- facial activity deviates from baseline;
- task accuracy and motor control remain stable.

Response:

- do not automatically reduce difficulty;
- continue monitoring;
- optionally request a brief subjective check-in at a natural break.

### Case C: behavioral deterioration without usable face signal

Observed:

- repeated errors or loss of rhythm;
- face not detected or camera disabled.

Response:

- adaptation continues from behavioral signals;
- no penalty or missing-data inference is applied.

### Case D: post-error recovery

After a challenge:

- facial response peaks;
- task performance destabilizes;
- facial state and performance gradually return toward baseline.

Potential derived variables:

- facial reaction amplitude;
- facial recovery time;
- behavioral recovery time;
- coupling between facial and behavioral recovery.

This is more informative than assigning a categorical emotion label.

## 7. Facial recovery metric

Let D_phi(t) represent distance from the child's calibrated facial baseline.

For example:

D_phi(t) = sqrt(sum_i w_i * z_phi,i(t)^2)

After challenge event e, define facial recovery time:

T_face_rec = first time after e when D_phi(t) remains below threshold theta for a prespecified duration.

This can be compared with behavioral recovery:

T_task_rec

The difference:

Delta_rec = T_face_rec - T_task_rec

is an exploratory measure of temporal coupling between facial behavior and task recovery.

It must not be interpreted as a diagnostic marker without external validation.

## 8. Facial-feature selection

The first implementation should avoid feeding all available facial coefficients into an opaque model.

Recommended approach:

1. select a small preregistered set of interpretable features;
2. use rolling means/slopes rather than single-frame values;
3. normalize per participant;
4. use explicit confidence thresholds;
5. include missingness and head-pose quality;
6. test robustness to glasses, lighting, skin tone, face angle and device position.

Candidate feature groups:

- brow contraction/elevation;
- eye squint/widening;
- blink dynamics;
- mouth press/stretch;
- jaw opening;
- head turning/downward orientation.

The scientific analysis should report features, not anthropomorphic labels.

## 9. Optional self-calibration loop

At selected moments, the game can ask the child:

"Was that easy, okay, or too hard?"

The answer can be paired with the immediately preceding facial-behavior window.

This enables supervised within-person calibration of difficulty-related facial responses without assuming that population-trained emotion labels apply to the child.

Importantly:

- the child is the primary source about subjective experience;
- facial analysis is auxiliary;
- disagreement between self-report and facial proxy should not be resolved in favor of the algorithm.

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
