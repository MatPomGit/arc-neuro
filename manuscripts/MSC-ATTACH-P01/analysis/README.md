# H1: exact-design Monte Carlo

Scientific owner: Mateusz Pomianek. Source: ARC Attachment Dynamics, revision `9ddb0708dfcd380bcdc5a33f3a52d3b3c8df4b62`, directory `software/study_design/`. Code and original environment lock: Apache-2.0 ([license](LICENSE)). Test configuration paths and command examples were adapted; numerical algorithms were not changed.

## Reproduction

Run from the ARC Neuro repository root using an isolated Python environment. The source lock is preserved; package resolution and runtime tests in the migrated layout have not yet been verified. No human data are needed.

```bash
python -m pip install -r manuscripts/MSC-ATTACH-P01/analysis/requirements-lock.txt
python -B -m unittest discover -s manuscripts/MSC-ATTACH-P01/analysis -p "test_h1_exact_monte_carlo.py" -v
python -B manuscripts/MSC-ATTACH-P01/analysis/h1_exact_monte_carlo.py --config manuscripts/MSC-ATTACH-P01/protocol/exact_design_config.json --output-dir manuscripts/MSC-ATTACH-P01/build/h1_smoke --smoke
```

Use a new output directory for each run. The smoke configuration is the historical exact-design configuration, not the later comparable-lag recalibration. The latter remains pending verification. The imported results must be classified as synthetic development evidence, not human findings. Do not start a full simulation or treat these files as proof of recruitment readiness.
