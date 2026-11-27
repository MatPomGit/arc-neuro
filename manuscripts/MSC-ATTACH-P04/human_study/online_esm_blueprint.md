# M04: remote ESM survey and longitudinal prediction blueprint

**2026-10-09 · PROPOSAL, NOT DEPLOYED OR ETHICS-APPROVED.** Canonical construct-to-observation map: `measurement_plan.md`. Reuse the authoritative Polish H1 items in `studies/pilot_h1/survey_items_pl.md` and preserve H1 registration/versioning rather than silently creating modified copies. M04 asks whether **baseline M03 propensity predicts later enacted action** beyond attachment and context.

## Two complementary questionnaires
**Baseline web form, once:** informed consent; 18+ adult eligibility; current romantic relationship; minimal context and relationship duration; *version-frozen and defensible* M03 scale **or a prospectively declared established substitute**; authorized Polish ECR-R anxiety/avoidance; justified contextual covariates; app/timezone and notification preferences. Retain M03 measure-version provenance. Never claim a speculative M03 factor is validated.

**ESM micro-form, repeatedly on phone (proposed schedule only, not frozen):**
| Order | H1 construct/field | Candidate question / anchor reference | Logic |
| --- | --- | --- | --- |
| 1 | `r_hat`, H1 A1 | Perceived closeness **now** (0–100) | Always |
| 2 | `r_star`, H1 A2 | Desired closeness **now** (0–100) | Always, after A1 |
| 3 | A3 | Momentary negative affect (0–100) | Always |
| 4 | B1/B1a | Recent stressor yes/no; conditional intensity | Skip if no |
| 5 | B2/D1 | Meaningful contact since previous prompt; if yes, perceived responsiveness (0–100) | Conditional, not partner-intent truth |
| 6 | C1 | Approach actions since previous prompt (0–100) | Always; record no opportunity separately |
| 7 | C2 | Distancing actions since previous prompt (0–100) | Always; can coexist with approach |
| 8 | C3 | Internal regulation since previous prompt (0–100) | Always |
| 9 | Observability | Did any relevant opportunity arise? Technical interruption, participant stop/skip | Disambiguate zeros, no-opportunity and missing |

If questions are adapted, create a **new version** and seek methodological review. The suggested additions (opportunity/observability) are exploratory proposals, **not changes to H1**.

## Temporal data and statistical plan
Record scheduled, delivered, opened and submitted timestamps in UTC with local timezone, prompt number, item timing, notification failures, last valid prompt and elapsed lag; avoid treating overnight intervals or first-morning responses as ordinary equally spaced lags. Do not fill gaps with zero actions. Derived discrepancy = desired − perceived; signed action = approach − distancing **only as secondary**, because both components can be high.

Primary M04 prediction candidate: prospectively recorded *later* action initiation ~ frozen baseline propensity + ECR-R + context/opportunity, assessed on unseen persons/couples. Secondary: within-person discrepancy-to-next-prompt action, missingness/compliance and reciprocal lag checks; do not make observational causal claims. Model clustering by person and any ethically/explicitly linked couple; avoid identifying partner relationships by default.

## TODO / gates
- [ ] **P0** Close M03 measure freeze or justify a prospectively specified alternative.
- [ ] **P0** Resolve ethics/consent, burden, sampling schedule, nighttime protection, missingness, retention and privacy safeguards.
- [ ] **P0** Cognitive-interview the full phone flow and test reminders, offline resubmission, duplicate prevention and withdrawal.
- [ ] **P0** Simulate power and interval sufficiency using observed compliance estimates; preserve H1 comparable-lag recalibration as a **separate** decision.
- [ ] **P1** Freeze timestamp, lag and held-out validation rules before participant data.
- [ ] **P2** Collect authorized ESM and publish uncertainty, lag sensitivity, attrition and null findings.

No private messages, geolocation, audio, EEG or partner reports are requested by default.
