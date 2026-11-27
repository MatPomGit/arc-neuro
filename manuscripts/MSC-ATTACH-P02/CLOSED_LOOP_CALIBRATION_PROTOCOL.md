# M02: pilot of full closed-loop paired-loss interval calibration

Migration status: source code and compact historical outputs are now present in ARC Neuro. CI has tested the migrated code; the independent full calibration remains unexecuted.


Status: **implemented, not yet executed on the full intended grid**.
This is *prospective method-development work*, not preregistered confirmation.

The prior distribution-only study established that no generic confidence
interval reliably maintained nominal coverage across all illustrative
paired-loss shapes. The new procedure uses the **actual M02** simulator:
separate fit, validation and final trajectories; validation-RMSE model
selection; frozen competitor; independent final test; actual noise,
missingness, clipping and measurement transformations.

## Reproducible pilot (run from repository root)

```bash
python -m unittest discover -s manuscripts/MSC-ATTACH-P02/analysis -p "test_m02_closed_loop_calibration.py" -v
python manuscripts/MSC-ATTACH-P02/analysis/m02_closed_loop_calibration.py --output build/MSC-ATTACH-P02/m02-closed-loop-calibration --reference-n 200 --trials 20 --sample-n 20 --bootstraps 199
```

For Windows, use `.venv\\Scripts\\python.exe` instead of `python`.

The default is a **small resource-limited pilot**, not an adequate final
coverage audit. Cases are reference, heavy-tail and combined adversity,
with nominal generators P and PID. Each cell generates separate
large-reference and calibration-trial seed streams. The independent
reference mean is only a Monte Carlo **estimate** of true expected paired
RMSE difference, and `reference_mc_se` explicitly records its
uncertainty. Apparent interval coverage against a noisy reference
cannot be treated as coverage against a known truth.

### Outputs

- `closed_loop_coverage.csv`: interval hit fraction against an estimated
  reference, evaluated trials, width, final-test failures, zero exclusion,
  and separate reference Monte Carlo standard error.
- `metadata.json`: source commit, config and output SHA-256 checksums,
  execution arguments and developmental-only status.
- Numerical results must not be inserted into Results until the script
  actually runs and their limitations are reviewed.

### Gates before any confirmatory run

1. Independently estimate reference means with error substantially smaller
   than the target confidence-interval widths; quantify that uncertainty
   in coverage acceptance criteria.
2. Increase calibration trials and bootstrap draws; preserve condition-
   specific fit failures, and assess false-equivalence decisions using
   candidate epsilon values fixed independently of favorable observations.
3. Design simultaneous uncertainty and multiplicity handling across the
   **preselected** primary contrast family. Do not silently select the
   family from observed calibration outcomes.
4. Freeze exact primary cells, comparator, eligibility, tie rules, epsilon,
   sample sizes, provenance and untouched confirmatory seed registry.
5. Register OSF snapshot **before** running the distinct final streams.

No assumption about validated human emotional or attachment mechanisms
follows from this numerical calibration.

## Calibration diagnostics (revision 2)

The calibration allocates disjoint ten-million seed blocks for each reference and trial within a run, avoiding overlaps when trial count reaches 2,000. The generator and observation substreams use offsets up to 5,029,998. Changing the grid or trial count changes the stream allocation; do not pool separate runs as independent without checking their allocations. Report interval validity, Wilson 95% uncertainty for coverage conditional on the estimated reference, median interval half-width and reference SE relative to that width. The fractions containing and overlapping the approximate reference uncertainty band provide sensitivity diagnostics, not exact coverage bounds or corrections. Output directories must be new. No confirmatory decision follows from these diagnostics alone.
