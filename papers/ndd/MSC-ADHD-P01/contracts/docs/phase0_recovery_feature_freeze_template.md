# ARC-ADHD Phase 0 recovery-feature freeze record

Status: template. Complete after Phase 0 measurement analysis and before Phase 1 inferential use.

This record is the auditable handoff from the prespecified candidate space to one frozen recovery model. It must be completed without using EDI, caregiver/teacher ratings, treatment-group differences, or other external clinical outcomes to choose the model.

Authoritative candidate specification:

- `docs/recovery_feature_operationalization.md`;
- `config/recovery_feature_candidates.phase0.json`.

## 1. Study and software identity

- Phase 0 study identifier:
- repository commit:
- intervention version:
- Signal Gate task version:
- recovery-event schema version:
- BYOD qualification-policy version:
- timing-benchmark version:
- analysis script commit:
- analysis date:

## 2. Candidate models

Evaluate all four models.

| Model | Components | Prespecified weights |
| --- | --- | --- |
| B | balanced rule success | B = 1.00 |
| B+S | behavior + correct-GO slowing | B = 0.50, S = 0.50 |
| B+V | behavior + RT variability increase | B = 0.50, V = 0.50 |
| B+S+V | behavior + slowing + variability | B = 0.50, S = 0.25, V = 0.25 |

No unregistered feature subset or alternative weight vector belongs in the primary Phase 0 selection analysis.

## 3. Hard-gate results

For each candidate report the numerator, denominator, proportion, confidence interval where useful, and pass/fail result.

| Gate | B | B+S | B+V | B+S+V |
| --- | --- | --- | --- | --- |
| Eligible-event computability ≥ 0.90 | | | | |
| Reference/device scale-floor fraction ≤ 0.20 | | | | |
| Worst leave-one-trial terminal-state flip fraction ≤ 0.20 | | | | |
| Timing-qualified event coverage ≥ 0.90 | N/A | | | |
| Overall hard-gate result | | | | |

The leave-one-trial result must be the worst value across:

- \(\delta\) = 0.25, 0.50, 0.75;
- stability windows = 2, 3 consecutive score updates.

Do not report only the most favorable combination.

## 4. Robustness matrix

Record the leave-one-trial terminal-state flip fraction for every model and every threshold pair.

| Model | δ=0.25,w=2 | δ=0.25,w=3 | δ=0.50,w=2 | δ=0.50,w=3 | δ=0.75,w=2 | δ=0.75,w=3 | Worst |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B | | | | | | | |
| B+S | | | | | | | |
| B+V | | | | | | | |
| B+S+V | | | | | | | |

## 5. Diagnostic quantities not used for model selection

Report these for transparency but do not rank candidate models by them:

- right-censoring fraction;
- median recovery latency;
- distribution of q;
- proportion of immediate/near-immediate recoveries;
- challenge-event count per participant/session.

## 6. Timing-feature diagnostics

For the target-rule recovery reference report:

- confirmation that (B), and when available (S/V), use the same versioned `RULE_CALIBRATION` reference for the target post-switch rule;
- confirmation that the reference rule and GO-stimulus identity match the recovery window;
- rule-specific calibration reference stability/drift across session order;
- whether any material device/profile change occurred after calibration;

For S and V additionally report:
- proportion of events on timing-qualified profiles;
- number of correct GO RT observations per reference and rolling window;
- proportion of reference windows where the device timing floor dominates MAD;
- distribution of the qualified-device timing floor;
- missingness caused by insufficient correct GO trials;
- missing timing-profile identifiers or timing-reference provenance.

## 7. Redundancy and interpretability check

Confirm:

- GO/NO-GO conditional success can be reconstructed from trial telemetry;
- omission and commission summaries are not entered as additional independent weights;
- no positive component compensation is possible;
- q stored in recovery events exactly matches the selected model weights and component deficits;
- measurement-context changes are classified as recovery-data-invalid, not as recovery or censoring.

## 8. Prespecified decision rule

Apply in this order:

1. Reject every candidate that fails a hard gate.
2. If B passes all hard gates, retain B unless a prespecified measurement failure specifically requires an enriched model and the enriched model resolves that failure.
3. If B fails and multiple enriched models pass, prefer the lowest complexity rank.
4. For equal complexity, prefer lower feature missingness and lower leave-one-trial instability.
5. Do not use clinical or external outcome association as a tie-breaker.
6. If no candidate passes, do not manufacture a winner. Redesign the recovery operationalization and repeat construct-validation work before Phase 1.

## 9. Decision

- selected model ID:
- models rejected:
- exact gate(s) causing each rejection:
- reason the selected model follows the prespecified rule:
- any deviations from the preregistered candidate space:
- whether outcome data external to the task were visible at the time of the decision:
- decision date:
- repository commit containing the frozen definition:

## 10. Final Phase 1 recovery definition

Freeze:

- selected model ID:
- feature definitions/version:
- immediate current-rule eligibility-reference rule:
- target-rule recovery-reference construction/version:
- target-rule recovery-reference source = RULE_CALIBRATION:
- within-session reference-update policy:
- rolling post-challenge window:
- update stride:
- minimum GO/NO-GO counts:
- correct-GO RT minimum counts:
- target-rule timing-reference rule:
- timing-floor rule:
- weights:
- delta:
- stability-window count in score updates:
- latency origin = RECOVERY_MONITORING onset:
- T_pre/T_rec/T_total definitions:
- monitoring censor limit:
- missing-feature policy:
- measurement-context lock version:
- right-censoring reasons:
- scientific-invalidity reasons:
- recovery-event schema version:

## 11. Prohibited evidence for model selection

Confirm that none of the following was used to select the model:

- EDI;
- caregiver symptom score;
- teacher symptom score;
- functional outcome;
- treatment-group contrast;
- association with later clinical change;
- nominal p value from an efficacy analysis.

Any later association with those outcomes is an independent test of mechanistic relevance, not a calibration criterion.
