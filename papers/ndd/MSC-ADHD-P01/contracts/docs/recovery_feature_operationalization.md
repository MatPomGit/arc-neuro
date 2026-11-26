# ARC-ADHD recovery feature operationalization

Status: pre-Phase 0 candidate-space specification.

This document defines the deliberately small feature space that may enter the Phase 0 calibration of \(q_e(t)\) for the first Signal Gate implementation. It prevents post hoc feature shopping by fixing the candidate families, transformations, admissible combinations, and rejection rules before participant data are inspected.

The machine-readable source is:

\`config/recovery_feature_candidates.phase0.json\`

The executable reference implementation is:

\`scripts/evaluate_recovery_feature_candidates.py\`

## 1. Scope

The first feature-space evaluation is restricted to the Signal Gate **rule-switch** challenge.

Other challenge families may still be prototyped, but they do not automatically inherit this recovery definition. A different challenge type must demonstrate that the same observable meaning and measurement assumptions remain valid before it is pooled with rule-switch events.

The candidate space contains:

- one mandatory goal-directed behavior feature, \(B\);
- optional correct-response slowing, \(S\);
- optional correct-response variability increase, \(V\).

There is no timing-only model.

## 2. Why the earlier feature list is reduced

The earlier candidate list contained accuracy, rule adherence, commission errors, omission errors, response latency, and response-time stability. Several of these are deterministic or near-deterministic recodings of the same trial outcome.

For the two-rule Signal Gate reversal:

- an omission on a current GO trial is failure to execute the active rule;
- a commission response on a current NO-GO trial is also failure to execute the active rule;
- ordinary accuracy and rule-error rate summarize the same response mapping from opposite directions.

Entering all of them separately would overweight behavioral errors merely because several telemetry fields encode them.

The operationalized space therefore collapses GO and NO-GO success into one balanced behavioral feature and retains timing only as a separate family.

## 3. Eligibility reference, recovery reference and rolling window

Three windows have distinct roles and must not be conflated.

### Immediate eligibility reference

Immediately before a candidate challenge, the current preswitch rule must have:

- 12 valid trials;
- at least 4 GO trials;
- at least 4 NO-GO trials.

This window is used to determine whether the participant is in a sufficiently observed current task state to schedule a challenge. It is **not** the normalization reference for (q_e(t)), because after A↔B switching it belongs to a different response mapping.

### Target-rule recovery reference

During `RULE_CALIBRATION`, a stable reference is collected separately for each rule mapping. For target post-switch rule (r^ast), the recovery reference contains:

- 12 valid trials under (r^ast);
- at least 4 GO trials;
- at least 4 NO-GO trials;
- the GO-stimulus identity for (r^ast);
- at least 4 correct-GO RT observations when timing-enriched models are eligible.

The target-rule recovery reference is the common normalization source for (B), (S), and (V). In the first Phase 0 implementation it is immutable within the session. This prevents later adaptive performance from silently redefining the recovery criterion.

### Rolling recovery window

The post-regulation recovery window uses:

- 8 valid trials;
- update stride of 1 valid trial;
- at least 2 GO trials;
- at least 2 NO-GO trials;
- at least 3 correct GO RTs for (S);
- at least 4 correct GO RTs for (V).

These counts are project-specific Phase 0 engineering hypotheses, not universal psychometric cut-offs. Phase 0 may falsify their feasibility, but they must not be changed opportunistically after external outcomes are inspected.

Stimulus generation should preserve the configured long-run target probability while avoiding local windows that systematically fail the required GO/NO-GO composition.

## 4. Feature B: balanced rule success

Let \(h\) be correct responses on GO trials and \(n_G\) the number of GO trials. Let \(c\) be correct withholds on NO-GO trials and \(n_N\) the number of NO-GO trials.

For each conditional success probability use the Jeffreys-smoothed estimate

\[
\tilde p =
\frac{s + 1/2}{n + 1}.
\]

The balanced rule-success feature is

\[
B =
\frac{1}{2}
\left(
\tilde p_{\mathrm{GO-hit}}
+
\tilde p_{\mathrm{NO-GO-CR}}
\right).
\]

GO and NO-GO success receive equal weight regardless of the configured target frequency.

For event (e) targeting post-switch rule (r^ast), define (B_{mathrm{ref},r^ast}) from the stable `RULE_CALIBRATION` reference for that same rule and GO-stimulus mapping. The immediate preswitch current-rule eligibility window does not enter this normalization.

For a Beta\((1/2,1/2)\) posterior, the conditional posterior variance is

\[
v(p)
=
\frac{ab}{(a+b)^2(a+b+1)},
\]

where \(a=s+1/2\) and \(b=n-s+1/2\).

Because the reference and rolling windows contain different finite samples, the behavioral comparison scale also includes the expected sampling variance of the current window under the reference success probabilities:

\[
s_{B,r^\ast}(t)
=
\frac{1}{2}
\sqrt{
v(\tilde p_{G,\mathrm{ref},r^\ast})
+
v(\tilde p_{N,\mathrm{ref},r^\ast})
+
\frac{
\tilde p_{G,\mathrm{ref},r^\ast}
(1-\tilde p_{G,\mathrm{ref},r^\ast})
}{n_G(t)}
+
\frac{
\tilde p_{N,\mathrm{ref},r^\ast}
(1-\tilde p_{N,\mathrm{ref},r^\ast})
}{n_N(t)}
}.
\]

The observed postchallenge success probabilities do not enter this denominator. Consequently, poor performance cannot make its own deficit appear smaller by increasing the estimated variance.

The one-sided behavioral deficit is

\[
d_B(t)
=
\max
\left[
0,
\frac{B_{\mathrm{ref},r^\ast} - B_t}
{\max(s_{B,r^\ast}(t),\epsilon_B)}
\right].
\]

Thus improved or reference-level behavioral performance produces no deficit. It cannot generate a positive credit that compensates for another impaired feature.

### Falsification conditions for B

The operationalization is not ready for Phase 1 if, under the frozen Phase 0 task:

- the required GO/NO-GO window composition is frequently unavailable;
- the feature cannot be reconstructed deterministically from telemetry;
- leave-one-trial perturbation changes the terminal recovery classification too often under the prespecified robustness gate;
- behavior-only model \(B\) fails the prespecified computability gate.

Because \(B\) is construct-essential, failure of \(B\) means the recovery measure requires redesign rather than replacement by a timing-only metric.


[Continue to part 2](recovery_feature_operationalization-part-2.md)
