# H1 ESM cognitive interview plan

Status: protocol for instrument refinement before confirmatory preregistration.

## 1. Objective

The purpose is to identify systematic interpretation problems before the ESM wording is frozen. This stage is not intended to estimate psychometric reliability from a small convenience sample.

Highest-risk distinctions:
- perceived closeness versus desired closeness;
- approach versus distancing as potentially co-occurring actions;
- overt distancing versus internal suppression/disengagement;
- current-state questions versus interval questions;
- meaningful interaction versus trivial logistical contact;
- perceived partner responsiveness versus agreement, obedience, or general relationship satisfaction.

## 2. Participants

Use two iterative rounds.

Round 1: 5-8 adults currently in a romantic relationship.

Round 2: 5-8 new adults after wording revisions.

Prefer participants broadly similar to the planned H1 sample:
- age 18+;
- current romantic relationship for at least 6 months;
- cohabiting when feasible;
- variation in relationship duration, age, gender, and communication patterns.

The sample is qualitative. Recruitment is not stopped because an item reaches a desired numerical distribution.

## 3. Procedure

Approximate session length: 30-45 minutes.

Sequence:
1. explain that the questionnaire, not the participant, is being tested;
2. show a realistic mock ESM prompt on a phone-sized interface;
3. obtain one uninterrupted completion and record completion time;
4. repeat selected items using think-aloud;
5. use retrospective probes;
6. present short hypothetical relational scenarios to test discriminant interpretation;
7. ask for confusing, overly broad, judgmental, or unnatural wording;
8. document every wording change and its rationale.

Do not coach the intended interpretation before the participant paraphrases the item.

## 4. Mandatory probes

### A1 versus A2

Ask participants to explain both questions in their own words and whether A2 concerns the current desired state or an ideal relationship in general.

Contrast scenarios:
- low current closeness, high desire for closeness: expected A1 low, A2 high;
- high current closeness, desire for more space: expected A1 high, A2 lower.

Failure signal: A2 is interpreted as a global relationship ideal, moral expectation, or prediction of future closeness.

### C1 and C2 may co-occur

Use a scenario in which the participant seeks reassurance and later withdraws.

Failure signal: the participant assumes approach and distancing are opposite ends of one bipolar item.

### C2 versus C3

Use one scenario with normal outward contact but strong internal suppression, and another with overt distancing without suppression.

Failure signal: both items are used interchangeably for any avoidance.

### Time reference

Ask participants to explain:
- “od przebudzenia dzisiaj” at the first prompt;
- “od poprzedniego pomiaru” at prompts 2-6.

Failure signal: answers routinely refer to the whole day, the relationship in general, or an earlier episode outside the intended interval.

### Meaningful interaction

Probe examples such as:
- a short logistical message;
- a 10-minute conversation;
- sitting together without interaction;
- messaging about emotions;
- a shared task.

Failure signal: substantial disagreement caused by the phrase “istotny kontakt”.

### Partner responsiveness

Probe the meaning of “zrozumienie, akceptacja i gotowość do reagowania na Twoje potrzeby”.

Failure signal: the item is interpreted only as agreement, obedience, relationship satisfaction, or partner mood.

## 5. Decision rules for wording revision

The following are operational instrument-development rules, not psychometric inferential criteria.

For each item and contrast, record:
- the exact number of participants who paraphrase the intended construct without coaching;
- all recurrent alternative interpretations;
- whether the intended contrast is correctly distinguished;
- whether branching logic is understood without explanation;
- whether wording appears judgmental or suggests a socially desirable response.

A practical retention target is at least 80% correct interpretation in each round, but the raw numerator and denominator must always be reported because n is small. Any recurrent misunderstanding in more than one participant should be reviewed qualitatively even if the nominal 80% target is met.

Any substantive failure triggers wording revision and retest in the next round.

## 6. Translation/adaptation control

Because these are study-specific momentary items rather than a direct translation of one validated questionnaire:
- preserve construct meaning rather than literal English syntax;
- maintain a versioned mapping between English concept, Polish wording, and variable ID;
- obtain independent bilingual review of the final Polish candidate;
- back-translate the two closeness items and three regulation items before v1.0 freeze;
- resolve semantic disagreements before the micro-pilot.

Do not silently modify wording in the study app after v1.0 freeze.

## 7. Completion-time micro-pilot

After cognitive round 2, run a short usability micro-pilot before the 14-day confirmatory study.

Recommended engineering pilot:
- 5-8 couples;
- 2-3 days;
- actual notification, expiry, and branching implementation.

Burden targets:
- median completed prompt <= 90 s;
- 90th percentile completed prompt <= 120 s;
- no fixed item repeatedly accounts for delays or confusion;
- conditional items appear only when triggered.

Also report:
- prompt response rate;
- expiry rate;
- response latency;
- frequency of conditional branches;
- item-level missingness;
- app/notification failures.

These are feasibility thresholds, not estimates of scientific effect sizes.

## 8. Version progression

- `v0.2-pl-cognitive`: current candidate;
- `v0.3-pl-cognitive`: after round 1 revisions;
- `v0.4-pl-cognitive`: after round 2 if further wording changes are necessary;
- `v0.9-pl-pilot`: candidate for the usability micro-pilot;
- `v1.0-confirmatory`: frozen wording, order, anchors, branch conditions, and variable IDs.

Any post-freeze correction is documented as a protocol deviation with old wording, new wording, date, reason, and affected records.
