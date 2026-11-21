"""Regression tests for a read-only ARC Neuro migration inventory."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from migration_preflight import audit


class NeuroMigrationPreflightTests(unittest.TestCase):
    def test_inventory_pass_does_not_approve_v2_migration(self):
        report = audit(ROOT)
        self.assertEqual(report["inventory_status"], "PASS", report["findings"])
        self.assertEqual(report["migration_status"], "BLOCKED")
        self.assertFalse(report["migration_ready"])
        self.assertEqual(report["record_count"], 63)
        self.assertEqual(report["record_kinds"], {"IDEA": 31, "MANUSCRIPT": 32})
        self.assertEqual(sum(report["research_lines"].values()), 63)
        self.assertGreater(len(report["historical_stage_values"]), 5)

    def test_duplicate_msc_fails(self):
        catalog = json.loads((ROOT / "papers/catalog.json").read_text(encoding="utf-8"))
        catalog["papers"][1]["id"] = catalog["papers"][0]["id"]
        other = [
            json.loads((ROOT / "areas/index.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "program.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "portfolio/papers.json").read_text(encoding="utf-8")),
        ]
        with patch("migration_preflight.json.loads", side_effect=[catalog, *other]):
            report = audit(ROOT)
        self.assertEqual(report["inventory_status"], "FAIL")
        self.assertTrue(any(s.startswith("duplicate_msc:") for s in report["findings"]))


if __name__ == "__main__":
    unittest.main()
