# Muse S Athena research-device verification record

Status: initial verification dated 2026-09-28. Recheck immediately before acquisition implementation and again before participant recruitment.

## Verified from current official Muse sources

The current Muse S Athena product page states that the headband records real-time brainwave activity and uses seven EEG sensors.

The current official product listing indexed on 2026-09-28 reports:

- EEG sampling rate: 256 Hz;
- sample resolution: 14 bits/sample;
- seven EEG sensors.

Muse also describes Athena as combining EEG with fNIRS and other physiological/motion sensing. The EEG paper deliberately does not make fNIRS a primary measurement channel.

The official Muse developer page states that the Muse SDK can provide access to Muse sensor data and manages Bluetooth acquisition. It also explicitly instructs academic and clinical researchers to contact Muse Research Partners for the appropriate research tools and licenses.

## Do not infer from older Muse generations

The repository must not copy electrode names, channel count conventions, reference montage, packet format, quality metrics, or timestamp semantics from Muse S Gen 2 or Muse 2 and assume that they are identical for Athena.

Before implementation, obtain Athena-specific research documentation and freeze:

- raw EEG channel labels and physical locations;
- reference and ground scheme;
- exact raw EEG units and scale conversion;
- sampling/timestamp semantics;
- packet sequence/dropout representation;
- contact/quality indicators;
- accelerometer/gyroscope channels available with the research interface;
- Bluetooth buffering behavior;
- Android integration method;
- whether raw EEG and research timestamps are available directly on the target Athena firmware;
- permitted storage/export formats;
- license terms for academic research and publication.

## Current integration gate

No participant EEG data should be collected for this study until all items above are resolved in a versioned acquisition specification.

The public product and developer pages are sufficient to justify the study concept, but they are not sufficient to freeze an acquisition pipeline.
