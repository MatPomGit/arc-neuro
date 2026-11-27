## 5. Fine-motor training

Holding and rotating a smartphone mainly trains wrist/forearm control rather than isolated fine finger dexterity.

To specifically target fine motor control, combine touch and IMU.

Candidate tasks:

### Stable-hand tracing

The child traces a narrow path with one finger while keeping the phone within a target orientation range.

Metrics:

- trace error;
- touch velocity variability;
- orientation drift;
- number of corrective movements.

### Tap sequence with postural constraint

The child performs a finger sequence while holding the phone at a prescribed angle.

Metrics:

- timing accuracy;
- sequence errors;
- unwanted device movement.

### Pinch/drag with rhythmic cue

Pinch or drag gestures must occur at specific points in a haptic rhythm.

Metrics:

- temporal error;
- spatial error;
- pressure proxy where the platform supports it;
- motion artifact.

### Dual-task motor control

Maintain device orientation while responding to occasional auditory targets.

This permits controlled examination of motor-cognitive interference.

## 6. Body-awareness integration

Each sensorimotor task can include a brief body-state loop.

Before:

- How tight are your hands?
- Are your shoulders relaxed?
- Is your breathing easy to notice?
- Does your body want to move quickly or slowly?

During:

- haptic cue guides the action;
- the child notices effort and tension;
- no requirement is made to label an emotion.

After:

- compare tension, breathing and activation;
- select whether the movement helped, changed nothing or made regulation harder.

This is the appropriate point where sensorimotor training can connect to interoceptive awareness.

## 7. Haptic entrainment model

For beat times h_k and detected movement peaks m_k, define temporal synchronization error:

e_k = m_k - h_k

Candidate derived measures:

mean absolute synchronization error:

MAE_sync = mean(|e_k|)

variability:

SD_sync = SD(e_k)

and signed phase bias:

Bias_sync = mean(e_k)

These allow separation of:

- systematic anticipation;
- systematic lag;
- unstable timing.

The adaptation controller can modify tempo only after a stable measurement window.

## 8. Movement smoothness

Raw IMU data should be filtered before analysis.

Candidate features:

- angular velocity RMS;
- peak angular velocity;
- angular jerk;
- number of direction reversals;
- spectral power around the target frequency;
- movement entropy;
- overshoot count.

These are process measures. They are not diagnostic biomarkers unless separately validated.

## 9. Camera-guided real-world search

The rear camera can turn the real environment into a visual-search space.

## 9.1 Color search

Example instruction:

"Find something blue."

The application can locally identify image regions in a target hue range.

The child moves the device until a sufficiently large stable region is detected.

Possible variables:

- search time;
- camera path;
- number of false candidate regions;
- dwell time before confirmation.

Color detection must account for illumination and white-balance variability.

## 9.2 Shape search

Example:

"Find a circle."

Possible first-stage implementation:

- contour extraction;
- polygon approximation;
- circle/ellipse detection;
- geometric confidence threshold.

This is preferable to unrestricted object recognition for the first research prototype because the rule is auditable and privacy risk is lower.

## 9.3 Combined rule

Examples:

- find a red circle;
- find a blue rectangular region;
- find one object matching color A but not shape B.

This supports:

- selective attention;
- working-memory rule maintenance;
- inhibition of distractors;
- rule switching.

## 10. Audio-guided real-world search

Sound can guide attention without requiring continuous fixation on the screen.

Candidate implementations:

### Proximity sonification

As the camera or AR system estimates that the searched target is closer to the center or target location:

- pulse rate increases;
- pitch changes;
- stereo balance shifts.

### Directional stereo cue

When a target is estimated to the left or right of the camera center:

- audio balance shifts toward that side.

The child searches the room by integrating auditory direction with real-world vision.

### Haptic complement

A brief vibration can indicate:

- target acquired;
- target lost;
- stop and verify;
- return to neutral orientation.

The audio should guide attention, not force the child to stare at the display.

## 11. Multisensor search loop

A complete search task can follow:

1. spoken instruction gives the rule;
2. child memorizes the target;
3. screen guidance fades;
4. child scans the real environment with the rear camera;
5. audio guides direction;
6. IMU measures search movement;
7. local vision verifies color/shape;
8. haptic signal confirms acquisition;
9. child lowers the phone;
10. brief body-state check follows.

This is a concrete realization of the ARC principle:

**screen -> body action -> environment -> multisensory feedback -> regulation -> goal completion**

## 12. Sensor-fusion state vector

Extend the modality model with a sensor state:

s_t = [omega_t, a_t, q_t, touch_t, cam_t, audio_t]

where:

- omega = angular velocity;
- a = acceleration;
- q = estimated orientation;
- touch = touch interaction state;
- cam = locally derived visual features;
- audio = output/input event state.

Observed behavior becomes:

y_t = f(x_t, d_t, m_t, s_t, c_t) + epsilon_t

This permits sensor-derived behavior to be modeled without treating raw sensor values as direct measures of ADHD severity.

## 13. Adaptation

Adaptation can occur on separate dimensions:

- cognitive load;
- motor precision;
- rhythm tempo;
- sensory complexity;
- visual-search complexity;
- amount of guidance.

Example:

A child may show accurate cognitive performance but poor motor synchronization. The system should lower motor tempo rather than simplify the cognitive rule.

Conversely, good motor rhythm with poor rule maintenance should not trigger faster movement.

## 14. Safety

### Movement

- no throwing the device;
- no rapid maximal-amplitude wrist movements;
- no tasks requiring movement near the face;
- optional seated version;
- pause on excessive acceleration;
- caregiver configuration for younger participants.

### Camera

- local frame processing;
- no recording by default;
- no face recognition;
- no upload of environmental imagery;
- do not ask the child to search for people.

### Haptics

- short bounded patterns;
- user-adjustable intensity;
- immediate disable option.

### Sensor interpretation

Do not classify a child as having a motor deficit, poor interoception or ADHD severity based solely on game telemetry.

## 15. Experimental decompositions

### Haptic entrainment experiment

Compare:

A. haptic rhythm;
B. auditory rhythm;
C. audio+haptic rhythm.

Outcome:

- synchronization error and variability.

### Visual-search guidance experiment

Compare:

A. visual screen arrow;
B. auditory guidance;
C. auditory+haptic guidance.

Outcome:

- real-world target acquisition time while minimizing screen fixation.

### Motor-cognitive dual-task experiment

Compare:

A. motor rhythm only;
B. cognitive task only;
C. simultaneous motor+cognitive task.

Outcome:

- dual-task cost for motor and cognitive performance.

### Camera-search experiment

Compare:

A. color rule;
B. shape rule;
C. conjunction rule.

Outcome:

- search time, false detections and rule errors.

## 16. Core research hypothesis

The smartphone should be treated as a **sensorimotor mediator** between cognition, body and environment.

The strongest testable claim is not that gyroscope training "treats ADHD", but that multimodal sensorimotor tasks can:

1. quantify and train specific motor-control processes;
2. create repeated opportunities for inhibition and rule maintenance during movement;
3. improve engagement with real-world space;
4. provide a structured bridge from externally cued movement to awareness of bodily state;
5. generate mechanistic variables that can be tested against independent outcomes.
