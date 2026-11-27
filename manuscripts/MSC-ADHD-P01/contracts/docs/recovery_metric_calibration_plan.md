# ARC-ADHD recovery-metric calibration plan

Status: pre-Phase 0 measurement plan.

This document defines how the prespecified candidate feature models, recovery threshold \(\delta\), stability-window count \(w\), and censoring limit \(c_e\) are stabilized before inferential use.

The exact primitive feature definitions are maintained in:

- \`docs/recovery_feature_operationalization.md\`;
- \`config/recovery_feature_candidates.phase0.json\`.

The core rule is that calibration is based on measurement behavior, task structure, device validity, safety, and interpretability. It must **not** optimize association with a later clinical endpoint.

## 1. Measurement objective

For a controlled rule-switch challenge event \(e\), the recovery metric estimates how long it takes the participant to return to a stable, goal-directed performance state relative to that participant's own pre-challenge reference.

The metric should be:

- computable from preregistered Signal Gate behavior;
- robust to a single lucky or unlucky trial;
- explicit about non-recovery;
- separable from technical missingness and scientific invalidity;
- reproducible from stored telemetry;
- minimally dependent on mobile timing when a behavior-only model is sufficient.

## 2. Fixed pre-Phase 0 feature space

The candidate primitive features are:

- \(B\): balanced rule success;
- \(S\): correct-GO slowing;
- \(V\): correct-GO variability increase.

The only allowed candidate models are:

1. \(B\);
2. \(B+S\);
3. \(B+V\);
4. \(B+S+V\).

The behavioral feature is mandatory in every model.

This candidate space is restricted to the first Signal Gate rule-switch challenge. Other challenge families require a separate invariance argument before sharing the same primary recovery definition.

## 3. Deficit coding

Each primitive feature is transformed into a non-negative deficit

\[
d_j(t)\ge 0.
\]

Component scores are

\[
z_j(t)=-d_j(t),
\]

and therefore cannot exceed zero.

The composite score is

\[
q_e(t)=\sum_j w_j z_j(t),
\qquad
\sum_j w_j=1,
\]

so

\[
q_e(t)\le 0.
\]

Above-reference performance in one component is clipped to zero deficit. It cannot compensate for a remaining deficit in another component.

This non-compensatory direction rule is part of the measurement definition and must not be changed after outcome inspection.

## 4. Behavioral feature

\(B\) uses equal conditional weighting of GO hits and NO-GO correct rejections, with Jeffreys Beta\((1/2,1/2)\) smoothing.

This replaces the earlier idea of entering accuracy, commission errors, omission errors and rule-error rate as separate components. Those variables remain available as descriptive telemetry but are not independent candidate dimensions of \(q_e(t)\).

## 5. Timing features

\(S\) and \(V\) use only correct GO responses.

A rule switch changes the GO mapping, so timing does not use the immediate pre-switch trials as its reference. Before eligible timing-based recovery events, both rule mappings must have a stable calibration exposure. For each event, the timing reference must match the target post-switch rule and GO-stimulus identity.

Timing features are eligible only on a timing-qualified device/profile. Their reference scale is bounded below by the qualified-device timing floor so that a near-zero within-child MAD does not create an arbitrarily large standardized deficit.

Faster correct responses do not count as a deficit. Increased variability and slowing are one-sided deficits.

If timing qualification is unavailable, \(B\) remains computable while timing-enriched candidates are marked unavailable rather than silently substituting another timing rule.

## 6. Reference and rolling windows

The current candidate engineering values are:

- 12 valid pre-challenge reference trials;
- 8 valid trials in the rolling recovery window;
- update stride of one valid trial.

Minimum class/sample composition is defined in the machine-readable candidate-space file.

These values are explicit Phase 0 hypotheses. They can be rejected by insufficient computability or robustness, but they must not be changed opportunistically after examining favorable external outcomes.

## 7. Phase 0 feature-model gates

Candidate feature models are evaluated using measurement properties only.

Current hard project gates are:

- at least 90% computability among otherwise eligible rule-switch events;
- no more than 20% of applicable reference windows dominated by a numerical/device scale floor;
- no more than 20% of terminal recovery classifications changed under the prespecified leave-one-trial perturbation analysis;
- for timing-enriched models, at least 90% timing-qualified event coverage.

Right-censoring fraction, median recovery latency, and mean \(q\) are reported as diagnostics but are not optimization targets for feature-set selection.

## 8. Parsimony rule

The post-Phase 0 model-selection rule is lexicographic.

1. Reject any model that fails a hard gate.
2. If \(B\) passes all hard gates, retain \(B\) unless a prespecified measurement failure specifically requires an enriched model and the enriched model resolves that failure.
3. If \(B\) fails and multiple enriched models pass, prefer the lowest complexity rank.
4. For equal complexity, prefer lower feature missingness and lower leave-one-trial instability.
5. Report all four candidates in the freeze record.

This prevents timing features from being retained merely because they make the score look more responsive.

## 9. Forbidden model-selection signals

Do not choose a feature model because it yields the strongest association with:

- EDI;
- caregiver symptom ratings;
- teacher ratings;
- functional outcomes;
- treatment-group differences;
- any later clinical endpoint.

Those relationships are tests of construct relevance after the mechanistic measure is frozen.

## 10. Recovery threshold and time origin

For the selected candidate model, recovery occurs when

\[
q_e(t)\ge -\delta
\]

for \(w\) consecutive score updates. A single transient crossing is insufficient.

The primary recovery clock begins on entry into `RECOVERY_MONITORING`, after the configured pause/orient/strategy sequence. Let \(T_{\mathrm{pre}}\) denote challenge-to-monitoring time and \(T_{\mathrm{rec}}\) denote monitoring-to-threshold-entry time. The complete challenge-to-return process is reported separately as

\[
T_{\mathrm{total}}=T_{\mathrm{pre}}+T_{\mathrm{rec}}.
\]

If a complete qualifying run is not confirmed before \(c_e\) milliseconds after recovery-monitoring onset, an otherwise valid \(T_{\mathrm{rec}}\) observation is right-censored.

## 11. Separate calibration dimensions

Feature-model selection is separated from the small threshold grid for:

- \(\delta\);
- stability-window count \(w\);
- censoring limit \(c_e\).

The Phase 0 freeze procedure should avoid unrestricted joint optimization across feature sets and thresholds. Report the prespecified grid and all tested definitions.

## 12. Scientific invalidity versus censoring

An event is right-censored only when:

- the recovery process remains observable;
- the recovery measurement context remains unchanged;
- the criterion is not met before \(c_e\).

A context change, corrupted event timing, lost task state, or unavailable required feature is not ordinary right-censoring.

The recovery-event schema explicitly separates:

- observed recovery;
- right-censoring;
- scientifically invalid recovery data;
- telemetry completeness.

## 13. Measurement-context lock

During an open recovery event, the active rule, cognitive difficulty, sensory configuration, response-window timing, stimulus distribution and event-level cue assignment are frozen.

Safety and explicit child requests always take priority. If they require a score-relevant context change, the event becomes scientifically invalid rather than artificially appearing to recover under easier conditions.

## 14. Phase 0 freeze decision

Before Phase 1, freeze:

- selected model ID;
- primitive feature definitions;
- reference and rolling-window definitions;
- feature weights;
- device timing-floor rule;
- \(\delta\);
- stability-window count \(w\);
- censor limit \(c_e\);
- missing-feature policy;
- measurement-context lock version;
- censoring and invalidity reasons;
- implementation/repository hash.

The decision record must show all four candidate models, including rejected ones.

## 15. Technical validation before human data

Synthetic tests must distinguish at least:

- reference-like performance;
- isolated behavioral deterioration;
- isolated correct-response slowing;
- isolated reaction-time variability increase;
- timing unavailability;
- immediate stable recovery;
- delayed recovery;
- no recovery before censor limit;
- scientific invalidation caused by measurement-context change.

Synthetic tests validate implementation behavior only. They do not establish psychological validity or clinical efficacy.
