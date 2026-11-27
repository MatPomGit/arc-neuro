# M02 inferential audit | 2026-10-09

Status: prospective methodological analysis, not an executed calibration, frozen protocol or preregistration. Sources: COMPUTATIONAL_ANALYSIS_SPEC.md, PRECISION_AND_INFERENCE_GATES.md, CLOSED_LOOP_CALIBRATION_PROTOCOL.md and simulation_protocol.yaml.

## Estimands and selection

Let j denote an independent fit/validation/final triad. Nominal family recovery among **all attempted** triads counts failed selections as nonrecovery. Recovery conditional on evaluability uses a different denominator. The paired final-test contrast D_j = RMSE(generator candidate) minus RMSE(validation-selected competitor) is only defined when both fits and final scores exist. Its mean therefore targets the paired-evaluable population; failures can select easier observation conditions. Report attempted, evaluable and paired N, plus failure categories. Resample triads, or whole matched seed blocks across conditions, never individual time points. Because the competitor is chosen on validation data, the contrast estimates a **selection procedure**, not an oracle fixed model.

## Equivalence and uncertainty

Structural observational equivalence is equality of induced observation probability laws; small RMSE differences do not establish it. Practical mean-loss equivalence requires a calibrated interval for E[D_j | paired evaluable] to lie entirely inside (-epsilon,+epsilon). A boundary-crossing interval is inconclusive. Trajectory near-tie probability P(abs(D_j)<epsilon) is distinct. Earlier development epsilon=0.005 is not a frozen threshold. Simultaneous claims over multiple cells require a prospectively specified comparison family and multiplicity control.

The newly merged closed-loop calibration script compares intervals with an **estimated reference mean** and reports its Monte Carlo SE. Coverage against a noisy reference is not guaranteed coverage against the true expected contrast. Before selecting an interval method, record reference paired N, reference SE divided by median interval half-width, calibration trial count, binomial uncertainty for observed coverage and false-equivalence decisions. Rechecking apparent coverage against reference mean +/- 1.96 reference SE is a sensitivity diagnostic, **not** an exact correction. Expand independent reference simulations where needed. Stress-test heavy tails, clipping, sparse evaluability and degenerate gains; bootstrap nomenclature alone does not establish nominal coverage.

## Prospective decision gates

- [ ] Primary generator-condition cells and separate sensitivity arms.
- [ ] Selector, competitor, candidate order, rank/tie/failure rules and estimands.
- [ ] Epsilon justified independently in action/RMSE units.
- [ ] Primary comparison family, multiplicity and calibrated interval method.
- [ ] Attempted and paired-evaluable precision, computational feasibility and stopping.
- [ ] Parameter interval likelihood or explicit exclusion of coverage claims.
- [ ] Locked source/config/environment, untouched seed registry and actual OSF registration before confirmation.

**Next executable action:** run the existing closed-loop pilot and unit tests, archive outputs and hashes, then review failures and reference uncertainty before scaling. No simulation was run for this audit. Historical and robustness outputs remain exploratory; no human mechanism is validated.
