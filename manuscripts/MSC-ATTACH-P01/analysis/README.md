# H1: exact-design Monte Carlo

Scientific owner: Mateusz Pomianek. Source: ARC Attachment Dynamics, revision `9ddb0708dfcd380bcdc5a33f3a52d3b3c8df4b62`, directory `software/study_design/`. Code and original environment lock: Apache-2.0 ([license](LICENSE)). Test configuration paths and command examples were adapted; numerical algorithms were not changed.

## Reproduction

Run from the ARC Neuro repository root using an isolated Python environment. The source lock is preserved; package resolution and runtime tests in the migrated layout have not yet been verified. No human data are needed.

```bash
python -m pip install -r manuscripts/MSC-ATTACH-P01/analysis/requirements-lock.txt
python -B -m unittest discover -s manuscripts/MSC-ATTACH-P01/analysis -p "test_h1_exact_monte_carlo.py" -v
python -B manuscripts/MSC-ATTACH-P01/analysis/h1_exact_monte_carlo.py --config manuscripts/MSC-ATTACH-P01/protocol/exact_design_config.json --output-dir build/MSC-ATTACH-P01/h1_smoke --smoke
```

Use a new output directory for each run. The smoke configuration is the historical exact-design configuration, not the later comparable-lag recalibration. The latter remains pending verification. The imported results must be classified as synthetic development evidence, not human findings. Do not start a full simulation or treat these files as proof of recruitment readiness.

## Additional historical design tools and Windows execution

`h1_design_simulation.py` is the earlier fixed-effect screening approximation, not the basis for final recruitment N. `h1_recalibration_summary.py` implements the historical comparable-lag selection guardrails; its output is not new scientific evidence until the corresponding grid has actually run and been reviewed. The original four protocol configurations are retained under `../protocol/`.

```bash
python -B -m unittest discover -s manuscripts/MSC-ATTACH-P01/analysis -p 'test_h1*.py'
python -B manuscripts/MSC-ATTACH-P01/analysis/run_h1_tests_isolated.py
```

Windows: `H1_CHECK.bat` creates/verifies Python 3.12 and runs isolated regression/development checks. `H1_FULL.bat` runs the historical full grid; `H1_RECALIBRATE.bat` runs the focused comparable-lag grid; `H1_VALIDATE_ASYMMETRY.bat` runs the historical sensitivity grid. These are explicit, potentially long computations; none is invoked by migration. GEE and generation probes are available separately. Generated outputs are local under ignored `build/MSC-ATTACH-P01/`; resumable full-grid runs are bound to configuration hash, Git revision, replication count and chunk size. Do not edit code or configs while a run is in progress. Original result-staging/commit scripts are intentionally excluded: public transfer of raw outputs and workstation metadata requires review. Windows execution and the original dependency lock have not been independently validated here.
