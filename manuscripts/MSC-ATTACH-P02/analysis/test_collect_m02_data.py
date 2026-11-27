# SPDX-License-Identifier: Apache-2.0
"""M02 collector tests: dry-run, resume, corruption, gating."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from collect_m02_data import DEFAULT_CONFIG, DEFAULT_OUTPUT, ROOT, collect
from report_m02_collection import summarize


class CollectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.config = self.root / "config.json"
        self.spec = {
            "evidence_status": "development_only", "evidence_id": "M02-TEST",
            "seed": 880001, "replications": 3,
            "generators": ["p"],
            "conditions": [{"id": "sample", "steps": 60, "stride": 1,
                            "noise_sd": 0.0, "missingness": 0.0,
                            "feedback": 0.5, "clip": 1.0}],
            "split": [0.6, 0.2], "epsilon": 0.005, "coverage": 0.95,
            "integral_leak": 0.85, "action_noise_sd": 0.005,
            "process_noise_sd": 0.003, "excitation_sd": 0.04,
            "nonlinear_width": 0.12,
            "gains": {"kp": 0.6, "ki": 0.06, "kd": 0.08,
                      "rho": 0.65, "amplitude": 0.15,
                      "kp_positive": 0.75, "kp_negative": 0.25},
        }
        self.config.write_text(json.dumps(self.spec), encoding="utf-8")
        self.out = self.root / "data"
        self.commit = patch("collect_m02_data.git_commit", return_value="test-commit")
        self.commit.start()

    def tearDown(self):
        self.commit.stop()
        self.temp.cleanup()

    def test_migrated_default_paths(self):
        self.assertTrue(DEFAULT_CONFIG.is_file())
        self.assertEqual(DEFAULT_OUTPUT, ROOT / "build/MSC-ATTACH-P02/m02-collection")
        self.assertTrue((ROOT / "AGENTS.md").is_file())

    def test_collection_report_checks_integrity(self):
        collect(self.config, self.out, chunk=2, execute=True)
        collection = next(self.out.iterdir())
        report = summarize(collection)
        self.assertTrue(report["complete"])
        self.assertEqual(report["attempts_completed"], 3)
        shard = next(collection.glob("c*-g*-r*"))
        with (shard / "summary.csv").open("a") as f:
            f.write("CORRUPTED\n")
        with self.assertRaisesRegex(RuntimeError, "Integrity failure"):
            summarize(collection)

    def test_dry_run_has_no_writes(self):
        result = collect(self.config, self.out, chunk=2, execute=False)
        self.assertEqual(result["shards_total"], 1)
        self.assertEqual(result["planned"], 1)
        self.assertFalse(self.out.exists())

    def test_completed_shard_is_reused_and_corruption_fails(self):
        first = collect(self.config, self.out, chunk=2, execute=True)
        self.assertEqual(first["executed"], 1)
        second = collect(self.config, self.out, chunk=2, execute=True)
        self.assertEqual(second["reused"], 1)
        shard = next(self.out.glob("*/c*-g*-r*"))
        with (shard / "summary.csv").open("a") as f:
            f.write("CORRUPTED\n")
        with self.assertRaisesRegex(RuntimeError, "checksum"):
            collect(self.config, self.out, chunk=2, execute=True)

    def test_rejects_confirmatory_and_invalid_chunk(self):
        self.spec["evidence_status"] = "confirmatory"
        self.config.write_text(json.dumps(self.spec))
        with self.assertRaises(ValueError):
            collect(self.config, self.out, chunk=2, execute=False)
        self.spec["evidence_status"] = "development_only"
        self.config.write_text(json.dumps(self.spec))
        with self.assertRaises(ValueError):
            collect(self.config, self.out, chunk=1, execute=False)


if __name__ == "__main__":
    unittest.main()
