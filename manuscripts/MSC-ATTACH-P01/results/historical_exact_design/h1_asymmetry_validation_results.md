# H1 focused M4 asymmetry validation: results

Status: completed before human outcome data.

## 1. Design

**Historical sample-size note.** This validation used N=84 because that was the H1 target at the time. The result remains valid for its narrow purpose of assessing the M4 asymmetry contrast at N=84, but it does not freeze the final H1 sample size after the later comparable-lag correction.

The focused validation used the then-current H1 analysis target of 84 couples and an
independent Monte Carlo seed. It evaluated:

- compliance targets 0.75 and 0.85;
- missingness-strength conditions 0 and 1;
- M3 truth (symmetric signed discrepancy);
- M4 truth (asymmetric positive/negative discrepancy slopes);
- 1000 replications per design cell;
- candidate practical-equivalence tolerances delta_asym = 0.25, 0.50, 0.75.

Total focused replications: 8,000.

The fitted M4 contrast was

    d_asym = beta_positive + beta_negative,

with beta_negative multiplying max(-e, 0). Under exact signed-discrepancy
symmetry, d_asym = 0. Under the focused M4 generating truth,
d_asym = 2.0 + (-1.2) = 0.8.

## 2. Prespecified guardrails

A candidate tolerance was required to satisfy all of the following across the
evaluated design cells:

- M3 symmetry-compatible rate >= 0.80;
- M3 false-asymmetry rate <= 0.05;
- M4 material-asymmetry rate >= 0.80;
- M4 false-symmetry rate <= 0.05.

No candidate passed all guardrails.

## 3. Candidate performance

### delta_asym = 0.25

Worst-cell results:

- M3 symmetry-compatible rate: 0.000;
- M3 false-asymmetry rate: 0.029;
- M4 material-asymmetry rate: 0.291;
- M4 false-symmetry rate: 0.000;
- maximum inconclusive rate: 0.980.

Across M4 cells, material asymmetry was classified in approximately
29.1% to 40.4% of replications.

### delta_asym = 0.50

Worst-cell results:

- M3 symmetry-compatible rate: 0.000;
- M3 false-asymmetry rate: 0.007;
- M4 material-asymmetry rate: 0.147;
- M4 false-symmetry rate: 0.000;
- maximum inconclusive rate: 0.996.

### delta_asym = 0.75

Worst-cell results:

- M3 symmetry-compatible rate: 0.016;
- M3 false-asymmetry rate: 0.001;
- M4 material-asymmetry rate: 0.059;
- M4 false-symmetry rate: 0.020;
- maximum inconclusive rate: 0.983.

## 4. Precision diagnosis

The Monte Carlo mean M4 d_asym estimate was close to its generating value:

- M3 truth: approximately -0.016 to +0.015;
- M4 truth: approximately 0.782 to 0.830.

Thus the problem is not substantial estimator bias.

The mean standard error of d_asym was approximately 0.416 to 0.491. This is
large relative to the M4 generating asymmetry of 0.8. Consequently, 90%
confidence intervals are usually too wide to lie wholly inside a practical
symmetry region under M3 or wholly outside it under M4.

The focused validation therefore diagnoses insufficient precision for a
three-state confirmatory M4 equivalence/asymmetry decision at N=84.

## 5. Design consequence

No numerical delta_asym is locked for confirmatory H1.

M4 remains in the prespecified model family because it is scientifically useful
for estimating separate positive- and negative-discrepancy slopes. However,
its asymmetry contrast is demoted to secondary structural evidence:

- report beta_positive and beta_negative;
- report d_asym and its 95% confidence interval;
- report the sign and magnitude of the contrast;
- do not classify M4 as symmetric/asymmetric using a confirmatory practical
  threshold;
- do not allow M4 asymmetry to rescue or overturn the co-primary H1-P1/H1-P2
  result.

A future study specifically designed to make asymmetry a confirmatory claim
would require separate prospective power/design work and should not be
retrofit into the N=84 H1 pilot.

## 6. Relation to the primary H1 Monte Carlo

The revised coefficient-first H1 analysis performs strongly at the locked
N=84 design when compliance is approximately 0.75 or higher. For M2-M4 truth,
the probability of full co-primary support is approximately 0.988-1.000 across
the evaluated compliance/missingness cells. Under M0 truth, full support is
essentially absent.

Therefore the failed d_asym guardrails do not invalidate the N=84 primary H1
design. They delimit the claims that may be made from M4.
