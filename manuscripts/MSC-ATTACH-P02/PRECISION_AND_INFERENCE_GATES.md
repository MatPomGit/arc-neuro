# M02 precision and inference gates (prospective)

Status: planning document, **not preregistered, not frozen, and not a
confirmatory result**. Prepared 2026-10-08 after the exploratory development
outputs were inspected. The already observed results must never be reused as
blind confirmatory evidence.

## 1. Precisely distinguish targets

1. **Nominal family recovery**: proportion selecting the generating label
   among *all attempted* seed triads, counting insufficient observations,
   rank failures and selector failure as nonrecovery.
2. **Conditional/evaluable recovery**: a separate descriptive proportion
   among triads with eligible candidate fits. Its denominator must be shown.
3. **Paired prediction contrast**: per independent seed triad, compare the
   frozen generating-family candidate with a prespecified alternative on the
   untouched final trajectory. Report the mean of the paired RMSE differences.
   If either model cannot be fitted, preserve the triad's failure and exclude
   it from this particular mean, with explicit paired-n.
4. **Practical equivalence**: requires the *entire appropriately calibrated*
   confidence interval for mean paired loss to lie within [-epsilon,+epsilon].
   Failure to reject a difference does not prove equivalence.
5. **Parameter recovery/coverage**: separate estimand conditional on a
   specified fit model, likelihood, and parameter-generating distribution.
   Fixed-design PID profiles do not quantify full closed-loop coverage.

## 2. Prospective precision calculation

The executable stdlib-only tool
`python software/simulator/m02_precision_planner.py` computes the minimum
number of independent attempted triads per cell for a maximum pointwise Wilson
interval half-width. Inputs include interval confidence, number of Bonferroni
comparisons, generators, grid cells, triad multiplicity and an explicitly
*assumed*, rather than measured, evaluable fraction.

`--comparisons 1` is a pointwise planning illustration. Simultaneous
Bonferroni adjustment over all 8 x 64 recovery cells corresponds to
`--comparisons 512`; that family is **only a sensitivity illustration** and
must not be mistaken for the final chosen multiplicity family. The calculation
does not justify a primary family of 512 hypotheses, nor guarantee precision
for rare paired comparisons or for parameter intervals.

A decision on the number of *primary* contrasts and the confidence family is
required before finalizing N. Report Monte Carlo computation costs for any
proposed N: attempted triads x three independently generated trajectories.
Failed attempts still consume computational resources. A target based solely
on attempts cannot guarantee precision for evaluable/pairwise analyses.

## 3. Required calibration experiment (not yet executed)

Before the confirmatory run, implement a *separate* coverage and power/precision
study on fresh calibration seeds. Vary generating family, condition, effective
paired n, heavy tails, degeneracy and missingness. Check empirical interval
coverage for both family recovery and paired-loss means at the proposed nominal
and familywise levels. Assess percentile, studentized, and/or suitably
constructed BCa/bootstrap alternatives where mathematically applicable,
without assuming any method will succeed. Count failures and undecidable
equivalence outcomes. Select the final method by prespecified coverage and
interval-width criteria rather than favorable equivalence findings.

Calibration seeds may guide method choice but cannot subsequently enter
confirmatory inference. Archive calibration source/config/seed hashes and
negative results separately.

## 4. Decisions required before OSF submission

- [ ] Freeze the primary generating families and observation-condition grid;
      explicitly partition primary and sensitivity arms.
- [ ] Freeze comparator, selection criterion, candidate order, tie resolution,
      rank/condition-number cutoff, effective order and failure handling.
- [ ] Declare **epsilon in physical simulator action/RMSE units**, with a
      prospective engineering resolution rationale, independently of any
      inspected equivalence counts. Keep other epsilon values sensitivity-only.
- [ ] Freeze the exact primary inferential family and multiplicity adjustment,
      its estimands, confidence intervals, and planned contrasts.
- [ ] Execute independent coverage/precision calibration; record acceptance
      thresholds and its source/seed/output hashes.
- [ ] Choose N using attempted and *paired-evaluable* precision plus resource
      feasibility; explicitly state stopping and no-peeking policy.
- [ ] Specify parameter intervals with an appropriate observation model or
      remove parameter-coverage claims from the confirmatory research question.
- [ ] Check the final executable against data leakage, rank failures,
      independence and provenance; record exact lockfile and commit hashes.
- [ ] Record untouched final seed registry before launch, submit OSF
      preregistration, then run new confirmatory seeds only.

No human-study ethics approval is implied. M02 remains synthetic-only.
M03 and M04 follow separate human-study and institutional-approval processes.
