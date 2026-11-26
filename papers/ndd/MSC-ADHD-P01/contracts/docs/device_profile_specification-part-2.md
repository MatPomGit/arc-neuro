## 11. Local performance benchmark

The cross-device engineering procedure is specified in `docs/byod_cross_device_benchmark_protocol.md`.

The qualification procedure should include a short deterministic benchmark using the same runtime path as the task.

The benchmark should assess:

- frame-time stability;
- dropped/stalled frames;
- task event scheduling;
- local storage write/read;
- monotonic sequence integrity;
- state-machine transitions;
- telemetry queue persistence;
- background/resume handling.

The benchmark produces a **qualification result**, not a hardware prestige score.

## 12. Thermal and power variability

Private phones may enter thermal throttling or battery-saving modes.

Before and during a session, where platform APIs permit, the app should detect or warn about conditions likely to alter performance.

The application should:

- warn before starting if available battery is clearly insufficient;
- record relevant power-saving/thermal warnings;
- pause/abort when device behavior makes scientific timing unreliable;
- never disable user safety protections to preserve the study.

## 13. Notifications and interruptions

Because the phone remains a personal device, incoming notifications, calls and app switches are expected risks.

The app should:

- recommend a low-interruption mode before session start;
- not silently change system-wide user settings without consent;
- record application focus loss/backgrounding;
- treat interruptions according to the state-machine validity rules;
- invalidate a recovery event when the interruption destroys its interpretability;
- allow safe resume when validity is preserved.

## 14. Audio

Ordinary audio is optional for the core.

Qualification records:

- whether audio output is available;
- whether required functional sound can be played;
- whether the study uses visual fallback.

The application must not inspect unrelated media/audio history.

Headphones are not required for the core.

## 15. Haptics

Haptics are optional.

Qualification records:

- capability available/unavailable;
- whether the configured test pattern can be invoked;
- fallback availability.

A phone without haptics may qualify for the core condition when haptics are not required by that condition.

## 16. Storage and app data

Research data are written only to application-controlled storage.

The app must not require broad storage/media permissions for core telemetry.

Before a session:

- verify writable storage;
- verify sufficient queue capacity;
- verify previous unacknowledged data remain recoverable.

If durable storage cannot be guaranteed, the device is not currently qualified for a participant-facing session.

## 17. Offline-first use

A qualified device must complete the core session without continuous internet access.

Network availability affects upload only, not:

- task difficulty;
- challenge eligibility;
- safety behavior;
- recovery computation;
- strategy selection;
- session timing.

## 18. Device changes across sessions

When a participant uses a different private phone or materially changed capability profile:

1. run full qualification;
2. assign/update the installation/capability profile;
3. log the profile change;
4. do not assume RT/reference comparability automatically;
5. apply the prespecified reference-reset/sensitivity rule.

Device switching must not silently merge timing-sensitive data.

## 19. Digital-exclusion monitoring

BYOD eligibility is a feasibility outcome.

Phase 0 should report:

- proportion of screened private phones that qualify;
- proportion qualifying only with fallbacks;
- reasons for non-qualification;
- Android-version distribution in coarse form;
- optional capability availability;
- frequency of device/profile changes;
- technical interruption rate by capability/performance class.

If qualification requirements exclude a substantial subgroup, the application requirements should be reconsidered before efficacy testing.

## 20. Privacy minimization

Do not collect a field merely because Android exposes it.

Default research telemetry should not contain:

- device serial;
- IMEI;
- phone number;
- SIM information;
- account identifiers;
- Wi-Fi SSID/BSSID;
- MAC address;
- advertising ID;
- installed-app list;
- contact list;
- precise GPS;
- personal filenames or media metadata.

## 21. Phase 0 compatibility support policy

Before recruitment, define a versioned compatibility policy containing:

- minimum supported Android/API range;
- excluded runtime configurations, if any;
- mandatory core capabilities;
- benchmark acceptance rules;
- fallback rules;
- requalification triggers.

These are frozen study rules even though the physical phone model is not.

## 22. Machine-readable template

The machine-readable template remains:

`config/device_profile.phase0.template.json`.

It now describes a **private-device qualification/capability profile**, not a standardized study handset.

Model/manufacturer are not required in the default frozen scientific profile.
