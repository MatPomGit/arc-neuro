# ARC-ADHD BYOD cross-device benchmark protocol

Status: pre-freeze engineering protocol, version 0.1.

This protocol defines how candidate private Android execution environments are tested before the Phase 0 BYOD compatibility policy is frozen.

It does **not** define final pass/fail timing thresholds. Numerical timing thresholds must be selected from engineering evidence and scientific requirements before participant outcome data are inspected.

## 1. Purpose

The benchmark answers four questions:

1. Can the core ARC-ADHD runtime execute reliably across the intended Android range?
2. Which device/runtime characteristics materially affect task/recovery telemetry?
3. Which technical checks can be enforced locally before a participant session?
4. What compatibility/fallback policy minimizes invalid measurement without unnecessary device exclusion?

The benchmark is an engineering-validation exercise, not a ranking of phone quality.

## 2. Boundary of what the app can measure

An app-only benchmark can validly characterize:

- application frame-time distribution;
- missed/stalled application frames;
- monotonic-clock ordering;
- software scheduling deviation relative to the app's own monotonic clock;
- task/state-machine determinism;
- telemetry write/persistence behavior;
- queue restart/retry/deduplication behavior;
- application background/resume behavior;
- runtime exceptions/fatal errors;
- coarse thermal/power warnings exposed by the platform;
- supported optional capabilities.

An app-only benchmark does **not** directly establish:

- physical display onset latency;
- touch-to-photon latency;
- absolute touchscreen hardware latency;
- acoustic output latency;
- haptic perceptual onset latency.

Those quantities require an external reference measurement if the scientific analysis later depends on them.

Do not infer physical timing accuracy from software timestamps alone.

## 3. Device sampling

The engineering pool should represent the intended BYOD population rather than only recent flagship phones.

Before freeze, document coverage across:

- Android major/API versions under consideration;
- low, middle and high runtime-performance classes;
- common refresh-rate classes;
- small/medium/large logical display classes;
- devices with and without haptics;
- devices with different memory/storage constraints;
- multiple vendors where available.

The study does not need equal numbers per commercial model.

Exact manufacturer/model may be retained in the private engineering benchmark log when necessary to reproduce technical faults. It is not automatically part of participant research telemetry.

## 4. Build freeze for a benchmark round

Every benchmark round must freeze:

- repository commit;
- Unity version;
- Android build/application version;
- task configuration;
- benchmark script/configuration version;
- telemetry schema;
- state-machine version;
- BYOD qualification-policy candidate version.

Results from materially different builds must not be pooled without explicit version handling.

## 5. Run identifiers

Every run receives:

- random benchmark run ID;
- engineering device label;
- capability-profile ID;
- application version;
- Android major version;
- benchmark protocol/config version;
- run index on the device;
- execution-condition code.

The engineering device label must not be derived from IMEI, serial number, Android ID, advertising ID or MAC address.

## 6. Benchmark conditions

At minimum test each candidate execution environment under:

### Condition A: ordinary foreground run

- app in foreground;
- no intentional network dependency;
- normal device state;
- complete deterministic benchmark sequence.

### Condition B: offline run

- network unavailable;
- full task/state-machine/telemetry path remains functional;
- upload remains queued rather than affecting intervention logic.

### Condition C: restart persistence

- write a committed telemetry batch;
- terminate/restart the app;
- verify the pending queue is recoverable;
- verify no duplicate scientific events are created after retry/acknowledgement.

### Condition D: background/resume

- background the app at predefined safe states;
- resume;
- verify allowed resume paths;
- verify an open recovery interval is invalidated when the configured validity rule requires it.

### Condition E: full-duration synthetic session

- execute at least the maximum planned Phase 0 session duration;
- include repeated task/challenge/state transitions;
- monitor frame-time, errors, queue integrity and thermal/power warnings.

Additional stress conditions may be added, but they must not replace the ordinary-use conditions.

## 7. Warm-up and repetition

The benchmark configuration should define:

- warm-up duration/trials;
- number of repeated runs per execution condition;
- full-duration synthetic-session length;
- whether runs are repeated after app restart;
- whether runs are repeated after device restart.

These values remain `UNSET` until the benchmark package is frozen.

Do not choose repetition counts after inspecting which devices fail.

## 8. Frame-time metrics

Record at least:

- sample count;
- median frame time;
- p95 frame time;
- p99 frame time;
- maximum frame time;
- count/rate of frames beyond a candidate stall boundary;
- longest consecutive degraded-frame sequence.

The candidate stall boundary is a versioned engineering parameter.

Do not define a device as scientifically invalid solely because its nominal refresh rate is lower.

The relevant question is whether the frozen task and measurement logic remain stable and interpretable.

## 9. Software scheduling metrics

For deterministic scheduled events record:

- requested monotonic schedule time;
- actual callback/dispatch monotonic time;
- signed deviation;
- absolute deviation;
- p50/p95/p99 absolute deviation;
- number of severe scheduling stalls.

This measures **software scheduling behavior**, not physical stimulus onset.

If absolute physical onset is needed for a later endpoint, perform a separate external validation.

## 10. Monotonic timing invariants

Hard invariants:

- scientific event timestamps never move backward within one clock domain;
- monotonic sequence numbers are strictly increasing where required;
- no duplicate event ID represents a second scientific event;
- wall-clock changes do not alter scientific interval computation.

Any violation is an implementation/integrity failure rather than ordinary device variability.


[Continue to part 2](byod_cross_device_benchmark_protocol-part-2.md)
