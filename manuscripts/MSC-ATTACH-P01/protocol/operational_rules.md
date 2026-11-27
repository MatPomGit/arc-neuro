# H1 operational sampling and data-validity rules

Status: locked before human outcome data unless explicitly marked as pending Monte Carlo validation.

## 1. Pair-specific waking window

Each enrolled couple selects one shared 14-hour local-time sampling window during onboarding.

Requirements:

- both partners expect to be awake for the full window on a typical study day;
- the same window is used on all 14 study days;
- the window is fixed before day 1 and is not adapted in response to study data;
- if the couple cannot identify a shared 14-hour waking window, the pair is not eligible for this synchronized-prompt protocol.

All timestamps are stored in UTC together with the local UTC offset. Scheduling follows local civil time if a daylight-saving transition occurs.

## 2. Six daily prompt strata

The 14-hour window is divided into six equal strata of 140 minutes.

For each study day:

- exactly one prompt is scheduled uniformly at random within each stratum;
- the six scheduled times are shared by both partners;
- the complete 14-day schedule is generated before day 1;
- the daily schedule is resampled until every pair of consecutive scheduled prompts is at least 90 minutes apart.

The scheduling seed is stored with the study metadata so the planned schedule can be reconstructed without using outcome data.

## 3. Response window

A prompt becomes available at its scheduled time.

- response window: 30 minutes;
- one reminder: 15 minutes after the scheduled time if no response has been submitted;
- the prompt expires after 30 minutes;
- expired prompts cannot be completed retrospectively;
- partial responses are retained as partial records but cannot form a confirmatory lag if a required H1 variable is missing.

## 4. Same-day lag definition

A confirmatory t -> t+1 lag requires:

- consecutive prompt numbers within the same study day;
- both prompts submitted within their 30-minute response windows;
- all variables required by the selected M0-M4 model available;
- signed action outcome at t+1 available;
- actual response-to-response elapsed time between 60 and 240 minutes inclusive;
- no technical-invalid-record flag on either prompt.

A missed or expired prompt breaks the lag. Confirmatory analysis never bridges across a missed prompt and never uses an overnight transition.

The first within-day transition, prompt 1 -> 2, is also excluded from confirmatory autoregressive analysis. The source action at prompt 1 refers to the overnight/first-of-day interval and is therefore not comparable with actions reported after a standardized same-day ESM interval. Eligible source prompts are 2-5, yielding transitions 2->3, 3->4, 4->5, and 5->6.

The actual response-to-response interval is used in the confirmatory context model. Scheduled spacing is retained for audit purposes.

## 5. Participant-level data sufficiency

Current locked minimum for confirmatory inclusion:

- at least 30 valid same-day lag pairs across the 14-day study;
- at least 3 valid lag pairs in the days 12-14 temporal holdout.

The exact-model Monte Carlo may increase these thresholds before recruitment if the operating-characteristic study shows that the current thresholds are inadequate. They cannot be relaxed after outcome data are observed.

If one partner fails the participant-level threshold, the other partner may remain in confirmatory analysis if that partner meets the criteria. The couple remains represented as one GEE cluster.

All enrolled participants remain in recruitment, compliance, and missingness reports regardless of confirmatory eligibility.

## 6. Technical-invalid records

A prompt record is technically invalid for confirmatory analysis if any of the following applies:

- administrative/test record rather than participant data;
- duplicate study-day-prompt record that cannot be resolved from immutable server timestamps;
- participant or couple identifier is absent or inconsistent with enrollment records;
- study day is outside 1-14 or prompt index is outside 1-6;
- response timestamp precedes the scheduled opening time;
- response timestamp is more than 30 minutes after scheduled opening;
- required H1 response is outside its defined instrument range because of a software/data-integrity error;
- timestamp metadata required to determine lag timing are absent or internally inconsistent.

Out-of-range values are never Winsorized into the valid scale. The source record is retained in the audit trail and excluded only under the technical rule above.

## 7. Non-exclusion rules

The following are not reasons for confirmatory exclusion:

- extreme but valid closeness, discrepancy, affect, or action values;
- extreme L/U baseline scores;
- an inconvenient coefficient or model ranking;
- short response time by itself;
- high simultaneous approach and distance;
- disagreement between partners;
- low relationship quality if eligibility criteria were met.

## 8. Missing prompts

No missed prompt is reconstructed, backfilled, or imputed as if a momentary response had occurred.

Primary H1 analysis uses valid observed lag pairs.

The mandatory sensitivity is a history-based stabilized IPW-GEE. The response-probability model is trained on days 1-11 only.

Numerator response model:

- study day;
- prompt stratum.

Denominator response model:

- study day and prompt stratum;
- prior response rate;
- immediately previous scheduled-prompt response status;
- explicit no-observed-history indicator;
- last observed negative affect;
- last observed absolute discrepancy;
- last observed absolute signed action.

The current prompt's psychological state or action is never used to predict whether that same prompt is observed.

Candidate weight-truncation rules:

- none;
- 1st/99th percentile;
- 2.5th/97.5th percentile.

Training lags determine the numeric truncation bounds. Those bounds are applied unchanged to the temporal holdout.

FINAL BEFORE DATA:
select one truncation rule from the prespecified candidates using targeted Monte Carlo bias, coverage, positivity, effective-sample-size, and architectural-decision diagnostics.

The IPW sensitivity is interpreted under a history-based MAR assumption. The contemporaneous state/action-dependent missingness condition in the exact simulator is an MNAR-like stress test and is not assumed to be fully corrected by IPW.

## 9. No outcome-adaptive changes

After recruitment begins, none of the following may be changed because of observed H1 effects or model ranking:

- prompt strata;
- reminder/expiry timing;
- lag timing thresholds;
- participant data-sufficiency thresholds;
- technical-invalid-record rules;
- missing-data model;
- M0-M4 definitions.
