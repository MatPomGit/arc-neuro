# M03: online questionnaire implementation blueprint

**2026-10-09 · PROPOSAL, NOT APPROVED/DEPLOYED.** Extends `measurement_plan.md` without modifying its construct definitions or replacing the ethics application. M03 measures **relational-control propensity**; this is neither attachment anxiety/avoidance nor a computational P/PI/PID gain.

## Sampling and phase separation
Target: adults 18+, Polish-language competence, currently in a romantic relationship; final relationship-duration rule must be set before recruitment. Recruit **individuals**, not required couples. Independent expert/content review, cognitive interviews, EFA development, **new-sample** CFA confirmation and an optional retest are **distinct phases**. Do not reuse EFA cases for independent CFA. Sample sizes follow precision/Monte Carlo on plausible ordinal distributions, not arbitrary counts.

## Candidate web form
| Order | Module | Variables / examples | Purpose |
| --- | --- | --- | --- |
| 0 | Information, consent, age and current-relationship eligibility | consent_version, 18+, relationship status, explicit opt-out | Ethics/governance |
| 1 | Context and exposure | Relationship duration band, cohabitation (if justified), opportunity to act in prior 4 weeks, optional “nie dotyczy” | Separate no opportunity from no action |
| 2 | Candidate relational action items | Frequency of **attempts**, not success. Sample unvalidated stem: “W ostatnich 4 tygodniach zaproponowałam/zaproponowałem zmianę sposobu planowania wspólnego czasu.” | Content domain; exclude coercive-control and communication overlap by design |
| 3 | Proposed construct facets | Negotiating contact, autonomy/time, disagreement, initiation; ask whether partner consent was present only where scientifically necessary | Factor/item discovery, not predetermined additive sum |
| 4 | Established comparator batteries | Authorized Polish ECR-R anxiety/avoidance and selected measures of assertiveness, agency, intolerance of uncertainty / dominance | Discriminant and incremental validity; verify licenses, translation and scoring |
| 5 | Independent brief criterion | Neutral hypothetical vignette: participant selects whether to discuss, negotiate, defer or impose unilateral change, plus confidence | Hypothetical intended behavior only; blinded coding rubric |
| 6 | Burden/quality and closing | Meaning clarity, response effort, sensitive-item skip, optional separate retest invitation | Feasibility, missingness, respect for privacy |

Example **candidate** response anchors: 0 never, 1 rarely, 2 sometimes, 3 often, 4 very often, plus “no opportunity / not applicable / prefer not to answer”. These are **not frozen**: a cognitive study must decide timeframe and response model. The item’s action, intention, consent and outcome must not be conflated. Maintain separate information on opportunities.

## Dataset and analysis
`participant_id`, `phase`, `instrument_version`, `item_version`, `item_id`, `response`, `not_applicable_reason`, `consent_version`, `duration_seconds`, `vignette_id`, `retest_wave`, `randomization_version`; personally identifying invite/contact data stored elsewhere. Version item wording and missing codes; never commit identifiable relationship narratives.

EFA: polychoric/ordinal-appropriate estimator and rotation prespecified; competing factor models documented. CFA: independent participant sample; ordinal estimator and preregistered fit/diagnostics. Reliability: coefficients with uncertainty, retest at prespecified interval. Validity: factor correlation vs comparators, incremental prediction for held-out vignettes; assess invariance only for adequately powered justified groups. Report failed differentiation and all discarded items.

## TODO / gates
- [ ] **P0** Expert review and cognitive interview plan; document item-to-construct rationale and comprehension.
- [ ] **P0** Verify exact Polish comparator translations, permissions, licensed items, scoring and minimum burden.
- [ ] **P0** Resolve ethics, privacy, withdrawal, recruitment and respondent eligibility; simulate numerical sample-size/precision.
- [ ] **P1** Freeze development form and independent confirmatory form as separate versions.
- [ ] **P1** Deploy/test skip logic and export on synthetic fixtures; then recruit only after authorization.
- [ ] **P2** Run retest and prospective criterion work after the main validation gate.

A successful online factor analysis **does not establish** clinical/diagnostic utility.
