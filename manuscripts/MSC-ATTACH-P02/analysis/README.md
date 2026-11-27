# M02: controller identifiability and calibration

Scientific owner: Mateusz Pomianek. Source: ARC Attachment Dynamics, `9ddb0708dfcd380bcdc5a33f3a52d3b3c8df4b62`, `software/simulator/`. Apache-2.0 ([license](LICENSE)). Numerical algorithms are preserved; the default calibration configuration path was adapted to this directory. The source environment lock is retained, not newly validated.

From the repository root, in an isolated Python environment:

```bash
python -m pip install -r manuscripts/MSC-ATTACH-P02/analysis/requirements-lock.txt
python -B -m unittest discover -s manuscripts/MSC-ATTACH-P02/analysis -p "test_*.py" -v
python -B manuscripts/MSC-ATTACH-P02/analysis/m02_precision_planner.py
```

Run the closed-loop calibration only into a new local build directory:

```bash
python -B manuscripts/MSC-ATTACH-P02/analysis/m02_closed_loop_calibration.py --output manuscripts/MSC-ATTACH-P02/build/m02_calibration --reference-n 200 --trials 20 --sample-n 20 --bootstraps 199
```

This is a development pilot, not a confirmatory run. Historical aggregate results were generated at older source commits and must not be attributed to this migrated revision. Complete reproduction, dependency installation and runtime validation remain outstanding.

## Resumable development data collection

The collector, descriptive reporter and regression tests were migrated from the same pinned source revision. Changes are limited to repository-relative defaults and additional path and report integrity tests. From the repository root:

```bash
python -B manuscripts/MSC-ATTACH-P02/analysis/collect_m02_data.py
python -B manuscripts/MSC-ATTACH-P02/analysis/collect_m02_data.py --execute --max-shards 1
python -B manuscripts/MSC-ATTACH-P02/analysis/report_m02_collection.py
```

The first command is a dry run. The second explicitly executes at most one shard; repeat with the same commit, configuration and chunk size to resume, or remove `--max-shards` for the full developmental collection. Outputs default to the ignored root `build/MSC-ATTACH-P02/m02-collection/`. Existing shards are checksum-verified; partial or corrupted shards require inspection. Pooled recovery counts are descriptive only. Historical collections have not been transferred or reproduced by this change.
