## 11. State-machine replay

The benchmark should execute deterministic reference paths covering:

- normal observed-recovery path;
- right-censored path;
- technical invalidation;
- child pause;
- safe stop;
- protocol abort;
- BYOD qualified-with-fallback path;
- technical interruption/resume.

For a frozen configuration and input sequence, recorded decisions must match the reference replay.

Any unexplained mismatch is a benchmark hard failure.

## 12. Signal Gate runtime check

The benchmark uses the same runtime path as the candidate Signal Gate task.

Record:

- rendered trial count;
- expected versus delivered state transitions;
- missed/duplicated trial IDs;
- input event count;
- task exceptions;
- timing summary.

Do not use a simplified benchmark loop that bypasses the scientific task/controller code.

## 13. Storage integrity

Hard checks:

- app-local store is writable;
- committed event survives ordinary app restart;
- queue survives offline operation;
- acknowledgement removes only acknowledged records;
- retry does not create duplicate event IDs;
- checksum/record-integrity checks pass when enabled.

Any durability failure means `benchmark_passed=false` regardless of frame-time performance.

## 14. Backgrounding and private-phone interruptions

Test:

- background during baseline task;
- background during a safe non-recovery state;
- background during recovery measurement;
- resume after allowed interruption;
- invalidation when recovery interpretability is lost.

Record:

- state at interruption;
- duration according to the app monotonic/elapsed clock;
- resume target;
- event validity decision;
- actual versus expected state-machine decision.

## 15. Thermal and power context

Where Android exposes reliable information, record coarse:

- thermal warning/state;
- power-saving state;
- battery level bucket;
- change over the full-duration run.

Do not disable user/system safety protections to obtain better benchmark results.

Final qualification rules should prefer warnings/fallbacks when scientifically valid rather than excluding devices solely for noncritical differences.

## 16. Audio and haptics

For core qualification:

- ordinary audio capability is optional;
- haptics are optional.

Benchmark:

- capability detection;
- command invocation success;
- fallback activation.

The core benchmark does not claim to validate auditory or haptic physical onset timing.

The bilateral-audio companion study requires a separate stereo/acoustic qualification.

## 17. Privacy

Engineering benchmark output should use the minimum device metadata required to diagnose compatibility.

Participant-facing qualification telemetry should remain coarser than private engineering logs.

Do not collect:

- IMEI;
- device serial;
- Android ID;
- advertising ID;
- MAC address;
- personal account identifiers;
- Wi-Fi SSID/BSSID;
- contacts;
- calls/messages;
- installed-app list;
- precise GPS;
- personal media metadata.

## 18. Hard-failure criteria independent of numerical thresholds

A run is technically invalid if any of the following occurs:

- fatal application error;
- monotonic timestamp ordering violation;
- deterministic state-machine/replay mismatch;
- missing or duplicated scientific event identity caused by runtime logic;
- durable-storage failure;
- telemetry queue cannot recover after required restart;
- retry creates duplicate scientific events;
- mandatory pause/stop path fails;
- offline run changes study-critical controller behavior;
- mandatory UI/touch check fails.

These invariants can be enforced before numerical performance thresholds are frozen.

## 19. Numerical threshold selection

Timing/performance thresholds are frozen only after a cross-device engineering dataset exists.

Selection process:

1. define which metric is scientifically relevant;
2. identify the failure mode the threshold is intended to prevent;
3. inspect the engineering-only cross-device distribution;
4. run sensitivity/replay checks;
5. choose the least restrictive threshold that still protects task/recovery interpretability;
6. document excluded device classes and expected exclusion burden;
7. freeze the threshold/version;
8. do not retune it using participant clinical or recovery outcomes.

Thresholds must not be chosen simply to preserve a desired percentage of devices.

## 20. Required candidate threshold fields

The future compatibility policy should explicitly freeze, where needed:

- minimum supported Android/API version;
- maximum acceptable p95/p99 application frame time or equivalent runtime criterion;
- stall definition and maximum allowed stall burden;
- software scheduling-deviation criterion if scientifically required;
- minimum free local storage;
- maximum allowed benchmark errors;
- full-duration run requirement;
- background/resume validity rules.

Fields not required for scientific validity should not become exclusion criteria.

## 21. Cross-device analysis

Before participant recruitment summarize:

- number of tested execution profiles;
- Android-version coverage;
- display/refresh classes;
- performance-class distribution;
- hard-failure rates by reason;
- optional fallback rates;
- frame-time distributions;
- scheduling-deviation distributions;
- storage/restart reliability;
- interruption/resume reliability;
- thermal/power warnings;
- proportion that would qualify under each candidate policy.

The final policy should report the expected technical exclusion burden.

## 22. Freeze rule

The BYOD compatibility policy may be marked frozen only after:

- benchmark protocol version is frozen;
- cross-device engineering data have been reviewed;
- mandatory hard invariants pass on supported profiles;
- numerical thresholds, if used, have documented rationale;
- expected device exclusion/fallback burden is known;
- the policy is encoded in machine-readable configuration;
- the repository commit is archived.

Participant outcome data must not be used to rescue or tighten the compatibility threshold after study start.

## 23. Machine-readable report

Each benchmark run should conform to:

`schemas/byod_benchmark_run.schema.json`.

Candidate threshold configuration is maintained in:

`config/byod_benchmark_thresholds.example.json`.

Both remain engineering contracts until the compatibility policy is frozen.
