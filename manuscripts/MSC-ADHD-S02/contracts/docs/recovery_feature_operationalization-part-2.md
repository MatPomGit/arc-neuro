## 5. Feature S: correct-GO slowing

Only correct GO responses enter the timing features.

A rule switch reverses which stimulus is GO. Therefore the immediate pre-switch RT distribution is **not** a valid timing baseline for the post-switch rule. Before eligible rule-switch challenges, the child must have a stable calibration exposure to both rules. For a challenge whose target post-switch rule is \(r^\ast\), timing features use the prior stable correct-GO distribution collected under the same rule and the same GO stimulus identity.

Let

\[
m_{\mathrm{ref},r^\ast}
=
\operatorname{median}(RT_{\mathrm{ref},r^\ast})
\]

and define the mapping-matched timing reference scale as

\[
s_{\mathrm{RT}}
=
\max
\left[
1.4826\operatorname{MAD}(RT_{\mathrm{ref},r^\ast}),
s_{\mathrm{device}}
\right],
\]

where \(s_{\mathrm{device}}\) is the timing floor from the qualified BYOD device profile/benchmark.

The slowing deficit is

\[
d_S(t)
=
\max
\left[
0,
\frac{
\operatorname{median}(RT_t)-m_{\mathrm{ref},r^\ast}
}{
s_{\mathrm{RT}}
}
\right].
\]

Faster correct responses are not penalized. If fast responding becomes impulsive and produces errors, that impairment enters through \(d_B\).

### Falsification conditions for S

Reject \(S\) from the frozen Phase 1 model if timing qualification or sufficient correct-GO observations are unavailable too often, or if its scale is dominated by the device timing floor beyond the prespecified Phase 0 gate.

## 6. Feature V: correct-GO variability increase

The robust reference timing scale is the same \(s_{\mathrm{RT}}\).

For the rolling window define

\[
s_t
=
\max
\left[
1.4826\operatorname{MAD}(RT_t),
s_{\mathrm{device}}
\right].
\]

The variability deficit is

\[
d_V(t)
=
\max
\left[
0,
\frac{s_t}{s_{\mathrm{RT}}}-1
\right].
\]

Reduced variability is not treated as a deficit and cannot offset impairment elsewhere.

### Falsification conditions for V

Reject \(V\) if the required number of correct GO trials makes it insufficiently computable, if its estimate is excessively sensitive to one trial, or if device timing noise dominates the within-child signal under the prespecified Phase 0 gates.

## 7. Four candidate models

Component scores are defined as

\[
z_j(t)=-d_j(t),
\qquad d_j(t)\ge 0.
\]

Therefore every component score is non-positive and

\[
q_e(t)
=
\sum_j w_j z_j(t)
\le 0.
\]

The four allowed candidates are:

| Model | Components | Weights |
| --- | --- | --- |
| \(B\) | balanced rule success | \(1.00\) |
| \(B+S\) | behavior + slowing | \(0.50, 0.50\) |
| \(B+V\) | behavior + variability increase | \(0.50, 0.50\) |
| \(B+S+V\) | behavior + both timing components | \(0.50, 0.25, 0.25\) |

When timing is included, the behavioral family always retains 50% of total weight. Adding a second timing variable therefore does not silently double the influence of timing.

No other feature subset or weight vector is eligible for primary Phase 0 model selection unless the candidate-space specification is amended before outcome inspection and the amendment is documented.

## 8. Why positive compensation is prohibited

The earlier generic weighted-z formulation allowed, in principle, a strongly above-reference value in one feature to cancel a deficit in another.

For the recovery construct this is undesirable. A child responding unusually quickly should not be classified as recovered if rule execution remains substantially impaired.

The operationalized model therefore clips feature-specific improvement at zero deficit. Recovery means that the included deficits have returned sufficiently close to zero; it does not mean that one domain has become exceptional enough to compensate for another.

## 9. Phase 0 hard gates

The current project thresholds are:

- at least 90% of otherwise eligible rule-switch events computable for the candidate;
- no more than 20% of applicable reference windows dominated by a numerical/device scale floor;
- no more than 20% of terminal recovery classifications changed by the prespecified leave-one-trial perturbation analysis;
- for timing-enriched models, at least 90% of otherwise eligible events must come from timing-qualified execution contexts.

These are project progression thresholds, not published universal norms. They must be locked before inspecting Phase 0 recovery results.

Censoring fraction, mean \(q\), and median \(T_{\mathrm{rec}}\) are reported as diagnostics. They are not optimization targets for selecting the feature set, because a feature definition could appear attractive merely by making recovery artificially easy.

## 10. Model-selection rule

Selection after Phase 0 is lexicographic.

1. Reject every model that fails any hard gate.
2. If \(B\) passes all gates, retain \(B\) unless a prespecified measurement failure specifically requires an enriched model and that enriched model resolves it.
3. If \(B\) fails and more than one enriched model passes, prefer the lowest complexity rank.
4. For equal complexity, prefer lower feature missingness and lower leave-one-trial instability.
5. Never use EDI, caregiver report, teacher report, functional outcome, treatment-group difference, or correlation with a later clinical outcome to choose among the four models.
6. Report the results for all four candidates, including rejected models, in the Phase 0 freeze record.

This rule intentionally favors the smallest construct-sufficient model.

## 11. Time origin, stability window and censoring

Feature-set selection and recovery-threshold calibration are related but separate.

Raw \(q\), \(T_{\mathrm{rec}}\), and censoring rates are not compared across feature models as if their scales were identical. The small \(\delta\)/stability grid tests whether each feature definition remains qualitatively stable across a prespecified local threshold neighborhood.

Recovery monitoring begins only after the pause/orient/strategy sequence is complete. Let:

- \(t_e\) be challenge onset;
- \(t_m^{(e)}\) be entry into \`RECOVERY_MONITORING\`;
- \(u_{e,k}\) be the timestamp of score update \(k\).

Define \(k_e^\ast\) as the first update beginning \(w\) consecutive updates satisfying

\[
q_{e,r}\ge-\delta,
\qquad
r=k,\ldots,k+w-1.
\]

The complete run must be confirmed before the censor boundary.

The primary performance-recovery latency is

\[
T_{\mathrm{rec}}^{(e)}
=
u_{e,k_e^\ast}-t_m^{(e)}.
\]

Also retain

\[
T_{\mathrm{pre}}^{(e)}
=
t_m^{(e)}-t_e,
\]

and

\[
T_{\mathrm{total}}^{(e)}
=
u_{e,k_e^\ast}-t_e
=
T_{\mathrm{pre}}^{(e)}+T_{\mathrm{rec}}^{(e)}.
\]

This decomposition is mandatory. A longer regulation strategy may increase \(T_{\mathrm{pre}}\) and \(T_{\mathrm{total}}\), but it must not mechanically lengthen the primary post-regulation \(T_{\mathrm{rec}}\).

The stability window \(w\) is defined in **consecutive score updates**, not an assumed constant wall-clock duration. If no complete qualifying run is confirmed before

\[
t_m^{(e)}+c_e,
\]

the otherwise valid \(T_{\mathrm{rec}}\) observation is right-censored at \(c_e\).

Phase 0 may evaluate the prespecified small grid for \(\delta\), \(w\), and \(c_e\), but feature models cannot be selected because a particular model-threshold combination produces a favorable clinical association.

The feature-set freeze record must state:

- selected model ID;
- feature definitions and versions;
- window definitions;
- device timing-floor rule;
- feature weights;
- \(\delta\);
- stability-window count \(w\);
- recovery time origin;
- censor limit \(c_e\);
- missing-feature rule;
- measurement-context lock version;
- repository commit.

## 12. Required synthetic validation

Before human Phase 0 data, executable tests must distinguish at least:

- reference-like performance;
- isolated behavioral deterioration;
- isolated correct-response slowing;
- isolated reaction-time variability increase;
- unavailable/unqualified timing.

The committed deterministic cases satisfy these requirements and make it possible to detect accidental changes in feature semantics during implementation.
