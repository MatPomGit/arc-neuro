# M02: preliminary calibration of paired-mean intervals

Status: **method calibration only**, not preregistered confirmation, not a
calibrated ARC/closed-loop generator likelihood. This computation evaluates
nominal 95% interval coverage for a known mean of zero under *illustrative*
i.i.d. paired-difference distributions. It does not use the uploaded
development trajectories as independent new evidence.

Reproduce with:

```bash
python manuscripts/MSC-ATTACH-P02/analysis/m02_interval_calibration.py --output build/MSC-ATTACH-P02/m02-calibration --seed 20261008 --trials 300 --sample-sizes 20 80 --bootstraps 399
python -m unittest discover -s manuscripts/MSC-ATTACH-P02/analysis -p 'test_m02_interval_calibration.py' -v
```

The deterministic seed initializes independent calibration streams per
scenario and sample size. Each observation is a paired difference, not an
individually resampled RMSE component or time point. Monte Carlo standard
errors are reported for the empirical coverage fractions.

## Preliminary coverage results (300 Monte Carlo trials per row)

| Scenario | n | normal CI | percentile bootstrap | studentized bootstrap |
|---|---:|---:|---:|---:|
| Normal | 20 | 0.950 | 0.937 | 0.957 |
| Normal | 80 | 0.943 | 0.937 | 0.943 |
| Skewed, centered exponential | 20 | 0.897 | 0.897 | 0.927 |
| Skewed, centered exponential | 80 | 0.917 | 0.923 | 0.937 |
| Student t(3), unit variance | 20 | 0.963 | 0.933 | 0.917 |
| Student t(3), unit variance | 80 | 0.947 | 0.940 | 0.940 |
| 2% high-variance contamination | 20 | 0.937 | 0.913 | 0.920 |
| 2% high-variance contamination | 80 | 0.957 | 0.933 | 0.900 |

These preliminary estimates have Monte Carlo SE of approximately 0.01--0.02
and use only 399 bootstrap draws, so they are insufficient for final
method selection. Normal intervals use a normal quantile with an estimated
SE; percentile and studentized intervals resample the *whole paired
difference*. A studentized interval may itself suffer poor coverage
under rare contamination. No one procedure uniformly attained 95%.

## Required next calibration before confirmatory preregistration

1. Run a larger accuracy/coverage study (e.g. at least 2,000 replicates per
   cell and >=1,999 bootstrap resamples; capacity planning required).
2. Execute **actual M02 closed-loop simulation** on previously unused
   calibration seeds, including generator/condition-dependent selection,
   fit failures, heavy tails, missing observations and paired-loss scaling.
3. Establish an independently estimable reference paired-mean truth with
   its own error bound; account for shared random-number streams between
   conditions. Quantify empirical false-equivalence calls as well as
   interval coverage and precision at plausible paired sample sizes.
4. Prespecify the required coverage criterion, primary comparison family
   and simultaneous-inference method before choosing the confirmatory
   method. Neither an epsilon value nor a final method is frozen here.
5. Lock the exact code, configs, seeds, environment and source hashes; do
   not reuse calibration seeds as confirmation.

The existing development epsilon of 0.005 has **not** been validated as
an engineering resolution threshold by this study. Simultaneous inference
and parameter coverage require separate designs.
