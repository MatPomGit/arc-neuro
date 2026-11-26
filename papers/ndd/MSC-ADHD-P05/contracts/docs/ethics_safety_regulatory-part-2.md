## 10. Algorithmic safety

The adaptive controller should be:

- bounded;
- inspectable;
- reproducible;
- versioned;
- deterministic for equivalent input state in the first clinical build.

Avoid online self-modifying models in the initial clinical study unless their behavior can be frozen, audited and validated.

## 11. Bias and inclusion

The study should report:

- sex and age distribution;
- ADHD presentation where available;
- medication status;
- co-occurring conditions;
- socioeconomic and device-access constraints where ethically collected;
- accessibility exclusions.

A game optimized only for fast, high-performing users could systematically disadvantage children with greater impairment. Adaptation quality should therefore be evaluated across baseline severity.

## 12. Publication safety statements

Every manuscript should state:

- the intervention version studied;
- that the game is investigational unless regulatory status changes;
- conflicts of interest and developer involvement;
- who had access to telemetry;
- whether any adverse events occurred;
- that in-game metrics are not diagnostic biomarkers unless independently validated.


## 13. Multisensory safety

Audio, haptic and visual stimulation must be adjustable independently.

Required safeguards:

- conservative default audio level;
- no sudden high-amplitude sounds;
- short haptic patterns rather than continuous vibration;
- immediate mute and haptic-disable controls;
- reduced-stimulation mode;
- no loss of reward or progress for disabling a modality;
- sensory intolerance logged as a design/safety event rather than non-compliance.

Participants with sensory hypersensitivity should be accommodated whenever the study question permits.

## 14. AR and movement safety

The first clinical research build should restrict AR to a caregiver-prepared indoor play zone.

Required rules:

- no running;
- no stairs, balconies, roads, water, kitchen hazards or other unsafe zones;
- short movement paths;
- caregiver setup/confirmation before AR use;
- automatic pause when AR tracking is unstable;
- no reward contingent on continuing movement after a safety stop;
- minimize screen fixation while walking;
- provide a stationary alternative when required by accessibility or protocol.

The application should not use outdoor geolocation mechanics in the first research version.

## 15. Camera privacy in AR

The camera is required for AR tracking, but environmental imagery is not an intended research outcome.

Default architecture:

- camera frames processed locally;
- no continuous video recording;
- no upload of room imagery;
- no face recognition;
- no object recognition aimed at identifying people or private possessions;
- no exact location collection.

Any usability recording must be a separate explicitly consented procedure.

## 16. Movement sensor privacy

Accelerometer and gyroscope streams can reveal behavioral patterns.

Therefore:

- derive only prespecified movement features on device where feasible;
- upload summaries rather than raw high-frequency streams;
- document sampling and retention;
- do not infer unrelated behavioral traits from movement telemetry.

## 17. Bilateral auditory research safeguards

Alternating left-right audio is investigational within ARC-ADHD.

It must not:

- be marketed as an established ADHD therapy;
- be presented as EMDR;
- be used to elicit or process traumatic memories;
- be described as clinically effective before controlled evidence exists.

Research use should include:

- matched non-alternating control;
- safe volume cap;
- immediate stop;
- stereo channel verification;
- adverse sensory response logging;
- explicit reporting of null findings.

The study should distinguish bilateral auditory stimulation from external trigeminal nerve stimulation or other electrical neuromodulation methods. These are different interventions and evidence for one cannot be transferred to the other.

## 18. Local facial-analysis safeguards

The front-camera module is optional research instrumentation, not a truth detector for emotion.

Required safeguards:

- local inference by default;
- no raw facial video in standard telemetry;
- no face recognition or identity embeddings;
- no population-level claim that a facial pattern means a specific emotion;
- personal baseline calibration;
- confidence gating and explicit missing-data state;
- ability to disable the module where protocol permits;
- no reward, penalty or feedback based on smiling, frowning or other individual expressions;
- explicit caregiver consent and age-appropriate child assent;
- clear explanation that the camera measures movement patterns, not hidden thoughts or intentions.

The child's self-report has epistemic priority over an algorithmic facial proxy when the two disagree.

If used in an educational institution, deployment requires specific legal review under Regulation (EU) 2024/1689. Article 5 restricts AI systems used to infer emotions in workplace and educational settings, subject to the regulation's stated medical or safety exception. The project must not assume that the exception applies automatically.

The research design should avoid unnecessary categorical emotion inference altogether and instead analyze descriptive facial-behavior dynamics and task-recovery relationships.

## 19. Body-awareness safety

Body-focused prompts should remain neutral and non-evaluative.

The game should not:

- tell the child what they "must" be feeling;
- infer emotional truth from a body response;
- reinforce hypervigilant monitoring of bodily sensations;
- require breath holding or uncomfortable breathing patterns;
- treat inability to notice a bodily signal as failure.

The intended skill is flexible noticing followed by useful action, not continuous self-monitoring.
