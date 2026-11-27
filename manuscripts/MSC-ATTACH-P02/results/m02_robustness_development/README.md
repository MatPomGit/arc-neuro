# M02 exploratory methodological robustness

Evidence `M02-DEV-ROBUSTNESS-2026-10-08`, development only. This preserves the earlier targeted/full-factorial archives unchanged. It was designed after those results were known and is not preregistered confirmation.

8 generators × 7 conditions × 160 independent seed triads = 8,960 attempts and 26,880 generated trajectories. The fit, validation and final roles use different innovation streams. The temporal comparator shares the fitting trajectory. A common observation-feasibility gate retains 968 failed triads in recovery denominators. AIC/BIC recovery is identical across modes because both use the same fitting data. Bootstrap intervals are pointwise exploratory percentile intervals, not calibrated coverage or multiplicity control.

## Reproduce

First regenerate the earlier full factorial trajectory ledger using the commands in `software/simulator/README.md`; verify its archived hash. Then:

```bash
.venv/bin/python software/simulator/controller_identifiability_robustness.py --config software/simulator/configs/m02_robustness_development.json --output artifacts/m02-robustness --source-commit <checked-out-source-commit> --existing-ledger artifacts/m02-factorial/trajectories.jsonl
.venv/bin/python software/simulator/report_identifiability_robustness.py --results artifacts/m02-robustness --manuscript manuscripts/02_identifiability
```

On Windows use `.venv\Scripts\python.exe`. The large `triads.jsonl` stays outside Git and is regenerable. Metadata records its exact hash, code/config/output hashes and the hash of the previously inspected factorial ledger. `conditional_information.csv` and `conditional_profiles.csv` describe the fixed-design Gaussian working regression, not a latent closed-loop FIM or valid gain-coverage calculation. Quantization is a computational stress test, not validated ordinal measurement.

All six numerical/config/ledger outputs were byte-identical in a second full execution under Python 3.12.14 / NumPy 2.3.5. This is same-environment deterministic reproduction, not an independent implementation or locked-environment reproduction. No new human data or approvals.

See `development_report.md` for outcome summaries and `manuscripts/02_identifiability/METHODOLOGICAL_REVIEW.md` for the assessment of comments and deferred scope.
