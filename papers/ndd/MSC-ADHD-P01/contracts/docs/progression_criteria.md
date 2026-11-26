# ARC-ADHD progression criteria

Status: provisional design specification. These thresholds must be ratified by the clinical, statistical and participant-facing research team before the relevant phase starts. They must not be changed after inspecting phase outcomes simply to permit progression.

The purpose of progression criteria is feasibility decision-making, not preliminary efficacy testing. This follows the logic of randomized pilot and feasibility guidance, which asks whether a definitive trial can and should be done, and if so, how. A traffic-light approach is used because remediable problems should be distinguished from intractable ones.

Methodological basis: Eldridge et al. (2016), Avery et al. (2017), Mellor et al. (2021).

## Decision rule

- **Green, go:** the domain is compatible with progression without major redesign.
- **Amber, amend:** progression may be possible after a documented corrective action and review.
- **Red, stop/reconsider:** the current design is not suitable for progression without major redesign or new feasibility work.
- **Safety override:** any intervention-related serious adverse event or recurrent unmitigated safety pattern triggers independent review regardless of other criteria.

No single green criterion compensates for a red safety criterion.

## Phase 0: co-design and construct validation

Phase 0 is iterative and does not use clinical efficacy outcomes.

| Domain | Green | Amber | Red |
| --- | --- | --- | --- |
| Understanding of the challenge-regulation-recovery sequence | At least 85% of participants can complete the sequence after onboarding with no more than one neutral prompt | 70–84% or recurrent confusion limited to a remediable interface/instruction element | Below 70% or confusion indicates that the construct is not represented understandably |
| Strategy selection | At least 80% can select and execute at least one strategy without researcher rescue | 60–79%, or one strategy family is consistently misunderstood | Below 60% or strategy execution creates recurrent distress/frustration |
| Recovery-event observability | At least 90% of eligible challenge events yield a valid recovery time or explicit right-censoring status | 75–89% | Below 75% |
| Recovery censoring | No more than 20% of eligible events are right-censored under the candidate window | 21–35% | Above 35%, suggesting that the event window or recovery definition is not operationally usable |
| Telemetry completeness | At least 95% of required event fields are captured | 85–94% | Below 85% |
| BYOD qualification | Compatibility policy and self-test procedure work across the intended Android test set; the preregistered device nonqualification threshold is met | Qualification/fallback burden exceeds target but appears remediable | Compatibility policy excludes an unacceptable share of intended users or produces unresolved measurement failures |
| Critical usability/safety failures | No new critical failure in two consecutive iterative rounds | A remediable recurring failure remains | An unmitigated hazard or construct-level usability failure remains |

The percentages are project design targets, not universal published cut-offs. Their purpose is to make the transition decision auditable. The numerical BYOD nonqualification threshold should be frozen before participant recruitment after cross-device engineering validation; it must not be selected after observing participant outcomes.

## Phase 1: feasibility study

The feasibility study should be judged against operational criteria defined before recruitment.

| Domain | Green | Amber | Red |
| --- | --- | --- | --- |
| Recruitment rate | At least 80% of the planned participants-per-site-per-month recruitment rate | 60–79% | Below 60% |
| Retention to post-intervention assessment | At least 80% | 65–79% | Below 65% |
| Dose completion | At least 75% of participants complete at least 75% of prescribed sessions | 55–74% meet this dose | Below 55% |
| Session completion | At least 90% of started sessions finish without safety-related termination | 80–89% | Below 80% |
| Telemetry completeness | At least 95% of sessions contain all fields required for the primary mechanistic analysis | 85–94% | Below 85% |
| BYOD technical feasibility | Prespecified private-phone qualification target met, fallbacks auditable, and device/profile changes can be handled without invalidating the planned analysis | Target missed for a remediable device/OS subgroup | Persistent compatibility or timing heterogeneity makes the planned mechanistic analysis uninterpretable |
| Valid recovery events | At least 85% of eligible events yield a valid recovery or censoring record | 70–84% | Below 70% |
| Recovery censoring | No more than 25% of eligible events are censored | 26–40% | Above 40% |
| Sensory-overload termination | No more than 10% of sessions terminate early because of overload | More than 10% to 20% | Above 20% |
| Acceptability | At least 80% of participants/caregivers indicate that the intervention is acceptable enough to continue under the planned dose | 65–79% | Below 65% |
| Serious intervention-related adverse events | 0 | Not applicable | Any event triggers stop/review |

## Phase 2: pilot randomized trial

The pilot is not progressed because of a promising p value on a clinical endpoint. Progression depends on whether the definitive trial design is viable.

Required domains include:

1. recruitment and retention under randomization;
2. active-control acceptability and dose balance;
3. outcome completion;
4. stable variance and correlation estimates for sample-size planning;
5. acceptable missingness pattern;
6. successful masking of outcome assessors where applicable;
7. adequate separation between the core intervention and active control;
8. no emergent safety or data-governance barrier;
9. feasibility of the planned follow-up interval.

The decision should be recorded as **go**, **amend**, or **stop/reconsider**, with rationale for every amber or red domain.

## Governance of criteria

The final thresholds should be reviewed before recruitment by:

- the principal investigator;
- a statistician or trial methodologist;
- a clinician/developmental specialist;
- the data-protection/safety lead where relevant;
- participant or caregiver representatives for acceptability-related criteria.

Any pre-study revision should be versioned in the repository and protocol. Post-outcome changes must be reported transparently as deviations rather than silently replacing the original criteria.
