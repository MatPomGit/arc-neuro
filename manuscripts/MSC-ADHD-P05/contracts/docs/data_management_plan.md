# ARC-ADHD research data management plan

Status: active programme policy, pre-recruitment.

This plan complements docs/local_data_store.md, docs/telemetry_specification.md, docs/ethics_safety_regulatory.md and study-specific protocols.

## Data classes
1. Protocol/configuration: intervention manifests, task parameters, eligibility/safety rules, random seeds and version locks.
2. Application telemetry: event streams, task performance, recovery events, controller state and timing.
3. Device engineering data: device profile, timing/latency, sensor capability, benchmark output and app/runtime version.
4. Optional sensing data: facial features, audio-condition integrity, AR/environmental data, wearable EEG and derived features.
5. External outcomes: validated questionnaires, near-transfer measures and functional outcomes.
6. Identity/contact data: recruitment and operational records, kept separate from analysis identifiers.
7. Derived analysis data: cleaned tables, quality flags, model outputs, figures and result bundles.

## Identity and provenance
Every reportable session/dataset must record pseudonymous participant ID; study/phase/session IDs; acquisition time; exact app build/version and Git commit; frozen configuration hashes; device profile and qualification status; schema version; source checksums; processing-code commit/version; and evidence class.

Register reportable evidence in research/evidence_registry.yaml.

## Raw, curated and derived data
Raw event history required for audit must be preserved immutably. Cleaning is represented through derived datasets plus explicit quality/exclusion flags. Raw observations are never overwritten to improve apparent data quality.

## Data minimisation
Only fields required by the frozen scientific purpose may leave the participant device. Camera, microphone, environmental imagery and EEG require module-specific justification and consent/assent. Prefer on-device features over raw media where scientifically sufficient.

## Storage and transfer
Before participant data collection define encryption, local-device protection, backend/controller/processor arrangements, retention, backup/restore, withdrawal/deletion semantics, identity-data separation and least-privilege access.

## Dataset lock
Each inferential dataset receives a unique lock identifier, generation timestamp, source-evidence list, derivation commit, schema version and checksum. Any post-lock correction creates a new dataset version and documented reason.

## Publication and sharing
No identifying or sensitive raw participant data belong in ordinary Git history. Public releases should contain code, schemas, protocols, synthetic examples, appropriately de-identified/aggregate derived artifacts and reproducibility metadata subject to consent, ethics, licensing and GDPR constraints.
