"""Regression smoke test for the migrated configured experiments."""
import csv
import json
import os
from pathlib import Path
import tempfile
import unittest

os.environ.setdefault("MPLBACKEND", "Agg")
from experiments import run_config
from summarize_recovery import summarize

HERE = Path(__file__).resolve().parent


class ExperimentMigrationTests(unittest.TestCase):
    def test_phase_map_smoke(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            run_config(HERE / "configs/smoke.json", out)
            self.assertTrue((out / "smoke.png").stat().st_size > 0)
            with (out / "smoke.csv").open(newline="", encoding="utf-8") as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), 9)

    def test_small_recovery_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            spec = json.loads((HERE / "configs/parameter_recovery.json").read_text())
            spec["n_runs"] = 2
            cfg = out / "config.json"
            cfg.write_text(json.dumps(spec), encoding="utf-8")
            run_config(cfg, out)
            summary = summarize(out / spec["csv"], cfg)
            self.assertEqual(summary["trajectories"], 2)


if __name__ == "__main__":
    unittest.main()
