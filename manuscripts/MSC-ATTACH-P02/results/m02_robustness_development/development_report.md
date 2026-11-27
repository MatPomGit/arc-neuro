# M02 exploratory robustness

Evidence: M02-DEV-ROBUSTNESS-2026-10-08; development only.
Source commit: b7eeee72e10343804bd4d082214789d9544ec71e.

8960 attempted triads; 26880 generated trajectories; 968 common split-feasibility failures.

Candidate rank failures: 663; full-rank fits without finite variance MLE: 1920; mode/criterion records without choice: 1280.
## Independent validation-RMSE PID recovery

- reference: 150/160; evaluable 160; paired mean -0.00086050.
- analyst_noise: 85/160; evaluable 160; paired mean -0.00015169.
- heavy_tail: 64/160; evaluable 160; paired mean 0.00054084.
- irregular: 32/160; evaluable 160; paired mean 0.00021876.
- quantized_7: 60/160; evaluable 160; paired mean -0.00021212.
- clipping: 40/160; evaluable 160; paired mean 0.00040835.
- combined: 5/160; evaluable 39; paired mean -0.00044759.

AIC/BIC use fitting data, so their recovery counts are identical across validation modes by construction. Comparisons of validation-RMSE modes share fitted coefficients and seed triads. No multiplicity-controlled or human inference.

Conditional information/profiles hold observed predictors fixed; they are not a full latent-state FIM or likelihood. Percentile bootstrap coverage is not established here.
