# ARC-ADHD core preregistration template

Status: template. Complete and freeze before the relevant participant-facing study.

## 1. Registration metadata

- study title:
- registration platform:
- registration date:
- repository commit:
- intervention manifest version:
- telemetry schema version:
- statistical analysis plan version:
- principal investigator:
- clinical/developmental lead:
- statistical lead:
- measurement/psychometrics lead:
- software/reproducibility lead:
- safety-monitoring lead:
- study-operations lead:
- controller representative:
- data-protection officer/privacy advisor:
- security/data-engineering lead:
- data manager:
- data-protection/safety lead (legacy combined field, if used):

Role assignments should reference `docs/study_roles_and_responsibilities.md`, including documented backups/delegates and any incompatible-role mitigations.

## 2. Study stage

Select one:

- Phase 0 co-design/construct validation;
- Phase 1 feasibility;
- Phase 2 pilot randomized trial;
- Phase 3 confirmatory randomized trial.

State explicitly what the study is **not** designed to establish.

## 3. Research questions

### Core mechanism

Does the challenge-regulation-recovery sequence yield a stable, measurable recovery process?

### Transfer question

Does change in recovery relate to independent outcomes beyond trained-task performance?

### Stage-specific question

Specify the single stage-specific primary research question.

## 4. Participants

- target age:
- diagnostic confirmation procedure:
- recruitment setting:
- medication policy:
- comorbidity policy:
- inclusion criteria:
- exclusion criteria:
- accessibility adaptations:
- target sample size and rationale:
- expected attrition:
- stopping/safety rules:

## 5. Intervention

Reference the frozen intervention manifest.

Specify:

- session duration;
- number of sessions;
- intervention period;
- executive task(s);
- challenge types;
- strategy library;
- sensory channels;
- adaptation hierarchy;
- BYOD compatibility-policy version;
- device-qualification rule version;
- handling of device/profile changes and timing-sensitive reference resets;
- caregiver involvement.

### BYOD feasibility

Predefine:

- mandatory qualification checks;
- optional-capability fallback rules;
- requalification triggers;
- how nonqualification is counted;
- how device/profile changes are handled analytically;
- which coarse capability fields are retained;
- which hardware/account identifiers are explicitly not collected.

## 6. Active control

Reference docs/active_control_specification.md and the frozen control manifest.

Specify:

- matched features;
- prohibited core-mechanism features;
- dose;
- reward structure;
- sensory configuration;
- credibility/expectancy assessment.

## 7. Challenge-event eligibility

Define exactly when an event can enter recovery analysis.

Required fields:

- exact challenge type and permitted rule directions;
- task and state identity;
- current and target rule;
- explicit switch-cue requirement;
- A/B calibration requirement;
- minimum immediate prechallenge reference count;
- minimum GO/NO-GO composition;
- reference-rule match;
- fresh-reference rule after pause and prior recovery;
- minimum valid trials after the previous recovery closes;
- exclusion interval after the previous challenge;
- maximum challenges per session;
- locked event-time-budget rule;
- remaining-session-time rule;
- telemetry/integrity requirements;
- open-recovery-event exclusion;
- technical-interruption state;
- safety and sensory-overload state;
- recent-pause state;
- core event eligibility versus timing-feature eligibility;
- timing-profile qualification;
- target-rule/mapping-matched timing reference;
- complete suppression and timing-unavailability reason vocabularies;
- confirmation that challenge eligibility is not conditioned on a post-switch error or other observed destabilization.

## 8. Recovery definition

Freeze:

- selected candidate model ID (B, B+S, B+V, or B+S+V);
- q_e(t) component features;
- feature direction signs;
- feature weights;
- reference-window duration;
- standardization rule;
- epsilon or numerical guard;
- delta;
- stability window w in consecutive score updates;
- recovery time origin = entry into RECOVERY_MONITORING;
- censor limit c_e measured from recovery-monitoring onset;
- definitions of T_pre, T_rec and T_total;
- missing-feature policy;
- right-censoring reasons.

## 9. Outcomes

### Stage-specific primary outcome

- exact instrument/measure:
- respondent:
- assessment time:
- scoring:
- direction of benefit:
- minimally important difference if applicable:

### Mechanistic outcome

- T_rec as the primary monitoring-anchored performance-recovery latency;
- T_pre as challenge-to-monitoring process duration;
- T_total = T_pre + T_rec as total challenge-to-stable-return time;
- unrecovered-event proportion;
- other prespecified recovery summaries.

### Independent near-transfer outcomes

List measures that are not trained-task variants.

### Secondary clinical/functional outcomes

List measures and roles.

## 10. Hypotheses

For each hypothesis specify:

- exact contrast;
- outcome;
- direction;
- time point/window;
- population;
- confirmatory/secondary/exploratory status;
- falsification criterion.

## 11. Randomization

For randomized studies specify:

- allocation ratio;
- sequence generation;
- concealment;
- stratification;
- block strategy;
- who can access allocation;
- outcome-assessor masking;
- procedures for accidental unmasking.

For micro-randomized events specify:

- eligibility;
- condition set;
- randomization probability;
- carryover window;
- proximal outcome window.

## 12. Analysis populations

- intention-to-treat;
- safety population;
- mechanistic event population;
- any per-protocol analysis and its strictly secondary role.

## 13. Statistical models

### External outcome model

Specify formula, baseline adjustment, time structure and covariance.

### Recovery model

Specify time-to-event model, participant/session structure and censoring treatment.

### Cue experiment

Specify proximal estimand and repeated-event method.

### Missing data

Specify primary assumption, imputation/likelihood strategy and sensitivity analysis.

## 14. Multiplicity

Identify:

- the single confirmatory primary endpoint if Phase 3;
- secondary families;
- exploratory analyses;
- whether/where multiplicity adjustment is used.

## 15. Progression criteria

Reference the frozen version of docs/progression_criteria.md.

State:

- green/amber/red thresholds;
- decision committee;
- treatment of amber domains;
- safety overrides.

## 16. Data exclusions

Predefine:

- technical-failure exclusions;
- protocol deviations;
- impossible timestamps;
- duplicate events;
- incomplete telemetry;
- events that remain analyzable as censored rather than excluded.

No exclusion may depend on whether the outcome is favorable.

## 17. Robustness and sensitivity analyses

Predefine a small number of justified checks.

For recovery:

- alternative delta values;
- alternative w values;
- alternative censor limits.

These cannot replace the primary specification.

## 18. Overlap with companion papers

Declare whether participants or sessions also contribute to:

- facial-feedback study;
- bilateral-audio study;
- embodied/AR study.

List exactly which observations overlap and which paper owns each primary hypothesis.

## 19. Deviations

Any change after registration must include:

- date;
- reason;
- decision maker;
- whether outcome data were visible;
- affected hypotheses/analyses;
- new repository commit.

## 20. Reproducibility record

Archive at study lock:

- preregistration PDF/export;
- repository commit hash;
- intervention manifest;
- active-control manifest;
- telemetry schema;
- analysis script version;
- task configuration files;
- randomization code/version;
- participant-facing materials.
