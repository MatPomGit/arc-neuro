# Sensorimotor fusion and smartphone-sensor training

## 1. Rationale

ARC-ADHD should treat the smartphone not only as a display and response surface, but as a compact multisensor device that can measure how the child moves, orients and synchronizes the device with sensory cues.

The core principle is **closed-loop sensorimotor training**:

**cue -> bodily action -> sensor measurement -> immediate feedback -> adaptation -> reflection**

This extends the intervention beyond visual cognitive training and creates experimentally measurable links between attention, inhibition, rhythm, motor control and body awareness.

## 2. Scientific distinction: interoception, proprioception and sensorimotor control

Moving a phone in response to vibration is not a pure interoception task.

It primarily combines:

- proprioception, awareness of limb and joint position;
- tactile/haptic perception;
- vestibular and visuospatial information;
- sensorimotor synchronization;
- motor planning and correction.

Interoception concerns signals originating from within the body, such as breathing, cardiac sensations, visceral state and perceived arousal.

ARC-ADHD should therefore describe these exercises as an **interoceptive-proprioceptive bridge** when they combine:

1. externally generated haptic rhythm;
2. controlled movement;
3. subjective observation of bodily tension, breathing or activation;
4. comparison of body state before and after movement.

This prevents conceptual overclaiming.

## 3. Smartphone sensor set

### 3.1 Gyroscope

Measures angular velocity around the device axes.

Primary uses:

- controlled wrist rotation;
- rhythmic pronation/supination-like movements;
- orientation-change tasks;
- smoothness measurement;
- stop/start motor inhibition;
- synchronization to haptic or auditory rhythm.

### 3.2 Accelerometer

Measures linear acceleration including the gravity component.

Primary uses:

- movement onset/offset detection;
- movement amplitude proxy;
- shake versus controlled motion discrimination;
- rhythmic up/down or lateral movement;
- movement regularity;
- detecting whether the device is stationary.

### 3.3 Sensor fusion / device orientation

Use fused orientation estimates rather than raw gyroscope integration when possible.

Primary uses:

- target-angle tasks;
- slow trajectory following;
- orientation memory;
- returning the device to a neutral pose;
- tracing spatial patterns by tilt.

### 3.4 Touchscreen

The touchscreen should be combined with IMU rather than treated as a separate interface.

Examples:

- stabilize the phone while tracing with one finger;
- drag an object while maintaining a target orientation;
- alternate thumb taps while following a haptic rhythm;
- perform a fine touch sequence while ignoring irrelevant device movement cues.

These tasks are better candidates for **fine motor control** than phone rotation alone.

### 3.5 Rear camera

The rear camera can support real-world visual search without storing images.

Candidate functions:

- detect a requested color region;
- detect simple geometric shapes;
- verify that a virtual task target corresponds to a real object property;
- recognize fiducial markers in controlled research tasks;
- estimate coarse object position in the image.

The first research build should prefer low-risk local computer-vision operations over open-ended semantic recognition.

### 3.6 Microphone

The microphone is not required for the initial core intervention.

Possible future uses:

- clap/tap rhythm timing;
- environmental sound-level estimation;
- voice-guided interaction.

Continuous audio recording should not be part of standard telemetry.

### 3.7 Magnetometer

Potential use:

- coarse orientation tasks;
- directional search.

Because indoor magnetic fields are noisy, it should not be a primary precision sensor.

### 3.8 Ambient light sensor

Where the platform exposes a reliable sensor, ambient light can support:

- automatic adaptation of visual contrast;
- detection of unsuitable camera-search lighting;
- logging environmental illumination class.

It should not become a therapeutic variable unless separately studied.

### 3.9 Proximity sensor

Where accessible, proximity can support simple near/far interaction states, but availability differs across devices and operating systems.

### 3.10 Barometer

On devices that expose pressure sensors, the barometer can support coarse vertical-change experiments, but it is not required for the core intervention.

### 3.11 Capability principle

Every non-core sensor must have:

- runtime capability detection;
- a defined fallback;
- a versioned device-capability record;
- no requirement that would unnecessarily exclude participants with lower-cost phones.

## 4. Motor-training modules

## 4.1 Haptic rhythm matching

The phone generates a haptic pulse train. The child moves the phone in time with the rhythm.

Example movements:

- slow left-right rotation;
- controlled forward-back tilt;
- small circular wrist motion;
- alternating movement and stillness.

Measured variables:

- phase lag relative to the haptic beat;
- inter-movement interval variability;
- amplitude variability;
- movement smoothness;
- premature movement;
- missed movement;
- overshoot.

The haptic rhythm can gradually change to train adaptation rather than rote repetition.

## 4.2 Auditory-haptic synchronization

Audio and haptic cues can be presented:

- synchronously;
- with a small deliberate phase offset;
- with one modality removed;
- with alternating modality leadership.

Research questions:

- Which modality produces the best synchronization?
- Does congruent audiovisual-haptic timing improve motor regularity?
- Can the child inhibit the dominant cue when the rule changes?

## 4.3 Stop-go motor inhibition

The child moves the phone rhythmically until a stop cue appears.

Stop cue variants:

- sound;
- vibration pattern;
- visual flash;
- multimodal cue.

Outcomes:

- stop latency;
- residual movement after stop cue;
- false starts;
- ability to resume the rhythm.

This combines motor control and inhibitory control in one observable task.

## 4.4 Orientation target

The game asks the child to place the phone at a target orientation.

Difficulty can change through:

- smaller tolerance window;
- memory delay before movement;
- removal of visual guidance;
- distractor sound;
- rule reversal.

Outcomes:

- angular error;
- movement time;
- overshoot;
- correction count;
- path efficiency.

## 4.5 Smooth trajectory task

The child follows an invisible or partially visible orientation trajectory.

This supports:

- slow controlled movement;
- continuous error correction;
- sustained attention;
- sensorimotor prediction.

Candidate metrics:

- RMS orientation error;
- mean angular jerk;
- correction frequency;
- spectral concentration around the target rhythm.

## 4.6 Bilateral hand-switching task

The same task is repeated with the phone held in the left and right hand.

The aim is not to diagnose lateralization. It is to:

- vary motor context;
- prevent overlearning with one hand;
- test transfer of a learned rhythm;
- compare within-person motor consistency.

Hand condition must be logged.


[Continue to part 2](sensorimotor_fusion-part-2.md)
